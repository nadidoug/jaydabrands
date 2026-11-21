const VERSION = '2026-11-21';
const ORIGINS = new Set(['https://jaynovabrands.com', 'https://www.jaynovabrands.com', 'https://nadidoug.github.io', 'http://127.0.0.1:4173', 'http://localhost:8080']);

function envKeys(name: string): Record<string,string> {
  try { return JSON.parse(Deno.env.get(name) || '{}'); } catch { return {}; }
}

Deno.serve(async (req: Request): Promise<Response> => {
  const origin = req.headers.get('origin') || '';
  const headers = {'Access-Control-Allow-Origin': ORIGINS.has(origin) ? origin : 'null', 'Access-Control-Allow-Methods':'POST, OPTIONS', 'Access-Control-Allow-Headers':'content-type, apikey', 'Vary':'Origin', 'Cache-Control':'no-store'};
  const reply = (status: number) => new Response(null, {status, headers});
  if (!ORIGINS.has(origin)) return reply(403);
  if (req.method === 'OPTIONS') return reply(204);
  if (req.method !== 'POST') return reply(405);
  // The endpoint accepts public app keys. A publishable key identifies the app,
  // not an individual person. No authenticated user or visitor identity is needed.
  const publicKeys = Object.values(envKeys('SUPABASE_PUBLISHABLE_KEYS'));
  const legacy = Deno.env.get('SUPABASE_ANON_KEY');
  if (legacy) publicKeys.push(legacy);
  if (!publicKeys.includes(req.headers.get('apikey') || '')) return reply(401);
  if (!req.headers.get('content-type')?.startsWith('application/json')) return reply(415);
  if (Number(req.headers.get('content-length') || 0) > 2048) return reply(413);
  try {
    const reader = req.body?.getReader();
    if (!reader) return reply(400);
    const chunks: Uint8Array[] = []; let length = 0;
    while (true) { const {value, done} = await reader.read(); if (done) break; length += value.length; if (length > 2048) { await reader.cancel(); return reply(413); } chunks.push(value); }
    const bytes = new Uint8Array(length); let offset = 0;
    for (const chunk of chunks) { bytes.set(chunk, offset); offset += chunk.length; }
    const body = JSON.parse(new TextDecoder().decode(bytes));
    if (body.product !== 'starter-guide' || body.consent !== true || body.version !== VERSION) return reply(400);
    const secret = envKeys('SUPABASE_SECRET_KEYS').default || Deno.env.get('SUPABASE_SERVICE_ROLE_KEY');
    const url = Deno.env.get('SUPABASE_URL');
    if (!secret || !url) return reply(503);
    // Use the address only in memory to derive a daily-rotating abuse-control hash.
    // Raw addresses, names, email addresses, and user agents are never written here.
    const address = (req.headers.get('cf-connecting-ip') || req.headers.get('x-forwarded-for')?.split(',')[0] || 'unknown').trim();
    const key = await crypto.subtle.importKey('raw', new TextEncoder().encode(secret), {name:'HMAC',hash:'SHA-256'}, false, ['sign']);
    const signed = await crypto.subtle.sign('HMAC', key, new TextEncoder().encode(`${new Date().toISOString().slice(0,10)}:${address}`));
    const hash = [...new Uint8Array(signed)].map(n=>n.toString(16).padStart(2,'0')).join('');
    const apiHeaders: Record<string,string> = {'content-type':'application/json','apikey':secret};
    if (!secret.startsWith('sb_')) apiHeaders.Authorization = `Bearer ${secret}`;
    const result = await fetch(`${url}/rest/v1/rpc/jaynova_record_download`, {method:'POST', headers:apiHeaders, body:JSON.stringify({p_product_slug:'starter-guide',p_visitor_hash:hash,p_consent_version:VERSION})});
    if (!result.ok) return reply(503);
    const accepted = await result.json();
    return reply(accepted === true ? 204 : 429);
  } catch { return reply(400); }
});
