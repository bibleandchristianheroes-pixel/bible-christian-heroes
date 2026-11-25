import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import *
from props import *

HX = 100            # her house
JX = 238            # the flour jar (and the little oil bottle beside it)
WX = 322            # where the widow stands
KX = 412            # where she kneels to bake
FX = 478            # the fire
SX = 566            # her son, sitting by the fire
EX = 770            # where Elijah stops
OFF = 1190
DOOR = 64           # her doorway
LOAF_Y = 14         # loaf sits this far above the ground on the coals

w_stand = pose("stand", rs=14, re=20, ls=10, le=16, head=6)
w_peer = pose("stand", rs=20, re=24, ls=14, le=18, head=34, lean=18)              # looks into the jar (face -1)
w_scoop = pose("reach", rs=88, re=34, ls=14, le=18, head=30, lean=36)              # hand down into the jar (face -1)
w_show = pose("reach", rs=58, re=-34, ls=46, le=-28, head=4, lean=2)               # open hands: "I have nothing"
w_hug = pose("stand", rs=34, re=96, ls=30, le=100, head=18, lean=4)                # jar held to her chest
w_bake = pose("kneel", rs=74, re=-14, ls=62, le=-8, head=26, lean=22)
w_hold = pose("stand", rs=40, re=70, ls=14, le=18, head=8)                         # loaf held in front
w_give = pose("reach", rs=78, re=-6, head=6, lean=8)
w_give_k = pose("kneel", rs=80, re=-4, ls=30, le=20, head=8, lean=10)
w_eat_k = pose("kneel", rs=24, re=136, ls=30, le=20, head=14, lean=10)            # hand to mouth
w_sad = pose("kneel", rs=30, re=10, ls=24, le=14, head=44, lean=30)
w_joy = pose("joy")

s_sit = ground_sit_pose(lean=10, head=20, rs=40, re=40, ls=30, le=40)
s_take = ground_sit_pose(lean=6, head=0, rs=80, re=-6, ls=30, le=40)
s_eat = ground_sit_pose(lean=8, head=14, rs=24, re=136, ls=30, le=40)
s_joy = ground_sit_pose(lean=-6, head=-18, rs=158, re=10, ls=150, le=10)
s_up = pose("stand", rs=20, re=30, head=4)

e_stand = pose("stand", rs=10, re=14, ls=26, le=-16, head=4)
e_ask = pose("reach", rs=80, re=-14, ls=26, le=-16, head=10, lean=6)
e_drop = pose("stand", rs=6, re=8, ls=26, le=-16, head=26, lean=4)
e_take = pose("reach", rs=76, re=-4, ls=26, le=-16, head=10, lean=6)
e_bless = pose("stand", rs=152, re=8, ls=26, le=-16, head=-12, lean=-2)


