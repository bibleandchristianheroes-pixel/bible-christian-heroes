import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import *
from props import *

THRONE_X = 150      # Joseph's seat of office (behind him)
JX0 = 290           # Joseph stands here at the start
JX1 = 360           # one step toward his brothers ("I am Joseph")
BRO = [640, 775, 905]        # brothers kneeling, bowed low
BACK = [730, 850, 965]      # where they shrink back in fear
NEAR = [520, 650, 780]       # where they stop when he calls them close
BS = 0.92

j_stand = pose("stand", head=6)
j_cloth = pose("stand", head=-4, ls=150, le=60)                     # far hand up to the head-cloth
j_chest = pose("stand", head=-4, lean=-2, rs=30, re=120, ls=20, le=20)  # "I am Joseph"
j_open = pose("stand", head=-6, rs=78, re=-10, ls=70, le=-10)         # open hands to them
j_weep = pose("stand", lean=12, head=30, rs=150, re=150, ls=40, le=30)  # face in his hand
j_beck1 = pose("stand", head=-4, rs=95, re=-20, ls=30, le=20)
j_beck2 = pose("stand", head=-4, rs=80, re=-95, ls=30, le=20)         # "Approach toward me"
j_hug = pose("stand", rs=95, re=-55, ls=95, le=-60, lean=8, head=10)

b_bow = pose("kneel", lean=48, head=30, rs=60, re=30, ls=50, le=30)
b_look = pose("kneel", lean=10, head=-14, rs=40, re=30, ls=35, le=30)
b_fear = pose("stand", lean=-14, head=-10, rs=140, re=40, ls=125, le=50)
b_cower = pose("kneel", lean=30, head=34, rs=150, re=150, ls=150, le=150)
b_shy = pose("stand", lean=10, head=22, rs=20, re=30, ls=15, le=30)
b_hug = pose("stand", rs=90, re=-60, ls=90, le=-55, lean=6, head=8)
b_glad = pose("stand", head=-6, rs=60, re=-10, ls=55, le=-10)


class JosephForgives(Episode):
    dur = 18.0
    cta = "Read it in Scroll the Catholic Bible"
    kicker = "GENESIS 45  •  JOSEPH AND HIS BROTHERS"
    headline = "They sold him into slavery.\nHe could have punished them."
    captions = [
        (cpdv("Genesis", 45, 3, "“I am Joseph. Is my father still alive?” His brothers were unable to respond, being terrified by a very great fear."), "Genesis 45:3", 4.6),
        (cpdv("Genesis", 45, 4, "And he said to them mildly, “Approach toward me.”"), "Genesis 45:4", 8.0),
        (cpdv("Genesis", 45, 5, "Do not be afraid… For God sent me before you into Egypt for your salvation."), "Genesis 45:5", 11.4),
    ]

    def draw_panel(self, cr, i, t, y0, gy):
        pyramids(cr, 830, gy, s=1.0)
        lotus_column(cr, 1045, gy, h=230)
        throne(cr, THRONE_X, gy, face=1)
        glow = prog(t, 11.2, 12.6) if i == 2 else 0.0
        warm_glow(cr, 470, gy - 110, 380, 0.8 * glow)

        # ---------------- Joseph ----------------
        jx, jwa, _ = track(t, [(1.6, JX0), (2.6, JX1)])
        jk = [(0.0, j_stand), (0.8, j_stand), (1.2, j_cloth), (1.7, j_cloth), (2.2, pose("stand", head=-4)), (2.8, j_chest), (4.0, j_chest), (4.6, j_open)]
        if i == 0:
            jk += [(6.4, j_open), (7.0, pose("stand", head=14, lean=6)), (7.8, j_weep)]
        else:
            jk += [(7.2, j_open), (7.7, j_beck1), (8.1, j_beck2), (8.5, j_beck1), (8.9, j_beck2), (9.4, j_open)]
            if i == 2:
                jx2, jwa2, _ = track(t, [(10.4, JX1), (11.2, 440)])
                if t > 10.4:
                    jx, jwa = jx2, jwa2
                jk += [(10.4, j_open), (11.2, j_hug)]
        jp = body(t, keyed(jk, t), jwa)

        # ---------------- brothers ----------------
        bros = []
        for k in range(3):
            d = 0.12 * k
            bk = [(0.0, b_bow), (2.9 + d, b_bow), (3.3 + d, b_look), (3.9 + d, b_look), (4.4 + d, b_fear)]
            keys = [(4.4 + d, BRO[k]), (5.4 + d, BACK[k])]
            if i == 0:
                bk += [(5.6 + d, b_fear), (6.4 + d, b_cower)]
            else:
                bk += [(6.0 + d, b_fear), (6.8 + d, pose("stand", lean=4, head=10, rs=40, re=40, ls=40, le=40)),
                       (8.6 + d, b_shy)]
                keys += [(8.6 + d, BACK[k]), (10.4 + d, NEAR[k])]
                if i == 2:
                    if k == 0:
                        bk += [(10.6, b_shy), (11.2, b_hug)]
                        keys += [(11.2, NEAR[0] - 40)]
                    else:
                        bk += [(11.4 + d, b_shy), (12.2 + d, b_glad)]
                        keys += [(11.6 + d, NEAR[k]), (12.4 + d, NEAR[k] - 50 - 20 * k)]
            x, wa, dirn = track(t, keys)
            p = keyed(bk, t)
            if t < 4.4 + d or (i == 0 and t > 6.4 + d):
                wa = 0.0
            arms = dict(p)
            p = body(t, p, wa * (0.8 if t > 8 else 1.0), speed=1.2 if t > 8 else 1.9)
            if t < 8:       # backing away: keep the frightened arms and lean while the legs walk
                for key in ("lean", "head", "rs", "re", "ls", "le"):
                    p[key] = arms[key]
            bros.append((x, p))

        hugging = i == 2 and t >= 11.1
        # brother being embraced is drawn first, Joseph on top
        for k, (x, p) in enumerate(bros):
            draw_figure(cr, x, gy, p, s=BS, face=-1, prop="robe")
        J = draw_figure(cr, jx, gy, jp, s=1.0, face=1, prop="robe")

        # head-cloth: worn, taken off, laid on the seat
        if t < 1.7:
            nemes(cr, J["head"], s=1.0, face=1)
        elif t < 2.3:
            hx, hy = J["lhand"]
            nemes_cloth(cr, lerp(hx, THRONE_X, prog(t, 1.9, 2.3)), lerp(hy + 6, gy - 58, prog(t, 1.9, 2.3)))
        else:
            nemes_cloth(cr, THRONE_X, gy - 58)

        # tears
        if i == 0 and t > 7.8:
            tears(cr, J["head"][0] + 6, J["head"][1] + 8, t, amount=prog(t, 7.8, 8.4))
        if i == 2 and t > 11.4:
            hx, hy = J["head"]
            tears(cr, hx + 8, hy + 8, t, amount=prog(t, 11.4, 12.0))
            bx, by = bros[0][0], gy - 175 * BS
            tears(cr, bx - 10, by, t + 0.4, amount=prog(t, 11.8, 12.4), face=-1)


OUTPUT_NAME = "day37a_joseph_forgives_genesis45"
