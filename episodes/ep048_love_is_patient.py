import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import *
from props import *

AX = 230            # the one who waits, on the bench
MEET = 322          # where the friend stops
WAIT = sit_pose(head=-6, rs=20, re=40, ls=15, le=40)

class LoveIsPatient(Episode):
    dur = 18.0
    cta = "Start your day with Ave Missal"
    kicker = "1 CORINTHIANS 13  •  LOVE IS PATIENT"
    headline = "Love waits. Love carries.\nLove is what remains."
    captions = [
        (cpdv("I Corinthians", 13, 4, "Charity is patient, is kind…"), "1 Corinthians 13:4", 10.6),
        (cpdv("I Corinthians", 13, 7, "Charity suffers all, believes all, hopes all, endures all."), "1 Corinthians 13:7", 8.4),
        (cpdv("I Corinthians", 13, 13, "But for now, these three continue: faith, hope, and charity. And the greatest of these is charity."), "1 Corinthians 13:13", 10.4),
    ]

    def hug(self, t, t0):
        open_ = pose("stand", rs=105, re=-10, ls=100, le=-10, head=-6)
        hold = pose("stand", rs=75, re=70, ls=70, le=75, head=8, lean=8)
        return keyed([(t0, pose("stand")), (t0 + 0.5, open_), (t0 + 1.0, hold)], t)

    def draw_panel(self, cr, i, t, y0, gy):
        bench(cr, AX - 60, AX + 60, gy)
        ap = WAIT; ax, awa, aface = AX, 0, 1
        if i == 0:      # ---- waits all day ----
            su = prog(t, 1.0, 10.0)
            sun(cr, lerp(1010, 830, su), lerp(y0 + 240, gy + 30, su * su), r=24)
            cr.set_source_rgb(*BG); cr.rectangle(0, gy + 2, W, 120); cr.fill()
            look = pose("stand", head=-8, rs=95, re=60)
            ap = keyed([(2.6, WAIT), (3.2, pose("stand", head=-4)), (3.8, look), (5.0, look), (5.6, pose("stand")), (6.2, WAIT),
                        (8.4, WAIT), (8.8, sit_pose(head=-4, rs=30, re=50))], t)
            if t > 6.2:   # glances again, still patient
                ap["head"] = -6 + 8 * math.sin(t * 1.3)
            if t >= 9.6:
                ap = keyed([(9.6, WAIT), (10.1, pose("stand"))], t)
                if t >= 10.1: ap = self.hug(t, 10.1)
            bx, bwa, _ = track(t, [(7.0, 1160), (10.4, MEET)])
            bp = body(t, pose("stand"), bwa)
            if t >= 10.4: bp = self.hug(t, 10.1)
            draw_figure(cr, bx, gy, bp, s=1.0, face=-1)
            draw_figure(cr, ax, gy, ap, s=1.0, face=1)
            warm_glow(cr, 276, gy - 120, 230, prog(t, 11.0, 12.4))
        elif i == 1:    # ---- the friend falls; he carries him ----
            bx, bwa, _ = track(t, [(1.0, 1160), (5.0, 560)])
            limp = pose("stand", lean=16, head=18, rs=30, re=60, ls=10, le=30)
            bent = pose("stand", lean=16, head=6, rs=-40, re=70, ls=-35, le=70)
            ax, awa, _ = track(t, [(5.4, AX), (6.4, 500), (7.2, 500), (7.5, 520), (8.6, 520), (13.4, 330)])
            if t < 5.4:
                ap = keyed([(4.8, WAIT), (5.3, pose("stand", head=-6))], t)
            elif t < 6.4:
                ap = run(t); aface = 1
            elif t < 7.3:
                kneel = pose("kneel", lean=40, head=30, rs=50, re=10, ls=40, le=10)
                ap = keyed([(6.4, pose("stand")), (6.8, kneel)], t); aface = 1
            elif t < 8.6:
                ap = keyed([(7.3, pose("stand")), (7.7, bent)], t); aface = -1
            else:
                ap = body(t, bent, awa, speed=1.3)
                for k_ in ("lean", "head", "rs", "re", "ls", "le"): ap[k_] = bent[k_]
                aface = -1
                if t > 13.4: ap = bent
            AJ = draw_figure(cr, ax, gy, ap, s=1.0, face=aface)
            # B: limps in, collapses, is lifted onto A's back
            ride = pose("stand", lean=34, head=14, lt=80, lk=75, rt=72, rk=66, rs=55, re=45, ls=50, le=50)
            if t < 5.0:
                bp = body(t, limp, bwa, speed=0.9); bp["lean"] = 16 + 6 * math.sin(t * 5)
                draw_figure(cr, bx, gy, bp, s=0.95, face=-1)
            else:
                fall = prog(t, 5.0, 5.6); u = prog(t, 7.7, 8.5) if t < 8.6 else 1.0
                rx = AJ["hip"][0] + 30; rground = AJ["hip"][1] - 38 + (49.8 + 2) * 0.95
                x = lerp(bx, rx, u); lift = lerp(0, gy - rground, u)
                rot = lerp(lerp(0, 90, fall), 0, u)
                bp = mix(mix(limp, pose("lie"), fall), ride, u)
                draw_rotated(cr, x, gy, rot, bp, s=0.95, face=-1, lift=lift)
                if u > 0: draw_figure(cr, ax, gy, ap, s=1.0, face=aface)
        else:           # ---- three remain ----
            bx, bwa, _ = track(t, [(1.0, 1160), (4.6, MEET)])
            bp = body(t, pose("stand"), bwa)
            ap = keyed([(3.6, WAIT), (4.1, pose("stand"))], t)
            if t >= 4.3:
                ap = self.hug(t, 4.3); bp = self.hug(t, 4.3) if t >= 4.6 else bp
            if t >= 6.4:
                turn = pose("stand", head=-12, rs=20, re=20)
                ap = keyed([(6.4, self.hug(6.4, 4.3)), (7.0, turn)], t); bp = keyed([(6.4, self.hug(6.4, 4.3)), (7.0, turn)], t)
            bface = -1 if t < 6.7 else 1
            draw_figure(cr, bx, gy, bp, s=1.0, face=bface)
            draw_figure(cr, ax, gy, ap, s=1.0, face=1)
            for k, (sx, tk) in enumerate(((610, 7.0), (785, 8.4), (955, 9.8))):
                a = prog(t, tk, tk + 0.9)
                if a <= 0: continue
                cr.save(); cr.translate(sx, gy); cr.scale(a, a); cr.translate(-sx, -gy)
                if k == 0: cross(cr, sx, gy, h=150, glow=0.0)
                elif k == 1: anchor(cr, sx, gy, h=140)
                else: heart(cr, sx, gy, h=150 + 8 * math.sin(t * 3) * prog(t, 11.0, 11.5), glow=prog(t, 10.4, 11.6))
                cr.restore()

OUTPUT_NAME = "day24b_love_is_patient_1corinthians13"
