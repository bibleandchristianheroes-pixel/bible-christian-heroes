import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import *
from props import *

WELL = 600      # well centre
JX = 830        # Jesus, seated on a stone, facing left
STOP = 480      # where the woman stops at the well
SUNX = 990
CITY_X, CITY_S = -175, 1.15
CITY_TOWER_L = CITY_X + 205 * CITY_S     # left edge of the tall right tower

walk_jar = pose("carry", rs=30, re=78)                       # jar held at the hip
lean_draw = pose("stand", lean=26, head=22, rs=70, re=10, ls=62, le=12)
drink = pose("stand", head=-14, lean=-4, rs=118, re=-50, ls=110, le=-45)
offer = pose("stand", lean=10, head=-4, rs=82, re=-6, ls=74, le=-4)
hold_low = pose("stand", head=-4, rs=30, re=78)
wonder = pose("stand", head=-14, lean=-5, rs=40, re=95, ls=38, le=98)   # hands to the heart


class WomanAtTheWell(Episode):
    dur = 18.0
    cta = "Read it in Scroll the Catholic Bible"
    kicker = "JOHN 4  •  THE WOMAN AT THE WELL"
    headline = "Same well. Same thirst.\nOnly one left her jar behind."
    captions = [
        (cpdv("John", 4, 13, "…“All who drink from this water will thirst again…"), "John 4:13", 7.8),
        (cpdv("John", 4, 14, "…the water that I will give to him will become in him a fountain of water, springing up into eternal life.”"), "John 4:14", 9.6),
        (cpdv("John", 4, 28, "And so the woman left behind her water jar and went into the city…"), "John 4:28", 11.2),
    ]

    def draw_panel(self, cr, i, t, y0, gy):
        sun(cr, SUNX, gy - 300, r=24, rays=10)
        gate = 30          # a spot hidden behind the city's tall right tower (city is drawn last)

        # ---------------- the woman: path and pose ----------------
        if i == 0:
            wx, wa, wd = track(t, [(0.4, gate - 10), (3.4, STOP), (8.4, STOP), (11.0, gate + 20), (11.6, gate + 20), (14.6, STOP - 20)])
        elif i == 1:
            wx, wa, wd = track(t, [(0.4, gate - 10), (3.4, STOP), (7.0, STOP), (8.4, JX - 100)])
        else:
            wx, wa, wd = track(t, [(0.4, gate - 10), (3.4, STOP), (7.0, STOP), (8.4, JX - 100), (11.2, JX - 100), (13.4, gate + 155)])
        wface = wd if wa > 0.05 else (1 if (i or t < 8.4) else -1)
        if i == 0 and t > 11.0: wface = 1

        keys = [(3.4, walk_jar), (4.2, pose("carry", rs=30, re=78, head=8)), (5.0, pose("carry", rs=30, re=78, head=8))]
        if i == 0:
            keys += [(5.6, pose("carry", rs=30, re=78, head=-14, lean=-4)), (6.0, lean_draw), (7.0, lean_draw),
                     (7.4, hold_low), (7.8, drink), (8.4, hold_low)]
            if t > 11.6:  # back again, tired and thirsty
                keys = [(11.6, pose("carry", rs=30, re=78, head=26, lean=12)), (15.0, pose("carry", rs=30, re=78, head=30, lean=14))]
        else:
            keys += [(5.6, lean_draw), (6.6, lean_draw), (7.0, hold_low), (8.4, hold_low), (8.9, offer), (9.4, offer), (10.0, wonder)]
            if i == 2:
                keys += [(10.6, wonder), (11.1, pose("stand", lean=34, head=24, rs=60, re=20, ls=55, le=20)), (11.4, pose("stand", head=-8))]
        p = keyed(keys, t)
        running = i == 2 and 11.4 < t < 13.4
        if running:
            p = mix(pose("joy"), run(t, speed=2.2), 0.75)
        elif wa > 0.05:
            p = body(t, p, wa, speed=1.3 if not (i == 0 and t > 11) else 1.0)
        if i == 2 and t > 13.4:
            p = keyed([(13.4, pose("joy", head=-24)), (14.2, pose("stand", rs=95, re=-10, head=-6))], t)

        # ---------------- the jar ----------------
        # jar position is resolved after the figure is drawn (it hangs from the hand), but a jar
        # dipping into the well must be drawn before the well so the drum hides it.
        dip = 0.0
        if 5.6 < t < 7.0 and (i or t < 8.4):
            dip = prog(t, 5.7, 6.2) * (1 - prog(t, 6.4, 6.9))
        jar_in_well = dip > 0.02
        if jar_in_well:
            hx = STOP + 78; top = gy - 66
            jy = lerp(top - 18, top + 34, dip)
            water_jar(cr, hx + 20, jy, s=0.9)
        stone_well(cr, WELL, gy)
        stone_seat(cr, JX + 8, gy)

        # ---------------- Jesus ----------------
        seated = sit_pose(head=6, rs=35, re=40, ls=30, le=45)
        ask = sit_pose(head=-2, rs=78, re=-8, ls=30, le=45)
        jkeys = [(3.4, seated), (4.0, sit_pose(head=-2, rs=35, re=40, ls=30, le=45)), (4.4, ask), (5.6, ask)]
        if i == 0:
            jkeys += [(6.4, sit_pose(head=10, rs=35, re=40, ls=30, le=45)), (12.0, sit_pose(head=10, rs=35, re=40, ls=30, le=45)),
                      (12.8, sit_pose(head=-2, rs=35, re=40, ls=30, le=45))]
        else:
            jkeys += [(8.4, ask), (8.9, sit_pose(head=-6, rs=96, re=-30, ls=30, le=45)), (9.4, sit_pose(head=-6, rs=96, re=-30, ls=30, le=45)),
                      (10.0, sit_pose(head=-4, rs=72, re=-4, ls=62, le=-6))]
            if i == 2:
                jkeys += [(12.0, sit_pose(head=-4, rs=72, re=-4, ls=62, le=-6)), (12.8, sit_pose(head=-10, rs=35, re=40, ls=30, le=45))]
        draw_figure(cr, JX, gy, keyed(jkeys, t), s=1.0, face=-1, prop="robe")

        if i == 2:
            warm_glow(cr, wx, gy - 120, 140, prog(t, 11.4, 12.2) * 0.8)

        # ---------------- the woman ----------------
        cr.save(); cr.rectangle(CITY_TOWER_L, y0, W, PANEL_H); cr.clip()   # hidden while "in the city"
        if i == 0 and t > 11.6:
            heat_waves(cr, wx + 10, gy - 215, t, prog(t, 12.0, 13.0))
        WJ = draw_figure(cr, wx, gy, p, s=0.92, face=wface, prop="robe")
        veil_drape(cr, WJ, s=0.92, face=wface)

        if jar_in_well:     # rope from her hands down into the well
            cr.set_source_rgb(*INK); cr.set_line_width(2.5)
            cr.move_to(*WJ["rhand"]); cr.line_to(STOP + 98, gy - 72); cr.stroke()

        # living water springing up within her (panels 2-3)
        if i >= 1:
            amt = prog(t, 9.4, 10.4) * (1 - (prog(t, 11.4, 12.2) if i == 2 else 0))
            sx, sy = WJ["sh"]
            living_water(cr, sx, sy + 14, amt, t, n=20, h=120, spread=55)

        # jar in hand / on the ground
        if not jar_in_well:
            hx, hy = WJ["rhand"]
            if i == 2 and t > 11.1:
                water_jar(cr, JX - 140, gy - 22, s=0.9)                  # left behind
            elif (7.6 < t < 8.3) and i == 0:
                water_jar(cr, hx + wface * 4, hy - 8, s=0.9, tilt=wface * -120)   # drinking
            elif 8.6 < t < 9.6 and i >= 1:
                water_jar(cr, hx - 6, hy + 4, s=0.9, tilt=-35)              # offered to him
            else:
                water_jar(cr, hx + wface * 2, hy + 14, s=0.9, tilt=0)

        # townspeople come out of the gate (panel 3)
        if i == 2:
            for k, t0 in enumerate((13.8, 14.3)):
                if t > t0:
                    px, pa, _ = track(t, [(t0, gate), (t0 + 2.6, gate + 290 - 55 * k)])
                    draw_figure(cr, px, gy, body(t + k, pose("stand", head=-6), pa, speed=1.3), s=0.94 - 0.04 * k, face=1)

        cr.restore()
        city_skyline(cr, CITY_X, gy, s=CITY_S)


OUTPUT_NAME = "day30a_woman_at_the_well_john4"
