import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import *
from props import *

ROCK = (650, 1110, 40, 60)          # x0, x1, height, slope
SAND_HX, ROCK_HX = 430, 875         # house centres

class TwoBuilders(Episode):
    dur = 18.0
    ground = False
    caption_bg = True
    cta = "Read it in Scroll the Catholic Bible"
    kicker = "MATTHEW 7  •  THE TWO BUILDERS"
    headline = "Same rain. Same storm.\nOnly one house stood."
    captions = [
        (cpdv("Matthew", 7, 26, "…a foolish man, who built his house upon the sand."), "Matthew 7:26", 9.8),
        (cpdv("Matthew", 7, 27, "…and the winds blew, and rushed upon that house, and it did fall, and great was its ruin."), "Matthew 7:27", 11.4),
        (cpdv("Matthew", 7, 25, "…but it did not fall, for it was founded on the rock."), "Matthew 7:25", 12.8),
    ]

    def draw_panel(self, cr, i, t, y0, gy):
        x0, x1, rh, sl = ROCK
        storm = prog(t, 7.0, 8.0) * (1 - prog(t, 12.2, 13.2))
        # sun after the storm (behind everything)
        su = prog(t, 12.8, 14.4)
        if su > 0:
            sun(cr, 1010, lerp(gy + 60, y0 + 150, su))
            cr.set_source_rgb(*BG); cr.rectangle(0, gy + 2, W, 200); cr.fill()
        ground_line(cr, gy, 0, x0 + 10)
        sand(cr, 140, 640, gy)

        # ---------- builder ----------
        hammer = lambda tt: pose("knock_up") if math.sin(tt * 18) > 0 else pose("knock_hit")
        fig_after_house = True
        if i < 2:
            hx = SAND_HX
            built = prog(t, 1.9, 4.7)
            if t < 1.9:
                x, wa, _ = track(t, [(0.2, -60), (1.7, 300)]); p = body(t, pose("stand"), wa); face = 1
            elif t < 4.7:
                x, wa, face = 300, 0, 1; p = hammer(t)
            elif i == 0:   # relaxes, wakes in the storm, steps back from the fall
                x, wa, _ = track(t, [(4.9, 300), (5.7, 250), (9.0, 250), (9.8, 150)])
                relax = pose("sad_sit", lean=-14, head=-12, ls=-35, le=0, rs=-35, re=0)
                p = keyed([(5.7, pose("stand")), (6.4, relax), (7.6, relax), (8.2, pose("stand", head=-20)),
                           (9.8, pose("stand", head=-10)), (10.4, pose("head_hands"))], t)
                p = body(t, p, wa); face = -1 if 5.0 < t < 7.9 else 1
            else:          # braces the wall with both hands, then the house goes anyway
                x, wa, _ = track(t, [(4.9, 300), (7.6, 300), (8.1, 330), (10.6, 330), (11.2, 200)])
                brace = pose("reach", lean=22, rs=85, re=-5, ls=80, le=0, lt=-14, rt=-30)
                p = keyed([(4.9, pose("stand", head=-15)), (7.6, pose("stand", head=-15)), (8.1, brace),
                           (10.6, brace), (11.1, pose("stand", head=-20)), (11.9, pose("kneel", lean=45, head=40, rs=20, re=10, ls=20, le=10))], t)
                p = body(t, p, wa); face = 1
                if 10.6 < t < 11.2: face = -1
            # house on sand: sinks, leans, collapses
            if i == 0:
                tilt = -7 * prog(t, 8.4, 9.4); sink = 14 * prog(t, 8.2, 9.4); col = prog(t, 9.4, 10.7)
            else:
                wob = math.sin(t * 7) * 2.5 * prog(t, 8.0, 8.6)
                tilt = wob + 6 * prog(t, 9.6, 10.6); sink = 16 * prog(t, 8.4, 10.6); col = prog(t, 10.6, 11.9)
            gyf = gy
            draw_figure(cr, x, gyf, p, s=1.0, face=face)
            small_house(cr, hx, gy, built=built, tilt=tilt, sink=sink, collapse=col)
            if i == 1 and 8.1 < t < 10.6:   # draw the bracing man on top so his hands stay visible
                draw_figure(cr, x, gyf, p, s=1.0, face=face)
            light = 0
        else:              # tests the sand, walks on to the rock, builds there
            built = prog(t, 5.3, 7.3)
            x, wa, _ = track(t, [(0.2, -60), (1.7, 300), (2.0, 330), (3.6, 330), (5.1, 760), (8.0, 760), (8.6, 840), (12.9, 840), (13.7, 740)])
            gyf = rock_y(x, x0, x1, gy, rh, sl)
            test = pose("kneel", lean=40, head=30, rs=60, re=-10, ls=40, le=20)
            p = keyed([(1.9, pose("stand")), (2.4, test), (2.9, test), (3.2, pose("stand", rs=50, re=40, head=0)), (3.6, pose("stand"))], t)
            if 3.0 < t < 3.6:
                p["head"] = 14 * math.sin(t * 16)
            if 5.1 <= t < 7.3:
                p = hammer(t)
            if t >= 13.6:
                p = keyed([(13.6, pose("stand", head=-10)), (14.3, pose("joy"))], t)
            p = body(t, p, wa); face = 1 if t < 13.0 else -1
            if 2.8 < t < 3.6:   # sand runs out of his hand
                for k in range(6):
                    u = ((t - 2.8) * 2.2 + k / 6.0) % 1.0
                    seed_dot(cr, 330 + 46 + k % 3 * 3, gy - 60 + u * 60, r=2.4)
            light = prog(t, 8.6, 9.2) * (1 - prog(t, 13.2, 14.0))
            cr.save()   # walking in through the door: only the part left of the wall shows
            cr.rectangle(0, y0, ROCK_HX - HOUSE_W / 2 - 14, PANEL_H); cr.clip()
            draw_figure(cr, x, gyf, p, s=1.0, face=face); cr.restore()

        # ---------- flood, rock, rock house ----------
        rise = prog(t, 7.8, 10.0) * (1 - prog(t, 12.0, 13.4))
        if rise > 0.02:
            water(cr, gy + 6 - 34 * rise, t, x0=0, x1=x0 + 40, rough=0.6 + storm, below=60)
        rock_mound(cr, x0, x1, gy, rh, sl)
        rb = gy - rh
        small_house(cr, ROCK_HX, rb, built=1.0 if i < 2 else built, light=light if i == 2 else 0)
        rain(cr, y0, PANEL_H, t, storm)
        wind(cr, y0, t, storm)
        lights = [(ROCK_HX - HOUSE_W / 2 + 38, rb - 30, 230, light)] if i == 2 else []
        darkness(cr, y0, PANEL_H, 0.6 * storm, lights)

OUTPUT_NAME = "day08a_two_builders_matthew7"
