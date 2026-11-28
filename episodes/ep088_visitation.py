import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import *
from props import *

HX = 830               # Zechariah's house (left edge); its door is at HX+40 .. HX+112
MX0, MX = 50, 700      # Mary: where she sets out, where she stops at the door
EX0, EX = 906, 806     # Elizabeth: in the doorway, where she steps out to

m_greet = pose("stand", rs=118, re=-10, head=-4)
m_humble = pose("stand", rs=20, re=110, ls=16, le=114, head=16, lean=4)       # hands to her heart
m_embrace = pose("stand", rs=76, re=30, ls=70, le=34, head=4, lean=6)
e_stand = pose("stand", lean=6, head=8)
e_belly = pose("stand", lean=2, head=18, rs=8, re=82, ls=4, le=86)           # hands on the child
e_joy = pose("joy", lean=-4, head=-16)
e_embrace = pose("stand", rs=76, re=30, ls=70, le=34, head=4, lean=8)
e_bless = pose("kneel", lean=16, head=24, rs=82, re=-6, ls=70, le=-4)         # "Blessed are you who believed"


class Visitation(Episode):
    dur = 18.0
    cta = "Start your day with Ave Missal"
    kicker = "LUKE 1  •  THE VISITATION"
    headline = "She carried Christ within her.\nSo she hurried to share him."
    captions = [
        (cpdv("Luke", 1, 39, "And in those days, Mary, rising up, traveled quickly into the hill country, to a city of Judah."), "Luke 1:39", 2.2),
        (cpdv("Luke", 1, 41, "…as Elizabeth heard the greeting of Mary, the infant leaped in her womb, and Elizabeth was filled with the Holy Spirit."), "Luke 1:41", 6.4),
        (cpdv("Luke", 1, 45, "And blessed are you who believed, for the things that were spoken to you by the Lord shall be accomplished."), "Luke 1:45", 11.4),
    ]

    def draw_panel(self, cr, i, t, y0, gy):
        sun(cr, 585, gy - 215, r=18, rays=10)
        mountain(cr, -60, gy, w=420, h=120, color=STONE)
        mountain(cr, 250, gy, w=360, h=90, color=STONE)
        for gx in (40, 330, 600):
            grass_tuft(cr, gx, gy, 12, sway=0.3 * math.sin(t * 2 + gx))
        door = prog(t, 4.8, 5.4) if i >= 1 else 0.0
        house(cr, HX, gy, door_open=door, light=0.8 * door)

        leap = prog(t, 6.3, 6.7) if i >= 1 else 0.0
        spirit = prog(t, 7.0, 7.8) if i >= 1 else 0.0
        blessed = prog(t, 11.0, 12.0) if i == 2 else 0.0

        # ---------- Mary ----------
        mx, mwa, _ = track(t, [(0.6, MX0), (4.0, MX)])
        mp = body(t, keyed([(0.0, pose("stand", head=10)), (0.6, pose("stand", head=-4, lean=6))], t), mwa, speed=2.0)
        if t > 4.0:
            mp = keyed([(4.0, pose("stand", head=-4)), (4.5, m_greet), (6.0, m_greet), (6.6, pose("stand", head=-2, rs=40, re=30))], t)
            if i == 0:
                mp = keyed([(4.0, pose("stand", head=-4)), (4.5, m_greet)], t)
            if i == 2 and t > 8.8:
                mp = keyed([(8.8, pose("stand", head=-2, rs=40, re=30)), (9.6, m_embrace), (10.6, m_embrace), (11.2, m_humble)], t)

        # ---------- Elizabeth ----------
        eliz = i >= 1 and t >= 4.9
        if eliz:
            ex, ewa, _ = track(t, [(5.1, EX0), (5.9, EX)])
            ep = body(t, e_stand, ewa, speed=1.2)
            if t > 5.9:
                ep = keyed([(5.9, e_stand), (6.2, e_stand), (6.5, e_belly), (7.0, e_belly), (7.6, e_joy)], t)
            if i == 2 and t > 8.8:
                ex, ewa, _ = track(t, [(9.0, EX), (9.6, 768)])
                ep = body(t, keyed([(8.8, e_joy), (9.4, e_embrace)], t), ewa, speed=1.2)
                if t > 9.6:
                    ex, ewa, _ = track(t, [(10.6, 768), (11.0, 812)])
                    ep = keyed([(9.6, e_embrace), (10.6, e_embrace), (11.0, e_stand), (11.6, e_bless)], t)
            # light first, so it sits behind both women
            G = ghost_joints(ex, gy, ep, s=0.93, face=-1)
            bx, by = lerp(G["hip"][0], G["sh"][0], 0.38) - 9 * 0.93, lerp(G["hip"][1], G["sh"][1], 0.38)
            fade = 1 - prog(t, 8.6, 9.6) * (1 if i == 2 else 0)
            warm_glow(cr, bx, by, 150, (0.6 * leap + 0.4 * spirit) * fade)
            light_rays(cr, bx, by, 0.7 * leap * (1 - prog(t, 7.4, 8.4)), r0=24, r1=46, n=10, t=t)
        if blessed > 0:
            G = ghost_joints(mx, gy, mp, s=0.93, face=1)
            light_rays(cr, G["head"][0], G["head"][1], 0.6 * blessed, r0=30, r1=52, n=12, t=t)

        J = draw_figure(cr, mx, gy, mp, s=0.93, face=1, prop="robe")
        veil_drape(cr, J, s=0.93, face=1)
        if eliz:
            J = draw_figure(cr, ex, gy, ep, s=0.93, face=-1, prop="robe")
            veil_drape(cr, J, s=0.93, face=-1)
            bump = 1.0 + 0.18 * math.sin(clamp((t - 6.3) / 0.4) * math.pi)
            belly(cr, J, s=0.93, face=-1, size=bump)


OUTPUT_NAME = "day44b_visitation_luke1"
