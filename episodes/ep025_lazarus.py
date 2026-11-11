import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import *
from props import *

CAVE = (610, 390, 200, 0.44, 106, 168)   # x, w, h, mouth frac, mouth w, mouth h
STONE_X0, STONE_X1, STONE_R = 782, 945, 86

class Lazarus(Episode):
    dur = 18.0
    cta = "Read it in Scroll the Catholic Bible"
    kicker = "JOHN 11  •  THE RAISING OF LAZARUS"
    headline = "Four days in the tomb.\nOne word, and he walked out."
    captions = [
        (cpdv("John", 11, 35, "And Jesus wept."), "John 11:35", 3.8),
        (cpdv("John", 11, 39, "Jesus said, “Take away the stone.”"), "John 11:39", 6.8),
        (cpdv("John", 11, 44, "And immediately, he who had been dead went forth, bound at the feet and hands with winding bands."), "John 11:44", 10.9),
    ]

    def draw_panel(self, cr, i, t, y0, gy):
        cx0, cw, ch, mf, mw, mh = CAVE
        mx, _, _ = rock_cave(cr, cx0, gy, w=cw, h=ch, mouth=mf, mw=mw, mh=mh)

        # ---------- Lazarus (panel 3) ----------
        if i == 2 and t > 10.2:
            lx, lwa, _ = track(t, [(10.3, mx), (12.8, 712)])
            wrap = 1.0 - prog(t, 13.4, 14.4)
            bound = pose("stand", ls=2, le=0, rs=2, re=0, lt=1, rt=-1)
            if t < 14.0:
                p = mix(bound, walk(t, speed=1.1, amp=7), 0.8 * lwa) if lwa > 0 else bound
            else:
                p = keyed([(14.0, bound), (14.8, pose("joy"))], t)
            cr.save(); cr.rectangle(0, y0, W, PANEL_H); cr.clip()
            wrapped_figure(cr, lx, gy, p, s=0.9, face=-1, wrap=wrap)
            cr.restore()

        # ---------- the stone ----------
        roll = prog(t, 7.9, 9.4) if i >= 1 else 0.0
        sx = lerp(STONE_X0, STONE_X1, roll)
        round_stone(cr, sx, gy + 2, r=STONE_R, rot=-(sx - STONE_X0) / STONE_R * 1.0)

        # ---------- helper who rolls the stone ----------
        hx, hwa, _ = track(t, [(7.0, 640), (7.8, 690), (9.4, 852), (9.8, 852), (11.0, 590)])
        if i == 0: hx, hwa = 640, 0
        push = pose("reach", lean=28, rs=85, re=-5, ls=80, le=0, lt=-14, rt=-34)
        hp = pose("stand", head=12)
        hface = 1
        if i >= 1:
            if 7.8 <= t < 9.5: hp = push
            elif t >= 9.5:
                hp = pose("stand", head=-5); hface = -1 if t < 11.0 else 1
                if i == 2 and t > 10.6:
                    hp = keyed([(11.0, pose("stand", head=-5)), (11.6, pose("stand", lean=-10, head=-20, rs=60, re=60, ls=60, le=60)), (14.4, pose("stand", lean=-10, head=-20, rs=60, re=60, ls=60, le=60)), (15.0, pose("joy"))], t)
        draw_figure(cr, hx, gy, body(t, hp, hwa), s=0.95, face=hface)

        # ---------- Mary and Martha ----------
        mary = pose("head_hands")
        martha = pose("stand", head=30, lean=6, rs=70, re=90, ls=60, le=90)
        if i >= 1:
            recoil = pose("stand", lean=-10, head=-6, rs=150, re=140, ls=40, le=60)
            martha = keyed([(7.1, martha), (7.7, recoil), (9.6, recoil), (10.2, pose("stand", head=0))], t)
        if i == 2 and t > 11.0:
            martha = keyed([(11.0, pose("stand", head=0)), (11.6, pose("stand", head=-10, lean=-4, rs=80, re=40))], t)
            mary = keyed([(11.0, pose("head_hands")), (11.8, pose("stand", head=-10)), (14.2, pose("stand", head=-10)), (14.8, pose("joy"))], t)
            if t > 14.2: martha = keyed([(14.2, martha), (14.8, pose("joy"))], t)
        draw_figure(cr, 210, gy, mary, s=0.9, face=1)
        draw_figure(cr, 300, gy, martha, s=0.9, face=1)

        # ---------- Jesus ----------
        jx, jwa, _ = track(t, [(0.2, -60), (2.6, 430)])
        weep = pose("stand", head=26, lean=8, rs=150, re=150, ls=12, le=20)
        jp = keyed([(2.6, pose("stand")), (3.3, weep)], t)
        if i >= 1:
            jp = keyed([(2.6, pose("stand")), (3.3, weep), (5.6, weep), (6.3, pose("reach", rs=95, re=-5, lean=4))], t)
            if t > 9.6:
                jp = keyed([(9.6, pose("reach", rs=95, re=-5, lean=4)), (10.1, pose("stand", rs=60, re=10))], t)
        if i == 2 and t > 9.6:
            call = pose("stand", rs=150, re=5, head=-14, lean=-3)
            jp = keyed([(9.6, pose("reach", rs=95, re=-5, lean=4)), (10.0, call), (12.4, call), (13.0, pose("reach", rs=100, re=-10, ls=30, le=20)), (14.4, pose("stand", rs=60, re=20))], t)
        J = draw_figure(cr, jx, gy, body(t, jp, jwa), s=1.05, face=1, prop="robe")
        if t > 3.4:
            amt = prog(t, 3.4, 3.8) * (1 - (prog(t, 5.6, 6.0) if i >= 1 else 0))
            tears(cr, J["head"][0] + 8, J["head"][1] + 10, t, amt)
        if i == 2:
            cry_lines(cr, J["head"][0] + 6, J["head"][1], face=1, amount=prog(t, 10.0, 10.3) * (1 - prog(t, 11.8, 12.3)), t=t)

OUTPUT_NAME = "day13a_lazarus_john11"
