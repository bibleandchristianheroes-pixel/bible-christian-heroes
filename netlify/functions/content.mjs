// Site content API: GET is public; POST (login check) and PUT (save) need the admin password.
// The password lives in the Netlify environment variable ADMIN_PASSWORD (never in the code).
import { getStore } from "@netlify/blobs";
import { createHash, timingSafeEqual } from "node:crypto";

const json = (body, status = 200, extra = {}) =>
  new Response(JSON.stringify(body), {
    status,
    headers: { "content-type": "application/json; charset=utf-8", "cache-control": "no-store", ...extra },
  });

const sha = (s) => createHash("sha256").update(String(s)).digest();
function passwordOk(given) {
  const real = (globalThis.Netlify?.env?.get("ADMIN_PASSWORD")) ?? process.env.ADMIN_PASSWORD;
  if (!real) return "missing";
  return timingSafeEqual(sha(given || ""), sha(real)) ? "ok" : "bad";
}

const REQUIRED = ["settings", "youtube", "quizzes", "heroDecks", "saintDecks", "freeBooks", "paidBooks", "apps"];

export default async (req) => {
  const store = getStore({ name: "site-content", consistency: "strong" });

  if (req.method === "GET") {
    const url = new URL(req.url);
    if (url.searchParams.get("history") === "1") {
      if (passwordOk(req.headers.get("x-admin-key")) !== "ok") return json({ error: "Wrong password" }, 401);
      const { blobs } = await store.list({ prefix: "backup/" });
      return json(blobs.map((b) => b.key).sort().reverse().slice(0, 20));
    }
    const backup = url.searchParams.get("backup");
    if (backup) {
      if (passwordOk(req.headers.get("x-admin-key")) !== "ok") return json({ error: "Wrong password" }, 401);
      return json(await store.get(backup, { type: "json" }));
    }
    const data = await store.get("content", { type: "json" });
    return json(data || null);
  }

  const check = passwordOk(req.headers.get("x-admin-key"));
  if (check === "missing")
    return json({ error: "The admin password is not set yet. In Netlify go to Site configuration → Environment variables and add ADMIN_PASSWORD, then redeploy." }, 500);
  if (check === "bad") return json({ error: "That password is not right." }, 401);

  if (req.method === "POST") return json({ ok: true });

  if (req.method === "PUT") {
    const text = await req.text();
    if (text.length > 3_000_000) return json({ error: "Content is too large (over 3 MB)." }, 413);
    let body;
    try { body = JSON.parse(text); } catch { return json({ error: "Content is not valid JSON." }, 400); }
    const missing = REQUIRED.filter((k) => !(k in (body || {})));
    if (missing.length) return json({ error: "Content is missing sections: " + missing.join(", ") }, 400);
    // keep a dated backup of what was live before this save
    const prev = await store.get("content", { type: "json" });
    if (prev) await store.setJSON("backup/" + new Date().toISOString(), prev);
    body.updatedAt = new Date().toISOString();
    await store.setJSON("content", body);
    return json({ ok: true, updatedAt: body.updatedAt });
  }

  return json({ error: "Method not allowed" }, 405);
};

export const config = { path: "/api/content" };
