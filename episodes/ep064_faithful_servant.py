import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import *
from props import *

MX0 = 320            # the master, at the start
SX0 = 430            # the servant he leaves in charge
BASKET_X = 510       # the household's bread
JAR_X = 590          # the household's wine
H1, H2 = 690, 820    # the household, sitting on the ground, facing left
HOUSE_X = 900
STOOL_S, STOOL_C = 430, 290   # stools (panel 2): the servant and his drinking companion

m_point = pose("reach", rs=86, re=-4, lean=2, head=-2)
m_hand = pose("stand", rs=60, re=-10, head=4)
m_stern = pose("reach", rs=62, re=-14, ls=8, le=14, head=18, lean=4)     # pointing down at him
m_bless = pose("reach", rs=80, re=-6, head=6)
m_open = pose("stand", rs=110, re=-10, ls=100, le=-10, head=-6)

s_listen = pose("stand", head=6, rs=10, re=30)
s_shrug = pose("stand", rs=-40, re=-60, head=-16, lean=-6)              # waves the thought away
s_yawn = pose("stand", rs=165, re=10, ls=160, le=12, head=-20, lean=-4)
lie = pose("lie", ls=150, le=30, rs=160, re=20)
carry = pose("stand", rs=30, re=62, ls=24, le=66)
give = pose("reach", rs=74, re=-6, lean=14, head=12)
kneel_low = pose("kneel", lean=26, head=34, rs=40, re=40, ls=30, le=40)

h_wait = ground_sit_pose(head=2, rs=40, re=40, ls=30, le=40)
h_hungry = ground_sit_pose(head=30, lean=12, rs=58, re=-14, ls=40, le=30)
h_reach = ground_sit_pose(head=-4, lean=4, rs=75, re=-10, ls=30, le=40)


def eat(t, t0):
    """Hand to mouth and back, repeating."""
    u = 0.5 + 0.5 * math.sin((t - t0) * 3.2 - math.pi / 2)
    return ground_sit_pose(head=-6, lean=0, rs=lerp(45, 30, u), re=lerp(60, 128, u), ls=30, le=40)


