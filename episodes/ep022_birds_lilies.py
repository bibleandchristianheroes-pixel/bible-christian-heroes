import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import *
from props import *

PACE = [(0.0, 330), (1.4, 600), (1.7, 600), (3.1, 330), (3.4, 330), (4.6, 520)]
LILIES = [(610, 0.0), (690, 0.5), (770, 0.9), (850, 0.3), (930, 0.7), (420, 1.1)]
PILE_X = 650

def load_pos(J, face, k):
    """Top-left of the k-th worry box stacked on his back."""
    shx, shy = J["sh"]
    return shx - face * 26 - 17, shy + 6 - k * 28

class BirdsLilies(Episode):
    dur = 18.0
    caption_bg = True
    cta = "Pray it with Ave – Catholic Prayer Lock"
    kicker = "MATTHEW 6  •  BIRDS AND LILIES"
    headline = "Carrying tomorrow's worries?\nLook at the birds."
    captions = [
        (cpdv("Matthew", 6, 26, "Consider the birds of the air… and yet your heavenly Father feeds them."), "Matthew 6:26", 6.4),
        (cpdv("Matthew", 6, 28, "…Consider the lilies of the field, how they grow; they neither work nor weave."), "Matthew 6:28", 7.6),
        (cpdv("Matthew", 6, 34, "Therefore, do not be anxious about tomorrow…"), "Matthew 6:34", 10.8),
    ]

    def draw_panel(self, cr, i, t, y0, gy):
        loaded = pose("stand", lean=16, head=24, rs=150, re=120, ls=20, le=20)   # bent, hand on head
        x, wa, d = track(t, PACE)
        face = d if wa > 0.05 else (1 if t > 4.6 else -1)
        if t < 4.6:
            p = body(t, loaded, wa, speed=1.3)
            if wa > 0.05: p["lean"] = 16; p["rs"] = 150; p["re"] = 120
        else:
            p = loaded
        nload, lie, carried = 3, 0.0, []
        night = 0.0
        # ---------- panel 1: the birds are fed ----------
        if i == 0:
            look = pose("stand", lean=10, head=6, rs=20, re=20)
            if t > 4.6:
                p = keyed([(4.6, loaded), (5.4, look), (9.0, look), (9.6, pose("stand", lean=12, head=-14, rs=20, re=20))], t)
            for k, bx in enumerate((760, 840, 920)):
                u = prog(t, 4.2 + k * 0.4, 5.6 + k * 0.4)
                for s in range(3):   # grain falls from above
                    st = 5.4 + k * 0.5 + s * 0.9
                    v = (t - st) / 0.9
                    if 0 <= v <= 1:
                        seed_dot(cr, bx + 18 + s * 6, lerp(y0 + 40, gy - 3, v), r=3)
                if u <= 0: continue
                fx, fy = lerp(1150 + k * 30, bx, u), lerp(y0 + 60, gy - 12, u) - 30 * math.sin(math.pi * u)
                peck = 0.0 if u < 1 else max(0.0, math.sin(t * 9 + k * 1.7))
                cr.save(); cr.translate(fx, fy); cr.rotate(-0.5 * peck if True else 0)
                bird(cr, 0, 0, math.sin(t * 15 + k) if u < 1 else 0.15, s=1.0, face=1 if u >= 1 else -1)
                cr.restore()
                if u >= 1:   # little legs
                    cr.set_source_rgb(*INK); cr.set_line_width(2)
                    cr.move_to(fx - 2, fy + 5); cr.line_to(fx - 2, gy); cr.stroke()
        # ---------- panel 2: the lilies grow ----------
        elif i == 1:
            for lx, dl in LILIES:
                lily(cr, lx, gy, prog(t, 4.4 + dl, 7.6 + dl), h=72, sway=math.sin(t * 1.4 + lx))
            if t > 4.6:
                kneel = pose("kneel", lean=30, head=30, rs=60, re=0, ls=30, le=20)
                p = keyed([(4.6, loaded), (5.6, pose("stand", lean=10, head=20)), (8.0, pose("stand", lean=10, head=20)), (8.8, kneel)], t)
            if t > 8.8: nload = 2
        # ---------- panel 3: sets it all down and sleeps ----------
        else:
            night = prog(t, 6.0, 9.0)
            if t > 4.6:
                x, wa, d = track(t, [(4.6, 520), (5.4, 520), (6.6, 560)])
                face = 1
                set_down = pose("stand", lean=40, head=25, rs=75, re=10, ls=60, le=10)
                p = keyed([(4.6, loaded), (6.6, pose("stand", lean=10, head=10)), (7.0, set_down), (9.6, set_down), (10.2, pose("stand", head=-12))], t)
                p = body(t, p, wa)
                for k in range(3):
                    tk = 7.0 + k * 0.85
                    if t > tk: nload = min(nload, 2 - k)
                    u = prog(t, tk, tk + 0.6)
                    if u > 0: carried.append((k, u))
                lie = prog(t, 10.2, 11.0)
        if lie <= 0:
            J = draw_figure(cr, x, gy, p, s=1.0, face=face)
        else:
            if lie < 1:
                cr.push_group(); draw_figure(cr, x, gy, pose("sad_sit", head=10), s=1.0, face=face); cr.pop_group_to_source(); cr.paint_with_alpha(1 - lie)
            breathe = 1.5 * math.sin(t * 2.2)
            cr.push_group(); draw_rotated(cr, x + 80, gy, -90, pose("lie", ls=150, le=30, head=-10), s=1.0, face=1, lift=12 + breathe * 0.3)
            cr.pop_group_to_source(); cr.paint_with_alpha(lie)
            J = None
        # the worries he carries
        for k in range(3):
            if k < nload and J is not None and not any(c[0] == 2 - k for c in carried):
                bx, by = load_pos(J, face, k)
                burden(cr, bx, by, w=34, h=28)
        if i == 1 and t > 8.8:   # one worry slides off beside the lilies
            u = prog(t, 8.8, 9.6)
            sx, sy = 520 - 26 - 17 + 40, gy - 170
            burden(cr, lerp(sx, 430, u), lerp(sy, gy - 28, u * u), w=34, h=28)
        for (k, u) in carried:   # set down in a pile
            src = (x - 26 - 17, gy - 170 - (2 - k) * 28)
            dst = (PILE_X + 20, gy - 28 - k * 28)
            burden(cr, lerp(src[0], dst[0], u), lerp(src[1], dst[1], u), w=34, h=28)
        if night > 0:
            darkness(cr, y0, PANEL_H, 0.75 * night, [(x + 40, gy - 30, 200, 0.35 * lie)])
            cr.save(); cr.push_group(); moon(cr, 900, y0 + 250 - 40 * night, r=26); cr.pop_group_to_source(); cr.paint_with_alpha(night); cr.restore()
            cr.set_source_rgba(0.98, 0.94, 0.8, 0.8 * night)
            for k in range(7):
                sx, sy = 800 + (k * 137) % 260, y0 + 210 + (k * 53) % 120
                if (sx - 900) ** 2 + (sy - (y0 + 250 - 40 * night)) ** 2 < 60 ** 2: continue
                cr.arc(sx, sy, 2.2 + 0.6 * math.sin(t * 3 + k), 0, 2 * math.pi); cr.fill()

OUTPUT_NAME = "day11b_birds_lilies_matthew6"
