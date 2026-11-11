import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import *
from props import *

SEAT = 820          # judgment seat
WX = 640            # where the widow pleads
JX = 832            # judge's hip when seated

# visits: (arrive_start, arrive_end, leave_start, leave_end)
VISITS = [(0.3, 2.4, 4.4, 5.4), (6.0, 7.2, 8.4, 9.3), (9.8, 10.8, 99, 99)]
NIGHTS = [(5.2, 6.2), (9.1, 10.0)]

class PersistentWidow(Episode):
    dur = 18.0
    caption_bg = True
    cta = "Start your day with Ave Missal"
    kicker = "LUKE 18  •  THE PERSISTENT WIDOW"
    headline = "He refused her. Again and again.\nShe kept coming back."
    captions = [
        (cpdv("Luke", 18, 3, "…she went to him, saying, ‘Vindicate me from my adversary.’"), "Luke 18:3", 3.0),
        (cpdv("Luke", 18, 4, "And he refused to do so for a long time."), "Luke 18:4", 7.6),
        (cpdv("Luke", 18, 5, "…because this widow is pestering me, I will vindicate her…"), "Luke 18:5", 12.1),
    ]

    def draw_panel(self, cr, i, t, y0, gy):
        nights = NIGHTS if i >= 1 else []
        night = 0.0
        for a, b in nights:
            m = (a + b) / 2
            night = max(night, prog(t, a, m) * (1 - prog(t, m, b)))
        # the sun crosses again each day
        if i == 0:
            day = 0.35
        else:
            day = prog(t, 0.0, 5.5) if t < 5.7 else (prog(t, 5.7, 9.4) if t < 9.55 else prog(t, 9.55, 14.0) * 0.5)
        a = math.pi * (1 - (0.15 + 0.7 * day))
        if night < 0.2:
            sun(cr, 950 + 95 * math.cos(a), y0 + 175 - 80 * math.sin(a), r=16, rays=8)
        if i == 2:
            warm_glow(cr, WX + 60, gy - 110, 380, prog(t, 12.6, 13.8))

        fy, st = judge_seat(cr, SEAT, gy, face=-1)

        # ---------- judge ----------
        sit = pose("stand", lt=88, lk=88, rt=82, rk=82, lean=-3, ls=40, le=50, rs=40, re=50, head=-6)
        wave = pose("stand", lt=88, lk=88, rt=82, rk=82, lean=-6, ls=40, le=50, rs=70, re=-70, head=-28)
        ears = pose("stand", lt=88, lk=88, rt=82, rk=82, lean=2, head=12, ls=150, le=150, rs=150, re=150)
        p = sit
        for k, (a0, a1, l0, l1) in enumerate(VISITS[: (1 if i == 0 else 3)]):
            if a1 + 1.2 <= t < a1 + 2.4:
                u = 0.5 + 0.5 * math.sin((t - a1 - 1.2) * 14)
                p = mix(wave, pose("stand", lt=88, lk=88, rt=82, rk=82, lean=-6, ls=40, le=50, rs=70, re=-20, head=-28), u)
        if i == 0 and t >= VISITS[0][1] + 2.4:
            p = keyed([(VISITS[0][1] + 2.4, wave), (VISITS[0][1] + 2.8, pose("stand", lt=88, lk=88, rt=82, rk=82, lean=-6, head=-28, ls=40, le=50, rs=40, re=50))], t)
        jx, jface = JX, -1
        if i == 1 and t >= 11.0:
            p = keyed([(11.0, sit), (11.5, ears)], t)
        if i == 2 and t >= 11.0:
            stand = pose("stand", head=-4)
            grant = pose("stand", rs=95, re=-10, head=-6)
            p = keyed([(11.0, sit), (11.5, stand), (12.0, stand), (12.4, grant)], t)
            jx, wa, _ = track(t, [(11.5, JX), (12.0, 770)])
            p = body(t, p, wa)
        draw_figure(cr, jx, fy, p, s=1.05, face=jface, prop="robe_hat")

        # ---------- widow ----------
        x, face, wp = -100, 1, pose("stand", lean=12, head=16)
        plead = pose("stand", lean=4, head=-18, rs=125, re=-15, ls=115, le=-10)
        bowed = pose("stand", lean=40, head=35, lt=25, lk=35, rt=5, rk=35, rs=60, re=10, ls=50, le=10)
        for k, (a0, a1, l0, l1) in enumerate(VISITS[: (1 if i == 0 else 3)]):
            if t >= a0:
                x, wa, d = track(t, [(a0, -80), (a1, WX), (l0, WX), (l1, -80)])
                face = d if wa > 0.05 else 1
                if wa > 0.05:
                    wp = body(t, pose("stand", lean=12, head=16), wa, speed=1.3)
                else:
                    wp = keyed([(a1, pose("stand", lean=12, head=16)), (a1 + 0.3, plead), (a1 + 1.4, plead), (a1 + 2.0, pose("stand", lean=14, head=24))], t)
                    if a1 + 0.3 < t < a1 + 1.4:
                        wp["rs"] += 10 * math.sin(t * 9); wp["ls"] += 10 * math.sin(t * 9 + 1)
        if i == 0 and t > VISITS[0][1] + 2.0:
            wp = keyed([(VISITS[0][1] + 2.0, pose("stand", lean=14, head=24)), (VISITS[0][1] + 2.6, bowed)], t)
            x, face = WX, 1
        if i == 1 and t > VISITS[2][1] + 1.4:
            wp = plead; wp["rs"] += 8 * math.sin(t * 7); wp["ls"] += 8 * math.sin(t * 7 + 1)
        if i == 2 and t > VISITS[2][1] + 1.4:
            wp = keyed([(12.2, plead), (12.6, pose("stand", head=-12)), (13.0, pose("joy"))], t)
        draw_figure(cr, x, gy, wp, s=0.98, face=face, prop="robe")

        if night > 0:
            darkness(cr, y0, PANEL_H, 0.75 * night)
            crescent_moon(cr, 960, y0 + 120, 20, alpha=night)

OUTPUT_NAME = "day20b_persistent_widow_luke18"
