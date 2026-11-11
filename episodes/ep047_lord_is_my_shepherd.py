import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import *
from props import *

WATER_X = 660
GRASS = [140, 205, 470, 535, 600, 660, 725, 790, 860, 930, 1000]

class LordIsMyShepherd(Episode):
    dur = 18.0
    ground = False
    caption_bg = True
    cta = "Read it in Scroll the Catholic Bible"
    kicker = "PSALM 22 (23)  •  THE LORD IS MY SHEPHERD"
    headline = "Green grass, still water, dark valley.\nThe same Shepherd in all three."
    captions = [
        (cpdv("Psalms", 22, 1, "…The Lord directs me, and nothing will be lacking to me."), "Psalm 22:1", 5.0),
        (cpdv("Psalms", 22, 2, "He has settled me here, in a place of pasture. He has led me out to the water of refreshment."), "Psalm 22:2", 7.0),
        (cpdv("Psalms", 22, 4, "…even if I should walk in the midst of the shadow of death, I will fear no evils. For you are with me…"), "Psalm 22:4", 8.6),
    ]

    def shepherd(self, cr, x, gy, p, face=1, wa=0.0, t=0.0, staff_on=True):
        bp = body(t, p, wa)
        if staff_on: bp["ls"], bp["le"] = 34, 30     # the staff hand stays forward
        J = draw_figure(cr, x, gy, bp, s=1.1, face=face, prop="robe")
        if staff_on:
            hx, hy = J["lhand"]; staff(cr, hx + face * 4, hy - 92, gy)
        return J

    def draw_panel(self, cr, i, t, y0, gy):
        walkp = pose("stand", ls=22, le=12)
        if i == 0:      # ---- green pasture ----
            ground_line(cr, gy)
            g = prog(t, 2.6, 5.0)
            for k, gx in enumerate(GRASS):
                grass_tuft(cr, gx, gy, (10 + 26 * g) * (0.8 + 0.3 * ((k * 5) % 3) / 2), sway=math.sin(t * 1.4 + k))
            sx, swa, _ = track(t, [(0.0, 60), (3.2, 330)])
            lean_on = pose("stand", ls=30, le=10, rs=10, re=20, head=12)
            p = walkp if t < 3.2 else keyed([(3.2, walkp), (3.8, lean_on)], t)
            self.shepherd(cr, sx, gy, p, wa=swa, t=t)
            lx, lwa, _ = track(t, [(0.0, -80), (3.4, 200), (3.6, 200), (5.0, 520)])
            graze = prog(t, 5.2, 5.7) * (0.75 + 0.25 * math.sin(t * 1.5))
            sheep(cr, lx, gy, s=0.95, face=1, step=t * 8 if lwa > 0.1 else 0, graze=graze)
            l2x, l2wa, _ = track(t, [(0.0, -200), (3.4, 90), (3.6, 90), (5.4, 690)])
            sheep(cr, l2x, gy, s=0.8, face=1, step=t * 8 + 1 if l2wa > 0.1 else 0, graze=prog(t, 5.6, 6.1) * (0.8 + 0.2 * math.sin(t * 1.2 + 2)))
            warm_glow(cr, 560, gy - 80, 330, 0.6 * prog(t, 5.0, 7.0))
        elif i == 1:    # ---- still water ----
            ground_line(cr, gy, 0, WATER_X + 10)
            for k, gx in enumerate(GRASS[:4]):
                grass_tuft(cr, gx, gy, 26, sway=math.sin(t * 1.4 + k))
            water(cr, gy + 6, t * 0.3, x0=WATER_X, x1=W + 20, amp=2, rough=0.25, below=60)
            sx, swa, _ = track(t, [(0.0, 60), (3.2, 330), (3.8, 330), (5.6, 520)])
            p = walkp
            if t > 5.6:
                p = keyed([(5.6, walkp), (6.2, pose("stand", ls=30, le=10, rs=60, re=40, head=14))], t)
            self.shepherd(cr, sx, gy, p, wa=swa, t=t)
            lx, lwa, _ = track(t, [(0.0, -80), (3.4, 200), (4.0, 200), (6.2, 615)])
            drink = prog(t, 6.4, 6.9)
            sheep(cr, lx, gy, s=0.95, face=1, step=t * 8 if lwa > 0.1 else 0, graze=drink)
            if t > 6.9:   # ripples where it drinks
                for k in range(3):
                    u = ((t - 6.9) * 0.5 + k / 3.0) % 1.0
                    cr.set_source_rgba(*INK, 0.6 * (1 - u)); cr.set_line_width(2)
                    cr.save(); cr.translate(682, gy + 10); cr.scale(10 + 50 * u, 3 + 8 * u); cr.arc(0, 0, 1, 0, 2 * math.pi); cr.restore(); cr.stroke()
            warm_glow(cr, 640, gy - 60, 300, 0.5 * prog(t, 7.0, 9.0))
        else:           # ---- the dark valley ----
            ground_line(cr, gy)
            cliff(cr, 150, gy, 150, side=-1)
            cliff(cr, 860, gy, 330, side=1)
            sx, swa, d = track(t, [(0.0, 60), (3.2, 330), (4.8, 430), (5.6, 430), (6.0, 415), (7.4, 415), (12.6, 760)])
            face = -1 if 5.4 < t < 7.4 else 1
            reach = pose("reach", rs=60, re=0, ls=60, le=-4, head=16)
            p = walkp
            if 5.4 <= t < 7.4:
                p = keyed([(5.4, walkp), (6.0, reach), (6.9, reach), (7.4, walkp)], t)
            J = self.shepherd(cr, sx, gy, p, face=face, wa=swa, t=t, staff_on=not (5.9 < t < 7.0))
            if 5.9 < t < 7.0:   # the staff reaches back to the frightened sheep
                hx, hy = J["rhand"]
                cr.set_source_rgb(*INK); cr.set_line_width(5); cr.move_to(hx, hy); cr.line_to(hx - 70, gy - 14); cr.stroke()
            lx, lwa, _ = track(t, [(0.0, -80), (3.4, 200), (4.8, 300), (5.4, 270), (6.4, 270), (7.4, 335), (12.6, 670)])
            shake = 3 * math.sin(t * 30) * (prog(t, 5.0, 5.4) - prog(t, 6.6, 7.0))
            sheep(cr, lx + shake, gy, s=0.95, face=1, step=t * 8 if lwa > 0.1 else 0, graze=0.15 if 5.0 < t < 6.8 else 0)
            dark = 0.88 * prog(t, 3.4, 5.4) * (1 - 0.65 * prog(t, 13.0, 15.0))
            darkness(cr, y0, PANEL_H, dark, [(sx + 10, gy - 110, 300, 1.0)])

OUTPUT_NAME = "day24a_lord_is_my_shepherd_psalm22"
