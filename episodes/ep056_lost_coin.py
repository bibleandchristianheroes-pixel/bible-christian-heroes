import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import *
from props import *

TX0, TX1 = 170, 360          # table
CX = 720                     # where the coin comes to rest
DOOR = 860

class LostCoin(Episode):
    dur = 18.0
    caption_bg = True
    cta = "Start your day with Ave Missal"
    kicker = "LUKE 15  •  THE LOST COIN"
    headline = "One coin lost in the dark.\nShe would not stop looking."
    captions = [
        (cpdv("Luke", 15, 8, "…would not light a candle, and sweep the house, and diligently search until she finds it?"), "Luke 15:8", 7.4),
        (cpdv("Luke", 15, 9, "And when she has found it, she calls together her friends and neighbors, saying: ‘Rejoice with me!…"), "Luke 15:9", 11.0),
        (cpdv("Luke", 15, 10, "…there will be joy before the Angels of God over even one sinner who is repentant."), "Luke 15:10", 14.0),
    ]

    def draw_panel(self, cr, i, t, y0, gy):
        tt = gy - 64
        dawn = prog(t, 13.4, 15.0) if i == 2 else 0.0
        door_open = prog(t, 12.8, 13.3) if i >= 1 else 0.0
        door_frame_lit(cr, DOOR, gy, open_=door_open, light=door_open * (0.5 if i == 1 else 0.9))
        feast_table(cr, TX0, TX1, gy)
        coin_stack(cr, 215, tt, 10 if t < 3.0 else 9, r=10)

        # ---------- the coin that is lost ----------
        found = i >= 1 and t >= 10.3
        if not found:
            if t < 3.0:
                pass
            elif t < 3.3:
                coin(cr, lerp(300, 362, prog(t, 3.0, 3.3)), tt - 10, r=10)
            elif t < 3.6:
                u = (t - 3.3) / 0.3
                coin(cr, lerp(362, 392, u), lerp(tt - 10, gy - 10, u * u), r=10)
            elif t < 4.9:
                coin(cr, lerp(392, CX, 1 - (1 - (t - 3.6) / 1.3) ** 2), gy - 10, r=10)
            else:
                sq = clamp(1 - (t - 4.9) / 0.4)
                cr.save(); cr.translate(CX, gy - 3 - 7 * sq); cr.scale(1, 0.3 + 0.7 * sq); coin(cr, 0, 0, r=10); cr.restore()

        # ---------- the woman ----------
        hold_lamp = pose("stand", ls=55, le=-15, rs=45, re=-5, lean=8, head=14)
        keys = [(0.3, 430)]
        if t >= 6.6:
            if i == 0:
                keys = [(6.6, 430), (9.4, 580), (10.2, 580), (12.8, 420), (13.4, 420), (16.2, 580)]
            else:
                keys = [(6.6, 430), (9.6, CX - 55)]
                if t >= 11.6: keys = [(11.8, CX - 55), (12.6, DOOR - 50)]
        x, wa, d = track(t, keys)
        face = -1 if t < 4.4 else 1
        count = pose("stand", rs=70, re=10, ls=60, le=10, head=20)
        p = keyed([(0.3, count), (3.0, count), (3.4, pose("stand", head=0, rs=30, re=20)), (4.4, pose("stand", head=0, rs=30, re=20)),
                   (5.0, pose("stand", rs=20, re=10, ls=20, le=10, head=5)), (5.4, pose("stand", lean=12, ls=80, le=-10, rs=30, re=10)),
                   (6.0, hold_lamp)], t)
        if 0.3 < t < 3.0:
            p["head"] = 20 + 8 * abs(math.sin(t * 5))
            p["re"] = 10 + 14 * abs(math.sin(t * 5))
        lamp_lit = prog(t, 5.6, 6.0)
        broom = t >= 6.2
        if t >= 6.6:
            face = d if wa > 0.05 else face
            if i == 0 and wa < 0.05: face = 1 if t < 11 or t > 13.0 else -1
            p = body(t, hold_lamp, wa * 0.6)
            p["ls"], p["le"], p["rs"], p["re"] = 55, -15, 45, -5
        if i >= 1 and t >= 9.6:
            reach = pose("kneel", lean=32, head=26, rs=75, re=-10, ls=55, le=-15)
            up = pose("stand", rs=165, re=0, ls=55, le=-15, head=-18)
            call = pose("stand", rs=150, re=10, ls=55, le=-15, head=-12)
            face = 1
            p = keyed([(9.6, hold_lamp), (10.0, reach), (10.4, reach), (11.0, up), (11.6, up), (11.8, hold_lamp)], t)
            broom = t < 9.9
            if t >= 11.8:
                p = body(t, keyed([(11.8, hold_lamp), (12.6, hold_lamp), (13.2, call)], t), wa)
                p["ls"], p["le"] = 55, -15
                if t >= 12.6: p["rs"] = 150 + 12 * math.sin(t * 9)
            if i == 2 and t >= 13.6:
                p = keyed([(13.6, call), (14.2, pose("joy", ls=55, le=-15))], t)
                face = 1
        bounce = 6 * abs(math.sin((t - 14.2) * 4.5)) if (i == 2 and t > 14.2) else 0
        J = draw_figure(cr, x, gy - bounce, p, s=0.95, face=face, prop="robe")
        veil_drape(cr, J, s=0.95, face=face)

        # lamp: on the table, then in her far hand
        if t < 5.6:
            lp = lamp(cr, 300, tt, lit=0)
        else:
            lx, ly = J["lhand"]
            lp = lamp(cr, lx + 6 * face, ly + 12, lit=lamp_lit, flicker=t)
        # broom: leaning by the table, then sweeping; dropped when she finds the coin
        if not broom and t < 6.2:
            sweep_broom(cr, 494, gy - 130, 482, gy)
        elif broom:
            hx, hy = J["rhand"]
            sw = 26 * math.sin(t * 7) if t >= 6.6 else 0
            sweep_broom(cr, hx, hy, hx + face * (40 + sw), gy)
        elif i >= 1:
            cr.set_source_rgb(*INK); cr.set_line_width(4); cr.move_to(CX - 160, gy - 3); cr.line_to(CX - 60, gy - 3); cr.stroke()
            cr.move_to(CX - 60, gy - 9); cr.line_to(CX - 30, gy - 14); cr.line_to(CX - 30, gy); cr.line_to(CX - 60, gy); cr.close_path(); cr.fill()
        if found:
            if t < 10.6:
                coin(cr, CX, gy - 8, r=10)
            else:
                hx, hy = J["rhand"]
                coin(cr, hx, hy - 6, r=10)
                coin_glint(cr, hx, hy - 6, prog(t, 10.6, 11.0) * (1 - prog(t, 12.0, 12.6)), t, r=34)
        if i >= 1:
            coin_glint(cr, CX, gy - 8, prog(t, 9.4, 9.8) * (1 - prog(t, 10.4, 10.6)), t)

        # ---------- neighbours (panel 3) ----------
        lights = [(lp[0], lp[1], 300, lamp_lit)]
        if i == 2:
            for k, (sx, ex) in enumerate(((1120, 950), (1190, 1020))):
                if t < 13.0: continue
                nx, nwa, _ = track(t, [(13.0 + 0.3 * k, sx), (14.4 + 0.3 * k, ex)])
                np_ = pose("stand", rs=50, re=-10)
                if t > 14.4 + 0.3 * k:
                    np_ = keyed([(14.4 + 0.3 * k, pose("stand", rs=50, re=-10)), (15.0 + 0.3 * k, pose("joy", rs=50, re=-10))], t)
                NJ = draw_figure(cr, nx, gy, body(t, np_, nwa), s=0.9, face=-1, prop="robe")
                veil_drape(cr, NJ, s=0.9, face=-1)
                nl = lamp(cr, NJ["rhand"][0] - 6, NJ["rhand"][1] + 12, lit=1.0, flicker=t + k)
                lights.append((nl[0], nl[1], 260, 1.0))
            warm_glow(cr, 800, gy - 120, 420, dawn)
        dark = 0.88 * prog(t, 4.2, 6.0) * (1 - 0.75 * dawn)
        if door_open > 0: lights.append((DOOR + 39, gy - 80, 200, door_open * 0.8))
        darkness(cr, y0, PANEL_H, dark, lights)

OUTPUT_NAME = "day28b_lost_coin_luke15"
