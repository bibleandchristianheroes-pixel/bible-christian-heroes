import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import *
from props import *

BANK = 600          # the Jordan starts here (water to the right)
TX = 260            # the tree being cut
MX = 400            # the woodcutter, facing the tree (left)
EDGE = 548          # where he stands at the water's edge
EX0, EX = 80, 400   # Elisha: where he waits, where he comes to
SINK = 800          # where the iron falls in
S_AMP, S_ROUGH = 5, 0.8
WD = 18              # the river surface sits a little below the bank

back = pose("stand", rs=210, re=-20, ls=220, le=-26, lean=-6, head=-6)      # axe swung up behind
fwd = pose("stand", rs=70, re=-8, ls=66, le=-4, lean=26, head=12, lt=14, lk=16)                   # blade in the trunk
hold = pose("stand", rs=30, re=20)
look = pose("stand", rs=30, re=20, head=12)
alas = pose("head_hands")
slump = pose("stand", head=34, lean=10, rs=6, re=8, ls=4, le=8)
call = pose("reach", rs=110, re=-6, lean=4, head=-6)                            # "Alas, my lord!"
point = pose("reach", rs=96, re=-4, lean=6, head=6)
wonder = pose("stand", rs=130, re=10, ls=120, le=14, head=-8, lean=-4)
kneel_r = pose("kneel", lean=40, head=24, rs=96, re=6, ls=40, le=20)
lift = pose("joy", rs=170, re=4, ls=140, le=16, head=-14)

e_stand = pose("stand", ls=30, le=-20, rs=8, re=10, head=4)
e_wave = pose("stand", ls=30, le=-20, rs=82, re=-10, head=4)
e_raise = pose("stand", ls=30, le=-20, rs=165, re=10, head=-4, lean=-6)
e_throw = pose("stand", ls=30, le=-20, rs=96, re=-6, head=8, lean=10)


def chop_pose(t):
    keys = [(0.0, fwd), (0.5, back), (0.85, fwd), (1.35, back), (1.7, fwd), (2.25, back), (2.55, fwd), (3.1, back), (3.5, hold)]
    return keyed(keys, t)


def surf(x, gy, t):
    return surface_y(x, gy + WD, t, S_AMP, S_ROUGH)


