"""Daily Verse Parables - minimalist 3-panel silhouette engine (1080x1920, 30fps)."""
import json, math, os, subprocess, random
import cairo
import numpy as np

W, H, FPS = 1080, 1920, 30
BG = (0.941, 0.922, 0.878)       # cream
INK = (0.13, 0.12, 0.11)         # near-black
SOFT = (0.60, 0.57, 0.52)        # faded ink
HEADER_H, PANEL_H = 300, 460
FOOTER_Y = HEADER_H + 3 * PANEL_H
GROUND_OFF = 395                  # ground line offset inside a panel

CPDV_PATH = os.environ.get("CPDV_JSON", os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "CPDV.json"))
_BIBLE = None

def verse(book, ch, vs):
    global _BIBLE
    if _BIBLE is None:
        d = json.load(open(CPDV_PATH))
        _BIBLE = {b["name"]: b for b in d["books"]}
    for x in _BIBLE[book]["chapters"][ch - 1]["verses"]:
        if x["verse"] == vs:
            return x["text"]
    raise KeyError((book, ch, vs))

def excerpt(book, ch, vs, start=None, end=None):
    """Exact CPDV substring; adds ellipses where trimmed. Fails loudly if not verbatim."""
    t = verse(book, ch, vs)
    a = 0 if start is None else t.index(start)
    b = len(t) if end is None else t.index(end, a) + len(end)
    s = t[a:b].strip()
    if a > 0: s = "…" + s[0].lower() + s[1:] if s[0].isupper() and start and start[0].islower() else "…" + s
    if b < len(t): s = s.rstrip(",.;:") + "…"
    return s

# ---------------- easing / keyframes ----------------
def clamp(x, a=0.0, b=1.0): return max(a, min(b, x))
def smooth(x): x = clamp(x); return x * x * (3 - 2 * x)
def prog(t, t0, t1): return smooth((t - t0) / (t1 - t0)) if t1 > t0 else float(t >= t1)
def lerp(a, b, u): return a + (b - a) * u

def keyed(keys, t):
    """keys: list of (time, dict). Smoothly interpolates dict values."""
    if t <= keys[0][0]: return dict(keys[0][1])
    for (t0, p0), (t1, p1) in zip(keys, keys[1:]):
        if t <= t1:
            u = prog(t, t0, t1)
            return {k: lerp(p0[k], p1.get(k, p0[k]), u) for k in p0}
    return dict(keys[-1][1])

# ---------------- poses (degrees; 0 = straight down, + = toward facing dir) ----------------
BASE = dict(lean=0, head=0, lt=3, lk=2, rt=-3, rk=2, ls=6, le=10, rs=10, re=12)
POSES = {
    "stand": {},
    "sow_back": dict(rs=-45, re=15, lean=-3),
    "sow_fwd": dict(rs=115, re=5, lean=8, lt=12, rt=-10),
    "look": dict(head=-8),
    "sad_sit": dict(lean=28, head=32, lt=128, lk=140, rt=122, rk=134, ls=55, le=-25, rs=60, re=-20),
    "head_hands": dict(lean=6, head=25, ls=150, le=150, rs=150, re=150),
    "joy": dict(lean=-6, head=-18, ls=165, le=8, rs=158, re=10, lt=6, rt=-6),
    "lie": dict(lt=2, lk=0, rt=-2, rk=0, ls=170, le=0, rs=8, re=4, head=-5),
    "knock_up": dict(rs=95, re=55),
    "knock_hit": dict(rs=78, re=40),
    "reach": dict(rs=80, re=0, lean=10),
    "hold_high": dict(rs=160, re=5, head=-10),
    "carry": dict(rs=40, re=70),
    "flail": dict(ls=150, le=30, rs=165, re=20, head=-25, lean=-5),
    "kneel": dict(lean=15, head=20, lt=95, lk=95, rt=-15, rk=110, rs=60, re=40, ls=40, le=30),
}
def pose(name, **over):
    p = dict(BASE); p.update(POSES[name]); p.update(over); return p

def walk(t, speed=1.6, amp=24):
    ph = t * speed * 2 * math.pi
    s = math.sin(ph)
    return dict(lt=amp * s, rt=-amp * s, lk=12 + 18 * max(0, -s), rk=12 + 18 * max(0, s),
                ls=-14 * s, rs=14 * s, le=18, re=18, lean=4, head=0)

def mix(a, b, u):
    return {k: lerp(a[k], b[k], u) for k in a}

