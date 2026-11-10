"""Reusable props for Daily Verse Parables."""
import math, cairo
from engine import INK, BG, SOFT, W, lerp, clamp

def house(cr, x, gy, w=230, h=250, door_open=0.0, light=0.0):
    """Wall with door at its left side. x = left edge. door_open 0..1, light 0..1."""
    dx, dw, dh = x + 40, 72, 150
    if light > 0:  # light spilling out of door onto ground
        cr.set_source_rgba(1, 0.97, 0.82, 0.9 * light)
        cr.move_to(dx, gy); cr.line_to(dx + dw, gy); cr.line_to(dx + dw - 30, gy - dh + 2)
        cr.line_to(dx - 160 * light, gy); cr.close_path(); cr.fill()
        g = cairo.RadialGradient(dx + dw/2, gy - dh/2, 10, dx + dw/2, gy - dh/2, 260 * light)
        g.add_color_stop_rgba(0, 1, 0.96, 0.78, 0.55 * light); g.add_color_stop_rgba(1, 1, 0.96, 0.78, 0)
        cr.set_source(g); cr.rectangle(dx - 300, gy - 400, 700, 400); cr.fill()
    cr.set_source_rgb(*INK); cr.set_line_width(5)
    cr.move_to(x, gy); cr.line_to(x, gy - h); cr.line_to(x + w, gy - h); cr.stroke()
    cr.move_to(x - 18, gy - h); cr.line_to(x + w/2, gy - h - 70); cr.line_to(x + w + 18, gy - h); cr.stroke()
    # door frame
    cr.set_line_width(4); cr.rectangle(dx, gy - dh, dw, dh); cr.stroke()
    if light > 0:
        cr.set_source_rgba(1, 0.97, 0.84, light); cr.rectangle(dx + 2, gy - dh + 2, dw - 4, dh - 4); cr.fill()
    # door leaf (swings inward: gets narrower)
    lw = dw * (1 - 0.85 * door_open)
    cr.set_source_rgb(*INK); cr.rectangle(dx + dw - lw, gy - dh, lw, dh); cr.fill()
    if door_open < 0.5:
        cr.set_source_rgb(*BG); cr.arc(dx + dw - lw + 12, gy - dh/2, 4, 0, 2*math.pi); cr.fill()
    # window
    cr.set_source_rgb(*INK); cr.set_line_width(4); cr.rectangle(x + 145, gy - 190, 55, 55); cr.stroke()
    cr.move_to(x + 172, gy - 190); cr.line_to(x + 172, gy - 135); cr.stroke()
    return (dx, dw, dh)

def coin(cr, x, y, r=11, alpha=1.0):
    cr.set_source_rgba(*INK, alpha); cr.arc(x, y, r, 0, 2*math.pi); cr.fill()
    cr.set_source_rgba(*BG, alpha); cr.set_line_width(2); cr.arc(x, y, r*0.62, 0, 2*math.pi); cr.stroke()

def coin_stack(cr, x, gy, n, r=14):
    """n coins (float allows the top coin to pop in). Stacks in columns of 5."""
    full = int(n); frac = n - full
    for k in range(full + (1 if frac > 0.02 else 0)):
        col, row = divmod(k, 5)
        a = 1.0 if k < full else frac
        coin(cr, x + col * (2*r + 6), gy - r - row * (r * 0.9) - (1 - a) * 30, r, a)

def lamp(cr, x, y, lit=0.0, flicker=0.0):
    """Small oil lamp; (x,y) = base centre."""
    cr.set_source_rgb(*INK)
    cr.save(); cr.translate(x, y - 8); cr.scale(20, 9); cr.arc(0, 0, 1, 0, math.pi); cr.restore(); cr.fill()
    cr.move_to(x + 14, y - 10); cr.line_to(x + 28, y - 16); cr.line_to(x + 18, y - 6); cr.fill()
    cr.set_line_width(3); cr.arc(x - 22, y - 10, 6, math.pi/2, 3*math.pi/2); cr.stroke()
    if lit > 0:
        f = 1 + 0.08 * math.sin(flicker * 13) + 0.05 * math.sin(flicker * 29)
        cr.save(); cr.translate(x + 26, y - 26); cr.scale(6 * lit * f, 13 * lit * f)
        cr.set_source_rgba(1, 0.75, 0.25, 1); cr.arc(0, 0, 1, 0, 2*math.pi); cr.restore(); cr.fill()
    return (x + 26, y - 26)