class FaithfulServant(Episode):
    dur = 18.0
    cta = "Start your day with Ave Missal"
    kicker = "MATTHEW 24  •  THE FAITHFUL SERVANT"
    headline = "The master went away.\nWhat will he find when he returns?"
    captions = [
        (cpdv("Matthew", 24, 48, "But if that evil servant has said in his heart, ‘My lord has been delayed in returning,’"), "Matthew 24:48", 5.8),
        (cpdv("Matthew", 24, 49, "…he eats and drinks with the inebriated…"), "Matthew 24:49", 7.2),
        (cpdv("Matthew", 24, 46, "Blessed is that servant, if, when his lord has arrived, he shall find him doing so."), "Matthew 24:46", 12.0),
    ]

    def draw_panel(self, cr, i, t, y0, gy):
        su = prog(t, 2.0, 12.0)
        sun(cr, lerp(800, 1010, su), lerp(gy - 330, gy - 300, su), r=22, rays=10)
        blessed = prog(t, 13.2, 14.2) if i == 2 else 0.0

        # ---------------- the house and its stores ----------------
        house(cr, HOUSE_X, gy, w=170, h=190)
        stone_water_jar(cr, JAR_X, gy, fill=0.9, fill_color=WINE_C, w=50, h=80)
        if not (i == 2 and t > 5.2):
            food_basket(cr, BASKET_X, gy, w=50, h=30, loaves=3)
        if True:   # same starting scene in every panel
            plain_stool(cr, STOOL_S, gy)
            plain_stool(cr, STOOL_C, gy)
        warm_glow(cr, 560, gy - 110, 260, blessed * 0.8)

        # ---------------- the household ----------------
        fed1 = i == 2 and t > 6.9
        fed2 = i == 2 and t > 10.4
        for k, hx in enumerate((H1, H2)):
            fed = fed1 if k == 0 else fed2
            t_give = 6.4 if k == 0 else 9.9
            if i == 2 and t > t_give - 0.6:
                if not fed:
                    hp = keyed([(t_give - 0.6, h_wait), (t_give, h_reach)], t)
                else:
                    hp = keyed([(t_give + 0.5, h_reach), (t_give + 1.0, eat(t, t_give + 1.0))], t)
            elif i < 2:
                hp = keyed([(5.6 + k * 0.5, h_wait), (6.6 + k * 0.5, h_hungry)], t)
                if t > 6.6:
                    hp["head"] += 2 * math.sin(t * 1.6 + k)
            else:
                hp = h_wait
            HJ = draw_figure(cr, hx, gy, hp, s=0.9, face=-1)
            rx, ry = HJ["rhand"]
            if fed:
                loaf(cr, rx - 4, ry - 2)
            else:
                bowl(cr, rx - 4, ry + 4, w=24)

        # ---------------- the master ----------------
        if t < 4.4:
            mx, mwa, _ = track(t, [(2.2, MX0), (4.4, -90)])
            mface = 1 if t < 2.0 else -1
            mp = keyed([(0.3, pose("stand")), (0.7, m_point), (1.4, m_point), (1.7, m_hand), (2.0, pose("stand"))], t)
        else:
            target = (230 if i == 0 else 190) if i < 2 else 400
            mx, mwa, _ = track(t, [(9.6, -90), (11.6, target)])
            mface = 1
            mp = pose("stand", head=4)
            if i < 2:
                mp = keyed([(11.6, pose("stand", head=4)), (12.2, m_stern)], t)
            else:
                mp = keyed([(11.6, pose("stand", head=4)), (12.0, m_open), (12.8, m_open), (13.2, pose("stand")),
                            (13.6, m_bless)], t)
        mp = body(t, mp, mwa, speed=1.4)
        if mx > -85:
            MJ = draw_figure(cr, mx, gy, mp, s=1.05, face=mface, prop="robe_hat")

        # ---------------- the drinking companion (panel 2) ----------------
        if i == 1 and t > 4.6:
            cx, cwa, _ = track(t, [(4.6, -80), (6.4, STOOL_C)])
            if t < 6.4:
                cp = body(t, pose("stand", lean=6), cwa, speed=1.6)
            else:
                sw = math.sin(t * 2.6)
                toast = sit_pose(lean=-6 + 6 * sw, head=-10 + 6 * sw, rs=125 + 15 * sw, re=-20, ls=40, le=30)
                cp = keyed([(6.4, pose("stand")), (6.9, toast)], t)
                if t > 6.9: cp = toast
                if t > 12.0:
                    cp = keyed([(12.0, toast), (12.5, sit_pose(lean=30, head=36, rs=30, re=30, ls=20, le=30))], t)
            CJ = draw_figure(cr, cx, gy, cp, s=0.95, face=1)
            if t > 6.6:
                wine_goblet(cr, CJ["rhand"][0], CJ["rhand"][1] + 4, s=0.9, wine=1.0)

        # ---------------- the servant ----------------
        sx, sface, sp = SX0, -1, keyed([(0.6, s_listen), (1.2, pose("stand", head=-4, rs=20, re=20))], t)
        held = None          # what's in his hands
        lying = False
        if t > 4.4:
            if i == 0:
                sp = keyed([(4.4, pose("stand")), (4.8, s_shrug), (5.3, s_shrug), (5.8, s_yawn), (6.3, pose("stand"))], t)
                if t > 6.3:
                    lying = True
            elif i == 1:
                sx, swa, sdir = track(t, [(4.6, SX0), (5.3, 480), (5.9, 480), (6.6, STOOL_S)])
                sface = sdir if swa > 0.05 else (1 if t < 5.9 else -1)
                if t < 6.6:
                    sp = body(t, keyed([(5.3, pose("stand")), (5.5, pose("stand", lean=30, head=30, rs=60, re=0)), (5.9, pose("stand", rs=30, re=60))], t), swa)
                    if t > 5.6: held = "cup"
                else:
                    sw = math.sin(t * 2.6 + 1.3)
                    drink = sit_pose(lean=-8 + 5 * sw, head=-16 + 6 * sw, rs=50, re=118, ls=60, le=-10)
                    cheers = sit_pose(lean=-4 + 5 * sw, head=-8, rs=128, re=-20, ls=60, le=-10)
                    if t < 12.0:
                        sp = keyed([(6.6, pose("stand", rs=30, re=60)), (7.1, drink), (8.4, drink), (8.9, cheers), (9.8, cheers), (10.3, drink)], t)
                        if t > 10.3: sp = drink
                        held = "cup"
                    else:
                        sp = keyed([(12.0, drink), (12.4, pose("stand", rs=60, re=-50, ls=55, le=-50, head=20, lean=-6))], t)
                        held = "dropped"
            else:
                skeys = [(4.4, SX0), (4.8, BASKET_X - 40), (5.6, BASKET_X - 40), (6.2, H1 - 140),
                         (7.2, H1 - 140), (8.6, H2 - 110), (11.8, H2 - 110), (12.9, 545)]
                sx, swa, sdir = track(t, skeys)
                sface = sdir if swa > 0.05 else (-1 if t > 11.6 else 1)
                if t < 5.6:
                    sp = keyed([(4.8, pose("stand")), (5.1, pose("stand", lean=34, head=30, rs=60, re=0)), (5.6, carry)], t)
                    held = "basket" if t > 5.2 else None
                elif t < 11.6:
                    gk = [(6.2, carry), (6.4, give), (6.9, give), (7.2, carry), (9.6, carry), (9.9, give), (10.4, give), (10.8, carry)]
                    sp = body(t, keyed(gk, t), swa)
                    held = "basket"
                else:
                    sp = body(t, carry, swa)
                    held = "basket"
                    if t > 12.9:
                        sp = keyed([(12.9, carry), (13.3, kneel_low), (13.7, kneel_low), (14.0, pose("kneel", lean=8, head=-4, rs=72, re=-12, ls=30, le=40))], t)
                        held = "set_down"
            if i == 0 and t > 6.3:
                # lying asleep; jolts up when the master returns
                if t < 12.4:
                    breathe = 2 * math.sin(t * 1.8)
                    draw_rotated(cr, SX0 + 40, gy, -90, pose("lie", ls=150, le=30, rs=160, re=20, lean=breathe), s=0.95, lift=9)
                else:
                    up = sit_pose(lt=84, lk=-4, rt=78, rk=6, lean=-14, head=-26, ls=150, le=30, rs=165, re=20)
                    if t < 13.3:
                        ki = keyed([(12.4, ground_sit_pose(lean=-40, head=-10, ls=150, le=30, rs=160, re=20)), (12.8, up)], t)
                        draw_figure(cr, SX0 - 46, gy, ki, s=0.95, face=1)
                    else:
                        ki = keyed([(13.3, pose("kneel", lean=0, head=-10, rs=60, re=-30, ls=50, le=-30)), (13.9, kneel_low)], t)
                        draw_figure(cr, SX0 - 46, gy, ki, s=0.95, face=-1)
            elif not lying:
                pass
        if not (i == 0 and t > 6.3):
            SJ = draw_figure(cr, sx, gy, sp, s=0.95, face=sface)
            hx, hy = SJ["rhand"]
            if held == "cup":
                wine_goblet(cr, hx, hy + 4, s=0.9, wine=1.0)
                loaf(cr, SJ["lhand"][0], SJ["lhand"][1])
            elif held == "dropped":
                u = prog(t, 12.0, 12.4)
                wine_goblet(cr, lerp(hx, sx - 50, u), lerp(hy + 4, gy, u), s=0.9, wine=1 - u)
            elif held == "basket":
                lx, ly = SJ["lhand"]
                bxx = (hx + lx) / 2 + sface * 6
                left = 3 - (1 if t > 6.6 else 0) - (1 if t > 10.1 else 0)
                food_basket(cr, bxx, max(hy, ly) + 18, w=46, h=28, loaves=left)
                for t_g, hxx in ((6.4, H1), (9.9, H2)):
                    if t_g < t < t_g + 0.5:
                        u = prog(t, t_g, t_g + 0.5)
                        loaf(cr, lerp(hx, hxx - 70, u), lerp(hy, gy - 70, u))

        # ---------------- the reward: set over all his goods ----------------
        if i == 2 and t > 13.6:
            u = prog(t, 13.8, 14.4)
            ax, ay = MJ["rhand"]; bx, by = SJ["rhand"]
            cx, cy = lerp(ax, bx, u), lerp(ay, by, u)
            coin_bag(cr, cx, cy - 8, s=1.0)
            coin_glint(cr, cx, cy - 4, prog(t, 14.2, 15.0), t)


OUTPUT_NAME = "day32b_faithful_servant_matthew24"
