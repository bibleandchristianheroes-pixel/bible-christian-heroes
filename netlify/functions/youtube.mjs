// Latest videos for a YouTube channel, read from YouTube's public RSS feed. Cached for 30 minutes.
const decode = (s) =>
  s.replace(/&amp;/g, "&").replace(/&quot;/g, '"').replace(/&#39;/g, "'").replace(/&lt;/g, "<").replace(/&gt;/g, ">");

export default async (req) => {
  const id = new URL(req.url).searchParams.get("id") || "";
  if (!/^UC[\w-]{22}$/.test(id)) {
    return new Response(JSON.stringify({ error: "Bad channel id" }), { status: 400, headers: { "content-type": "application/json" } });
  }
  try {
    const r = await fetch("https://www.youtube.com/feeds/videos.xml?channel_id=" + id, { headers: { "user-agent": "Mozilla/5.0" } });
    if (!r.ok) throw new Error("YouTube answered " + r.status);
    const xml = await r.text();
    const items = [...xml.matchAll(/<entry>([\s\S]*?)<\/entry>/g)].slice(0, 12).map((m) => {
      const e = m[1];
      const pick = (re) => (e.match(re) || [])[1] || "";
      return {
        id: pick(/<yt:videoId>([^<]+)<\/yt:videoId>/),
        title: decode(pick(/<title>([^<]*)<\/title>/)),
        published: pick(/<published>([^<]+)<\/published>/),
      };
    }).filter((v) => v.id);
    return new Response(JSON.stringify(items), {
      headers: { "content-type": "application/json", "cache-control": "public, max-age=1800" },
    });
  } catch (err) {
    return new Response(JSON.stringify({ error: String(err.message || err) }), { status: 502, headers: { "content-type": "application/json" } });
  }
};

export const config = { path: "/api/youtube" };