def lampstand(cr, x, gy, h=150):
    cr.set_source_rgb(*INK); cr.set_line_width(6)
    cr.move_to(x, gy); cr.line_to(x, gy - h); cr.stroke()
    cr.move_to(x - 30, gy); cr.line_to(x + 30, gy); cr.stroke()
    cr.move_to(x - 26, gy - h); cr.line_to(x + 26, gy - h); cr.stroke()
    return gy - h - 3

def basket(cr, x, y, w=70, h=48):
    """Upside-down basket whose rim sits at y."""
    cr.set_source_rgb(*INK)
    cr.move_to(x - w/2, y); cr.line_to(x - w/2 + 10, y - h); cr.line_to(x + w/2 - 10, y - h); cr.line_to(x + w/2, y); cr.close_path(); cr.fill()
    cr.set_source_rgb(*BG); cr.set_line_width(2)
    for k in range(1, 4):
        yy = y - k * h / 4; cr.move_to(x - w/2 + 3 + k*2.5, yy); cr.line_to(x + w/2 - 3 - k*2.5, yy); cr.stroke()

def darkness(cr, y0, ph, amount, lights=()):
    """Night overlay on a panel; lights = [(x, y, radius, strength)] punch warm holes."""
    if amount <= 0: return
    cr.save(); cr.rectangle(0, y0, W, ph); cr.clip()
    cr.push_group()
    cr.set_source_rgba(0.06, 0.06, 0.09, 0.88 * amount); cr.paint()
    cr.set_operator(cairo.OPERATOR_DEST_OUT)
    for (x, y, r, st) in lights:
        if r <= 1 or st <= 0: continue
        g = cairo.RadialGradient(x, y, 0, x, y, r)
        g.add_color_stop_rgba(0, 0, 0, 0, st); g.add_color_stop_rgba(0.55, 0, 0, 0, st * 0.8); g.add_color_stop_rgba(1, 0, 0, 0, 0)
        cr.set_source(g); cr.paint()
    cr.pop_group_to_source(); cr.paint()
    cr.set_operator(cairo.OPERATOR_OVER)
    for (x, y, r, st) in lights:  # warm tint
        if r <= 1 or st <= 0: continue
        g = cairo.RadialGradient(x, y, 0, x, y, r)
        g.add_color_stop_rgba(0, 1, 0.8, 0.4, 0.22 * st); g.add_color_stop_rgba(1, 1, 0.8, 0.4, 0)
        cr.set_source(g); cr.paint()
    cr.restore()

def water(cr, gy, t, x0=0, x1=W, amp=6, rough=1.0, below=70):
    """Covers everything below the wavy surface with background, then draws the surface line."""
    pts = []
    for x in range(int(x0), int(x1) + 10, 10):
        pts.append((x, gy + amp * rough * math.sin(x * 0.03 + t * 2.4) + 2 * rough * math.sin(x * 0.11 - t * 3.1)))
    cr.set_source_rgb(*BG); cr.move_to(x0, gy + below)
    for (x, y) in pts: cr.line_to(x, y)
    cr.line_to(x1, gy + below); cr.close_path(); cr.fill()
    cr.set_source_rgb(*INK); cr.set_line_width(4); cr.move_to(*pts[0])
    for (x, y) in pts[1:]: cr.line_to(x, y)
    cr.stroke()
    cr.set_line_width(2.5)
    for k in range(6):
        xx = (x0 + 70 + k * 170 + t * 30 * (1 + rough)) % (x1 - x0) + x0
        yy = gy + 22 + (k % 2) * 18
        cr.move_to(xx, yy); cr.curve_to(xx + 10, yy - 6, xx + 20, yy - 6, xx + 30, yy); cr.stroke()

def surface_y(x, gy, t, amp=6, rough=1.0):
    return gy + amp * rough * math.sin(x * 0.03 + t * 2.4) + 2 * rough * math.sin(x * 0.11 - t * 3.1)