# ---------------- drawing primitives ----------------
def seg(x, y, ang, L, face=1):
    r = math.radians(ang)
    return x + face * L * math.sin(r), y + L * math.cos(r)

def draw_figure(cr, x, ground, p, s=1.0, face=1, color=INK, prop=None):
    """Silhouette person. Returns dict of joint positions (for props / emitters)."""
    T, L1, L2, UA, LA, HR = 60*s, 43*s, 43*s, 34*s, 32*s, 12.5*s
    def leg_depth(a, k):
        return L1 * math.cos(math.radians(a)) + L2 * math.cos(math.radians(a - k))
    hip_y = ground - max(leg_depth(p["lt"], p["lk"]), leg_depth(p["rt"], p["rk"]), 8*s) - 2*s
    hip = (x, hip_y)
    lean = math.radians(p["lean"])
    sh = (x + face * T * math.sin(lean), hip_y - T * math.cos(lean))
    hd_a = math.radians(p["lean"] + p["head"])
    neck = (sh[0] + face * 7*s * math.sin(hd_a), sh[1] - 7*s * math.cos(hd_a))
    head = (neck[0] + face * HR * math.sin(hd_a), neck[1] - HR * math.cos(hd_a))
    J = {"hip": hip, "sh": sh, "head": head}
    cr.set_source_rgb(*color)
    cr.set_line_cap(cairo.LINE_CAP_ROUND); cr.set_line_join(cairo.LINE_JOIN_ROUND)

    def limb(start, a1, l1, a2, l2, w1, w2, key):
        k = seg(*start, a1, l1, face); e = seg(*k, a2, l2, face)
        cr.set_line_width(w1); cr.move_to(*start); cr.line_to(*k); cr.stroke()
        cr.set_line_width(w2); cr.move_to(*k); cr.line_to(*e); cr.stroke()
        J[key] = e; J[key + "_mid"] = k
        return e
    # far limbs slightly lighter for depth
    far = tuple(min(1, c + 0.10) for c in color)
    cr.set_source_rgb(*far)
    limb(hip, p["rt"], L1, p["rt"] - p["rk"], L2, 11*s, 9*s, "rfoot")
    shoulder = (sh[0] - face*1*s, sh[1] + 5*s)
    limb(shoulder, p["ls"], UA, p["ls"] + p["le"], LA, 8*s, 7*s, "lhand")
    if prop == "bag":  # seed bag on far hip
        cr.set_source_rgb(*color)
        cr.save(); cr.translate(hip[0] - face*10*s, hip[1] - 10*s); cr.scale(13*s, 16*s)
        cr.arc(0, 0, 1, 0, 2*math.pi); cr.restore(); cr.fill()
        cr.set_line_width(3*s); cr.move_to(hip[0]-face*10*s, hip[1]-24*s); cr.line_to(sh[0]+face*4*s, sh[1]+2*s); cr.stroke()
    cr.set_source_rgb(*color)
    limb(hip, p["lt"], L1, p["lt"] - p["lk"], L2, 12*s, 10*s, "lfoot")
    # torso (tapered)
    cr.set_line_width(19*s); cr.move_to(hip[0], hip[1]-4*s); cr.line_to(sh[0], sh[1]+6*s); cr.stroke()
    cr.set_line_width(7*s); cr.move_to(*sh); cr.line_to(*neck); cr.stroke()
    cr.save(); cr.translate(*head); cr.rotate(face * hd_a); cr.scale(1.0, 1.15)
    cr.arc(0, 0, HR, 0, 2*math.pi); cr.restore(); cr.fill()
    if prop in ("robe", "robe_hat"):
        hb = (hip[0] - face*2*s, hip[1] - 6*s)
        cr.move_to(sh[0] - 9*s, sh[1] + 4*s); cr.line_to(sh[0] + 9*s, sh[1] + 4*s)
        hem = min(ground - 14*s, hip[1] + 62*s)
        cr.line_to(hb[0] + 20*s, hem); cr.line_to(hb[0] - 20*s, hem); cr.close_path(); cr.fill()
    if prop == "robe_hat":
        cr.save(); cr.translate(*head); cr.rotate(face * hd_a)
        cr.rectangle(-9*s, -HR*1.15 - 13*s, 18*s, 14*s); cr.fill(); cr.restore()
    limb(shoulder, p["rs"], UA, p["rs"] + p["re"], LA, 9*s, 7.5*s, "rhand")
    return J

