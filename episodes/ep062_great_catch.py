import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import *
from props import *

SHORE = 400       # the beach ends here; open water to the right
BCX = 690         # boat centre
JX = 540          # Jesus, seated at the stern, facing the bow
PX = 820          # Peter, at the bow
NET_X = 985       # where the net goes into the water

haul = pose("stand", lean=-16, head=-6, rs=70, re=-20, ls=64, le=-16, lt=14, rt=-16, lk=8, rk=8)
slump = sit_pose(lean=22, head=34, rs=40, re=40, ls=34, le=44)
empty_hands = sit_pose(lean=4, head=-6, rs=70, re=-35, ls=62, le=-30)
despair = sit_pose(lean=34, head=40, rs=20, re=30, ls=14, le=30)


class GreatCatch(Episode):
    dur = 18.0
    ground = False
    caption_bg = True
    cta = "Pray it with Ave – Catholic Prayer Lock"
    kicker = "LUKE 5  •  THE GREAT CATCH"
    headline = "Empty nets all night.\nThen they cast at his word."
    captions = [
        (cpdv("Luke", 5, 5, "…“Teacher, working throughout the night, we caught nothing…"), "Luke 5:5", 6.6),
        (cpdv("Luke", 5, 6, "…they enclosed such a copious multitude of fish that their net was rupturing."), "Luke 5:6", 9.2),
        (cpdv("Luke", 5, 11, "And having led their boats to land, leaving behind everything, they followed him."), "Luke 5:11", 12.8),
    ]

    def draw_panel(self, cr, i, t, y0, gy):
        night = 0.78 * (1 - prog(t, 3.0, 6.0))
        su = prog(t, 3.0, 8.0)
        sun(cr, 1000, lerp(gy + 40, y0 + 240, su), r=24)

        catch = i >= 1
        fill = prog(t, 8.3, 9.6) if catch else 0.0
        burst = prog(t, 9.0, 9.8) if catch else 0.0
        released = i == 2 and t > 10.6
        tilt = 4.5 * fill * (1 - prog(t, 10.6, 11.4) if i == 2 else 1) + 1.2 * math.sin(t * 1.4)
        bob = 2 * math.sin(t * 1.7)
        gun = gy - 34 + bob
        fy = gun + 18

        # shore
        cr.set_source_rgb(*INK); cr.set_line_width(4)
        cr.move_to(0, gy); cr.line_to(SHORE, gy); cr.curve_to(SHORE + 20, gy + 4, SHORE + 30, gy + 14, SHORE + 44, gy + 26); cr.stroke()
        rock_path_tufts(cr, gy, (90, 240))

        def rot(pt):
            a = math.radians(tilt); dx, dy = pt[0] - BCX, pt[1] - gun
            return BCX + dx * math.cos(a) - dy * math.sin(a), gun + dx * math.sin(a) + dy * math.cos(a)

        cr.save(); cr.translate(BCX, gun); cr.rotate(math.radians(tilt)); cr.translate(-BCX, -gun)

        # ---------------- Jesus ----------------
        point = sit_pose(head=-6, rs=100, re=-10, ls=30, le=45)
        wait = sit_pose(head=4, rs=40, re=40, ls=30, le=45)
        jkeys = [(4.0, wait), (4.6, point), (6.4, point), (7.0, wait)]
        jx, jg, jface, jwa = JX, fy, 1, 0
        jp = keyed(jkeys, t)
        if catch and t > 9.6:
            jp = keyed([(9.6, wait), (10.2, sit_pose(head=-6, rs=60, re=-10, ls=50, le=-10))], t)
        on_shore = False
        if i == 2 and t > 11.6:
            stand_up = pose("stand", rs=30, re=20, ls=20, le=20)
            jface = -1
            if t < 12.2:
                jp = keyed([(11.6, sit_pose(head=-6, rs=60, re=-10, ls=50, le=-10)), (12.2, stand_up)], t)
            else:
                jx, jwa, _ = track(t, [(12.2, JX), (14.6, 150)])
                jp = body(t, stand_up, jwa, speed=1.2)
                if t > 14.6:
                    jp = keyed([(14.6, stand_up), (15.2, pose("stand", rs=55, re=-10, head=-4))], t)
                    jface = 1
                u = clamp((JX - 30 - jx) / 110.0)
                jg = lerp(fy, gy, u)
                on_shore = jx < SHORE + 20
        if not on_shore:
            draw_figure(cr, jx, jg, jp, s=1.02, face=jface, prop="robe")

        # ---------------- Peter ----------------
        pface = 1; px = PX; pg = fy; pwa = 0
        if t < 2.6:
            p = haul if t < 2.0 else keyed([(2.0, haul), (2.6, pose("stand", head=20))], t)
        elif not catch and t > 6.2:
            p = keyed([(6.2, empty_hands), (6.8, despair)], t)
            if t > 6.8: p["lean"] += 2 * math.sin(t * 3)
        elif t < 6.2:
            p = keyed([(2.6, pose("stand", head=20)), (3.4, slump), (4.8, slump), (5.4, empty_hands)], t)
            if t > 5.0: pface = -1
        else:
            cast_back = pose("sow_back", rs=-60, re=10, lean=-8)
            cast_fwd = pose("sow_fwd", rs=105, re=-5, lean=12)
            p = keyed([(6.2, empty_hands), (6.7, pose("stand")), (7.1, cast_back), (7.5, cast_fwd), (8.0, pose("stand", rs=80, re=-10)),
                       (8.4, haul)], t)
            if t > 8.4:
                p = dict(haul); p["lean"] = -16 - 6 * fill + 2 * math.sin(t * 9) * (1 - burst * 0.5)
            if i == 1 and t > 9.8:
                p = keyed([(9.8, p), (10.6, pose("stand", lean=-14, head=-12, rs=70, re=-20, ls=64, le=-16, lt=14, rt=-16, lk=8, rk=8))], t)
            if i == 2 and t > 10.4:
                pface = -1
                kneel = pose("kneel", lean=24, head=30, rs=40, re=40, ls=30, le=40)
                p = keyed([(10.4, haul), (10.8, pose("stand")), (11.4, kneel), (12.4, kneel), (12.9, pose("stand", head=-6))], t)
                if t > 12.9:
                    px, pwa, _ = track(t, [(12.9, PX), (15.4, 300)])
                    p = body(t, pose("stand", head=-6), pwa, speed=1.2)
                    if t > 15.4: p = pose("stand", head=-6)
                    u = clamp((JX - 30 - px) / 110.0)
                    pg = lerp(fy, gy, u)
        if p.get("lt", 0) > 60 and pwa == 0:   # seated on the thwart, not on the floor
            pg = fy + 26
        p_on_shore = px < SHORE + 20
        if not p_on_shore:
            PJ = draw_figure(cr, px, pg, p, s=1.0, face=pface)
        if not catch or t < 6.6:
            if t > 2.4:
                empty_net_pile(cr, 900, fy - 16, w=60)
        fishing_boat(cr, BCX, gun, w=420, mast=0)
        cr.restore()

        water(cr, gy, t, x0=SHORE + 30, x1=W + 20, amp=4, rough=0.5 + 0.8 * burst * (1 - prog(t, 11.0, 12.0)), below=80)

        # figures that have stepped onto the beach are drawn after the water
        if on_shore:
            draw_figure(cr, jx, jg, jp, s=1.02, face=jface, prop="robe")
        if p_on_shore:
            draw_figure(cr, px, pg, p, s=1.0, face=pface)

        # ---------------- the net ----------------
        if t < 2.4:   # the empty net hauled in at dawn
            hx, hy = rot(PJ["rhand"])
            hh = 60 * (1 - prog(t, 1.0, 2.3))
            ny = lerp(gy + 6, hy + 10, prog(t, 1.0, 2.3))
            fishing_net(cr, hx, hy, lerp(NET_X, hx + 30, prog(t, 1.0, 2.3)), ny, w=110, h=max(hh, 6), fish_n=0, t=t)
        elif catch and t > 7.5:
            hx, hy = rot(PJ["rhand"]) if not released else rot((BCX + 228, gun - 8))
            if t < 8.0:     # flying out over the water
                u = prog(t, 7.5, 8.0)
                nx = lerp(hx + 20, NET_X, u); ny = lerp(hy, gy + 6, u) - 70 * math.sin(math.pi * u)
                fishing_net(cr, hx, hy, nx, ny, w=lerp(40, 110, u), h=lerp(20, 60, u), t=t)
            else:
                n = int(30 * fill)
                fishing_net(cr, hx, hy, NET_X, gy - 2, w=110, h=52, fish_n=n, burst=burst, t=t)
                splash(cr, NET_X, gy + 2, burst * (1 - prog(t, 11.0, 12.0) if i == 2 else 1), t, n=10, spread=80)
        darkness(cr, y0, PANEL_H, night)
        if night > 0.05:
            moon(cr, 180, y0 + 110 + 40 * prog(t, 0, 5), r=24)


OUTPUT_NAME = "day31b_great_catch_luke5"
