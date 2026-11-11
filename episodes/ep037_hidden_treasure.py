import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import *
from props import *

HX = 120            # his house (centre)
TX = 790            # buried treasure
MX = 715            # where he digs
OWN = 470           # owner of the field
PILE = [(235, "sack"), (285, "plain_stool"), (330, "lamp")]

class HiddenTreasure(Episode):
    dur = 18.0
    cta = "Read it in Scroll the Catholic Bible"
    kicker = "MATTHEW 13  •  THE HIDDEN TREASURE"
    headline = "He found a treasure.\nHe gave everything for it."
    captions = [
        (cpdv("Matthew", 13, 44, "…a treasure hidden in a field. When a man finds it, he hides it…"), "Matthew 13:44", 5.6),
        (cpdv("Matthew", 13, 44, "…because of his joy, he goes and sells everything that he has, and he buys that field."), "Matthew 13:44", 9.4),
        (cpdv("Matthew", 13, 46, "Having found one pearl of great value, he went away and sold all that he had, and he bought it."), "Matthew 13:46", 12.4),
    ]

    def item(self, cr, kind, x, gy):
        if kind == "sack": grain_sack(cr, x, gy, s=0.9)
        elif kind == "plain_stool": plain_stool(cr, x, gy, h=34, w=40)
        else: lamp(cr, x, gy)

    def draw_panel(self, cr, i, t, y0, gy):
        small_house(cr, HX, gy, light=0.0)
        rock_path_tufts(cr, gy, [520, 610, 880, 960, 1040])

        # ---------- the treasure ----------
        rise = prog(t, 3.1, 3.9)
        sink = prog(t, 5.3, 6.1)
        up2 = prog(t, 11.6, 12.1) if i == 2 else 0.0
        depth = 50 * (1 - rise) + 50 * sink * (1 - up2)
        glow = 0.55 * rise * (1 - sink) + up2
        opened = prog(t, 12.1, 12.6) if i == 2 else 0.12 * rise * (1 - sink)
        if glow > 0:
            warm_glow(cr, TX, gy - 30, 260 + 160 * up2, glow * 0.9)
        cr.save(); cr.rectangle(TX - 200, y0, 400, gy - y0); cr.clip()
        treasure_chest(cr, TX, gy + depth, open_=opened, glow=glow * 0.6 if i < 2 else glow)
        cr.restore()
        if i == 2 and t > 12.3:
            pu = prog(t, 12.3, 13.0)
            pearl(cr, TX, gy - 50 - 80 * pu, r=17, glow=pu)
        mound = 12 * sink * (1 - up2)
        dirt_mound(cr, TX + 40, gy, 70, mound)

        # ---------- goods and the field's owner ----------
        sold = i >= 1
        owner_x, owner_face = OWN, -1
        owner_p = pose("stand", head=-4)
        if sold and t > 10.4:
            owner_x, owa, _ = track(t, [(10.4, OWN), (11.8, -90)])
            owner_p = body(t, pose("stand", rs=60, re=60), owa)
        elif sold and t > 7.6:
            give = pose("stand", rs=80, re=-10, head=-4)
            owner_p = keyed([(7.6, pose("stand")), (8.0, give), (9.6, give), (10.0, pose("stand", rs=-70, re=0, head=-4))], t)
            if t > 9.6: owner_face = -1
        for k, (px, kind) in enumerate(PILE):
            if not sold or t < 7.7 + 0.6 * k:
                self.item(cr, kind, px, gy)
            elif t < 10.4:
                u = prog(t, 7.7 + 0.6 * k, 8.2 + 0.6 * k)
                ex = OWN + 45 + k * 32
                self.item(cr, kind, lerp(px, ex, u), gy - 80 * math.sin(math.pi * u))
                if 0 < u < 1:   # coin back to him
                    coin(cr, lerp(OWN - 20, 330, u), gy - 110 - 40 * math.sin(math.pi * u), r=8)
        J = draw_figure(cr, owner_x, gy, owner_p, s=1.05, face=owner_face, prop="robe_hat")
        if sold and t > 10.4:
            grain_sack(cr, J["rhand"][0], J["rhand"][1] + 40, s=0.8)

        # ---------- the man who finds it ----------
        dig_lo = pose("stand", rs=70, re=5, ls=60, le=5, lean=28, head=20, lt=14, lk=20, rt=-16, rk=16)
        dig_hi = pose("stand", rs=50, re=40, ls=40, le=50, lean=12, head=10)
        kneel = pose("stand", lean=45, head=30, rs=60, re=10, ls=50, le=10, lt=25, lk=35, rt=5, rk=35)
        x, face, wa, tool = MX, 1, 0.0, None
        if t < 2.8:
            p = mix(dig_hi, dig_lo, 0.5 + 0.5 * math.sin((t - 0.4) / 0.8 * 2 * math.pi)) if t > 0.4 else dig_hi
            tool = "spade"
        elif t < 4.4:
            p = keyed([(2.8, dig_lo), (3.2, kneel), (4.0, kneel), (4.4, pose("stand", head=-4))], t)
        elif t < 6.4 or i == 0:
            look = pose("stand", head=-4)
            p = look
            if 4.4 < t < 5.3:
                face = -1 if (t - 4.4) % 0.6 < 0.3 else 1
            elif t < 6.2:
                p = keyed([(5.3, dig_hi), (5.6, dig_lo), (5.9, dig_hi), (6.2, pose("stand"))], t); tool = "spade"
            elif i == 0:
                p = keyed([(6.2, pose("stand")), (6.7, pose("joy"))], t)
                if t > 6.7:
                    x = MX; p = pose("joy")
                    J0 = draw_figure(cr, x, gy - 12 * abs(math.sin((t - 6.7) * 4)), p, s=1.0, face=1)
                    spade(cr, MX - 60, gy - 118, MX - 50, gy + 4)
                    return
        else:
            x, wa, d = track(t, [(6.4, MX), (7.5, 330), (10.2, 330), (11.0, MX)])
            face = d if wa > 0.05 else 1
            give = pose("stand", rs=85, re=-10, ls=70, le=0)
            if t < 7.5:
                p = body(t, pose("stand"), wa); face = -1
            elif t < 10.2:
                p = keyed([(7.5, pose("stand")), (7.7, give), (9.6, give), (10.0, pose("stand", rs=40, re=80))], t)
                face = 1
            elif t < 11.0:
                p = body(t, pose("stand", rs=40, re=80), wa); face = 1
            elif i == 1:
                p = keyed([(11.0, pose("stand")), (11.6, pose("joy"))], t)
            else:
                p = keyed([(11.0, dig_hi), (11.3, dig_lo), (11.6, dig_hi), (12.0, kneel), (12.6, pose("stand", head=-20, rs=90, re=-20, ls=80, le=-10)),
                           (13.2, pose("joy"))], t)
                tool = "spade" if t < 11.9 else None
        J = draw_figure(cr, x, gy, p, s=1.0, face=face)
        if tool == "spade":
            hx, hy = J["rhand"]
            spade(cr, hx, hy - 6, hx + face * 28, min(gy + 6, hy + 92))
        else:
            spade(cr, MX - 60, gy - 118, MX - 50, gy + 4)

OUTPUT_NAME = "day19a_hidden_treasure_matthew13"