def draw_rotated(cr, x, gy, rot_deg, p, s=1.0, face=1, prop=None, color=INK, lift=0):
    """Figure rotated about its feet (rot -90 = lying with head to the left, when face=1)."""
    cr.save(); cr.translate(x, gy - lift); cr.rotate(math.radians(rot_deg))
    J = draw_figure(cr, 0, 0, p, s=s, face=face, prop=prop, color=color); cr.restore(); return J

def ground_line(cr, y, x0=0, x1=W, w=4):
    cr.set_source_rgb(*INK); cr.set_line_width(w); cr.move_to(x0, y); cr.line_to(x1, y); cr.stroke()

def sun(cr, x, y, r=30, rays=10, color=INK):
    cr.set_source_rgb(*color); cr.set_line_width(4)
    cr.arc(x, y, r, 0, 2*math.pi); cr.stroke()
    for i in range(rays):
        a = i * 2*math.pi/rays
        cr.move_to(x + math.cos(a)*(r+10), y + math.sin(a)*(r+10))
        cr.line_to(x + math.cos(a)*(r+22), y + math.sin(a)*(r+22)); cr.stroke()

def bird(cr, x, y, flap, s=1.0, face=-1, color=INK):
    """flap in [-1,1]; face -1 = looking left."""
    cr.set_source_rgb(*color)
    cr.save(); cr.translate(x, y); cr.scale(face*s, s)
    cr.save(); cr.scale(14, 7); cr.arc(0, 0, 1, 0, 2*math.pi); cr.restore(); cr.fill()
    cr.arc(12, -5, 5.5, 0, 2*math.pi); cr.fill()
    cr.move_to(16, -6); cr.line_to(23, -4); cr.line_to(16, -2); cr.fill()      # beak
    cr.move_to(-12, -1); cr.line_to(-24, -7); cr.line_to(-22, 3); cr.fill()      # tail
    wy = -22 * flap
    cr.set_line_width(5); cr.move_to(-2, -2); cr.curve_to(-6, wy*0.6-4, -14, wy-2, -18, wy); cr.stroke()
    cr.restore()

def sprout(cr, x, gy, h, wither=0.0, s=1.0):
    """Small seedling; wither 0..1 bends it over and fades it."""
    if h <= 0.5: return
    col = tuple(lerp(INK[i], SOFT[i], wither) for i in range(3))
    cr.set_source_rgb(*col); cr.set_line_width(3*s)
    bend = wither * 1.3
    tipx = x + math.sin(bend) * h; tipy = gy - math.cos(bend) * h * (1 - 0.35*wither)
    cr.move_to(x, gy); cr.curve_to(x, gy - h*0.6, tipx - (tipx-x)*0.2, tipy, tipx, tipy); cr.stroke()
    lf = min(1, h / 18) * 7 * s * (1 - 0.3*wither)
    for d in (-1, 1):
        cr.save(); cr.translate(tipx, tipy); cr.rotate(d*0.9 + bend*0.8); cr.scale(lf, lf*0.42)
        cr.arc(d*1.0, 0, 1, 0, 2*math.pi); cr.restore(); cr.fill()

def wheat(cr, x, gy, h, sway=0.0, grain=1.0):
    cr.set_source_rgb(*INK); cr.set_line_width(3)
    tx = x + sway * h * 0.12; ty = gy - h
    cr.move_to(x, gy); cr.curve_to(x, gy - h*0.5, tx, ty + h*0.3, tx, ty); cr.stroke()
    # leaves
    for f, d in ((0.35, 1), (0.55, -1)):
        if h > 40:
            ly = gy - h*f; lx = x + sway*h*0.12*f
            cr.move_to(lx, ly); cr.curve_to(lx + d*14, ly - 6, lx + d*22, ly - 2, lx + d*26, ly + 6); cr.stroke()
    if grain > 0 and h > 30:
        n = 6
        for i in range(n):
            u = i / (n - 1); yy = ty + 4 + u * 34 * grain; sz = 4.5 * grain * (1 - 0.3*u)
            for d in (-1, 1):
                cr.save(); cr.translate(tx + d*4*grain, yy); cr.rotate(d*0.5); cr.scale(sz, sz*1.7)
                cr.arc(0, 0, 1, 0, 2*math.pi); cr.restore(); cr.fill()
        cr.move_to(tx, ty + 2); cr.line_to(tx + sway*3, ty - 16*grain); cr.stroke()  # awn

def seed_dot(cr, x, y, r=3.4, color=INK):
    cr.set_source_rgb(*color); cr.save(); cr.translate(x, y); cr.scale(r, r*0.7)
    cr.arc(0, 0, 1, 0, 2*math.pi); cr.restore(); cr.fill()

