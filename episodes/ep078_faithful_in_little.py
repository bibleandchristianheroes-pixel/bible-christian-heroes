import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import *
from props import *

SX = 430            # the servant
MX0 = 640           # the master, at the start
MRET = 600          # where the master stands when he comes back
OFF = 1180          # off-screen right
LOST_X = 175        # where the tossed coin lands (panel 2)
SEAT_X = 470        # where he lounges (panel 2)

m_give = pose("reach", rs=78, re=-6, ls=20, le=30, head=8, lean=6)
m_hold = pose("stand", ls=20, le=30, rs=12, re=14)
m_ask = pose("reach", rs=70, re=-30, ls=20, le=30, head=4, lean=2)          # palm out: "the coin?"
m_down = pose("stand", ls=20, le=30, rs=20, re=20, head=26, lean=6)
m_point = pose("reach", rs=60, re=-10, ls=20, le=30, head=20, lean=6)
m_offer = pose("reach", rs=30, re=20, ls=78, le=-6, head=6, lean=6)        # holds out the bag
m_bless = pose("stand", rs=128, re=-14, ls=-36, le=12, head=-6, lean=-2)

s_take = pose("reach", rs=74, re=-8, head=6, lean=4)
s_look = pose("stand", rs=40, re=70, head=24, lean=4)                      # looking at the coin in his hand
s_hug = pose("stand", rs=34, re=96, ls=30, le=100, head=18, lean=4)         # coin held close to his chest
s_pocket = pose("stand", rs=-34, re=22, head=16, lean=4)                    # hand at the pouch behind his hip
s_whistle = pose("stand", rs=-20, re=30, ls=-16, le=30, head=-14, lean=-4)  # hands behind his back
s_toss = pose("stand", rs=60, re=60, head=-20, lean=-2)
s_flick = pose("stand", rs=96, re=10, head=-26, lean=-4)
s_shrug = pose("stand", rs=60, re=-60, ls=55, le=-60, head=-10, lean=-6)    # empty hands
s_give = pose("reach", rs=80, re=-8, head=4, lean=8)
s_receive = pose("reach", rs=72, re=-6, ls=66, le=-6, head=4, lean=6)
s_raise = pose("stand", rs=150, re=5, ls=140, le=10, head=-14, lean=-4)
s_hang = pose("stand", head=28, lean=6, rs=6, re=6, ls=4, le=6)
lounge = ground_sit_pose(lean=-22, head=-12, rs=-30, re=60, ls=-26, le=60)  # leaning back on his hands


