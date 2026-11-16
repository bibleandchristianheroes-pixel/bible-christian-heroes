import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import *
from props import *

CX = 935          # the creditor, seated, facing left
KX = 770          # where each debtor kneels
OIL = (0.78, 0.60, 0.25)

c_base = sit_pose(rs=30, re=50, ls=25, le=55, head=4)
c_take = sit_pose(rs=82, re=-10, ls=25, le=55, lean=8, head=6)
c_hold = sit_pose(rs=75, re=-10, ls=60, le=10, head=0)
c_tear = sit_pose(rs=85, re=-40, ls=85, le=-40, head=6)
c_open = sit_pose(rs=60, re=-20, ls=50, le=0, head=-4)
c_bless = sit_pose(rs=62, re=38, ls=40, le=10, lean=12, head=22)

k_kneel = pose("kneel", lean=20, head=10, rs=30, re=30, ls=25, le=30)
k_offer = pose("kneel", lean=18, head=-6, rs=96, re=-22, ls=25, le=30)
k_bow = pose("kneel", lean=45, head=30, rs=20, re=10, ls=15, le=10)
k_lift = pose("kneel", lean=10, head=-10, rs=40, re=40, ls=40, le=40)


class TwoDebtors(Episode):
    dur = 18.0
    cta = "Read it in Scroll the Catholic Bible"
    kicker = "LUKE 7  •  THE TWO DEBTORS"
    headline = "Both debts were cancelled.\nWho loved him more?"
    captions = [
        (cpdv("Luke", 7, 41, "A certain creditor had two debtors: one owed five hundred denarii, and the other fifty."), "Luke 7:41", 7.6),
        (cpdv("Luke", 7, 42, "…he forgave them both. So then, which of them loves him more?"), "Luke 7:42", 7.0),
        (cpdv("Luke", 7, 47, "…many sins are forgiven her, because she has loved much. But he who is forgiven less, loves less."), "Luke 7:47", 10.4),
    ]

    def draw_panel(self, cr, i, t, y0, gy):
        big = i >= 1
        bw, bh = (58, 66) if big else (34, 30)
        sc = 1.45 if big else 0.8
        if i == 2:
            warm_glow(cr, 850, gy - 90, 230, prog(t, 10.4, 12.0))
        stool(cr, CX, gy, h=46)

        # ---------------- the debtor ----------------
        walk_base = pose("stand", lean=18 if big else 6, head=10 if big else 2, rs=30, re=30, ls=25, le=30)
        x, wa, _ = track(t, [(0.2, 170), (3.0, KX)])
        face = 1
        keys = [(3.0, walk_base), (3.4, k_kneel), (3.6, k_kneel), (3.9, k_offer), (4.4, k_offer), (4.8, k_bow)]
        if i == 0:
            keys += [(6.4, k_lift), (7.0, pose("stand", head=-4)), (7.4, pose("stand", head=8))]
            if t > 7.6:
                x, wa, _ = track(t, [(7.6, KX), (11.0, -90)])
                face = -1
        elif i == 1:
            keys += [(6.0, k_bow), (6.4, k_lift), (6.9, pose("stand", head=-8)), (7.3, pose("joy"))]
        else:
            pour = pose("kneel", lean=58, head=30, rs=58, re=10, ls=30, le=30)
            kiss = pose("kneel", lean=64, head=38, rs=40, re=20, ls=30, le=20)
            jar_up = pose("kneel", lean=14, head=-4, rs=95, re=-35, ls=30, le=40)
            keys += [(6.0, k_bow), (6.4, k_lift), (7.0, jar_up), (7.8, jar_up), (8.4, pour), (10.0, pour), (10.6, kiss)]
            x = lerp(x, KX + 22, prog(t, 7.8, 8.4)) if t > 7.8 else x
        p = keyed(keys, t) if t >= 3.0 else dict(walk_base)
        p = body(t, p, wa, speed=1.4)
        if i == 1 and t > 7.3:
            p["lean"] = -6 + 3 * math.sin(t * 6)
        if x > -80:
            J = draw_figure(cr, x, gy, p, s=1.0, face=face)
            if i == 2:
                veil_drape(cr, J, s=1.0, face=1)
        # the load on his back falls off when the debt is torn up
        fx, fy = KX - 52 - bw / 2, gy - bh
        if t < 5.6:
            shx, shy = J["sh"]
            burden(cr, shx - bw - 2, shy - bh * 0.3, w=bw, h=bh)
            drop_from = (shx - bw - 2, shy - bh * 0.3)
        else:
            u = prog(t, 5.6, 6.2)
            # where it sat at 5.6 (bowed) — recomputed from the bow pose
            Jb = draw_figure_ghost(KX, gy, k_bow)
            sx0, sy0 = Jb["sh"][0] - bw - 2, Jb["sh"][1] - bh * 0.3
            burden(cr, lerp(sx0, fx, u), lerp(sy0, fy, u * u), w=bw, h=bh)

        # the jar of ointment (P3)
        if i == 2 and t > 6.6:
            hx, hy = J["rhand"]
            a = prog(t, 6.6, 7.0)
            cr.push_group(); flask(cr, hx + 4, hy - 2); cr.pop_group_to_source(); cr.paint_with_alpha(a)
            pour_drops(cr, hx + 12, hy + 12, gy - 4, t, amount=prog(t, 8.3, 8.6) * (1 - prog(t, 10.0, 10.4)), color=OIL, drift=4)
            if t > 8.6:
                tears(cr, J["head"][0] + 10, J["head"][1] + 8, t, prog(t, 8.6, 9.2))

        # ---------------- the creditor ----------------
        ck = [(0.0, c_base), (3.9, c_base), (4.3, c_take), (4.6, c_hold), (5.0, c_hold), (5.3, c_tear), (5.8, c_open)]
        if i == 0:
            ck += [(8.4, c_open), (9.4, sit_pose(rs=30, re=50, ls=25, le=55, head=-6)), (11.0, sit_pose(rs=30, re=50, ls=25, le=55, head=-6)), (12.0, sit_pose(rs=30, re=50, ls=25, le=55, head=18, lean=4))]
        elif i == 1:
            ck += [(7.3, c_open), (7.8, sit_pose(rs=75, re=-30, ls=65, le=-20, head=-8))]
        else:
            ck += [(9.6, c_open), (10.6, c_bless)]
        CJ = draw_figure(cr, CX, gy, keyed(ck, t), s=1.05, face=-1, prop="robe")

        # ---------------- the debt scroll ----------------
        if t < 4.3:
            if t > 3.6:
                hx, hy = J["rhand"]
                debt_scroll(cr, hx + 14, hy - 8, s=sc)
        elif t < 5.0:
            hx, hy = CJ["rhand"]
            debt_scroll(cr, hx - 14, hy - 8, s=sc)
        else:
            debt_scroll(cr, CX - 72, gy - 128, tear=prog(t, 5.0, 5.4), fall=prog(t, 5.7, 6.5), gy=gy - 14 * sc, s=sc)


def draw_figure_ghost(x, gy, p, s=1.0, face=1):
    """Joint positions of a figure without drawing it."""
    surf = cairo.ImageSurface(cairo.FORMAT_A8, 4, 4)
    return draw_figure(cairo.Context(surf), x, gy, p, s=s, face=face)


OUTPUT_NAME = "day33a_two_debtors_luke7"
