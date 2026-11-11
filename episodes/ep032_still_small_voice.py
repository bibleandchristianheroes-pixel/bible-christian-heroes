import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import *
from props import *

CAVE = (580, 460, 200, 0.62, 104, 168)
CRAG = (150, 470, 50, 50)
CHUNKS = [(250, 16, 2.3), (330, 20, 2.9), (410, 14, 3.4), (290, 12, 3.9), (380, 18, 4.4)]   # x, r, start time
FIRES = [(250, 0.0), (380, 0.4), (510, 0.8)]

class StillSmallVoice(Episode):
    dur = 18.0
    cta = "Start your day with Ave Missal"
    kicker = "1 KINGS 19  •  THE STILL SMALL VOICE"
    headline = "Not in the wind. Not in the fire.\nIn a whisper."
    captions = [
        (cpdv("I Kings", 19, 11, "…a great and strong wind, tearing apart the mountains, and crushing the rocks… But the Lord was not in the wind."), "1 Kings 19:11", 3.0),
        (cpdv("I Kings", 19, 12, "And after the earthquake, there was a fire. But the Lord was not in the fire."), "1 Kings 19:12", 8.0),
        (cpdv("I Kings", 19, 13, "…he covered his face with his cloak, and going out, he stood at the entrance of the cave."), "1 Kings 19:13", 12.6),
    ]

    def draw_panel(self, cr, i, t, y0, gy):
        windy = prog(t, 1.8, 2.4) * (1 - prog(t, 5.0, 5.8))
        quake = prog(t, 6.0, 6.2) * (1 - prog(t, 7.0, 7.3)) if i >= 1 else 0.0
        fire = prog(t, 7.4, 8.2) * (1 - (prog(t, 10.4, 11.2) if i == 2 else 0)) if i >= 1 else 0.0
        hush = prog(t, 11.4, 12.2) if i == 2 else 0.0
        cr.save(); cr.translate(9 * quake * math.sin(t * 47), 3 * quake * math.sin(t * 61))
        warm_glow(cr, 380, gy - 40, 420, 0.9 * fire)
        warm_glow(cr, 760, gy - 120, 380, 0.6 * prog(t, 13.4, 14.8) if i == 2 else 0)
        cx0, cw, ch, mf, mw, mh = CAVE
        mx, _, _ = rock_cave(cr, cx0, gy, w=cw, h=ch, mouth=mf, mw=mw, mh=mh)
        x0, x1, rh, sl = CRAG
        rock_mound(cr, x0, x1, gy, rh, sl)
        # rocks torn off by the wind
        for k, (rx, r, ts) in enumerate(CHUNKS):
            u = clamp((t - ts) / 1.3)
            if u <= 0:
                rock_chunk(cr, rx, gy - rh - r * 0.7, r, rot=k)
            else:
                dist = 170 + 40 * k
                land = rx - dist
                x = lerp(rx, land, u); y = lerp(gy - rh - r * 0.7, gy - r * 0.8, u) - 90 * math.sin(math.pi * u) * (1 - 0.4 * u)
                rock_chunk(cr, x, y, r, rot=k + 6 * u)

        # ---------- Elijah ----------
        ex, ewa, eface = mx, 0, -1
        brace = pose("stand", lean=10, head=15, rs=150, re=120, ls=140, le=120)
        ep = pose("stand", head=6)
        if windy > 0.2 or fire > 0.2: ep = brace
        if quake > 0.2: ep = pose("kneel", lean=20, head=20, rs=40, re=20, ls=40, le=20)
        col = SOFT
        if i == 2 and t > 11.6:
            cover = pose("stand", lean=8, head=24, rs=150, re=140, ls=120, le=130)
            ep = keyed([(11.6, pose("stand", head=-6)), (12.2, cover)], t)
            ex, ewa, _ = track(t, [(12.4, mx), (13.8, 742)])
            ep = body(t, ep, ewa * 0.7, speed=1.1)
            c = prog(t, 12.6, 13.4)
            col = tuple(lerp(SOFT[j], INK[j], c) for j in range(3))
        draw_figure(cr, ex, gy, ep, s=0.86, face=eface, color=col)

        # ---------- fire ----------
        for (fx, dl) in FIRES:
            h = 120 * fire * prog(t, 7.4 + dl, 8.2 + dl)
            flames(cr, fx, gy, h, t, w=1.1, seed=fx)
        cr.restore()
        wind(cr, y0 + 70, t, 1.4 * windy)
        breeze(cr, lerp(60, 380, prog(t, 11.4, 15.0)), gy - 150, t, hush * (1 - 0.5 * prog(t, 15.0, 16.5)), length=260)

OUTPUT_NAME = "day16b_still_small_voice_1kings19"
