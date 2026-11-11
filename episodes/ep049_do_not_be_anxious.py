import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import *
from props import *

MX = 840                                   # where he stops
DROPS = [2.6, 3.3, 4.0, 4.7]               # worries landing on his back (all panels)
BW, BH = 34, 30

class DoNotBeAnxious(Episode):
    dur = 18.0
    cta = "Read it in Scroll the Catholic Bible"
    kicker = "PHILIPPIANS 4  •  DO NOT BE ANXIOUS"
    headline = "Same worries piled up.\nOnly one let them go."
    captions = [
        (cpdv("Philippians", 4, 6, "Be anxious about nothing."), "Philippians 4:6", 8.0),
        (cpdv("Philippians", 4, 6, "…with prayer and supplication, with acts of thanksgiving, let your petitions be made known to God."), "Philippians 4:6", 8.2),
        (cpdv("Philippians", 4, 7, "And so shall the peace of God, which exceeds all understanding, guard your hearts and minds in Christ Jesus."), "Philippians 4:7", 10.6),
    ]

    def slot(self, J, k):
        sx, sy = J["sh"]
        return sx + 2, sy + 4 - k * (BH - 2)

    def falling(self, cr, t, tk, x, y, top=None):
        """Box dropping from above the panel onto (x, y) at time tk."""
        u = clamp((t - (tk - 0.5)) / 0.5)
        if u <= 0: return
        burden(cr, x, lerp(top, y, u * u), BW, BH)

    def draw_panel(self, cr, i, t, y0, gy):
        top = y0 - 40
        x, wa, _ = track(t, [(0.2, 1150), (2.3, MX)])
        n_on = sum(1 for d in DROPS if t >= d)
        stoop = pose("stand", lean=4 + 4 * n_on, head=8 + 4 * n_on, ls=4, le=12, rs=8, re=14)
        p = body(t, stoop, wa)
        carried = list(range(4))           # boxes still on his back
        lifted = []                        # (k, t_start) rising away in prayer
        pile = []
        glow, ring = 0.0, 0.0
        if i == 0:
            if t >= 6.4:
                sit = pose("sad_sit", lean=30, head=40, ls=150, le=150, rs=150, re=150)
                p = keyed([(6.4, stoop), (7.3, sit)], t)
                carried = [] if t >= 7.0 else carried
            for k in range(4):
                if t >= 7.0:
                    pile.append((k, 7.0 + 0.12 * k))
        else:
            kt = 5.3
            fold = pose("kneel", lean=8, head=14, rs=45, re=105, ls=40, le=110)
            raise_ = pose("kneel", lean=-2, head=-18, rs=160, re=5, ls=150, le=10)
            t_up = 7.0 if i == 1 else 6.4
            rise_times = [7.4, 8.0, 8.6, 9.2] if i == 1 else [6.8, 7.2, 7.6, 8.0]
            if t >= kt:
                keys = [(kt, stoop), (kt + 0.9, fold), (t_up, fold), (t_up + 0.6, raise_)]
                if i == 1:
                    keys += [(10.4, raise_), (11.2, pose("stand", head=-6)), (12.0, pose("stand", head=-18, rs=125, re=20, ls=115, le=25))]
                else:
                    keys += [(9.4, raise_), (10.2, pose("stand", head=-6, rs=14, re=10, ls=10, le=10))]
                p = keyed(keys, t)
            for k in range(4):
                tk = rise_times[3 - k]       # top box first
                if t >= tk:
                    carried.remove(k); lifted.append((k, tk))
            if i == 1:
                glow = prog(t, 7.2, 8.4) * (1 - 0.6 * prog(t, 10.0, 11.5))
            else:
                glow = prog(t, 6.6, 7.6) * (1 - 0.5 * prog(t, 9.0, 10.0))
                ring = prog(t, 9.0, 10.2)

        # glow above (heaven receives the petitions)
        warm_glow(cr, MX + 20, y0 + 60, 260, glow)
        if ring > 0:
            cx, cy, R = MX, gy - 92, 135
            warm_glow(cr, cx, cy, R + 40, 0.8 * ring)
            cr.set_source_rgba(1, 0.82, 0.4, 0.75 * ring); cr.set_line_width(4)
            cr.arc(cx, cy, R, math.pi * 0.93, math.pi * 2.07); cr.stroke()

        J = draw_figure(cr, x, gy, p, s=1.0, face=-1)

        # boxes on his back / still falling onto it
        for k in carried:
            bx, by = self.slot(J, k)
            if t < DROPS[k]:
                self.falling(cr, t, DROPS[k], bx, by, top)
            else:
                burden(cr, bx, by, BW, BH)
        # lifted up in prayer: rise and fade
        for k, tk in lifted:
            u = prog(t, tk, tk + 1.6)
            bx = MX - 4 + 30 * math.sin(k * 1.7) * u
            by = lerp(gy - 150 - k * 28, y0 + 30, u)
            col = tuple(lerp(INK[j], BG[j], u) for j in range(3))
            if u < 0.98: burden(cr, bx, by, BW, BH, color=col)
        # panel 1: they slide off into a heap beside him, and more keep coming
        if i == 0:
            heap = [(MX + 34, gy - BH), (MX + 70, gy - BH), (MX + 52, gy - 2 * BH + 2), (MX + 106, gy - BH),
                    (MX - 110, gy - BH), (MX + 88, gy - 2 * BH + 2), (MX - 74, gy - BH)]
            for k, ts in pile:
                bx, by = self.slot(J, k)
                u = prog(t, ts, ts + 0.5)
                hx, hy = heap[k]
                burden(cr, lerp(bx, hx, u), lerp(by, hy, u) - 30 * math.sin(math.pi * u), BW, BH)
            for j, tk in enumerate((9.0, 10.0, 11.0)):
                hx, hy = heap[4 + j]
                if t >= tk - 0.5:
                    self.falling(cr, t, tk, hx, hy, top)
        # panel 3: new worries fall but stop at the guard of peace
        if i == 2:
            for j, (tk, ox) in enumerate(((11.2, -40), (12.0, 30), (12.8, -5))):
                if t < tk - 0.6: continue
                stop = gy - 92 - 135 - BH + 4
                u = clamp((t - (tk - 0.6)) / 0.6)
                fade = prog(t, tk, tk + 0.7)
                col = tuple(lerp(INK[c], BG[c], fade) for c in range(3))
                if fade < 0.98:
                    burden(cr, MX + ox - BW / 2, lerp(top, stop, u * u), BW, BH, color=col)
                if 0 < fade < 1:
                    cr.set_source_rgba(1, 0.8, 0.35, 0.8 * (1 - fade)); cr.set_line_width(3)
                    for a in range(5):
                        ang = math.pi + (a + 0.5) * math.pi / 5
                        cx, cy = MX + ox, stop + BH
                        cr.move_to(cx + math.cos(ang) * 12, cy + math.sin(ang) * 6)
                        cr.line_to(cx + math.cos(ang) * (20 + 30 * fade), cy + math.sin(ang) * (10 + 18 * fade)); cr.stroke()

OUTPUT_NAME = "day25a_do_not_be_anxious_philippians4"