def boat(cr, x, y, w=210, bob=0.0):
    """Hull centred at x, gunwale at y."""
    y += bob
    cr.set_source_rgb(*INK)
    cr.move_to(x - w/2 - 15, y); cr.line_to(x + w/2 + 15, y)
    cr.curve_to(x + w/2, y + 34, x + w/3, y + 42, x, y + 42)
    cr.curve_to(x - w/3, y + 42, x - w/2, y + 34, x - w/2 - 15, y); cr.close_path(); cr.fill()
    cr.set_line_width(5); cr.move_to(x - 30, y); cr.line_to(x - 30, y - 210); cr.stroke()
    cr.set_line_width(3); cr.move_to(x - 26, y - 200); cr.curve_to(x + 40, y - 150, x + 40, y - 70, x - 26, y - 20); cr.stroke()

def wind(cr, y0, t, strength=1.0):
    if strength <= 0: return
    cr.set_source_rgba(*INK, 0.55 * strength); cr.set_line_width(3)
    for k in range(5):
        xx = ((t * 520 + k * 260) % 1400) - 200; yy = y0 + 150 + k * 37
        cr.move_to(xx, yy); cr.curve_to(xx + 60, yy - 10, xx + 110, yy + 8, xx + 150, yy - 4); cr.stroke()

def rock_path_tufts(cr, gy, xs):
    cr.set_source_rgb(*INK); cr.set_line_width(2.5)
    for x in xs:
        for d in (-6, 0, 6):
            cr.move_to(x, gy); cr.line_to(x + d, gy - 12 + abs(d)); cr.stroke()

# ---- props added for days 1b-7b ----
def run(t, speed=2.4, amp=40):
    ph = t * speed * 2 * math.pi; s = math.sin(ph)
    return dict(lt=amp * s, rt=-amp * s, lk=30 + 50 * max(0, -s), rk=30 + 50 * max(0, s),
                ls=-45 * s + 20, rs=45 * s + 20, le=80, re=80, lean=14, head=-4)

def offertory_box(cr, x, gy, glow=0.0):
    cr.set_source_rgb(*INK)
    cr.rectangle(x - 45, gy - 95, 90, 95); cr.fill()
    cr.rectangle(x - 55, gy - 105, 110, 14); cr.fill()
    cr.set_source_rgb(*BG); cr.rectangle(x - 18, gy - 101, 36, 5); cr.fill()
    if glow > 0:
        g = cairo.RadialGradient(x, gy - 100, 0, x, gy - 100, 380 * glow)
        g.add_color_stop_rgba(0, 1, 0.85, 0.45, 0.55 * glow); g.add_color_stop_rgba(1, 1, 0.85, 0.45, 0)
        cr.set_source(g); cr.rectangle(x - 500, gy - 500, 1000, 500); cr.fill()
        cr.set_source_rgba(1, 0.8, 0.35, 0.8 * glow); cr.set_line_width(3)
        for k in range(9):
            a = math.pi + (k + 0.5) * math.pi / 9
            cr.move_to(x + math.cos(a) * 40, gy - 110 + math.sin(a) * 40)
            cr.line_to(x + math.cos(a) * (60 + 70 * glow), gy - 110 + math.sin(a) * (60 + 70 * glow)); cr.stroke()

def temple(cr, x, gy, w=300, h=230):
    cr.set_source_rgb(*INK); cr.set_line_width(5)
    cr.rectangle(x, gy - 14, w, 14); cr.fill()
    for k in range(4):
        cx = x + 30 + k * (w - 60) / 3
        cr.rectangle(cx - 9, gy - h, 18, h - 14); cr.fill()
    cr.rectangle(x - 10, gy - h - 18, w + 20, 18); cr.fill()
    cr.move_to(x - 10, gy - h - 18); cr.line_to(x + w / 2, gy - h - 80); cr.line_to(x + w + 10, gy - h - 18); cr.close_path(); cr.stroke()

