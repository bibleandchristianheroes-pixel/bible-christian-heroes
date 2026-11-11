import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import *
from props import *

FIRE = 430
PX = 585          # Peter's seat
JX = 300          # where Jesus stops

class PeterRestored(Episode):
    dur = 18.0
    ground = False
    caption_bg = True
    cta = "Pray it with Ave – Catholic Prayer Lock"
    kicker = "JOHN 18 & 21  •  PETER RESTORED"
    headline = "Three times he said no.\nThree times he was asked again."
    captions = [
        (cpdv("John", 18, 27, "Therefore, again, Peter denied it. And immediately the rooster crowed."), "John 18:27", 9.2),
        (cpdv("John", 21, 15, "“Simon, son of John, do you love me…?” …“Yes, Lord, you know that I love you.” …“Feed my lambs.”"), "John 21:15", 7.6),
        (cpdv("John", 21, 17, "…“Lord, you know all things. You know that I love you.” He said to him, “Feed my sheep."), "John 21:17", 10.6),
    ]

    def peter_start(self, t):
        warm = sit_pose(lean=14, head=30, rs=72, re=10, ls=64, le=14)
        warm["rs"] += 4 * math.sin(t * 1.3)
        return warm

    def draw_panel(self, cr, i, t, y0, gy):
        if i == 0:
            self.denial(cr, t, y0, gy)
        else:
            self.beach(cr, i, t, y0, gy)

    # ---------------- panel 1: the courtyard fire at night ----------------
    def denial(self, cr, t, y0, gy):
        ground_line(cr, gy)
        courtyard_wall(cr, 840, 1100, gy)
        stone_seat(cr, PX, gy); stone_seat(cr, 300, gy, w=56)
        fl = campfire(cr, FIRE, gy, t)
        # servant girl comes in from the left and points
        gx, gwa, _ = track(t, [(0.8, -60), (2.6, 215)])
        point = pose("reach", rs=95, re=-5, lean=4)
        gp = keyed([(2.6, pose("stand")), (3.0, point), (4.6, point), (5.0, pose("stand"))], t)
        draw_figure(cr, gx, gy, body(t, gp, gwa), s=0.92, face=1)
        # man by the fire stands and accuses too
        mp = sit_pose(lean=6, head=6, rs=70, re=10, ls=60, le=14)
        mp = keyed([(4.8, mp), (5.4, pose("stand")), (5.8, pose("reach", rs=95, re=-5)), (8.6, pose("reach", rs=95, re=-5)), (9.0, pose("stand", head=-14))], t)
        draw_figure(cr, 300, gy, mp, s=1.0, face=1)
        # Peter
        no = lambda tt: pose("stand", rs=70 + 25 * math.sin(tt * 10), re=-40, ls=70 - 25 * math.sin(tt * 10), le=-40, head=-6)
        px, pwa, _ = track(t, [(6.4, PX), (7.6, 720)])
        face = -1
        if t < 3.2:
            p = self.peter_start(t)
        elif t < 4.4:
            p = sit_pose(lean=4, head=6 + 14 * math.sin(t * 13), rs=80, re=-30, ls=80, le=-30)
        elif t < 6.4:
            p = keyed([(4.4, sit_pose(lean=4, head=-4, rs=40, re=40, ls=40, le=40)), (5.8, sit_pose(lean=4, head=-4, rs=40, re=40, ls=40, le=40)), (6.3, pose("stand"))], t)
        elif t < 7.7:
            p = body(t, pose("stand", head=10), pwa); face = 1
        elif t < 9.3:
            p = keyed([(7.7, pose("stand")), (8.1, no(t))], t) if t < 8.1 else no(t)
            face = -1
        else:
            cry = pose("kneel", lean=12, head=32, rs=150, re=150, ls=150, le=150)
            p = keyed([(9.3, pose("stand", head=-25)), (10.0, pose("stand", head=-25)), (10.8, cry)], t)
            face = 1 if t < 10.4 else -1
            if t > 10.8: p["lean"] = 12 + 3 * math.sin(t * 5)
        draw_figure(cr, px, gy, p, s=1.05, face=face)
        crow = prog(t, 8.9, 9.4) * (1 - prog(t, 10.6, 11.2))
        rooster(cr, 960, gy - 104, s=1.0, face=-1, crow=crow)
        dawn = prog(t, 8.3, 9.2)
        darkness(cr, y0, PANEL_H, 0.86, [(FIRE, gy - 40, 340, 1.0), (980, gy - 150, 240, 0.75 * dawn)])

    # ---------------- panels 2 and 3: the charcoal fire on the beach ----------------
    def beach(self, cr, i, t, y0, gy):
        su = prog(t, 2.5, 8.0)
        sun(cr, 1010, lerp(gy + 40, y0 + 210, su), r=26)
        cr.set_source_rgb(*BG); cr.rectangle(0, gy + 2, W, 120); cr.fill()
        ground_line(cr, gy, 0, 780)
        water(cr, gy + 4, t, x0=770, x1=W + 20, amp=4, rough=0.4, below=60)
        boat(cr, 935, gy - 8 + 3 * math.sin(t * 1.6), w=170)
        stone_seat(cr, PX, gy)
        campfire(cr, FIRE, gy, t)
        fish(cr, FIRE - 10, gy - 20, s=0.7); fish(cr, FIRE + 16, gy - 26, s=0.6, face=-1)

        # Jesus walks in from the left at dawn and offers bread from the fire
        jx, jwa, _ = track(t, [(1.6, -70), (4.8, JX)])
        offer = pose("reach", rs=82, re=-6, lean=6)
        jp = keyed([(4.8, pose("stand")), (5.2, pose("stand", lean=30, head=20, rs=40, re=0)), (5.7, offer), (7.1, offer), (7.5, pose("stand", rs=30, re=20))], t)
        if i == 2 and t > 7.5:
            ask = pose("stand", rs=60, re=10, head=-4)
            jp = keyed([(7.5, pose("stand")), (7.9, ask), (8.2, pose("stand")), (8.6, ask), (8.9, pose("stand")), (9.3, ask), (9.9, pose("stand")),
                        (10.3, pose("reach", rs=80, re=-10)), (11.2, pose("reach", rs=80, re=-10)), (11.6, pose("stand")),
                        (12.4, pose("stand", rs=55, re=-5, head=-4))], t)
        jface = 1
        if i == 2 and t > 11.6: jface = -1
        J = draw_figure(cr, jx, gy, body(t, jp, jwa), s=1.1, face=jface, prop="robe")

        # Peter
        lift = keyed([(0, {"h": 30}), (6.0, {"h": 30}), (7.0, {"h": -4})], t)["h"]
        face = -1; px = PX; pwa = 0
        if t < 6.0:
            p = self.peter_start(t)
        elif t < 7.6:
            p = keyed([(6.0, self.peter_start(t)), (6.6, sit_pose(lean=6, head=lift, rs=80, re=-4, ls=40, le=30)),
                       (7.2, sit_pose(lean=2, head=lift, rs=40, re=60, ls=40, le=30))], t)
        else:
            heart = sit_pose(lean=0, head=-6, rs=30, re=125, ls=40, le=30)
            if i == 1:
                feed = pose("kneel", lean=35, head=30, rs=65, re=0, ls=30, le=20)
                p = keyed([(7.6, sit_pose(lean=2, head=-4, rs=40, re=60, ls=40, le=30)), (8.0, heart), (10.4, heart),
                           (11.0, pose("stand", head=10)), (12.2, pose("stand", head=14)), (12.8, feed)], t)
                px, pwa, _ = track(t, [(11.0, PX), (11.4, PX - 10), (11.6, PX - 10), (12.4, PX - 30)])
                if t > 11.4: face = 1
            else:
                grieve = sit_pose(lean=16, head=34, rs=40, re=40, ls=30, le=40)
                tall = pose("stand", rs=30, re=125, head=-8)
                hold = pose("stand", rs=55, re=-5, ls=10, le=10, head=-6)
                p = keyed([(7.6, sit_pose(lean=2, head=-4, rs=40, re=60, ls=40, le=30)), (8.0, heart), (8.6, grieve), (9.4, grieve),
                           (10.0, pose("stand", head=0)), (10.4, tall), (10.9, tall), (11.3, hold)], t)
        PJ = draw_figure(cr, px, gy, body(t, p, pwa), s=1.05, face=face)

        # the bread passes from his hand to Peter's
        if 5.7 <= t < 7.6:
            u = prog(t, 6.3, 6.9)
            bx = lerp(J["rhand"][0] + 6, PJ["rhand"][0] - 6, u); by = lerp(J["rhand"][1], PJ["rhand"][1], u) - 20 * math.sin(math.pi * u)
            loaf(cr, bx, by - 4)
        elif t < 5.7:
            loaf(cr, FIRE + 46, gy - 9)

        if i == 1:   # a lamb comes; Peter feeds it
            lx, lwa, _ = track(t, [(10.6, 1150), (12.6, 650)])
            if t > 10.6:
                sheep(cr, lx, gy, s=0.58, face=-1, step=t * 10 if lwa > 0.1 else 0, graze=0.5 * prog(t, 12.8, 13.3))
            if t > 12.8:
                loaf(cr, PJ["rhand"][0] + 4, PJ["rhand"][1] + 4)
        else:        # the staff passes to Peter; sheep gather to him
            if 10.3 <= t < 11.2:
                u = prog(t, 10.6, 11.0)
                hx = lerp(J["rhand"][0], PJ["rhand"][0], u); hy = lerp(J["rhand"][1], PJ["rhand"][1], u)
                staff(cr, hx, hy - 70, hy + 50)
            elif t >= 11.2:
                hx, hy = PJ["rhand"]; staff(cr, hx, hy - 76, gy)
            for k, (sx0, sx1) in enumerate(((-120, 70), (-200, 150), (-290, 225))):
                sx, swa, _ = track(t, [(11.6 + 0.3 * k, sx0), (14.2 + 0.2 * k, sx1)])
                if sx > -80:
                    sheep(cr, sx, gy, s=0.72, face=1, step=t * 9 + k if swa > 0.1 else 0, graze=0.0)

        night = 0.86 * (1 - prog(t, 2.5, 7.5))
        darkness(cr, y0, PANEL_H, night, [(FIRE, gy - 40, 340, 1.0)])

OUTPUT_NAME = "day21b_peter_restored_john21"
