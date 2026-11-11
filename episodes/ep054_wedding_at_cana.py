import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import *
from props import *

GUESTS = [110, 215]
SX = 340                     # steward
JARS = [585, 655, 725]
MX0, JX = 845, 975           # Mary, Jesus

class WeddingAtCana(Episode):
    dur = 18.0
    cta = "Pray it with Ave – Catholic Prayer Lock"
    kicker = "JOHN 2  •  THE WEDDING AT CANA"
    headline = "The wine ran out.\nShe knew who to ask."
    captions = [
        (cpdv("John", 2, 3, "And when the wine was failing, the mother of Jesus said to him, “They have no wine.”"), "John 2:3", 5.0),
        (cpdv("John", 2, 5, "His mother said to the servants, “Do whatever he tells you.”"), "John 2:5", 7.4),
        (cpdv("John", 2, 9, "…the chief steward had tasted the water made into wine…"), "John 2:9", 13.6),
    ]

    def draw_panel(self, cr, i, t, y0, gy):
        wine = prog(t, 12.0, 13.2) if i == 2 else 0.0
        joy = prog(t, 13.8, 14.6) if i == 2 else 0.0
        warm_glow(cr, 655, gy - 60, 260, wine)
        # ---------- jars (filled by the servant in panels 2-3) ----------
        fills = [0.0, 0.0, 0.0]
        if i >= 1:
            for k, ts in enumerate((8.6, 9.6, 10.6)):
                fills[k] = prog(t, ts, ts + 0.7)
        col = tuple(lerp(WATER_C[j], WINE_C[j], wine) for j in range(3))
        for k, jx in enumerate(JARS):
            stone_water_jar(cr, jx, gy, fill=fills[k], fill_color=col)

        # ---------- guests behind the table ----------
        sad = prog(t, 4.0, 5.0) * (1 - joy)
        for k, gx in enumerate(GUESTS):
            sway = math.sin(t * 3 + k * 2)
            toast = pose("stand", rs=120 + 15 * sway, re=-20, head=-8)
            low = pose("stand", rs=30, re=50, head=22, lean=6)
            cheer = pose("stand", rs=150 + 10 * sway, re=0, ls=140, le=10, head=-14)
            p = mix(mix(toast, low, sad), cheer, joy)
            J = draw_figure(cr, gx, gy, p, s=0.95, face=1 if k == 0 else -1)
            wine_goblet(cr, J["rhand"][0], J["rhand"][1] + 4, s=0.9, wine=joy)
        feast_table(cr, 50, 285, gy)

        # ---------- steward: pours, the jug is empty ----------
        sface = -1
        pour = pose("stand", rs=80, re=-10, lean=8)
        dismay = pose("stand", rs=60, re=-60, ls=55, le=-60, head=20)
        sp = keyed([(1.6, pose("stand", rs=45, re=-10)), (2.3, pour), (3.6, pour), (4.3, dismay)], t)
        tilt = 40 * prog(t, 2.3, 2.8) + 70 * prog(t, 3.0, 3.4) + (8 * math.sin(t * 25) if 3.4 < t < 3.9 else 0)
        jug_on = True
        cup = None
        if i == 2 and t >= 12.6:
            sface = 1
            taste = pose("stand", rs=40, re=120, head=-14, lean=-4)
            sp = keyed([(12.6, dismay), (13.0, pose("stand", rs=70, re=-10)), (13.4, pose("stand", rs=70, re=-10)), (13.9, taste),
                        (14.4, pose("joy", rs=150, re=0))], t)
            jug_on = False
            if t >= 13.1: cup = "steward"
        SJ = draw_figure(cr, SX, gy, sp, s=1.0, face=sface)
        if jug_on:
            watering_jug(cr, SJ["rhand"][0], SJ["rhand"][1] - 6, tilt=tilt if t < 4.0 else 0, face=-1)
        else:
            watering_jug(cr, SX - 40, gy - 38, face=-1)

        # ---------- servant ----------
        vkeys = [(0, 470)]
        if i >= 1:
            vkeys = [(7.8, 470), (8.4, 545), (9.3, 545), (9.6, 615), (10.3, 615), (10.6, 685)]
            if i == 2: vkeys += [(11.6, 685), (12.8, 420)]
        vx, vwa, vd = track(t, vkeys)
        vface = 1
        vp = pose("stand", rs=25, re=30)
        pouring = i >= 1 and any(ts - 0.1 < t < ts + 0.75 for ts in (8.6, 9.6, 10.6))
        if i >= 1 and 8.2 < t < 11.4:
            vp = pose("stand", rs=70, re=-10, lean=6)
        if i == 2 and t >= 11.3:
            vp = keyed([(11.3, pose("stand", lean=30, head=25, rs=70, re=0)), (11.7, pose("stand", rs=70, re=-10))], t)
            if t >= 11.6: vface = -1
            if t >= 12.8: vp = keyed([(12.8, pose("stand", rs=70, re=-10)), (13.2, pose("stand", rs=20, re=10))], t)
            if 11.5 <= t < 13.1: cup = "servant"
        VJ = draw_figure(cr, vx, gy, body(t, vp, vwa), s=0.95, face=vface)
        if i >= 1 and 8.0 < t < 11.4:
            tip = watering_jug(cr, VJ["rhand"][0], VJ["rhand"][1] - 6, tilt=60 if pouring else 0, face=1)
            if pouring: pour_drops(cr, tip[0], tip[1], gy - 40, t, drift=4)
        if cup == "servant":
            wine_goblet(cr, VJ["rhand"][0], VJ["rhand"][1] + 4, s=0.9, wine=wine)
        elif cup == "steward":
            wine_goblet(cr, SJ["rhand"][0], SJ["rhand"][1] + 4, s=0.9, wine=1.0)

        # ---------- Jesus and Mary ----------
        jp = pose("stand", head=6)
        if i >= 1:
            jp = keyed([(7.9, pose("stand", head=6)), (8.4, pose("stand", rs=95, re=-5)), (11.2, pose("stand", rs=95, re=-5)), (11.8, pose("stand", head=4))], t)
        draw_figure(cr, JX, gy, jp, s=1.05, face=-1, prop="robe")
        mx, mwa, _ = track(t, [(4.0, MX0), (4.6, 885)] + ([(6.2, 885), (6.9, 810)] if i >= 1 else []))
        mface = -1
        mp = pose("stand", head=8)
        if t >= 3.9:
            mface = 1
            mp = keyed([(4.6, pose("stand")), (5.0, pose("stand", rs=65, re=-10, head=-6))], t)
        if i >= 1 and t >= 6.1:
            mface = -1
            mp = keyed([(6.1, pose("stand")), (6.9, pose("stand")), (7.3, pose("stand", rs=75, re=-5, head=-4)), (8.6, pose("stand", rs=75, re=-5)), (9.2, pose("stand", head=6))], t)
        MJ = draw_figure(cr, mx, gy, body(t, mp, mwa), s=0.95, face=mface, prop="robe")
        veil_drape(cr, MJ, s=0.95, face=mface)

OUTPUT_NAME = "day27b_wedding_at_cana_john2"