def vines(cr, x0, x1, gy, t=0.0, h=120):
    cr.set_source_rgb(*INK); cr.set_line_width(4)
    posts = list(range(int(x0), int(x1) + 1, 110))
    for px in posts:
        cr.move_to(px, gy); cr.line_to(px, gy - h); cr.stroke()
    cr.set_line_width(2); cr.move_to(x0, gy - h + 10); cr.line_to(x1, gy - h + 10); cr.stroke()
    for k, px in enumerate(posts[:-1]):
        for j in range(3):
            lx = px + 25 + j * 30 + 3 * math.sin(t * 1.5 + k + j); ly = gy - h + 18
            cr.save(); cr.translate(lx, ly); cr.scale(11, 7); cr.arc(0, 0, 1, 0, 2 * math.pi); cr.restore(); cr.fill()
            for g in range(4):
                cr.arc(lx - 3 + (g % 2) * 6, ly + 12 + g * 6, 3.6, 0, 2 * math.pi); cr.fill()

def snow(cr, y0, ph, t, n=70, seed=5):
    import random as _r
    r = _r.Random(seed); cr.set_source_rgba(*SOFT, 0.85)
    for k in range(n):
        x0 = r.uniform(0, W); sp = r.uniform(25, 55); ph0 = r.uniform(0, ph); sz = r.uniform(1.8, 3.6)
        y = y0 + ((ph0 + t * sp) % ph); x = x0 + 12 * math.sin(t * 0.8 + k)
        cr.arc(x, y, sz, 0, 2 * math.pi); cr.fill()

def cross(cr, x, gy, h=150, glow=0.0):
    if glow > 0:
        g = cairo.RadialGradient(x, gy - h * 0.7, 0, x, gy - h * 0.7, 260 * glow)
        g.add_color_stop_rgba(0, 1, 0.88, 0.5, 0.6 * glow); g.add_color_stop_rgba(1, 1, 0.88, 0.5, 0)
        cr.set_source(g); cr.rectangle(x - 300, gy - 450, 600, 450); cr.fill()
    cr.set_source_rgb(*INK); cr.set_line_width(9)
    cr.move_to(x, gy); cr.line_to(x, gy - h); cr.stroke()
    cr.move_to(x - h * 0.3, gy - h * 0.72); cr.line_to(x + h * 0.3, gy - h * 0.72); cr.stroke()

def burden(cr, x, y, w=34, h=30, color=INK):
    cr.set_source_rgb(*color); r = 6
    cr.new_sub_path(); cr.arc(x + w - r, y + r, r, -math.pi / 2, 0); cr.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    cr.arc(x + r, y + h - r, r, math.pi / 2, math.pi); cr.arc(x + r, y + r, r, math.pi, 3 * math.pi / 2); cr.close_path(); cr.fill()
    cr.set_source_rgb(*BG); cr.set_line_width(2); cr.move_to(x + w / 2, y + 3); cr.line_to(x + w / 2, y + h - 3); cr.stroke()

def flask(cr, x, y):
    cr.set_source_rgb(*INK)
    cr.save(); cr.translate(x, y); cr.scale(9, 12); cr.arc(0, 0, 1, 0, 2 * math.pi); cr.restore(); cr.fill()
    cr.rectangle(x - 3, y - 20, 6, 10); cr.fill()

def loaf(cr, x, y):
    cr.set_source_rgb(*INK); cr.save(); cr.translate(x, y); cr.scale(15, 9); cr.arc(0, 0, 1, 0, 2 * math.pi); cr.restore(); cr.fill()
    cr.set_source_rgb(*BG); cr.set_line_width(2)
    for d in (-6, 0, 6): cr.move_to(x + d - 2, y - 6); cr.line_to(x + d + 2, y - 1); cr.stroke()

def finish_line(cr, x, gy, h=140):
    cr.set_source_rgb(*INK); cr.set_line_width(5)
    cr.move_to(x, gy); cr.line_to(x, gy - h); cr.stroke()
    for k in range(4):
        for j in range(3):
            if (k + j) % 2 == 0: cr.rectangle(x + k * 13, gy - h + j * 13, 13, 13); cr.fill()
    cr.set_line_width(2); cr.rectangle(x, gy - h, 52, 39); cr.stroke()