class LostAxeHead(Episode):
    dur = 18.0
    ground = False
    cta = "Read it in Scroll the Catholic Bible"
    kicker = "2 KINGS 6  •  THE LOST AXE HEAD"
    headline = "The borrowed axe head sank.\nOnly one cried out for help."
    captions = [
        (cpdv("II Kings", 6, 5, "…the iron of the ax fell into the water. And he cried out…“Alas, alas, alas, my lord! For this thing was borrowed.”"), "2 Kings 6:5", 4.8),
        (cpdv("II Kings", 6, 6, "Then the man of God said, “Where did it fall?” And he indicated to him the place…And the iron floated up."), "2 Kings 6:6", 10.0),
        (cpdv("II Kings", 6, 7, "And he said, “Take it.” And he extended his hand, and took it."), "2 Kings 6:7", 12.4),
    ]

    def draw_panel(self, cr, i, t, y0, gy):
        sun(cr, 980, gy - 300, r=22, rays=10)
        ground_line(cr, gy, 0, BANK)
        cr.set_source_rgb(*INK); cr.set_line_width(4); cr.move_to(BANK - 2, gy)
        cr.curve_to(BANK + 10, gy + 2, BANK + 14, gy + WD - 6, BANK + 26, gy + WD + 8); cr.stroke()   # the bank drops to the river
        far_bank(cr, 880, W + 10, gy + WD, h=26)
        for gx in (40, 150):
            grass_tuft(cr, gx, gy, 12, sway=0.3 * math.sin(t * 2 + gx))
        olive_tree(cr, TX, gy, h=200, s=1.0)

        # ---------- the iron: flies off, sinks; later floats up ----------
        head_on = t < 2.95
        iron = None                      # (x, y, rot) when visible above water
        fly = prog(t, 2.95, 3.65) if t >= 2.95 else 0
        hx0, hy0 = self.detach_point(gy)
        if 2.95 <= t < 3.65:
            u = (t - 2.95) / 0.7
            x = lerp(hx0, SINK, u); y = lerp(hy0, surf(SINK, gy, t), u) - 230 * u * (1 - u) * 1.6
            iron = (x, y, 400 * u)
        floated = False
        if i > 0 and t >= 9.9:
            floated = True
            rise = prog(t, 9.9, 10.6)
            ix = SINK
            if i == 2:
                ix = lerp(SINK, 668, prog(t, 10.6, 11.8))
            taken = i == 2 and t >= 12.15
            if not taken:
                iy = surf(ix, gy, t) - 6 * rise + 2 * math.sin(t * 2.2)
                iron = (ix, iy + 16 * (1 - rise), 6 * math.sin(t * 1.8))
                if rise < 1:          # still coming up: draw it under the surface fill
                    axe_head(cr, *iron, s=1.1); iron = None
            warm_glow(cr, ix, surf(ix, gy, t) - 6, 120, 0.7 * prog(t, 9.9, 10.5) * (1 - prog(t, 13.5, 15.5)))

        # the stick, thrown in by Elisha
        stick_xy = None
        if i > 0 and 8.85 <= t < 9.5:
            u = (t - 8.85) / 0.65
            sx0, sy0 = self.throw_point(gy)
            stick_xy = (lerp(sx0, SINK, u), lerp(sy0, surf(SINK, gy, t), u) - 200 * u * (1 - u), 520 * u)

        # ---------- water ----------
        water(cr, gy + WD, t, x0=BANK + 14, x1=W + 20, amp=S_AMP, rough=S_ROUGH, below=60)
        ripples(cr, SINK, surf(SINK, gy, t) + 2, 1 - prog(t, 6.0, 7.5), t, t0=3.65)
        splash(cr, SINK, surf(SINK, gy, t), prog(t, 3.6, 3.7) * (1 - prog(t, 3.9, 4.6)), t)
        if i > 0:
            splash(cr, SINK, surf(SINK, gy, t), prog(t, 9.45, 9.55) * (1 - prog(t, 9.7, 10.3)), t, n=6, seed=7)
            ripples(cr, SINK, surf(SINK, gy, t) + 2, 1 - prog(t, 11.5, 13.0), t, t0=9.5)
            if t > 9.5:   # the stick floats where it fell
                stick(cr, SINK + 40, surf(SINK + 40, gy, t) - 3, ang=8 * math.sin(t * 1.6))
        if iron:
            axe_head(cr, *iron, s=1.1)
        if stick_xy:
            stick(cr, *stick_xy)

        # ---------- Elisha ----------
        ex, ewa, edir = EX0, 0, 1
        ep = e_stand
        if i == 0:
            ep = keyed([(6.0, e_stand), (6.6, e_wave), (9.4, e_wave), (10.2, pose("stand", ls=30, le=-20, rs=8, re=10, head=24, lean=6))], t)
        else:
            ex, ewa, _ = track(t, [(5.6, EX0), (7.8, EX)])
            base = keyed([(5.0, e_stand), (5.4, e_wave), (5.9, e_stand), (7.8, e_stand), (8.3, e_raise),
                          (8.7, e_raise), (8.95, e_throw), (9.6, e_throw), (10.2, e_stand)], t)
            ep = body(t, base, ewa, speed=1.3)
            for k_ in ("ls", "le"):
                ep[k_] = e_stand[k_]
        EJ = draw_figure(cr, ex, gy, ep, s=1.0, face=1, prop="robe")
        lx, ly = EJ["lhand"]
        staff(cr, lx, gy - 190, gy)
        if i > 0 and 6.6 <= t < 8.85:     # the piece of wood he cut, in his hand
            hx, hy = EJ["rhand"]
            stick(cr, hx + 6, hy - 4, ang=held_angle(ep, 1) - 90, L=48)

        # ---------- the woodcutter ----------
        mx, mwa, mdir = MX, 0, 1
        face = -1
        handle = "hand"
        if t < 3.5:
            p = chop_pose(t)
        elif t < 4.4:
            mx, mwa, _ = track(t, [(3.6, MX), (4.3, EDGE)])
            p = body(t, keyed([(3.5, hold), (3.8, look)], t), mwa, speed=1.6)
            face = 1
        else:
            mx = EDGE; face = 1
            handle = "ground"
            if i == 0:
                p = keyed([(4.4, look), (4.8, alas), (6.0, alas), (6.5, slump)], t)
                if t > 6.6:
                    face = -1
                    mx, mwa, _ = track(t, [(6.8, EDGE), (11.4, -90)])
                    p = body(t, slump, mwa, speed=1.1)
            else:
                p = keyed([(4.4, look), (4.8, alas), (5.2, alas), (5.6, call), (7.6, call), (8.0, point),
                           (9.4, point), (9.9, pose("stand", head=8)), (10.4, wonder)], t)
                if 5.4 < t < 7.7:
                    face = -1
                if i == 2 and t > 10.6:
                    mx, mwa, _ = track(t, [(10.6, EDGE), (11.2, EDGE + 22)])
                    p = keyed([(10.6, wonder), (11.4, kneel_r), (11.9, kneel_r), (12.15, dict(kneel_r, rs=70, head=10)),
                               (12.7, pose("stand", rs=60, re=40)), (13.4, lift)], t)
                    if t > 13.4:
                        p["lean"] += 2 * math.sin(t * 4)
        if mx > -100:
            J = draw_figure(cr, mx, gy, p, s=1.0, face=face)
            if handle == "hand":
                axe(cr, *J["rhand"], held_angle(p, face), head=head_on)
            if i == 2 and t >= 12.15:
                hx, hy = J["rhand"]
                axe_head(cr, hx, hy - 6, rot=-20, s=1.1)
            cry_lines(cr, J["head"][0], J["head"][1], face=face, t=t,
                      amount=prog(t, 4.7, 5.0) * (1 - prog(t, 5.8, 6.3)) if i == 0 else prog(t, 5.5, 5.8) * (1 - prog(t, 7.4, 7.8)))
        if handle == "ground":
            axe(cr, EDGE - 30, gy - 5, -84, head=False)

    def detach_point(self, gy):
        p = chop_pose(2.95); J = ghost_joints(MX, gy, p, s=1.0, face=-1)
        a = math.radians(held_angle(p, -1)); hx, hy = J["rhand"]
        return hx + math.sin(a) * 66, hy - math.cos(a) * 66

    def throw_point(self, gy):
        J = ghost_joints(EX, gy, e_throw, s=1.0, face=1)
        return J["rhand"]


OUTPUT_NAME = "day43a_lost_axe_head_2kings6"
