import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import *
from props import *

GX = 175            # the invited guest, by his new farm
SX = 505            # the servant's place at the end of the table
TX0, TX1 = 560, 945 # the feast table
HX = 1000           # the host, facing left
SEATS = [625, 715, 805, 895]

beckon = pose("reach", rs=70, re=-45, lean=6)
point_back = pose("stand", rs=-70, re=-10, head=-12, lean=-4)
stop = pose("stand", rs=75, re=95, head=6, lean=-4)
shrug = pose("stand", rs=50, re=-45, ls=45, le=-40, head=14)
h_point = pose("reach", rs=86, re=-4, lean=4, head=-2)
h_ready = pose("stand", rs=70, re=-20, ls=60, le=-20, head=6)
h_sad = pose("stand", head=34, lean=8, rs=8, re=24, ls=6, le=24)
h_welcome = pose("stand", rs=105, re=-10, ls=95, le=-10, head=-8)
seated = sit_pose(rs=70, re=-25, ls=62, le=-20, head=4)
seated_cane = sit_pose(rs=55, re=-5, ls=62, le=-20, head=-10)


def walker(t, x_keys, base, sit, amp=24, speed=1.7, arm_fixed=False):
    """Walk along x_keys, then sit down at the end. Returns (x, pose)."""
    x, wa, _ = track(t, x_keys)
    t_end = x_keys[-1][0]
    if t > t_end:
        return x, keyed([(t_end, base), (t_end + 0.5, sit)], t)
    p = mix(base, walk(t, speed=speed, amp=amp), wa) if wa > 0 else dict(base)
    if arm_fixed:
        p["rs"], p["re"] = base["rs"], base["re"]
    return x, p


