import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import *
from props import *

MX = 470            # where the storm catches him
CAVE = (770, 300, 200, 0.5, 116, 156)     # x, w, h, mouth, mw, mh -> mouth centre 920
FALL_X = 330        # P1: where he trips while running away
DROP_X = 330        # P3: where he lays the load down
HILL = (0.80, 0.77, 0.71)
CHUNKS = [(560, 13, 2.9), (640, 17, 3.3), (600, 11, 3.8), (700, 15, 6.6)]   # stones shaken off the hill

BENT = pose("stand", lean=34, head=12, rs=20, re=110, ls=15, le=115)
s_flinch = pose("stand", lean=-6, head=-16, rs=150, re=110, ls=140, le=120)
s_brace = pose("stand", lean=20, head=26, rs=150, re=140, ls=145, le=140)
s_shrug = pose("stand", lean=10, head=10, rs=40, re=40, ls=30, le=40)
k_down = pose("kneel", lean=8, head=16, rs=20, re=20, ls=15, le=20)
k_empty = pose("kneel", lean=-4, head=-16, rs=138, re=-24, ls=128, le=-24)   # open, empty hands
k_cower = pose("kneel", lean=36, head=34, rs=150, re=150, ls=150, le=150)


class BeStill(Episode):
    dur = 18.0
    cta = "Pray it with Ave – Catholic Prayer Lock"
    caption_bg = True
    kicker = "PSALM 45 (46)  •  BE STILL"
    headline = "When everything shakes,\ndo you run, hide, or be still?"
    captions = [
        (cpdv("Psalms", 45, 3, "…the earth will be turbulent and the mountains will be transferred into the heart of the sea."), "Psalm 45:3", 5.8),
        (cpdv("Psalms", 45, 4, "They thundered, and the waters were stirred up…"), "Psalm 45:4", 7.8),
        (cpdv("Psalms", 45, 11, "Be empty, and see that I am God."), "Psalm 45:11", 10.4),
    ]

    def draw_panel(self, cr, i, t, y0, gy):
        storm = prog(t, 2.4, 3.2)
        if i == 2:
            storm *= 1 - prog(t, 9.4, 11.0)
        quake = (prog(t, 2.6, 2.8) * (1 - prog(t, 4.0, 4.4)) + prog(t, 6.5, 6.7) * (1 - prog(t, 7.2, 7.5))) * storm
        flashes = [(3.0, 0), (7.6, 3)] + ([(8.3, 5)] if i == 1 else [])
        flash, bolt_seed, bolt_x = 0.0, 0, 0
        for tf, sd in flashes:
            f = clamp(1 - abs(t - tf) / 0.18) * (storm > 0.5)
            if f > flash:
                flash, bolt_seed, bolt_x = f, sd, 640 + 90 * sd
        calm = prog(t, 10.0, 12.0) if i == 2 else 0.0

        cr.save(); cr.translate(8 * quake * math.sin(t * 47), 3 * quake * math.sin(t * 61))
        mountain(cr, 430, gy, w=420, h=230, color=HILL)
        for gx in (60, 280, 720):
            grass_tuft(cr, gx, gy, 12, sway=0.5 * storm * math.sin(t * 5 + gx))
        cx0, cw, ch, mf, mw, mh = CAVE
        mx_c, _, _ = rock_cave(cr, cx0, gy, w=cw, h=ch, mouth=mf, mw=mw, mh=mh)
        for k, (rx, r, ts) in enumerate(CHUNKS):
            if k == 3 and i == 2:
                continue
            u = clamp((t - ts) / 1.0)
            if u > 0:
                land = rx + (40 if k % 2 else -50)
                x = lerp(rx, land, u); y = lerp(gy - 200 + 30 * k, gy - r * 0.8, u * u)
                rock_chunk(cr, x, y, r, rot=k + 5 * u, color=(0.55, 0.52, 0.47))

        # ---------------- the man and his load ----------------
        x, wa, _ = track(t, [(0.0, -60), (2.6, MX)])
        face = 1
        p = body(t, BENT, wa, speed=1.0)
        for k_ in ("lean", "head", "rs", "re", "ls", "le"): p[k_] = BENT[k_]
        load = "back"; col = INK; fallen = None
        if t >= 2.6:
            p = keyed([(2.6, BENT), (3.1, s_flinch)], t)
        if i == 0 and t >= 3.4:
            face = -1
            x, wa, _ = track(t, [(3.6, MX), (4.9, FALL_X)])
            if t < 4.9:
                p = run(t, speed=2.2); p["lean"] = 26; p["head"] = -4
                p["rs"], p["re"], p["ls"], p["le"] = 20, 110, 15, 115
            else:
                fallen = prog(t, 4.9, 5.4)
        elif i == 1 and t >= 3.4:
            x, wa, _ = track(t, [(3.6, MX), (5.4, mx_c)])
            if t < 5.4:
                p = run(t, speed=2.2); p["lean"] = 26
                p["rs"], p["re"], p["ls"], p["le"] = 20, 110, 15, 115
            else:
                p = keyed([(5.4, s_brace), (5.9, k_cower)], t)
                x += 2.5 * math.sin(t * 38) * (t > 6.0)                # trembling
                col = tuple(lerp(INK[j], SOFT[j], prog(t, 5.4, 5.9)) for j in range(3))
        elif i == 2 and t >= 3.4:
            x, wa, _ = track(t, [(4.6, MX), (5.4, MX - 40), (6.4, MX - 40)])
            p = keyed([(3.1, s_flinch), (3.8, s_brace), (4.6, s_brace), (5.2, s_shrug), (5.8, pose("stand", head=6)),
                       (6.8, k_down), (7.6, k_down), (8.4, k_empty)], t)
            p = body(t, p, wa * 0.6, speed=1.0)
            if t > 5.0:
                load = "drop"

        if fallen is None:
            J = draw_figure(cr, x, gy, p, s=1.0, face=face, color=col)
        else:
            fp = mix(pose("stand", lean=30, head=-10, rs=150, re=20, ls=140, le=20),
                     pose("lie", ls=170, le=0, rs=165, re=0, head=0), fallen)
            J = draw_rotated(cr, x, gy, -90 * fallen, fp, s=1.0, face=1, lift=19 * fallen)

        # the burden
        if load == "back" and fallen is None:
            sx, sy = J["sh"]
            bx = sx - 72 if face == 1 else sx + 8
            if i == 1 and t > 5.4:
                bx = lerp(bx, mx_c - 4, prog(t, 5.4, 5.9)); sy = lerp(sy, gy + 34 - 26 - 60, prog(t, 5.4, 5.9))
            burden(cr, bx, sy - 26, w=64, h=60, color=col if i == 1 else INK)
            draw_figure(cr, x, gy, p, s=1.0, face=face, color=col)
        elif load == "back":
            u = fallen
            burden(cr, x - 120 * u - 30, lerp(gy - 200, gy - 78, u), w=64, h=60)
        elif load == "drop":
            u = prog(t, 5.0, 5.8)
            sx, sy = J["sh"]
            bx = lerp(sx - 72, DROP_X, u); by = lerp(sy - 26, gy - 60, u * u)
            burden(cr, bx, by, w=64, h=60)
        cr.restore()

        # ---------------- sky ----------------
        storm_sky(cr, y0, PANEL_H, storm, flash)
        rain(cr, y0, PANEL_H, t, amount=storm)
        wind(cr, y0 + 70, t, 1.1 * storm)
        lightning(cr, bolt_x, y0 + 10, gy - 220, flash, seed=bolt_seed)
        if i == 2:
            sun(cr, 930, y0 + 110 + 40 * (1 - calm), r=30 * calm, rays=10) if calm > 0.05 else None
            warm_glow(cr, MX - 40, gy - 100, 320, 0.8 * calm)
            light_rays(cr, MX - 40, gy - 150, 0.5 * calm, r0=60, r1=110, n=14, t=t)
            for k in range(2):
                bx = lerp(1150, 700 - 120 * k, prog(t, 12.0 + 0.5 * k, 15.0 + 0.5 * k))
                if t > 12.0 + 0.5 * k:
                    bird(cr, bx, y0 + 150 + 30 * k + 8 * math.sin(t * 2 + k), math.sin(t * 9 + k), s=0.9, face=-1)


OUTPUT_NAME = "day37b_be_still_psalm45"
