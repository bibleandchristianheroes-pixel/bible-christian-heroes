import math, sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from engine import *
from props import *

SM = (95, 265)       # Samuel's mat (head to the left)
SFEET = 252          # Samuel's feet when lying
SHIP = 186           # Samuel's hips when he sits up
SSTAND = 225         # where he stands up
LAMP_X = 420         # the lamp of God, on its stand
EM = (690, 900)      # Eli's mat (head to the right)
EFEET = 700
EHIP = 783           # Eli's hips when he sits up
AT_ELI = 620         # where Samuel stops beside Eli
SS, ES = 0.76, 0.95  # Samuel (a boy), Eli (an old man)

s_here = pose("stand", head=-4, lean=4, rs=70, re=-20, ls=58, le=-14)          # "Here I am."
s_look_up = pose("stand", head=-26, lean=-4, rs=12, re=20, ls=10, le=20)
e_sit = ground_sit_pose(lean=-2, head=4, rs=25, re=45, ls=20, le=40)
e_wave = ground_sit_pose(lean=-2, head=8, rs=95, re=-30, ls=20, le=40)        # "Return and sleep."
e_wave2 = ground_sit_pose(lean=-2, head=8, rs=80, re=10, ls=20, le=40)
e_point = ground_sit_pose(lean=-8, head=-18, rs=150, re=-6, ls=20, le=40)     # it is the Lord
k_listen = pose("kneel", lean=-2, head=-12, rs=120, re=-8, ls=112, le=-6)      # "Speak, Lord"
k_rise = pose("kneel", lean=10, head=6)


def breathe(t, k=0.0):
    return 2.5 * math.sin(t * 1.7 + k)


