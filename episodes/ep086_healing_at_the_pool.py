import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import *
from props import *

CROWD = (0.50, 0.48, 0.45)
PE = 640              # pool edge (water to the right)
WD = 18               # water surface below the paving
MAT = (232, 430)      # the man's mat
FX = 244              # his feet (he lies with his head toward the pool)
JX = 104              # where Jesus stops
BATHERS = [(520, 712, 3.0), (575, 812, 3.25)]     # (seat x, spot in the pool x, start time)


def stir(t):
    return prog(t, 2.6, 3.2) * (1 - prog(t, 5.4, 7.0))


def lying(t, head=0.0, reach=0.0):
    """On his back, face up (drawn rotated 90 with face=-1)."""
    return pose("lie", ls=10, le=6, rs=lerp(8, 172, reach), re=lerp(4, -10, reach), head=head)


def crawl_pose(t, amt=1.0):
    k = math.sin(t * 5.0) * amt
    return dict(lean=0, head=-18, lt=4, lk=0, rt=-6, rk=14,
                ls=lerp(10, 168 - 14 * k, amt), le=lerp(6, 8, amt), rs=lerp(10, 168 + 14 * k, amt), re=lerp(6, 8, amt))


class HealingAtThePool(Episode):
    dur = 18.0
    ground = False
    cta = "Pray it with Ave – Catholic Prayer Lock"
    kicker = "JOHN 5  •  THE HEALING AT THE POOL"
    headline = "Thirty-eight years by the pool.\nThen Jesus walked over."
    captions = [
        (cpdv("John", 5, 5, "And there was a certain man in that place, having been in his infirmity for thirty-eight years."), "John 5:5", 6.0),
        (cpdv("John", 5, 7, "…“Lord, I do not have any man to put me in the pool…as I am going, another descends ahead of me.”"), "John 5:7", 6.6),
        (cpdv("John", 5, 8, "Jesus said to him, “Rise, take up your stretcher, and walk.”"), "John 5:8", 9.2),
    ]

    def draw_panel(self, cr, i, t, y0, gy):
        colonnade(cr, 70, 1010, gy, h=170, n=5)
        ground_line(cr, gy, 0, PE)
        cr.set_source_rgb(*INK); cr.set_line_width(4); cr.move_to(PE, gy); cr.line_to(PE, gy + 70); cr.stroke()
        pool_steps(cr, PE, gy, n=3, step=18, rise=14)
        st = stir(t)
        warm_glow(cr, 850, gy + WD - 10, 260, 0.75 * st)

        # ---------- bathers: wait at the edge, then hurry down into the stirred water ----------
        in_water = []
        for k, (sx, px, t0) in enumerate(BATHERS):
            down = prog(t, t0 + 0.9, t0 + 1.6)
            if t < t0:
                continue
            x, wa, _ = track(t, [(t0, sx), (t0 + 0.9, PE + 10), (t0 + 1.6, px)])
            in_water.append((x, gy + 76 * down, body(t, pose("stand", rs=40 + 20 * down, re=30, head=6 * k), wa, speed=2.0), k))
        late = None
        if i == 1 and t > 4.4:      # the one who always gets there first
            x, wa, _ = track(t, [(4.4, -70), (5.9, PE + 6), (6.5, 760)])
            down = prog(t, 5.9, 6.5)
            p = mix(run(t, speed=1.8), pose("stand", rs=60, re=20), max(down, 1 - wa))
            if down > 0:
                in_water.append((x, gy + 76 * down, p, 2))
            else:
                late = (x, p)
        for (x, yb, p, k) in in_water:
            draw_figure(cr, x, yb, p, s=0.85, face=1, color=CROWD)

        water(cr, gy + WD, t, x0=PE, x1=W + 20, amp=4 + 3 * st, rough=0.4 + 1.4 * st, below=60)
        for k, (sx, px, t0) in enumerate(BATHERS):
            splash(cr, px, gy + WD, prog(t, t0 + 1.3, t0 + 1.5) * (1 - prog(t, t0 + 1.8, t0 + 2.4)), t, n=6, seed=k + 2)
        if i == 1:
            splash(cr, 760, gy + WD, prog(t, 6.2, 6.4) * (1 - prog(t, 6.7, 7.3)), t, n=7, seed=9)

        # bathers still waiting at the edge
        for k, (sx, px, t0) in enumerate(BATHERS):
            if t < t0:
                p = ground_sit_pose(lean=10, head=10 + 4 * k, rs=40, re=40, ls=30, le=40)
                if t > t0 - 0.5:
                    p = mix(p, pose("stand"), prog(t, t0 - 0.5, t0))
                draw_figure(cr, sx, gy, p, s=0.85, face=1, color=CROWD)

        # ---------- the man ----------
        if i == 0:
            self.waits(cr, t, gy)
        elif i == 1:
            self.crawls(cr, t, gy)
        else:
            self.rises(cr, t, gy)

        if late:
            draw_figure(cr, late[0], gy, late[1], s=0.85, face=1, color=CROWD)

    # panel 1: he lifts his head, watches the others go in, and lies back down
    def waits(self, cr, t, gy):
        sleeping_mat(cr, *MAT, gy, h=9)
        hd = keyed([(0, {"h": 0, "r": 0}), (3.0, {"h": 0, "r": 0}), (3.6, {"h": 34, "r": 0.55}), (5.0, {"h": 34, "r": 0.55}),
                    (5.8, {"h": 0, "r": 0}), (6.4, {"h": -4, "r": 0})], t)
        p = lying(t, head=hd["h"], reach=hd["r"])
        if t > 6.4:   # an arm over his eyes
            u = prog(t, 6.4, 7.2); p["ls"] = lerp(10, 160, u); p["le"] = lerp(6, 40, u)
        draw_rotated(cr, FX, gy - 9, 90, p, s=0.9, face=-1)

    # panel 2: he drags himself toward the water, and someone else steps in first
    def crawls(self, cr, t, gy):
        sleeping_mat(cr, *MAT, gy, h=9)
        if t < 3.4:
            hd = prog(t, 3.0, 3.4)
            draw_rotated(cr, FX, gy - 9, 90, lying(t, head=34 * hd, reach=0.55 * hd), s=0.9, face=-1)
            return
        # rolls over (3.4-3.9), then drags himself forward (3.9-6.3)
        x = keyed([(3.9, {"x": FX}), (6.3, {"x": 432})], t)["x"]
        amt = prog(t, 3.6, 4.0) * (1 - prog(t, 6.2, 6.6))
        p = crawl_pose(t, amt)
        rot = keyed([(3.9, {"r": 90}), (4.2, {"r": 78}), (6.3, {"r": 78}), (6.9, {"r": 88})], t)["r"]
        if t > 6.6:   # he lays his head down on his arms
            u = prog(t, 6.6, 7.4)
            p["head"] = lerp(-18, 6, u); p["ls"] = p["rs"] = lerp(p["rs"], 170, u); p["le"] = p["re"] = lerp(8, 4, u)
        lift = 0 if x < 300 else 0
        draw_rotated(cr, x, gy - 3, rot, p, s=0.9, face=1, lift=lift)

    # panel 3: Jesus comes to him; he rises, takes up his mat, and walks
    def rises(self, cr, t, gy):
        jx, jwa, _ = track(t, [(5.6, -80), (8.0, JX)])
        jp = keyed([(8.0, pose("stand", head=14)), (8.6, pose("stand", head=18)),
                    (9.2, pose("reach", rs=78, re=-8, head=16)), (11.2, pose("reach", rs=78, re=-8, head=10)),
                    (12.0, pose("stand", rs=30, re=10, head=0))], t)
        draw_figure(cr, jx, gy, body(t, jp, jwa), s=0.98, face=1, prop="robe")

        hd = keyed([(0, {"h": 0, "r": 0}), (3.0, {"h": 0, "r": 0}), (3.6, {"h": 34, "r": 0.55}), (5.0, {"h": 34, "r": 0.55}),
                    (5.8, {"h": 0, "r": 0}), (8.0, {"h": 0, "r": 0}), (8.6, {"h": 30, "r": 0})], t)
        if t < 9.8:
            sleeping_mat(cr, *MAT, gy, h=9)
            draw_rotated(cr, FX, gy - 9, 90, lying(t, head=hd["h"], reach=hd["r"]), s=0.9, face=-1)
            return
        if t < 11.2:
            sleeping_mat(cr, *MAT, gy, h=9)
            u = prog(t, 9.8, 10.8)
            p = mix(lying(t, head=30), pose("stand", head=-6), u)
            draw_rotated(cr, FX, gy - 9 * (1 - u), 90 * (1 - u), p, s=0.9, face=-1)
            return
        # standing: turns to his mat, stoops, rolls it up and lifts it, then walks
        stoop = pose("stand", lean=36, head=22, rs=60, re=10, ls=55, le=10, lt=20, lk=30, rt=10, rk=30)
        carry = pose("stand", rs=14, re=50, ls=12, le=54, head=-6)
        joy = pose("joy", head=-14)
        p = keyed([(11.2, pose("stand", head=-6)), (11.6, stoop), (12.2, stoop), (12.9, joy), (13.6, joy), (14.0, carry)], t)
        face = 1
        x = FX + 40 * prog(t, 11.2, 11.6)
        if t > 14.0:
            face = 1
            x, wa, _ = track(t, [(14.0, FX + 40), (15.4, FX + 170)])
            p = body(t, carry, wa, speed=1.4)
            for k_ in ("rs", "re", "ls", "le"):
                p[k_] = carry[k_]
        if t < 12.2:
            sleeping_mat(cr, MAT[0] + 60 * prog(t, 11.2, 12.0), MAT[1], gy, h=9)
        J = draw_figure(cr, x, gy, p, s=0.9, face=face)
        if t >= 12.2:
            hx = (J["rhand"][0] + J["lhand"][0]) / 2; hy = min(J["rhand"][1], J["lhand"][1])
            u = prog(t, 13.6, 14.0)        # from overhead down to under his arm
            hx = lerp(hx, J["hip"][0] + 4, u); hy = lerp(hy - 4, J["hip"][1] - 26, u)
            rolled_mat(cr, hx, hy, ang=lerp(0, -12, u), L=lerp(110, 72, prog(t, 12.2, 12.9)))


OUTPUT_NAME = "day43b_healing_at_the_pool_john5"