# ---------------- text ----------------
def wrap(cr, text, maxw):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if cr.text_extents(t).x_advance > maxw and cur:
            lines.append(cur); cur = w_
        else: cur = t
    if cur: lines.append(cur)
    return lines

def text_block(cr, text, x, y, size, maxw, face="Lora", slant=cairo.FONT_SLANT_NORMAL,
               weight=cairo.FONT_WEIGHT_NORMAL, color=INK, alpha=1.0, lh=1.32, align="left"):
    cr.select_font_face(face, slant, weight); cr.set_font_size(size)
    lines = [ln for para in text.split("\n") for ln in wrap(cr, para, maxw)]
    cr.set_source_rgba(*color, alpha)
    for i, ln in enumerate(lines):
        ext = cr.text_extents(ln)
        xx = x if align == "left" else (x - ext.x_advance/2 if align == "center" else x - ext.x_advance)
        cr.move_to(xx, y + i * size * lh); cr.show_text(ln)
    return y + len(lines) * size * lh

# ---------------- music (original, synthesized) ----------------
def make_music(path, dur, bpm=72, seed=3):
    sr = 44100; n = int(sr * dur); out = np.zeros(n)
    beat = 60 / bpm / 2
    # D major-ish gentle progression: D, Bm, G, A
    chords = [[62, 66, 69, 74], [59, 62, 66, 71], [55, 59, 62, 67], [57, 61, 64, 69]]
    t_ = 0; i = 0
    def note(m, start, length, amp):
        f = 440 * 2 ** ((m - 69) / 12); s0 = int(start * sr); L = int(length * sr)
        if s0 >= n: return
        L = min(L, n - s0); tt = np.arange(L) / sr
        env = np.exp(-tt * 2.2) * np.minimum(1, tt / 0.008)
        w = np.sin(2*np.pi*f*tt) + 0.35*np.sin(4*np.pi*f*tt)*np.exp(-tt*4) + 0.12*np.sin(6*np.pi*f*tt)*np.exp(-tt*6)
        out[s0:s0+L] += amp * env * w
    while t_ < dur - 0.2:
        ch = chords[(i // 8) % 4]
        order = [0, 1, 2, 3, 2, 1, 2, 3]
        note(ch[order[i % 8]] + 12, t_, 2.5, 0.16)
        if i % 8 == 0:
            note(ch[0] - 12, t_, 4.0, 0.22); note(ch[0], t_, 4.0, 0.08)
        t_ += beat; i += 1
    # soft pad
    tt = np.arange(n) / sr
    for m in (50, 57, 62):
        f = 440 * 2 ** ((m - 69) / 12); out += 0.03 * np.sin(2*np.pi*f*tt) * (0.6 + 0.4*np.sin(2*np.pi*tt/8))
    fade = int(0.6 * sr); out[:fade] *= np.linspace(0, 1, fade); out[-fade:] *= np.linspace(1, 0, fade)
    # simple reverb-ish echo
    for d, g in ((0.11, 0.25), (0.23, 0.15), (0.37, 0.08)):
        k = int(d * sr); out[k:] += g * out[:-k].copy()
    out = out / (np.abs(out).max() + 1e-9) * 0.5
    pcm = (out * 32767).astype(np.int16)
    import wave
    with wave.open(path, "wb") as wf:
        wf.setnchannels(1); wf.setsampwidth(2); wf.setframerate(sr); wf.writeframes(pcm.tobytes())

# ---------------- renderer ----------------
class Episode:
    """Subclass: set dur, header, captions(3 x (text, ref, t_in)), cta; implement draw_panel(cr, i, t, y0, gy)."""
    dur = 18.0
    loop_fade = 0.8
    series = "DAILY VERSE PARABLES"
    kicker = ""
    headline = ""
    captions = []
    cta = "Read it in Scroll the Catholic Bible"
    caption_bg = False
    ground = True

    def draw_frame(self, cr, t):
        cr.set_source_rgb(*BG); cr.paint()
        # header
        text_block(cr, self.kicker, W/2, 108, 26, 960, face="Poppins", weight=cairo.FONT_WEIGHT_BOLD,
                   color=SOFT, align="center")
        text_block(cr, self.headline, W/2, 172, 46, 980, face="Lora", color=INK, align="center", lh=1.2)
        for i in range(3):
            y0 = HEADER_H + i * PANEL_H; gy = y0 + GROUND_OFF
            cr.save(); cr.rectangle(0, y0, W, PANEL_H); cr.clip()
            self.draw_panel(cr, i, t, y0, gy)
            txt, ref, t_in = self.captions[i]
            a = prog(t, t_in, t_in + 0.6)
            if a > 0 and self.caption_bg:
                cr.select_font_face("Lora", cairo.FONT_SLANT_ITALIC, cairo.FONT_WEIGHT_NORMAL); cr.set_font_size(31)
                nl = len(wrap(cr, txt, 700)); hh = nl * 31 * 1.28 + 52
                cr.set_source_rgba(*BG, 0.92 * a); rr = 18; bx, by, bw = 30, y0 + 18, 740
                cr.new_sub_path(); cr.arc(bx + bw - rr, by + rr, rr, -math.pi/2, 0); cr.arc(bx + bw - rr, by + hh - rr, rr, 0, math.pi/2)
                cr.arc(bx + rr, by + hh - rr, rr, math.pi/2, math.pi); cr.arc(bx + rr, by + rr, rr, math.pi, 3*math.pi/2); cr.close_path(); cr.fill()
            if a > 0:
                yy = text_block(cr, txt, 48, y0 + 52, 31, 700, slant=cairo.FONT_SLANT_ITALIC, alpha=a, lh=1.28)
                text_block(cr, ref.upper(), 48, yy + 6, 21, 700, face="Poppins",
                           weight=cairo.FONT_WEIGHT_BOLD, color=SOFT, alpha=a)
            cr.restore()
            if self.ground: ground_line(cr, gy)
        # footer
        text_block(cr, self.cta, W/2, FOOTER_Y + 95, 30, 960, face="Poppins", weight=cairo.FONT_WEIGHT_NORMAL,
                   color=INK, align="center")
        text_block(cr, self.series + "  •  CPDV", W/2, FOOTER_Y + 145, 20, 960, face="Poppins",
                   weight=cairo.FONT_WEIGHT_BOLD, color=SOFT, align="center")

    def render(self, out_mp4, music=True, preview_times=None):
        surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); cr = cairo.Context(surf)
        start = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); self.draw_frame(cairo.Context(start), 0.0)
        def frame(t):
            self.draw_frame(cr, t)
            u = prog(t, self.dur - self.loop_fade, self.dur)
            if u > 0:
                cr.set_source_surface(start, 0, 0); cr.paint_with_alpha(u)
            surf.flush(); return surf
        if preview_times:
            for tt in preview_times:
                frame(tt).write_to_png(f"{out_mp4}.t{tt:05.1f}.png")
            return
        tmp = out_mp4.replace(".mp4", ".tmp.mp4"); silent = out_mp4.replace(".mp4", ".silent.mp4")
        p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}",
                              "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
                              "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
        for k in range(int(self.dur * FPS)):
            p.stdin.write(bytes(frame(k / FPS).get_data()))
        p.stdin.close(); assert p.wait() == 0
        os.replace(tmp, silent)
        wav = out_mp4.replace(".mp4", ".wav"); make_music(wav, self.dur)
        tmp2 = out_mp4.replace(".mp4", ".tmp2.mp4")
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", silent, "-i", wav, "-map", "0:v", "-map", "1:a",
                        "-c:v", "copy", "-c:a", "aac", "-b:a", "160k", "-shortest", "-movflags", "+faststart", tmp2], check=True)
        os.replace(tmp2, out_mp4); os.remove(silent); os.remove(wav)

# ---------------- helpers for episodes ----------------
def cpdv(book, ch, vs, part):
    """Caption text that must be verbatim CPDV (ellipses allowed at the ends)."""
    full = verse(book, ch, vs); pos = 0
    for piece in [x.strip().rstrip(",") for x in part.split("\u2026") if x.strip()]:
        k = full.find(piece, pos)
        assert k >= 0, f"Not verbatim CPDV {book} {ch}:{vs}: {piece!r}"
        pos = k + len(piece)
    return part

def track(t, keys):
    """keys [(time, x)] -> (x, walk_amount 0..1, direction +1/-1)."""
    K = [(a, {"x": b}) for a, b in keys]
    x = keyed(K, t)["x"]; x2 = keyed(K, t + 0.05)["x"]
    v = (x2 - x) / 0.05
    return x, clamp(abs(v) / 70.0), (1 if v >= 0 else -1)

def body(t, base, walk_amt, speed=1.6):
    return mix(base, walk(t, speed=speed), walk_amt) if walk_amt > 0 else base
