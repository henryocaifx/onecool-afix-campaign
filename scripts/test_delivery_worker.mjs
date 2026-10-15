import assert from "node:assert/strict";
import worker, {canonical} from "./delivery-worker.mjs";

const key="campaigns/test/film.mp4";
const hash="a".repeat(64);
const now=Math.floor(Date.now()/1000);
const secret=crypto.randomUUID()+crypto.randomUUID();
let reads=0, writes=0;
const env={PREFIX:"campaigns/test/",ALLOWED_KEYS:JSON.stringify([key]),SIGNING_KEY:secret,EXPIRES_AT:String(now+3600),UPLOAD_EXPIRES_AT:String(now+600),BUCKET:{
  head:async()=>{reads++;return null;},
  get:async()=>{reads++;return null;},
  put:async(k,body,opts)=>{writes++;assert.equal(k,key);assert.equal(opts.onlyIf.etagDoesNotMatch,"*");assert.equal(Buffer.from(opts.sha256).toString("hex"),hash);return null;},
}};
async function signed(method,override={}) {
  const p={e:String(now+300),h:hash,s:"3",t:"video/mp4",...override};
  const k=await crypto.subtle.importKey("raw",new TextEncoder().encode(secret),{name:"HMAC",hash:"SHA-256"},false,["sign"]);
  const sig=await crypto.subtle.sign("HMAC",k,new TextEncoder().encode(canonical(method,key,p.e,p.h,p.s,p.t)));
  p.sig=Array.from(new Uint8Array(sig),b=>b.toString(16).padStart(2,"0")).join("");
  return "https://example.invalid/"+key+"?"+new URLSearchParams(p);
}
assert.equal((await worker.fetch(new Request("https://example.invalid/"+key),env)).status,410);
assert.equal(reads,0);
assert.equal((await worker.fetch(new Request(await signed("GET",{e:String(now-1)})),env)).status,410);
assert.equal(reads,0);
const valid=await signed("GET");
assert.equal((await worker.fetch(new Request(valid.replace("s=3","s=4")),env)).status,403);
assert.equal(reads,0);
assert.equal((await worker.fetch(new Request(valid),env)).status,404);
assert.equal(reads,1);
assert.equal((await worker.fetch(new Request(await signed("PUT"),{method:"PUT",headers:{"Content-Type":"video/mp4","Content-Length":"3"},body:"abc"}),env)).status,412);
assert.equal(writes,1);
assert.equal((await worker.fetch(new Request(valid.replace("campaigns/test/","outside/")),env)).status,404);
console.log("Delivery bridge: signatures, expiry, path scope, metadata binding, and overwrite prevention passed.");
