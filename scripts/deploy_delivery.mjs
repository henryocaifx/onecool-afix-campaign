// Execute deployDelivery inside Cloudflare's connected JavaScript tool, where
// cloudflare.request() and accountId are supplied by the authenticated service.
// The signing secret is generated server-side and never returned or committed.
export async function deployDelivery(cloudflare, accountId, options) {
  const {source, files, prefix, workerName, subdomain} = options;
  const now=Math.floor(Date.now()/1000);
  const downloadExpiry=now+7*86400;
  const uploadExpiry=now+7200;
  const secret=Array.from(crypto.getRandomValues(new Uint8Array(32)),x=>x.toString(16).padStart(2,"0")).join("");
  const metadata={
    main_module:"worker.mjs",
    compatibility_date:"2026-10-15",
    compatibility_flags:["nodejs_compat"],
    observability:{enabled:true,head_sampling_rate:1,redact_query_string:true},
    bindings:[
      {name:"BUCKET",type:"r2_bucket",bucket_name:"aifx-studio-campaign"},
      {name:"SIGNING_KEY",type:"secret_text",text:secret},
      {name:"PREFIX",type:"plain_text",text:prefix},
      {name:"ALLOWED_KEYS",type:"plain_text",text:JSON.stringify(files.map(f=>f.key))},
      {name:"EXPIRES_AT",type:"plain_text",text:String(downloadExpiry)},
      {name:"UPLOAD_EXPIRES_AT",type:"plain_text",text:String(uploadExpiry)},
    ],
  };
  const boundary="AIFX"+crypto.randomUUID().replaceAll("-","");
  const body=["--"+boundary,'Content-Disposition: form-data; name="metadata"',"Content-Type: application/json","",JSON.stringify(metadata),"--"+boundary,'Content-Disposition: form-data; name="worker.mjs"; filename="worker.mjs"',"Content-Type: application/javascript+module","",source,"--"+boundary+"--",""] .join("\r\n");
  const deployment=await cloudflare.request({method:"PUT",path:`/accounts/${accountId}/workers/scripts/${workerName}`,contentType:`multipart/form-data; boundary=${boundary}`,rawBody:true,body});
  if (!deployment.success) throw new Error("Delivery worker upload failed: "+deployment.status);
  const enable=await cloudflare.request({method:"POST",path:`/accounts/${accountId}/workers/scripts/${workerName}/subdomain`,body:{enabled:true,previews_enabled:false}});
  if (!enable.success) throw new Error("Delivery worker URL enable failed: "+enable.status);
  const key=await crypto.subtle.importKey("raw",new TextEncoder().encode(secret),{name:"HMAC",hash:"SHA-256"},false,["sign"]);
  async function sign(file,method,expiry) {
    const canonical=[method,file.key,String(expiry),file.sha256,String(file.bytes),file.content_type].join("\n");
    const signed=await crypto.subtle.sign("HMAC",key,new TextEncoder().encode(canonical));
    const sig=Array.from(new Uint8Array(signed),x=>x.toString(16).padStart(2,"0")).join("");
    const url=new URL(`https://${workerName}.${subdomain}.workers.dev/`+file.key);
    for (const [k,v] of Object.entries({e:String(expiry),h:file.sha256,s:String(file.bytes),t:file.content_type,sig})) url.searchParams.set(k,v);
    return url.toString();
  }
  const tickets=[];
  for (const file of files) tickets.push({...file,upload_url:await sign(file,"PUT",uploadExpiry),download_url:await sign(file,"GET",downloadExpiry)});
  return {worker_name:workerName,base_url:`https://${workerName}.${subdomain}.workers.dev`,upload_expires_at_utc:new Date(uploadExpiry*1000).toISOString(),download_expires_at_utc:new Date(downloadExpiry*1000).toISOString(),bucket:"aifx-studio-campaign",prefix,tickets};
}