class FaithfulInLittle(Episode):
    dur = 18.0
    cta = "Pray it with Ave – Catholic Prayer Lock"
    kicker = "LUKE 16  •  FAITHFUL IN LITTLE"
    headline = "Each was trusted with one coin.\nOnly one was trusted with more."
    captions = [
        (cpdv("Luke", 16, 10, "…whoever is unjust in what is small, is also unjust in what is greater."), "Luke 16:10", 6.0),
        (cpdv("Luke", 16, 11, "So then, if you have not been faithful with iniquitous mammon, who will trust you with what is true?"), "Luke 16:11", 6.8),
        (cpdv("Luke", 16, 10, "Whoever is faithful in what is least, is also faithful in what is greater."), "Luke 16:10", 13.0),
    ]

    def draw_panel(self, cr, i, t, y0, gy):
        sun(cr, 990, gy - 300, r=22, rays=10)
        olive_tree(cr, 90, gy, h=130)
        for gx in (150, 240, 720, 1010):
            grass_tuft(cr, gx, gy, 12, sway=0.3 * math.sin(t * 2 + gx))
        reward = prog(t, 13.6, 14.4) if i == 2 else 0.0
        warm_glow(cr, SX, gy - 120, 300, 0.8 * reward)

        # ---------------- the master ----------------
        mface = -1; mwa = 0.0; mx = MX0
        mp = keyed([(0.0, m_hold), (0.6, m_hold), (1.0, m_give), (1.7, m_give), (2.0, m_hold)], t)
        if t >= 2.0 and t < 9.6:
            mx, mwa, d = track(t, [(2.0, MX0), (4.4, OFF)]); mface = 1
            mp = m_hold
        elif t >= 9.6:
            mx, mwa, d = track(t, [(9.6, OFF), (11.4, MRET)]); mface = -1
            mp = m_hold
            if i == 0:
                mp = keyed([(11.4, m_hold), (11.8, m_ask), (12.6, m_ask), (13.0, m_down), (13.8, m_down)], t)
                if t > 13.9:
                    mx, mwa, d = track(t, [(13.9, MRET), (16.4, OFF)]); mface = 1; mp = m_hold
            elif i == 1:
                mp = keyed([(11.4, m_hold), (11.8, m_ask), (12.8, m_ask), (13.1, m_point), (13.9, m_point), (14.1, m_hold)], t)
                if t > 14.2:
                    mx, mwa, d = track(t, [(14.2, MRET), (16.6, OFF)]); mface = 1; mp = m_hold
            else:
                mp = keyed([(11.4, m_hold), (11.8, m_ask), (12.6, m_ask), (12.9, m_hold), (13.1, m_offer), (13.6, m_offer),
                            (14.0, m_hold), (14.6, m_bless)], t)
        mp = body(t, mp, mwa, speed=1.4)
        MJ = None
        if mx < OFF - 20:
            MJ = draw_figure(cr, mx, gy, mp, s=1.05, face=mface, prop="robe_hat")
            if not (i == 2 and t > 13.4):
                lx, ly = MJ["lhand"]
                coin_bag(cr, lx, ly + 2, s=1.0)

        # ---------------- the servant ----------------
        sx, sface, swa = SX, 1, 0.0
        sp = keyed([(0.0, pose("stand", head=4)), (0.8, pose("stand", head=4)), (1.1, s_take), (1.8, s_take), (2.3, s_look)], t)
        coin_at = "s_hand" if t > 1.5 else ("m_hand" if t < 1.2 else "pass")
        sitting = False
        if t >= 2.3:
            sp = keyed([(2.3, s_look), (3.6, s_look)], t)
            sp["head"] += 3 * math.sin(t * 1.5)
        if i == 0 and t >= 4.0:
            # glances back, then slips the coin into his own pouch
            sp = keyed([(4.0, s_look), (4.4, pose("stand", head=-6)), (5.4, pose("stand", head=-6)),
                        (5.7, s_pocket), (6.3, s_pocket), (6.7, s_whistle)], t)
            if 4.5 < t < 5.3:
                sface = -1
            if t > 5.9:
                coin_at = "pouch"
            if t > 11.4:
                sp = keyed([(11.4, s_whistle), (11.9, s_shrug), (12.7, s_shrug), (13.2, s_hang)], t)
            if t > 12.4:
                coin_at = "falling"
        elif i == 1 and t >= 4.0:
            if t < 7.6:
                # flips it into the air, again and again ... and the last flip goes wide
                ph = (t - 4.0) % 0.9
                sp = s_toss if ph > 0.25 else mix(s_flick, s_toss, ph / 0.25)
                coin_at = "toss" if t < 6.7 else "lost"
            else:
                sitting = True
                sx = SEAT_X
                if t < 11.0:
                    sp = keyed([(7.6, s_shrug), (8.1, pose("stand", head=-8)), (8.8, lounge)], t)
                    sitting = t > 8.8
                    if t < 8.8: sx = lerp(SX, SEAT_X, prog(t, 7.6, 8.6))
                else:
                    sp = keyed([(11.0, lounge), (11.6, pose("stand", head=-6)), (12.0, s_shrug), (13.0, s_shrug),
                                (13.3, pose("stand", head=-20, lean=-4, rs=6, re=10)), (14.2, s_hang)], t)
                    sitting = t < 11.6
                coin_at = "lost"
        elif i == 2 and t >= 4.0:
            sp = keyed([(4.0, s_look), (4.6, s_hug)], t)
            sp["head"] += 3 * math.sin(t * 1.3)
            if t > 11.2:
                sx, swa, d = track(t, [(11.2, SX), (11.9, SX + 50)])
                sp = keyed([(11.4, s_hug), (11.9, s_give), (12.6, s_give), (12.9, pose("stand")), (13.2, s_receive),
                            (13.8, s_receive), (14.4, s_raise)], t)
                sp = body(t, sp, swa)
            if t > 12.2:
                coin_at = "m_hand" if t > 12.6 else "pass_back"
        if sitting:
            SJ = draw_figure(cr, sx + 40, gy, sp, s=0.95, face=sface)
        else:
            SJ = draw_figure(cr, sx, gy, sp, s=0.95, face=sface)
        # his own little pouch behind his hip
        hpx, hpy = SJ["hip"]
        fat = 1.0 if coin_at in ("pouch",) else 0.0
        coin_bag(cr, hpx - sface * 16, hpy - 8, s=0.62 + 0.1 * fat)

        # ---------------- the big bag changes hands (panel 3) ----------------
        if i == 2 and t > 13.4 and MJ is not None:
            u = prog(t, 13.4, 13.8)
            lx, ly = MJ["lhand"]
            tx = (SJ["rhand"][0] + SJ["lhand"][0]) / 2; ty = min(SJ["rhand"][1], SJ["lhand"][1])
            bx, by = lerp(lx, tx, u), lerp(ly + 2, ty - 26, u)
            coin_bag(cr, bx, by, s=1.0)
            if t > 14.2:
                coin_glint(cr, bx + 20, by - 10, prog(t, 14.2, 14.8), t=t, r=22)

        # ---------------- the one coin ----------------
        sh = SJ["rhand"]
        mh = MJ["rhand"] if MJ is not None else (MX0, gy - 100)
        if coin_at == "m_hand":
            if i == 2 and t > 12.6:
                if t < 14.0:
                    coin(cr, mh[0], mh[1] - 4, r=9)
            else:
                coin(cr, mh[0], mh[1] - 4, r=9)
        elif coin_at == "pass":
            coin(cr, mh[0], mh[1] - 4, r=9)
        elif coin_at == "s_hand":
            if i == 2 and t > 4.6:
                coin(cr, (sh[0] + SJ["lhand"][0]) / 2, min(sh[1], SJ["lhand"][1]) - 2, r=9)
            else:
                coin(cr, sh[0] + 2, sh[1] - 6, r=9)
            if i == 2 and 5.2 < t < 6.6:
                coin_glint(cr, sh[0] + 6, sh[1] - 16, prog(t, 5.2, 5.6) * (1 - prog(t, 6.1, 6.6)), t=t, r=18)
        elif coin_at == "pass_back":
            u = prog(t, 12.2, 12.6)
            coin(cr, lerp(sh[0], mh[0], u), lerp(sh[1], mh[1], u) - 4, r=9)
        elif coin_at == "toss":
            ph = (t - 4.0) % 0.9
            hgt = 70 * math.sin(math.pi * clamp((ph - 0.12) / 0.7))
            coin(cr, sh[0] + 2, sh[1] - 6 - hgt, r=9)
        elif coin_at == "lost":
            u = clamp((t - 6.7) / 0.9)
            cx = lerp(sh[0] if t < 6.8 else SX + 40, LOST_X, u)
            cy = lerp(gy - 150, gy - 9, u) - 120 * math.sin(math.pi * u) * 0.6
            if t < 6.7 + 0.9:
                coin(cr, cx, cy, r=9)
            else:
                coin(cr, LOST_X, gy - 9, r=9)
                if 13.1 < t < 14.4:
                    coin_glint(cr, LOST_X, gy - 12, prog(t, 13.1, 13.4) * (1 - prog(t, 14.0, 14.4)), t=t, r=20)
        elif coin_at == "falling":
            u = clamp((t - 12.4) / 0.45)
            fx = hpx - sface * 15 - 20 * u
            coin(cr, fx, lerp(hpy + 8, gy - 9, u * u), r=9)
            if t > 12.8:
                coin_glint(cr, fx, gy - 12, prog(t, 12.8, 13.1) * (1 - prog(t, 14.4, 15.0)), t=t, r=20)


OUTPUT_NAME = "day39b_faithful_in_little_luke16"
