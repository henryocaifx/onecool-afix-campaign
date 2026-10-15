// Extend the existing user-approved endpoint. Its original secret binding and
// 17 original object authorizations remain intact; native files use a new key.
export async function extendDelivery(cloudflare,accountId,options) {
  const {source,files,prefix,workerName,subdomain,legacy}=options;
  const now=Math.floor(Date.now()/1000), downloadExpiry=now+7*86400, uploadExpiry=now+7200;
  const secret=Array.from(crypto.getRandomValues(new Uint8Array(32)),x=>x.toString(16).padStart(2,"0")).join("");
  const metadata={main_module:"worker.mjs",compatibility_date:"2026-10-15",compatibility_flags:["nodejs_compat"],keep_bindings:["secret_text"],observability:{enabled:true,head_sampling_rate:1,redact_query_string:true},bindings:[
    {name:"BUCKET",type:"r2_bucket",bucket_name:"aifx-studio-campaign"},
    {name:"PREFIX",type:"plain_text",text:legacy.prefix},
    {name:"ALLOWED_KEYS",type:"plain_text",text:JSON.stringify(legacy.keys)},
    {name:"EXPIRES_AT",type:"plain_text",text:String(legacy.downloadExpiry)},
    {name:"UPLOAD_EXPIRES_AT",type:"plain_text",text:String(legacy.uploadExpiry)},
    {name:"NATIVE_PREFIX",type:"plain_text",text:prefix},
    {name:"NATIVE_ALLOWED_KEYS",type:"plain_text",text:JSON.stringify(files.map(x=>x.key))},
    {name:"NATIVE_EXPIRES_AT",type:"plain_text",text:String(downloadExpiry)},
    {name:"NATIVE_UPLOAD_EXPIRES_AT",type:"plain_text",text:String(uploadExpiry)},
    {name:"NATIVE_SIGNING_KEY",type:"secret_text",text:secret},
  ]};
  const boundary="AIFX"+crypto.randomUUID().replaceAll("-","");
  const body=["--"+boundary,'Content-Disposition: form-data; name="metadata"',"Content-Type: application/json","",JSON.stringify(metadata),"--"+boundary,'Content-Disposition: form-data; name="worker.mjs"; filename="worker.mjs"',"Content-Type: application/javascript+module","",source,"--"+boundary+"--",""] .join("\r\n");
  const r=await cloudflare.request({method:"PUT",path:`/accounts/${accountId}/workers/scripts/${workerName}`,contentType:`multipart/form-data; boundary=${boundary}`,rawBody:true,body});
  if(!r.success)throw new Error("Native delivery extension failed: "+r.status);
  const k=await crypto.subtle.importKey("raw",new TextEncoder().encode(secret),{name:"HMAC",hash:"SHA-256"},false,["sign"]);
  async function signed(f,method,e){
    const canonical=[method,f.key,String(e),f.sha256,String(f.bytes),f.content_type].join("\n");
    const sig=Array.from(new Uint8Array(await crypto.subtle.sign("HMAC",k,new TextEncoder().encode(canonical))),x=>x.toString(16).padStart(2,"0")).join("");
    const url=new URL(`https://${workerName}.${subdomain}.workers.dev/`+f.key);
    for(const [key,value] of Object.entries({e:String(e),h:f.sha256,s:String(f.bytes),t:f.content_type,sig}))url.searchParams.set(key,value);
    return url.toString();
  }
  const tickets=[];
  for(const f of files)tickets.push({...f,upload_url:await signed(f,"PUT",uploadExpiry),download_url:await signed(f,"GET",downloadExpiry)});
  return {worker_name:workerName,base_url:`https://${workerName}.${subdomain}.workers.dev`,bucket:"aifx-studio-campaign",prefix,upload_expires_at_utc:new Date(uploadExpiry*1000).toISOString(),download_expires_at_utc:new Date(downloadExpiry*1000).toISOString(),original_links_preserved:true,tickets};
}
