import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import *
from props import *

VX = 420            # vine stock
BL = 260            # branch length
FX = 900            # fire (panel 2)

class VineAndBranches(Episode):
    dur = 18.0
    cta = "Pray it with Ave – Catholic Prayer Lock"
    kicker = "JOHN 15  •  THE VINE AND THE BRANCHES"
    headline = "Same vine. Same start.\nOnly one branch stayed."
    captions = [
        (cpdv("John", 15, 4, "…the branch is not able to bear fruit of itself, unless it abides in the vine…"), "John 15:4", 7.0),
        (cpdv("John", 15, 6, "…he will be cast away, like a branch, and he will wither, and they will gather him and cast him into the fire…"), "John 15:6", 10.6),
        (cpdv("John", 15, 5, "I am the vine; you are the branches. Whoever abides in me, and I in him, bears much fruit."), "John 15:5", 8.8),
    ]

    def draw_panel(self, cr, i, t, y0, gy):
        if i == 1:
            fire(cr, FX, gy, prog(t, 11.5, 12.3) * (0.85 + 0.15 * math.sin(t * 2)), t)
        if i == 2:
            warm_glow(cr, 560, gy - 140, 420, prog(t, 12.2, 13.6))
        ax, ay = grapevine(cr, VX, gy, h=160)
        grow = prog(t, 0.4, 3.4)
        grapes = 0.35 * prog(t, 2.8, 4.4)
        wither = 0.0
        bx, by, rot = ax, ay, 0.0
        carried = None
        if i < 2 and t >= 4.7:
            if t < 5.0:
                rot = 3 * math.sin(t * 60)
            else:
                u = prog(t, 5.0, 5.8) ** 1.5
                bx, by = lerp(ax, ax + 50, u), lerp(ay, gy - 22, u)
                rot = 34 * math.sin(math.pi * min(1, u * 1.1)) * (1 - u) + lerp(0, -21, u)
                wither = prog(t, 6.0, 9.0)
                cr.set_source_rgb(*INK); cr.set_line_width(3)   # broken stub on the vine
                cr.move_to(ax, ay); cr.line_to(ax + 12, ay - 2); cr.stroke()
        elif i == 2:
            grapes = lerp(grapes, 1.0, prog(t, 5.0, 8.6))

        # ---------- vinedresser ----------
        x, wa, face = 220, 0.0, 1
        p = pose("stand", head=-6)
        held = None
        if i == 0:
            p = keyed([(4.6, pose("stand", head=-6)), (5.4, pose("stand", head=14)), (7.0, pose("stand", head=14)),
                       (7.6, pose("stand", head=22, lean=6))], t)
            if 7.6 < t < 8.6:
                p["head"] = 22 + 10 * math.sin((t - 7.6) * 18)
        elif i == 1:
            x, wa, d = track(t, [(8.8, 220), (9.6, 545), (10.3, 545), (11.1, 790)])
            bend = pose("stand", lean=50, head=30, rs=50, re=10, ls=40, le=10, lt=20, lk=30, rt=0, rk=30)
            carry = pose("stand", rs=60, re=40, ls=40, le=50)
            throw = pose("stand", rs=120, re=-10, ls=100, le=-10, lean=10)
            if t < 9.6:
                p = body(t, keyed([(4.6, pose("stand", head=-6)), (5.4, pose("stand", head=14))], t), wa)
            elif t < 10.3:
                p = keyed([(9.6, pose("stand")), (9.9, bend), (10.0, bend), (10.3, carry)], t)
            elif t < 11.1:
                p = body(t, carry, wa)
            else:
                p = keyed([(11.1, carry), (11.4, throw), (12.0, pose("stand", head=6)), (13.5, pose("stand", head=6))], t)
        else:
            x, wa, d = track(t, [(9.2, 220), (10.6, 770)])
            reach = pose("stand", rs=125, re=10, head=-18, ls=20, le=10)
            p = body(t, pose("stand", head=-6), wa)
            if t >= 10.6:
                face = -1
                p = keyed([(10.6, pose("stand")), (10.9, reach), (11.4, reach), (11.8, pose("stand", rs=110, re=10)),
                           (12.4, pose("joy", ls=20, le=10, rs=135, re=-5))], t)
        J = draw_figure(cr, x, gy, p, s=1.0, face=face)

        # ---------- the branch ----------
        if i == 1 and t >= 9.9:
            hx, hy = J["rhand"]
            if t < 11.3:
                u = prog(t, 9.9, 10.3)
                tbx, tby = hx - BL * 0.45, hy - 4
                bx, by = lerp(bx, tbx, u), lerp(by, tby, u); rot = lerp(rot, -18, u)
                vine_branch(cr, bx, by, rot, BL, 1.0, 0.35, 1.0)
            else:
                u = prog(t, 11.3, 11.8)
                if u < 1:
                    bx2 = lerp(hx - BL * 0.45, FX - BL * 0.4, u); by2 = lerp(hy - 4, gy - 30, u) - 60 * math.sin(math.pi * u)
                    vine_branch(cr, bx2, by2, -18 - 10 * u, BL * (1 - 0.3 * u), 1.0, 0.35, 1.0)
                else:
                    sh = 1 - prog(t, 11.8, 13.2)
                    if sh > 0:
                        cr.save(); cr.translate(FX, gy - 10); cr.scale(sh, sh); cr.translate(-FX, -(gy - 10))
                        vine_branch(cr, FX - 70, gy - 40, -10, 140, 1.0, 0.0, 1.0); cr.restore()
                    fire(cr, FX, gy, prog(t, 11.5, 12.3) * (0.85 + 0.15 * math.sin(t * 2)), t, logs=False)
        else:
            vine_branch(cr, bx, by, rot, BL, grow, grapes, wither)
        if i == 2:
            if t >= 11.4:
                hx, hy = J["rhand"]
                grape_cluster(cr, hx + 2, hy + 2, s=1.15)

OUTPUT_NAME = "day17b_vine_and_branches_john15"
