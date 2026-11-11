import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import *
from props import *

MX = 440          # where he stops to look at the seed
TREE_X = 910

class MustardSeed(Episode):
    dur = 18.0
    cta = "Pray it with Ave – Catholic Prayer Lock"
    kicker = "MATTHEW 13  •  THE MUSTARD SEED"
    headline = "The smallest seed.\nNever underestimate it."
    captions = [
        (cpdv("Matthew", 13, 31, "…a grain of mustard seed, which a man took and sowed in his field."), "Matthew 13:31", 4.4),
        (cpdv("Matthew", 13, 32, "…it becomes a tree, so much so that the birds of the air come and dwell in its branches."), "Matthew 13:32", 10.6),
        (cpdv("Matthew", 17, 19, "…faith like a grain of mustard seed, you will say to this mountain, ‘Move from here to there,’ and it shall move."), "Matthew 17:19", 8.4),
    ]

    def draw_panel(self, cr, i, t, y0, gy):
        look = pose("stand", rs=115, re=-35, head=-14)
        # ---------- scenery ----------
        if i == 1:
            for k, px in enumerate((560, 620, 700, 760, 1040)):
                sprout(cr, px, gy, 16 + (k % 2) * 8)
            grow = prog(t, 5.0, 11.0) if t < 5.6 else 0.12 + 0.88 * prog(t, 5.6, 11.0)
            if t < 5.6: grow = 0.12 * prog(t, 4.6, 5.6)
            perches = mustard_tree(cr, TREE_X, gy, grow, sway=4 * math.sin(t * 1.3))
        if i == 2:
            move = prog(t, 7.6, 10.6)
            sun(cr, 880, gy - 92, r=24)
            shake = 3 * math.sin(t * 40) * prog(t, 6.8, 7.4) * (1 - move)
            mountain(cr, 620 + shake + 700 * move * move, gy, w=440, h=200)
            if 7.4 < t < 10.8:   # dust
                cr.set_source_rgba(*SOFT, 0.6 * (1 - prog(t, 9.8, 10.8)))
                for k in range(10):
                    dx = 620 + 700 * move * move + (k * 41) % 120 - 30
                    cr.arc(dx, gy - 6 - (k * 7) % 22, 5 + k % 3 * 2, 0, 2 * math.pi); cr.fill()
        # ---------- the man ----------
        x, wa, _ = track(t, [(0.0, -60), (1.6, MX)]); face = 1
        p = body(t, pose("stand"), wa)
        if 1.6 <= t:
            p = keyed([(1.6, pose("stand")), (2.0, look), (3.4, look), (3.8, pose("stand"))], t)
        seed_at = "hand" if 1.8 < t < 3.6 else None
        if i == 0 and t >= 3.6:
            x, wa, _ = track(t, [(3.6, MX), (4.0, 480)])
            kneel = pose("kneel", lean=45, head=35, rs=70, re=-5)
            p = keyed([(4.0, pose("stand")), (4.4, kneel), (5.4, kneel), (6.0, pose("kneel", lean=20, head=30, rs=30, re=30)),
                       (12.0, pose("kneel", lean=20, head=30, rs=30, re=30)), (12.8, pose("kneel", lean=10, head=20, rs=150, re=15, ls=140, le=15))], t)
            p = body(t, p, wa)
            if t < 4.6: seed_at = "hand"
            sprout(cr, 545, gy, 30 * prog(t, 5.6, 9.0))
            if 4.6 <= t < 5.6: seed_dot(cr, 545, gy - 4, r=2.6)
        elif i == 1 and t >= 3.6:
            x, wa, d = track(t, [(3.6, MX), (4.6, 845), (6.2, 845), (7.0, 620)])
            kneel = pose("kneel", lean=45, head=35, rs=70, re=-5)
            if t < 4.6:
                p = body(t, pose("stand"), wa); seed_at = "hand"
            elif t < 6.2:
                p = keyed([(4.6, pose("stand")), (5.0, kneel), (5.8, kneel), (6.2, pose("stand"))], t)
                if t < 5.0: seed_at = "hand"
            else:
                face = -1 if t < 7.0 else 1
                p = keyed([(7.0, pose("stand")), (7.6, pose("stand", head=-25)), (10.4, pose("stand", head=-35)), (11.4, pose("joy"))], t)
                p = body(t, p, wa)
        elif i == 2 and t >= 3.6:
            pray = pose("stand", rs=120, re=-30, ls=120, le=-30, head=-10)
            raise_ = pose("stand", rs=150, re=-10, head=-18, lean=4)
            p = keyed([(3.6, pose("stand")), (4.2, pray), (6.0, pray), (6.6, raise_), (10.8, raise_), (11.2, pose("stand"))], t)
            if t < 10.8: seed_at = "hand" if t > 6.4 else None
            if t >= 11.2:
                x, wa, _ = track(t, [(11.2, MX), (13.6, 760)])
                p = body(t, keyed([(13.6, pose("stand")), (14.2, pose("joy"))], t), wa)
        J = draw_figure(cr, x, gy, p, s=1.0, face=face)
        if seed_at == "hand":
            hx, hy = J["rhand"]
            warm_glow(cr, hx, hy - 6, 34, 0.8)
            seed_dot(cr, hx, hy - 6, r=3.0)
        # ---------- birds come to dwell ----------
        if i == 1 and t > 9.6:
            for k, (px, py) in enumerate(perches[:4]):
                u = prog(t, 9.8 + k * 0.45, 11.4 + k * 0.45)
                sx, sy = 1150 + k * 40, y0 + 40 + k * 20
                bx, by = lerp(sx, px, u), lerp(sy, py - 8, u) - 40 * math.sin(math.pi * u)
                flap = math.sin(t * 14 + k) if u < 1 else 0.1
                bird(cr, bx, by, flap, s=0.85, face=-1 if (u < 1 or k % 2) else 1)

OUTPUT_NAME = "day09b_mustard_seed_matthew13"
