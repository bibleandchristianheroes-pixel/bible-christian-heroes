import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import *
from props import *

class TwoSons(Episode):
    dur = 18.0
    cta = "Read it in Scroll the Catholic Bible"
    kicker = "MATTHEW 21  •  THE TWO SONS"
    headline = "One said no.\nOne said yes. Watch what they did."
    captions = [
        (cpdv("Matthew", 21, 28, "…Son, go out today to work in my vineyard."), "Matthew 21:28", 1.6),
        (cpdv("Matthew", 21, 29, "…he said, ‘I am not willing.’ But afterwards, being moved by repentance, he went."), "Matthew 21:29", 9.4),
        (cpdv("Matthew", 21, 30, "…he said, ‘I am going, lord.’ And he did not go."), "Matthew 21:30", 10.4),
    ]
    FX = 150

    def draw_panel(self, cr, i, t, y0, gy):
        vines(cr, 640, 1010, gy, t)
        point = prog(t, 1.0, 1.6) * (1 - prog(t, 4.0, 4.6))
        fp = mix(pose("stand"), pose("reach", rs=105, re=-5), point)
        if t > 10 and i == 2:
            fp = keyed([(10.0, pose("stand")), (10.8, pose("stand", head=25, ls=150, le=150, rs=150, re=150))], t)
        draw_figure(cr, self.FX, gy, fp, s=1.1, prop="robe")
        if i == 0:
            # both sons hear the request: one shakes head, one nods
            for k, sx in enumerate((330, 430)):
                hm = math.sin(t * 9) * 14 * prog(t, 2.2, 2.5) * (1 - prog(t, 3.6, 3.9))
                p = pose("stand", head=(hm if k == 1 else abs(hm) + 4), lean=0)
                if k == 0:
                    p = keyed([(2.0, pose("stand")), (2.6, pose("stand", ls=60, le=110, rs=60, re=110, head=-10))], t)
                draw_figure(cr, sx, gy, p, s=0.98, face=-1)
        elif i == 1:   # says no, walks off... then turns and goes to work
            x, wa, d = track(t, [(2.6, 330), (4.4, 150), (6.4, 150), (9.0, 700)])
            face = -1 if t < 6.4 else 1
            if t < 4.4:
                p = keyed([(2.0, pose("stand")), (2.6, pose("stand", ls=60, le=110, rs=60, re=110, head=-10))], t)
                face = -1 if t < 2.6 else 1
                if t >= 2.6: face = -1 if False else 1
            elif t < 6.4:
                p = keyed([(4.4, pose("stand", head=10)), (5.2, pose("stand", head=35, lean=8)), (6.0, pose("stand", head=0))], t)
            elif t < 9.0:
                p = pose("stand")
            else:
                work = 0.5 + 0.5 * math.sin(t * 6)
                p = keyed([(9.0, pose("stand")), (9.6, pose("reach", rs=150, re=-10 + 40 * work, ls=130, le=20, head=-25))], t)
                if t > 9.6: p = pose("reach", rs=140 + 20 * work, re=10, ls=130, le=20 + 30 * work, head=-25)
            if t < 2.6:
                face = -1
            elif t < 4.4:
                face = -1
            draw_figure(cr, x, gy, body(t, p, wa), s=0.98, face=face)
        else:          # says yes, sets off, then sits down and never goes
            x, wa, d = track(t, [(2.6, 430), (4.6, 520), (5.2, 520)])
            hm = math.sin(t * 9) * 14 * prog(t, 2.0, 2.3) * (1 - prog(t, 2.8, 3.0))
            if t < 4.6:
                p = pose("stand", head=hm + 4, rs=110 if 3.0 < t < 3.8 else 10, re=10)
            else:
                p = keyed([(4.6, pose("stand")), (6.0, pose("stand", head=-20)), (7.0, pose("sad_sit", head=-10, lean=-6, ls=40, le=60, rs=40, re=60))], t)
            face = -1 if t < 3.8 else 1
            draw_figure(cr, x, gy, body(t, p, wa), s=0.98, face=face)

OUTPUT_NAME = "day05b_two_sons_matthew21"