class WidowOfZarephath(Episode):
    dur = 18.0
    cta = "Read it in Scroll the Catholic Bible"
    kicker = "1 KINGS 17  •  THE WIDOW OF ZAREPHATH"
    headline = "Three widows had one handful left.\nOnly one baked for him first."
    captions = [
        (cpdv("I Kings", 17, 12, "…I have no bread, except a handful of flour in a jar… so that we may eat it and die."), "1 Kings 17:12", 7.6),
        (cpdv("I Kings", 17, 13, "Do not be afraid… first make for me, from the same flour, a little bread baked under ashes, and bring it to me."), "1 Kings 17:13", 9.8),
        (cpdv("I Kings", 17, 16, "…the jar of flour did not fail, and the bottle of oil was not diminished, in accord with the word of the Lord…"), "1 Kings 17:16", 12.6),
    ]

    def draw_panel(self, cr, i, t, y0, gy):
        house_light = 0.7 * prog(t, 9.2, 10.0) if i == 0 else 0.0
        small_house(cr, HX, gy, light=house_light)
        sun(cr, 1000, gy - 300, r=22, rays=10)
        for gx in (660, 900, 1040):
            grass_tuft(cr, gx, gy, 10, sway=0.2 * math.sin(t * 2 + gx))

        # ---------------- jar level ----------------
        level = 0.22
        jar_on_ground = True
        if i == 0 and t > 6.0:
            jar_on_ground = False
        if i == 1:
            level = 0.22 * (1 - prog(t, 5.9, 6.4))
        if i == 2:
            level = 0.22 * (1 - prog(t, 6.1, 6.6)) + 0.78 * prog(t, 12.5, 13.6)
        jar_glow = 0.9 * prog(t, 12.3, 13.4) if i == 2 else 0.0
        if jar_on_ground:
            flour_jar(cr, JX, gy, level=level, glow=jar_glow)
        flask(cr, JX + 44, gy - 12)

        # ---------------- fire ----------------
        lit = 1.0 - (prog(t, 8.5, 11.0) if i == 0 else 0.0)
        campfire(cr, FX, gy, t, s=0.9, lit=lit)

        # ---------------- Elijah ----------------
        ex, ewa, _ = track(t, [(0.4, OFF + 30), (2.9, EX)]); eface = -1
        ep = keyed([(0.0, e_stand), (3.1, e_stand), (3.6, e_ask), (5.0, e_ask)], t)
        if i in (0, 1):
            t_drop = 7.4 if i == 0 else 8.6
            ep = keyed([(0.0, e_stand), (3.1, e_stand), (3.6, e_ask), (t_drop, e_ask), (t_drop + 0.6, e_drop)], t)
            if t > t_drop + 1.6:
                ex, ewa, _ = track(t, [(t_drop + 1.7, EX), (t_drop + 4.4, OFF + 40)]); eface = 1
                ep = keyed([(t_drop + 1.6, e_drop), (t_drop + 2.0, e_stand)], t)
        elif i == 2 and t > 5.0:
            ep = keyed([(5.0, e_ask), (5.6, e_stand), (9.4, e_stand), (9.8, e_take), (10.6, e_take), (11.2, e_bless)], t)
        ep = body(t, ep, ewa, speed=1.3)
        EJ = None
        if ex < OFF + 20:
            EJ = draw_figure(cr, ex, gy, ep, s=1.04, face=eface, prop="robe")
            sx_, sy_ = EJ["lhand"]
            staff(cr, sx_, sy_ - 78, min(gy, sy_ + 80))

        # ---------------- the son ----------------
        sp = s_sit; sx, sface, sdraw = SX, -1, True
        if i == 0:
            if t > 7.0:
                u = prog(t, 7.0, 7.7)
                sp = mix(s_sit, s_up, u) if u < 1 else s_up
                if t > 7.7:
                    sx, swa, _ = track(t, [(7.8, SX), (9.2, DOOR)])
                    sp = body(t, s_up, swa, speed=1.8)
        elif i == 1:
            sp = keyed([(0.0, s_sit), (8.9, s_sit), (9.2, s_take), (9.6, s_take), (10.0, s_eat), (11.0, s_eat), (11.4, s_sit)], t)
        else:
            sp = keyed([(0.0, s_sit), (13.0, s_sit), (13.6, s_joy)], t)
        s_alpha = 1 - prog(t, 9.1, 9.5) if i == 0 else 1.0
        SJ = None
        if s_alpha > 0:
            cr.push_group()
            SJ = draw_figure(cr, sx, gy, sp, s=0.62, face=sface)
            cr.pop_group_to_source(); cr.paint_with_alpha(s_alpha)

        # ---------------- the widow ----------------
        wx, wface = WX, 1
        wp = keyed([(0.0, w_stand), (0.6, w_stand)], t)
        if t < 3.2:                                       # looks into the jar: a handful left
            wface = -1
            wp = keyed([(0.0, w_stand), (0.5, w_peer), (2.4, w_peer), (2.9, w_stand)], t)
            if t > 2.9: wface = 1
        else:
            wp = keyed([(3.2, w_stand), (3.9, w_stand), (4.4, w_show), (5.2, w_show)], t)
        carry = None; loaf_at = None; w_alpha = 1.0
        if i == 0 and t > 5.2:
            wp = keyed([(5.2, w_show), (5.6, w_stand)], t)
            if 5.2 < t < 6.0:
                wp["head"] += 9 * math.sin(t * 10)          # shakes her head
            if t > 5.6:
                wface = -1
                wp = keyed([(5.6, w_stand), (5.9, w_scoop), (6.1, w_scoop), (6.5, w_hug)], t)
            if t > 6.0:
                carry = "chest"
            if t > 6.6:
                wx, wwa, _ = track(t, [(6.7, WX), (8.9, DOOR + 4)])
                wp = body(t, w_hug, wwa, speed=1.4)
            w_alpha = 1 - prog(t, 8.9, 9.4)
        elif i == 1 and t > 5.2:
            wface = -1
            wp = keyed([(5.2, w_show), (5.5, w_stand), (5.8, w_scoop), (6.4, w_scoop), (6.7, w_stand)], t)
            if t > 6.7:
                wface = 1
                wx, wwa, _ = track(t, [(6.8, WX), (7.4, KX)])
                wp = body(t, keyed([(7.4, w_stand), (7.7, w_bake)], t), wwa, speed=1.5)
            if t > 7.7:
                wx = KX
                wp = keyed([(7.7, w_bake), (8.5, w_bake), (8.8, w_give_k), (9.5, w_give_k), (9.9, w_eat_k), (11.0, w_eat_k), (11.3, w_bake)], t)
                loaf_at = "fire" if t < 8.6 else ("her" if t < 9.0 else "split")
            if t > 11.4:
                u = prog(t, 11.4, 11.8)
                wp = mix(w_bake, w_stand, u)
                if t > 11.8:
                    wface = -1
                    wx, wwa, _ = track(t, [(11.9, KX), (12.6, WX)])
                    wp = body(t, keyed([(12.6, w_stand), (12.9, w_scoop), (13.5, w_scoop), (13.9, w_peer), (14.6, w_sad)], t), wwa, speed=1.5)
                    if 13.5 < t < 14.1:
                        wp["head"] += 8 * math.sin(t * 11)
        elif i == 2 and t > 5.2:
            wp = keyed([(5.2, w_show), (5.6, w_stand)], t)
            if 5.3 < t < 6.0:
                wp["head"] += 10 * max(0, math.sin((t - 5.3) * 9))   # nods
            if t > 5.8:
                wface = -1
                wp = keyed([(5.8, w_stand), (6.1, w_scoop), (6.6, w_scoop), (6.9, w_stand)], t)
            if t > 6.9:
                wface = 1
                wx, wwa, _ = track(t, [(7.0, WX), (7.5, KX)])
                wp = body(t, keyed([(7.5, w_stand), (7.8, w_bake)], t), wwa, speed=1.5)
            if t > 7.8:
                wx = KX
                wp = w_bake
                loaf_at = "fire" if t < 8.5 else "her"
            if t > 8.5:
                u = prog(t, 8.5, 8.9)
                wp = mix(w_bake, w_hold, u)
            if t > 8.9:
                wx, wwa, _ = track(t, [(8.95, KX), (9.8, EX - 140)])
                wp = body(t, keyed([(9.8, w_hold), (10.1, w_give), (10.6, w_give), (10.9, w_stand)], t), wwa, speed=1.5)
                if t > 10.35:
                    loaf_at = "pass" if t < 10.6 else "elijah"
            if t > 10.9:
                wface = -1
                wx, wwa, _ = track(t, [(11.0, EX - 140), (12.1, WX)])
                wp = body(t, keyed([(12.1, w_stand), (12.4, w_scoop), (13.4, w_scoop), (13.8, w_stand), (14.4, w_joy)], t), wwa, speed=1.6)
        cr.push_group()
        WJ = draw_figure(cr, wx, gy, wp, s=0.97, face=wface)
        veil_drape(cr, WJ, s=0.97, face=wface)
        if carry == "chest":
            hx = (WJ["rhand"][0] + WJ["lhand"][0]) / 2; hy = max(WJ["rhand"][1], WJ["lhand"][1])
            u = prog(t, 6.0, 6.4)
            flour_jar(cr, lerp(JX, hx, u), lerp(gy, hy + 26, u), level=0.22, w=lerp(50, 40, u), h=lerp(74, 58, u))
        cr.pop_group_to_source(); cr.paint_with_alpha(w_alpha)

        # a pinch of flour as she scoops
        if i in (1, 2):
            ts = 6.0 if i == 1 else 6.2
            flour_puff(cr, JX, gy - 74, prog(t, ts, ts + 0.2) * (1 - prog(t, ts + 0.4, ts + 0.8)), t)
        if i == 2:
            flour_puff(cr, JX, gy - 74, prog(t, 12.4, 12.8) * (1 - prog(t, 14.2, 15.0)), t, n=10, seed=5)
            light_rays(cr, JX, gy - 86, 0.75 * prog(t, 12.5, 13.5), r0=30, r1=70, n=14, t=t)

        # ---------------- the little loaf ----------------
        if loaf_at == "fire":
            ts = 7.7 if i == 1 else 7.8
            a = prog(t, ts, ts + 0.6)
            cr.push_group(); loaf(cr, FX, gy - LOAF_Y); cr.pop_group_to_source(); cr.paint_with_alpha(a)
        elif loaf_at == "her":
            hx, hy = WJ["rhand"]
            ts = 8.6 if i == 1 else 8.5
            u = prog(t, ts, ts + 0.3)
            loaf(cr, lerp(FX, hx, u), lerp(gy - LOAF_Y, hy - 4, u))
        elif loaf_at == "split" and SJ is not None:
            u = prog(t, 9.0, 9.4)
            hx, hy = WJ["rhand"]; sx2, sy2 = SJ["rhand"]
            if t < 11.2:
                bread_half(cr, lerp(hx, sx2, u), lerp(hy - 4, sy2 - 4, u), face=-1)
                bread_half(cr, hx - 4, hy - 4 if t < 9.6 else hy - 2, face=1)
        elif loaf_at in ("pass", "elijah") and EJ is not None:
            hx, hy = WJ["rhand"]; ex2, ey2 = EJ["rhand"]
            u = prog(t, 10.35, 10.6)
            loaf(cr, lerp(hx, ex2, u), lerp(hy - 4, ey2 - 6, u))
        if i == 2 and t > 11.0 and EJ is not None:
            ex2, ey2 = EJ["rhand"]
            light_rays(cr, ex2, ey2 - 8, 0.5 * prog(t, 11.2, 11.8) * (1 - prog(t, 12.6, 13.2)), r0=22, r1=44, n=10, t=t)


OUTPUT_NAME = "day41a_widow_of_zarephath_1kings17"
