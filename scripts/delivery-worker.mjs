// Private-bucket transfer bridge. Secrets are deployed as secret_text bindings.
// No bucket listing, deletion, unsigned reads, or overwrite route is exposed.
const enc = new TextEncoder();

export function canonical(method, key, expiry, hash, size, type) {
  return [method, key, expiry, hash, size, type].join("\n");
}

export default {
  async fetch(request, env) {
    try {
      const url = new URL(request.url);
      const key = decodeURIComponent(url.pathname.slice(1));
      const native=Boolean(env.NATIVE_PREFIX && key.startsWith(env.NATIVE_PREFIX));
      const prefix=native?env.NATIVE_PREFIX:env.PREFIX;
      const allowed = JSON.parse(native?env.NATIVE_ALLOWED_KEYS:env.ALLOWED_KEYS);
      const expires=Number(native?env.NATIVE_EXPIRES_AT:env.EXPIRES_AT);
      const uploadExpires=Number(native?env.NATIVE_UPLOAD_EXPIRES_AT:env.UPLOAD_EXPIRES_AT);
      const signingKey=native?env.NATIVE_SIGNING_KEY:env.SIGNING_KEY;
      if (!key.startsWith(prefix) || !allowed.includes(key)) {
        return new Response("Not found", { status: 404 });
      }
      const method = request.method === "HEAD" ? "GET" : request.method;
      if (!["GET", "PUT"].includes(method)) {
        return new Response("Method not allowed", { status: 405 });
      }
      const e = url.searchParams.get("e") || "";
      const h = url.searchParams.get("h") || "";
      const size = url.searchParams.get("s") || "";
      const type = url.searchParams.get("t") || "";
      const sig = url.searchParams.get("sig") || "";
      const now = Math.floor(Date.now() / 1000);
      const max = method === "PUT" ? uploadExpires : expires;
      if (!/^\d+$/.test(e) || Number(e) < now || Number(e) > max || now > expires) {
        return new Response("Link expired", { status: 410 });
      }
      if (!/^[a-f0-9]{64}$/.test(h) || !/^\d+$/.test(size) || Number(size) > 99*1024*1024 || !/^[a-f0-9]{64}$/.test(sig)) {
        return new Response("Forbidden", { status: 403 });
      }
      const secret = await crypto.subtle.importKey("raw", enc.encode(signingKey), {name:"HMAC",hash:"SHA-256"}, false, ["verify"]);
      const signature = Uint8Array.from(sig.match(/../g), v => parseInt(v, 16));
      const verified = await crypto.subtle.verify("HMAC", secret, signature, enc.encode(canonical(method,key,e,h,size,type)));
      if (!verified) return new Response("Forbidden", {status:403});
      if (method === "PUT") {
        if (request.headers.get("Content-Type") !== type || request.headers.get("Content-Length") !== size || !request.body) {
          return new Response("Upload metadata mismatch", {status:400});
        }
        const object = await env.BUCKET.put(key, request.body, {
          onlyIf: {etagDoesNotMatch:"*"},
          sha256: Uint8Array.from(h.match(/../g), v => parseInt(v,16)),
          httpMetadata: {contentType:type,cacheControl:"private, no-store"},
          customMetadata: {sha256:h,campaign:"aifx-studio-20261015"},
        });
        if (!object) return new Response("Object already exists", {status:412});
        return Response.json({key,size:object.size,etag:object.etag,sha256:h});
      }
      const object = request.method === "HEAD" ? await env.BUCKET.head(key) : await env.BUCKET.get(key, {range:request.headers});
      if (!object) return new Response("Not found", {status:404});
      if (object.size !== Number(size) || object.customMetadata?.sha256 !== h) {
        return new Response("Object integrity metadata mismatch", {status:409});
      }
      const headers = new Headers();
      object.writeHttpMetadata(headers);
      headers.set("etag",object.httpEtag);
      headers.set("X-Content-SHA256",h);
      headers.set("Cache-Control","private, no-store");
      headers.set("X-Content-Type-Options","nosniff");
      headers.set("Accept-Ranges","bytes");
      const filename=key.split("/").pop();
      headers.set("Content-Disposition",(type==="video/mp4"?"inline":"attachment")+'; filename="'+filename+'"');
      let status=200;
      if (object.range && request.headers.has("Range")) {
        const start=object.range.offset ?? Math.max(0,object.size-(object.range.suffix || 0));
        const length=object.range.length ?? object.size-start;
        headers.set("Content-Range",`bytes ${start}-${start+length-1}/${object.size}`);
        headers.set("Content-Length",String(length));
        status=206;
      } else {
        headers.set("Content-Length",String(object.size));
      }
      return new Response(request.method==="HEAD"?null:object.body,{status,headers});
    } catch {
      console.error(JSON.stringify({event:"campaign_delivery_operation_failed"}));
      return new Response("Delivery operation failed",{status:500});
    }
  },
};
