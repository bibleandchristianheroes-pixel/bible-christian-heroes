import math, random, sys
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.dirname(__import__("os").path.abspath(__file__))))
from engine import *

class Sower(Episode):
    dur = 18.0
    kicker = "MATTHEW 13  •  THE SOWER"
    headline = "Same seed. Same sower.\nThree different endings."
    captions = [
        (cpdv("Matthew", 13, 4, "…some fell beside the road, and the birds of the air came and ate it."), "Matthew 13:4", 6.2),
        (cpdv("Matthew", 13, 6, "…because they had no roots, they withered."), "Matthew 13:6", 10.2),
        (cpdv("Matthew", 13, 8, "…some others fell upon good soil, and they produced fruit…"), "Matthew 13:8", 13.0),
    ]

    def __init__(self):
        rng = random.Random(7)
        self.seeds = []  # (release_t, land_x, land_t, peak)
        for rel in (2.95, 3.95):
            for k in range(7):
                lx = 330 + k * 72 + rng.uniform(-18, 18) + (36 if rel > 3 else 0)
                self.seeds.append((rel + rng.uniform(0, 0.08), lx, rel + 0.75 + rng.uniform(0, 0.25), rng.uniform(90, 140)))
        self.seeds.sort(key=lambda s: s[1])
        self.rocks = [(r.uniform(300, 880), r.uniform(10, 22)) for r in [random.Random(11)] for _ in range(9)]
        self.walk_x = lambda t: lerp(-60, 190, prog(t, 0.3, 2.2))

    # ---- sower pose per panel ----
    def sower_pose(self, i, t):
        if t < 2.2:
            return mix(walk(t), pose("stand"), prog(t, 1.9, 2.2))
        if t < 4.5:
            keys = [(2.2, pose("stand")), (2.5, pose("sow_back")), (2.95, pose("sow_fwd")),
                    (3.45, pose("sow_back")), (3.95, pose("sow_fwd")), (4.5, pose("look"))]
            return keyed(keys, t)
        if i == 0:
            return keyed([(4.5, pose("look")), (8.6, pose("look")), (9.6, pose("sad_sit"))], t)
        if i == 1:
            return keyed([(4.5, pose("look")), (10.8, pose("look")), (11.6, pose("head_hands"))], t)
        return keyed([(4.5, pose("look")), (13.9, pose("look")), (14.7, pose("joy"))], t)

    def seed_pos(self, s, t, gy, hand):
        rel, lx, lt, peak = s
        if t < rel: return None
        if t >= lt: return (lx, gy - 3)
        u = (t - rel) / (lt - rel)
        x = lerp(hand[0], lx, u)
        y = lerp(hand[1], gy - 3, u) - peak * 4 * u * (1 - u)
        return (x, y)

    def draw_panel(self, cr, i, t, y0, gy):
        # sun (same for all three panels)
        su = prog(t, 7.4, 9.6)
        if su > 0:
            sun(cr, 905, lerp(gy + 45, y0 + 125, su))
            cr.set_source_rgb(*BG); cr.rectangle(0, gy + 2, W, 200); cr.fill()
        # ground dressing
        if i == 0:   # road: paving stones under the surface
            cr.set_source_rgb(*INK); cr.set_line_width(2.5)
            for k in range(11):
                x = 280 + k * 60
                cr.rectangle(x, gy + 8, 50, 16); cr.stroke()
                cr.rectangle(x + 28, gy + 30, 50, 16); cr.stroke()
        elif i == 1:  # rocky
            cr.set_source_rgb(*INK)
            for (rx, rr) in self.rocks:
                cr.save(); cr.translate(rx, gy); cr.scale(rr, rr * 0.55)
                cr.arc(0, 0, 1, math.pi, 2 * math.pi); cr.restore(); cr.fill()
            for k in range(30):
                cr.arc(300 + k * 20, gy + 14 + (k * 7) % 22, 2.2, 0, 2 * math.pi); cr.fill()
        else:        # good soil: furrows + soil dots
            cr.set_source_rgb(*INK); cr.set_line_width(2.5)
            for k in range(9):
                x = 300 + k * 66; cr.move_to(x, gy); cr.curve_to(x + 12, gy - 9, x + 40, gy - 9, x + 52, gy); cr.stroke()
            for k in range(60):
                cr.arc(290 + (k * 97) % 620, gy + 10 + (k * 29) % 44, 1.6, 0, 2 * math.pi); cr.fill()

        # plants / seeds
        for j, s in enumerate(self.seeds):
            lx = s[1]
            if i == 0:
                gone = 6.6 + abs(j - 6.5) * 0.11
                if t > gone: continue
            elif i == 1:
                if t > s[2] + 0.2:
                    h = 26 * prog(t, 4.9 + j * 0.03, 5.9 + j * 0.03)
                    sprout(cr, lx, gy, h, wither=prog(t, 9.8 + j * 0.04, 11.8 + j * 0.04))
                    if h > 1: continue
            else:
                if t > s[2] + 0.2:
                    g1 = 22 * prog(t, 5.4 + j * 0.04, 8.0 + j * 0.04)
                    grow = prog(t, 9.0 + j * 0.05, 13.6 + j * 0.05)
                    if grow <= 0.02:
                        sprout(cr, lx, gy, g1)
                    else:
                        hgt = lerp(22, 140 + (j * 29) % 45, grow)
                        sw = math.sin(t * 1.6 + j) * grow
                        wheat(cr, lx, gy, hgt, sway=sw, grain=prog(t, 11.8 + j * 0.04, 14.0 + j * 0.04))
                    if g1 > 1: continue
            # seed itself (falling or resting)
            hand = (self.walk_x(t) + 40, gy - 135)
            p = self.seed_pos(s, t, gy, hand)
            if p: seed_dot(cr, *p)

        # birds (panel 1)
        if i == 0:
            for b, (lx, delay) in enumerate(((self.seeds[3][1], 0.0), (self.seeds[10][1], 0.35))):
                t0 = 5.2 + delay
                if t < t0: continue
                if t < t0 + 1.2:
                    u = prog(t, t0, t0 + 1.2)
                    x = lerp(1160, lx + 10, u); y = lerp(y0 + 90, gy - 12, u) - 40 * math.sin(math.pi * u)
                    bird(cr, x, y, math.sin(t * 22), s=1.6, face=-1)
                elif t < 8.2 + delay:
                    peck = abs(math.sin((t - t0) * 7)) * 0.5
                    cr.save(); cr.translate(lx + 10, gy - 12); cr.rotate(-peck * 0.7)
                    bird(cr, 0, 0, -0.3, s=1.6, face=-1); cr.restore()
                    # walk slightly while pecking
                elif t < 9.6 + delay:
                    u = prog(t, 8.2 + delay, 9.6 + delay)
                    x = lerp(lx + 10, lx + 380, u); y = lerp(gy - 12, y0 - 40, u)
                    bird(cr, x, y, math.sin(t * 24), s=1.6, face=1)

        # sower
        p = self.sower_pose(i, t)
        draw_figure(cr, self.walk_x(t), gy, p, s=1.05, prop="bag")

OUTPUT_NAME = "day01a_sower_matthew13"
