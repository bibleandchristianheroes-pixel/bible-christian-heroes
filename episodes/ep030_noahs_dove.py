import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import *
from props import *

AX, AW = 820, 340        # ark centre / width
TX, TH = 300, 130        # olive tree

class NoahsDove(Episode):
    dur = 18.0
    ground = False
    caption_bg = True
    cta = "Pray it with Ave – Catholic Prayer Lock"
    kicker = "GENESIS 7–9  •  NOAH'S DOVE"
    headline = "Forty days of rain.\nThen one green leaf."
    captions = [
        (cpdv("Genesis", 7, 12, "And rain came upon the earth for forty days and forty nights."), "Genesis 7:12", 3.6),
        (cpdv("Genesis", 8, 11, "And she came to him in the evening, carrying in her mouth an olive branch with green leaves."), "Genesis 8:11", 10.4),
        (cpdv("Genesis", 9, 13, "I will place my arc in the clouds, and it will be the sign of the pact…"), "Genesis 9:13", 12.8),
    ]

    def draw_panel(self, cr, i, t, y0, gy):
        g = gy
        rain_amt = prog(t, 1.0, 1.8) * (1 - (prog(t, 6.0, 7.0) if i >= 1 else 0))
        wl = lerp(g + 40, g - 70, prog(t, 1.6, 4.4))
        if i >= 1: wl = lerp(wl, g - 52, prog(t, 7.0, 8.4))
        if i == 2: wl = lerp(wl, g + 40, prog(t, 11.2, 12.8))
        # rainbow behind everything
        if i == 2:
            rainbow(cr, 840, g + 20, 232, prog(t, 12.2, 13.8))
            warm_glow(cr, 900, g - 120, 420, prog(t, 12.2, 14.0) * 0.7)
        ground_line(cr, g)
        olive_tree(cr, TX, g, h=TH)
        # ---------- Noah walking out (panel 3) ----------
        if i == 2 and t > 13.0:
            nx, wa, _ = track(t, [(13.0, AX - 120), (14.4, 470)])
            npose = keyed([(14.4, pose("stand", head=-10)), (15.0, pose("joy"))], t)
            draw_figure(cr, nx, g, body(t, npose, wa), s=0.95, face=-1)
        # ---------- ark ----------
        ay = min(g - 30, wl + 10) + 3 * math.sin(t * 1.6) * (1 if wl < g - 40 else 0)
        wx, wy = ark(cr, AX, ay, w=AW)
        # Noah at the window
        if not (i == 2 and t > 12.4):
            cr.set_source_rgb(*INK)
            cr.save(); cr.translate(wx, wy - 2); cr.scale(1, 1.15); cr.arc(0, 0, 9, 0, 2 * math.pi); cr.restore(); cr.fill()
            cr.rectangle(wx - 12, wy + 8, 24, 10); cr.fill()
            reach = prog(t, 7.6, 8.0) * (1 - prog(t, 8.3, 8.7)) if i >= 1 else 0
            reach = max(reach, prog(t, 10.4, 10.8) * (1 - prog(t, 11.6, 12.0))) if i >= 1 else 0
            if reach > 0:
                cr.set_line_width(7); cr.move_to(wx + 6, wy + 10); cr.line_to(wx + 6 + 40 * reach, wy + 2 - 14 * reach); cr.stroke()
        # ---------- water ----------
        if wl < g + 30:
            water(cr, wl, t, rough=0.6 + 1.4 * rain_amt, below=g + 70 - wl)
        # ---------- the dove ----------
        if i >= 1 and t > 7.9:
            tree_top = (TX + 6, g - TH - 8)
            perch = (AX + 40, ay - 186)
            if t < 9.0:
                u = prog(t, 7.9, 9.0); bx = lerp(wx + 30, tree_top[0], u); by = lerp(wy - 10, tree_top[1], u) - 70 * math.sin(math.pi * u); bf = -1; fl = math.sin(t * 22)
            elif t < 9.6:
                bx, by, bf, fl = tree_top[0], tree_top[1], -1, 0.2
            elif t < 10.6 or i == 2:
                u = prog(t, 9.6, 10.6); bx = lerp(tree_top[0], perch[0], u); by = lerp(tree_top[1], perch[1], u) - 60 * math.sin(math.pi * u); bf = 1; fl = math.sin(t * 22) if u < 1 else 0.2
                if i == 2 and t > 13.4:
                    u2 = prog(t, 13.4, 14.6); bx = lerp(perch[0], 590, u2); by = lerp(perch[1], g - 175, u2) - 10 * math.sin(math.pi * u2); bf = -1; fl = math.sin(t * 22) if u2 < 1 else math.sin(t * 22)
            else:
                bx, by, bf, fl = perch[0], perch[1], 1, 0.2
            bird(cr, bx, by, fl, s=1.3, face=bf)
            if t > 9.4:
                olive_sprig(cr, bx + bf * 26, by - 6, s=1.5, rot=0.3 if bf > 0 else math.pi - 0.3)
        rain(cr, y0, PANEL_H, t, rain_amt)
        darkness(cr, y0, PANEL_H, 0.45 * rain_amt)

OUTPUT_NAME = "day15b_noahs_dove_genesis8"
