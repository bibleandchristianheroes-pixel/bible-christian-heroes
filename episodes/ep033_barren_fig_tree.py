import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import *
from props import *

TX = 850            # fig tree
GX = 745            # gardener's working spot (left of the trunk)
OX = 600            # owner after giving the order

class BarrenFigTree(Episode):
    dur = 18.0
    cta = "Read it in Scroll the Catholic Bible"
    kicker = "LUKE 13  •  THE BARREN FIG TREE"
    headline = "Three years, no fruit.\nOne more year of mercy."
    captions = [
        (cpdv("Luke", 13, 7, "…I came seeking fruit on this fig tree, and I have found none. Therefore, cut it down."), "Luke 13:7", 7.0),
        (cpdv("Luke", 13, 8, "…Lord, let it be for this year also, during which time I will dig around it and add fertilizer."), "Luke 13:8", 8.6),
        (cpdv("Luke", 13, 9, "And, indeed, it should bear fruit."), "Luke 13:9", 12.2),
    ]

    def owner(self, cr, i, t, gy):
        x, wa, d = track(t, [(0.3, -60), (2.2, GX - 10), (5.6, GX - 10), (6.4, OX)])
        if i == 2:
            x, wa, d = track(t, [(0.3, -60), (2.2, GX - 10), (5.6, GX - 10), (6.4, OX), (12.0, OX), (12.6, GX - 10)])
        search = pose("stand", rs=155, re=10, ls=140, le=10, head=-25)
        point = pose("stand", rs=-80, re=0, head=-4)
        p = keyed([(2.2, pose("stand", head=-10)), (2.6, search), (3.8, search), (4.2, pose("stand", head=0))], t)
        if 2.6 < t < 3.8:
            p["rs"] += 12 * math.sin(t * 7); p["ls"] += 12 * math.sin(t * 7 + 2); p["head"] -= 6 * math.sin(t * 4)
        if 3.9 < t < 4.4:
            p["head"] = 14 * math.sin((t - 3.9) * 25)
        face = 1
        if t >= 4.4:
            face = -1
            p = keyed([(4.4, pose("stand")), (4.7, point), (5.6, point), (5.9, pose("stand"))], t)
        if t >= 6.4:
            face = 1
            p = pose("stand", head=-4)
            if i == 1 or i == 2:
                p = keyed([(6.4, pose("stand", head=-4)), (7.6, pose("stand", head=-4)), (8.0, pose("stand", head=8)), (8.3, pose("stand", head=-4))], t)
                if 7.6 < t < 8.3:
                    p["head"] = 10 * abs(math.sin((t - 7.6) * 9))
        fig_up = None
        if i == 2 and t >= 12.0:
            if t < 12.6:
                p = pose("stand")
            else:
                pick = pose("stand", rs=160, re=5, head=-25)
                p = keyed([(12.6, pose("stand")), (12.9, pick), (13.2, pick), (13.6, pose("joy"))], t)
                fig_up = True
        J = draw_figure(cr, x, gy, body(t, p, wa), s=1.06, face=face, prop="robe")
        return J, fig_up

    def draw_panel(self, cr, i, t, y0, gy):
        leaves, figs, fall, dug = 0.3, 0.0, 0.0, 0.0
        if i == 0:
            fall = 82 * prog(t, 8.6, 9.7) ** 2
        elif i == 1:
            dug = prog(t, 8.6, 11.6); leaves = lerp(0.3, 0.62, prog(t, 11.0, 14.0))
        else:
            dug = prog(t, 8.6, 10.0); leaves = lerp(0.3, 1.0, prog(t, 10.4, 12.2)); figs = prog(t, 11.4, 12.6)
            su = prog(t, 10.0, 12.2)
            if 0 < su < 1:
                a = math.pi * (1 - su)
                cr.save(); cr.set_source_rgba(*INK, 1)
                sun(cr, 905 + 130 * math.cos(a), y0 + 175 - 95 * math.sin(a), r=18, rays=8)
                cr.restore()
        # dug ring + fertilizer around the trunk
        if dug > 0:
            cr.set_source_rgb(*INK)
            cr.save(); cr.translate(TX, gy); cr.scale(70 * dug, 12 * dug); cr.arc(0, 0, 1, math.pi, 2 * math.pi); cr.restore(); cr.fill()
        if i == 2:
            warm_glow(cr, TX, gy - 150, 380, prog(t, 13.2, 14.4))
        tips = fig_tree(cr, TX, gy, s=1.0, leaves=leaves, figs=figs, fall=fall)

        # ---------- gardener ----------
        if t < 5.4:
            gx, wa, face = 430, 0.0, 1
        else:
            gx, wa, _ = track(t, [(5.4, 430), (6.6, GX)]); face = 1
        hold = pose("stand", rs=8, re=4)
        p = body(t, hold, wa)
        tool = "axe"
        axe_ground = None
        spade_ground = (690, gy - 118, 700, gy + 4)
        if i == 0 and t >= 6.6:
            up = pose("stand", rs=175, re=10, ls=165, le=10, lean=-4)
            hit = pose("stand", rs=85, re=-15, ls=80, le=-10, lean=14, lt=10, rt=-14)
            if t < 8.6:
                ph = ((t - 6.8) / 0.45) % 1.0 if t > 6.8 else 0.0
                p = mix(up, hit, smooth(clamp((ph - 0.55) / 0.3))) if t > 6.8 else keyed([(6.6, hold), (6.8, up)], t)
                if t > 6.8 and ph < 0.55: p = mix(hit, up, smooth(ph / 0.55))
            else:
                p = keyed([(8.6, hit), (9.0, pose("stand", rs=8, re=4, head=-6)), (9.8, pose("stand", rs=8, re=4, head=10))], t)
            if 6.8 < t < 8.6:   # chips fly at each stroke
                ph = ((t - 6.8) / 0.45) % 1.0
                if ph > 0.8:
                    u = (ph - 0.8) / 0.2
                    for k in range(4):
                        seed_dot(cr, TX - 6 - 30 * u * (k + 1) / 4, gy - 40 - 26 * math.sin(math.pi * u) * (1 + k * 0.3), r=3)
        elif i >= 1 and t >= 6.6:
            plead = pose("stand", rs=105, re=-25, ls=95, le=-20, lean=10, head=-8)
            dig_lo = pose("stand", rs=70, re=5, ls=60, le=5, lean=28, head=20, lt=14, lk=20, rt=-16, rk=16)
            dig_hi = pose("stand", rs=50, re=40, ls=40, le=50, lean=12, head=10)
            dig_end = 11.6 if i == 1 else 10.0
            if t < 8.2:
                face = -1
                p = keyed([(6.6, hold), (7.0, plead), (8.0, plead), (8.2, pose("stand"))], t)
                axe_ground = True; tool = None
            elif t < dig_end:
                ph = (t - 8.4) / 0.8
                p = mix(dig_hi, dig_lo, 0.5 + 0.5 * math.sin(ph * 2 * math.pi)) if t > 8.4 else keyed([(8.2, pose("stand")), (8.4, dig_hi)], t)
                tool = "spade"; axe_ground = True; spade_ground = None
                u = ((t - 8.4) / 0.8) % 1.0
                if t > 8.6 and 0.25 < u < 0.75:   # clods tossed to the side
                    v = (u - 0.25) / 0.5
                    for k in range(3):
                        seed_dot(cr, GX + 70 + 40 * v + k * 8, gy - 6 - 40 * math.sin(math.pi * v) + k * 4, r=4.5)
            else:
                axe_ground = True; spade_ground = (690, gy - 118, 700, gy + 4)
                if i == 1:
                    sow = 0.5 + 0.5 * math.sin((t - dig_end) * 7)
                    p = keyed([(dig_end, pose("stand")), (dig_end + 0.3, pose("sow_back"))], t)
                    if dig_end + 0.3 < t < 13.4:
                        p = mix(pose("sow_back"), pose("sow_fwd", rs=80, lean=14), sow)
                        J0 = None
                        for k in range(5):
                            u = ((t - dig_end) * 1.6 + k / 5) % 1
                            seed_dot(cr, GX + 50 + 60 * u, gy - 60 + 60 * u ** 1.4 - 20 * math.sin(math.pi * u), r=3)
                    elif t >= 13.4:
                        p = keyed([(13.4, pose("stand")), (14.0, pose("stand", head=-14))], t)
                    tool = "bag"
                else:
                    gx, wa, _ = track(t, [(10.0, GX), (11.0, 970)])
                    p = body(t, pose("stand"), wa); tool = None
                    if t > 11.0:
                        face = -1
                        p = keyed([(11.0, pose("stand")), (11.6, pose("stand", head=-14)), (13.0, pose("stand", head=-14)), (13.6, pose("joy"))], t)
        J = draw_figure(cr, gx, gy, p, s=1.0, face=face, prop="bag" if tool == "bag" else None)
        if tool == "axe":
            axe(cr, *J["rhand"], held_angle(p, face))
        elif tool == "spade":
            hx, hy = J["rhand"]
            spade(cr, hx, hy - 6, hx + 28, min(gy + 6, hy + 92))
        if axe_ground:
            axe(cr, 640, gy - 6, 95)
        if spade_ground and i >= 1:
            spade(cr, *spade_ground)
        if i == 0 and spade_ground:
            spade(cr, *spade_ground)

        # ---------- owner ----------
        JO, fig_up = self.owner(cr, i, t, gy)
        if fig_up:
            u = prog(t, 12.9, 13.3)
            tx, ty = tips[2]
            fx, fy = lerp(tx - 12, JO["rhand"][0], u), lerp(ty + 34, JO["rhand"][1] - 4, u)
            cr.set_source_rgb(*INK); cr.arc(fx, fy, 8, 0, 2 * math.pi); cr.fill()

OUTPUT_NAME = "day17a_barren_fig_tree_luke13"