class GreatBanquet(Episode):
    dur = 18.0
    cta = "Read it in Scroll the Catholic Bible"
    kicker = "LUKE 14  •  THE GREAT BANQUET"
    headline = "The feast was ready.\nWho will take the empty seats?"
    captions = [
        (cpdv("Luke", 14, 18, "And at once they all began to make excuses."), "Luke 14:18", 4.6),
        (cpdv("Luke", 14, 21, "…lead here the poor, and the disabled, and the blind, and the lame."), "Luke 14:21", 9.8),
        (cpdv("Luke", 14, 23, "…compel them to enter, so that my house may be filled."), "Luke 14:23", 13.4),
    ]

    def draw_panel(self, cr, i, t, y0, gy):
        sun(cr, 1000, gy - 300, r=22, rays=10)
        filled = prog(t, 13.2, 14.2) if i == 2 else 0.0
        warm_glow(cr, 760, gy - 90, 300, filled * 0.8)

        # ---------------- the guest's farm ----------------
        for k, wx in enumerate((28, 58, 88, 118)):
            wheat(cr, wx, gy, 112 + 14 * (k % 2), sway=math.sin(t * 1.3 + k))

        # ---------------- the invited guest makes his excuse ----------------
        if t < 4.6:
            gp = keyed([(0, pose("stand", head=-8)), (3.2, pose("stand", head=-8)), (3.6, point_back),
                        (4.0, point_back), (4.3, stop)], t)
            GJ = draw_figure(cr, GX, gy, gp, s=1.0, face=1, prop="robe_hat")
            if t > 4.1: stop_hand(cr, GJ, face=1)
        else:
            gx, gwa, _ = track(t, [(4.8, GX), (6.8, -90)])
            if gx > -80:
                gp = body(t, keyed([(4.6, stop), (5.0, pose("stand", head=-6))], t), gwa, speed=1.5)
                GJ = draw_figure(cr, gx, gy, gp, s=1.0, face=-1, prop="robe_hat")
                if t < 4.9: stop_hand(cr, GJ, face=-1)

        # ---------------- the servant ----------------
        skeys = [(0.8, SX), (2.6, 290), (5.4, 290), (7.0, SX)]
        if i >= 1:
            skeys += [(7.6, SX), (8.6, 150)]
            back = (10.0, 12.0) if i == 1 else (10.8, 12.8)
            skeys += [(back[0], 150), (back[1], SX)]
        sx, swa, sdir = track(t, skeys)
        sface = -1 if t < 5.2 else 1
        sp = pose("stand", rs=20, re=20)
        if 2.6 <= t < 5.2:
            sp = keyed([(2.6, pose("stand")), (2.9, beckon), (3.5, beckon), (3.9, pose("stand", lean=-6, head=-6))], t)
        elif i == 0 and t >= 7.0:
            sp = keyed([(7.0, pose("stand")), (7.5, shrug)], t)
        elif i >= 1 and 7.4 <= t:
            sface = sdir if swa > 0.05 else (-1 if t < 9.8 else 1)
            if 8.6 <= t < 9.8:
                sp = keyed([(8.6, pose("stand")), (8.9, beckon), (9.6, beckon), (9.9, pose("stand"))], t)
        sp = body(t, sp, swa, speed=1.6)
        draw_figure(cr, sx, gy, sp, s=0.95, face=sface)

        # ---------------- the poor, the blind, the lame (and more) ----------------
        bench(cr, TX0 + 25, TX1 - 15, gy, h=44)
        guests = []
        if i >= 1:
            guests.append(("blind", [(8.2, -70), (12.0, SEATS[3])]))
            guests.append(("lame", [(8.6, -70), (12.2, SEATS[2])]))
        if i == 2:
            guests.append(("woman", [(9.6, -70), (12.8, SEATS[1])]))
            guests.append(("old", [(10.0, -70), (13.2, SEATS[0])]))
        for kind, keys in guests:
            if t < keys[0][0]:
                continue
            if kind == "blind":
                base = pose("stand", rs=55, re=-15, head=-12)
                x, p = walker(t, keys, base, seated_cane, arm_fixed=True)
                J = draw_figure(cr, x, gy, p, s=0.95, face=1)
                cane(cr, J["rhand"][0], J["rhand"][1], gy, lean=26 if t < keys[-1][0] else 10)
            elif kind == "lame":
                base = pose("stand", lean=12, head=8, rs=40, re=-5)
                x, p = walker(t, keys, base, seated, amp=13, speed=1.5, arm_fixed=True)
                if t < keys[-1][0]:
                    p["lean"] += 5 * abs(math.sin(t * 1.5 * math.pi))      # the limp
                J = draw_figure(cr, x, gy, p, s=0.95, face=1)
                if t < keys[-1][0] + 0.3:
                    cane(cr, J["rhand"][0], J["rhand"][1], gy, lean=10)
            elif kind == "woman":
                base = pose("stand", head=4, rs=30, re=60)
                x, p = walker(t, keys, base, seated, speed=1.7)
                J = draw_figure(cr, x, gy, p, s=0.92, face=1)
                veil_drape(cr, J, s=0.92, face=1)
            else:
                base = pose("stand", lean=20, head=12, rs=45, re=-10)
                x, p = walker(t, keys, base, seated, amp=16, speed=1.4, arm_fixed=True)
                J = draw_figure(cr, x, gy, p, s=0.95, face=1)
                if t < keys[-1][0] + 0.3:
                    cane(cr, J["rhand"][0], J["rhand"][1], gy, lean=8)

        # ---------------- the feast table ----------------
        top = gy - 50
        feast_table(cr, TX0, TX1, gy, h=50)
        for k, lx in enumerate(SEATS):
            loaf(cr, lx + 28, top - 8)
            wine_goblet(cr, lx - 4, top, s=0.85)

        # ---------------- the host ----------------
        hkeys = [(0.2, pose("stand")), (0.6, h_ready), (1.2, h_ready), (1.6, h_point), (2.6, h_point), (3.0, pose("stand", head=4))]
        if i == 0:
            hkeys += [(6.8, pose("stand", head=4)), (7.6, h_sad)]
        else:
            hkeys += [(6.9, pose("stand", head=4)), (7.3, h_point), (8.6, h_point), (9.0, pose("stand"))]
            if i == 1:
                hkeys += [(11.6, pose("stand")), (12.3, h_welcome)]
            else:
                hkeys += [(11.6, pose("stand")), (12.3, h_welcome), (13.2, h_welcome), (13.8, pose("joy", ls=128, le=24))]
        hp = keyed(hkeys, t)
        if i == 0 and t > 7.6:
            hp["head"] += 2 * math.sin(t * 2)
        draw_figure(cr, HX, gy, hp, s=1.05, face=-1, prop="robe")


OUTPUT_NAME = "day32a_great_banquet_luke14"