class SpeakLord(Episode):
    dur = 18.0
    cta = "Start your day with Ave Missal"
    caption_bg = True
    kicker = "1 SAMUEL 3  •  SPEAK, LORD"
    headline = "He kept running to the wrong voice.\nThen he learned to listen."
    captions = [
        (cpdv("I Samuel", 3, 5, "…“Here I am. For you called me.” And he said: “I did not call. Return and sleep.”"), "1 Samuel 3:5", 5.4),
        (cpdv("I Samuel", 3, 9, "Then Eli understood that the Lord had called the boy."), "1 Samuel 3:9", 11.9),
        (cpdv("I Samuel", 3, 10, "And Samuel said, “Speak, Lord, for your servant is listening.”"), "1 Samuel 3:10", 10.9),
    ]

    def draw_panel(self, cr, i, t, y0, gy):
        night = 1.0
        sleeping_mat(cr, SM[0], SM[1], gy, pillow="left")
        sleeping_mat(cr, EM[0], EM[1], gy, pillow="right")
        top = lampstand(cr, LAMP_X, gy, h=150)
        fx, fy = lamp(cr, LAMP_X - 6, top + 2, lit=1.0, flicker=t)

        # ---------------- the call ----------------
        calls = [(1.4, 3.0)]
        if i >= 1:
            calls.append((8.8, 10.4))
        voice = 0.0
        for a, b in calls:
            voice = max(voice, prog(t, a, a + 0.4) * (1 - prog(t, b - 0.4, b)))
        listen = prog(t, 10.4, 12.0) if i == 2 else 0.0

        # ---------------- Eli ----------------
        e_up = [(4.7, 6.8)]
        if i == 1:
            e_up.append((11.0, 99))
        sitting = None
        for a, b in e_up:
            if a <= t < b:
                sitting = (a, b)
        if sitting is None:
            draw_rotated(cr, EFEET, gy, 90, pose("lie", ls=4, le=4, rs=7, re=4, head=0, lean=breathe(t, 1.0)), s=ES, face=-1, lift=19)
        else:
            a, b = sitting
            if a < 8:
                ek = [(a, ground_sit_pose(lean=-40, head=-10)), (a + 0.4, e_sit), (5.3, e_sit), (5.6, e_wave), (5.9, e_wave2), (6.2, e_wave), (6.6, e_sit)]
            else:
                ek = [(a, ground_sit_pose(lean=-40, head=-10)), (a + 0.4, e_sit), (11.6, e_sit), (12.1, e_point)]
            draw_figure(cr, EHIP, gy - 9, keyed(ek, t), s=ES, face=-1, prop="robe")

        # ---------------- Samuel ----------------
        runs = [(2.3, False)]                       # (time he wakes, stays at his mat?)
        if i == 1:
            runs.append((9.7, False))
        if i == 2:
            runs.append((9.7, True))
        mode, J = "lie", None
        for tw, stay in runs:
            if t >= tw:
                mode = ("listen", tw) if stay else ("run", tw)
        if mode == "lie":
            draw_rotated(cr, SFEET, gy, -90, pose("lie", ls=4, le=4, rs=7, re=4, head=0, lean=breathe(t)), s=SS, lift=19)
        elif mode[0] == "listen":
            tw = mode[1]
            if t < tw + 0.5:
                sp = keyed([(tw, ground_sit_pose(lean=-40, head=-10)), (tw + 0.5, ground_sit_pose(head=-10))], t)
                draw_figure(cr, SHIP, gy - 9, sp, s=SS, face=1, prop="robe")
            else:
                sp = keyed([(tw + 0.5, k_rise), (tw + 1.0, k_rise), (tw + 1.5, k_listen)], t)
                sp["head"] += 1.5 * math.sin(t * 1.2)
                J = draw_figure(cr, SSTAND, gy - 9, sp, s=SS, face=1, prop="robe")
        else:
            tw = mode[1]
            last = tw > 8
            back = None if last else tw + 3.6          # first time: sent back to sleep
            if t < tw + 0.5:
                sp = keyed([(tw, ground_sit_pose(lean=-40, head=-10)), (tw + 0.5, ground_sit_pose(head=-6))], t)
                draw_figure(cr, SHIP, gy - 9, sp, s=SS, face=1, prop="robe")
            elif back is not None and t >= back + 1.4:
                if t < back + 1.9:
                    sp = keyed([(back + 1.4, pose("stand", head=10)), (back + 1.9, ground_sit_pose(head=10))], t)
                    draw_figure(cr, SHIP if t > back + 1.65 else SSTAND, gy - 9 * prog(t, back + 1.4, back + 1.9), sp, s=SS, face=1, prop="robe")
                else:
                    u = prog(t, back + 1.9, back + 2.4)
                    if u < 1:
                        draw_figure(cr, SHIP, gy - 9, ground_sit_pose(lean=lerp(-4, -40, u), head=10), s=SS, face=1, prop="robe")
                    else:
                        draw_rotated(cr, SFEET, gy, -90, pose("lie", ls=4, le=4, rs=7, re=4, head=0, lean=breathe(t)), s=SS, lift=19)
            else:
                keys = [(tw + 0.8, SSTAND), (tw + 2.1, AT_ELI)]
                if back is not None:
                    keys += [(back, AT_ELI), (back + 1.4, SSTAND)]
                x, wa, d = track(t, keys)
                face = -1 if (back is not None and t > back - 0.1) else 1
                sk = [(tw + 0.5, pose("stand", head=-6)), (tw + 2.1, pose("stand")), (tw + 2.5, s_here)]
                if back is not None:
                    sk += [(back - 0.4, s_here), (back, pose("stand", head=14, lean=6))]
                else:
                    sk += [(tw + 3.4, s_here), (tw + 3.9, pose("stand")), (tw + 4.3, s_look_up)]
                    if t > tw + 3.9:
                        face = -1
                sp = keyed(sk, t) if t > tw + 0.5 else pose("stand")
                if t < tw + 0.8:
                    sp = keyed([(tw + 0.5, ground_sit_pose(head=-6)), (tw + 0.8, pose("stand", head=-6))], t)
                J = draw_figure(cr, x, gy, body(t, sp, wa, speed=2.2 if back is None or t < back else 1.4), s=SS, face=face, prop="robe")

        # ---------------- night, lamp, voice ----------------
        lights = [(fx, fy, 430, 0.75), (fx, fy, 230, 1.0), (800, gy - 50, 230, 0.45)]
        if listen > 0:
            lights.append((SSTAND + 40, gy - 90, 300 * listen, 1.0))
        darkness(cr, y0, PANEL_H, 0.86 * night, lights)
        warm_glow(cr, fx, fy, 110, 0.6 + 0.08 * math.sin(t * 9))
        call_rings(cr, fx, fy, voice, t, t0=calls[0][0], r1=105)
        if listen > 0:
            warm_glow(cr, (fx + SSTAND) / 2, gy - 120, 260, 0.7 * listen)
            light_rays(cr, fx, fy, 0.6 * listen, r0=24, r1=56, n=12, t=t)


OUTPUT_NAME = "day36b_speak_lord_1samuel3"
