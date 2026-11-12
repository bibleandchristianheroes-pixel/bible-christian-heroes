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

# ---- props added for day 8 (Two Builders, Lost Sheep) ----
def rock_mound(cr, x0, x1, gy, h=40, slope=60):
    """Flat-topped rock from x0 to x1 (slopes included). Returns (top_y, plateau_x0, plateau_x1)."""
    top = gy - h; px0, px1 = x0 + slope, x1 - slope
    cr.set_source_rgb(*INK)
    cr.move_to(x0, gy + 2); cr.curve_to(x0 + slope * 0.4, gy - h * 0.2, x0 + slope * 0.6, top, px0, top)
    cr.line_to(px1, top); cr.curve_to(x1 - slope * 0.6, top, x1 - slope * 0.4, gy - h * 0.2, x1, gy + 2)
    cr.close_path(); cr.fill()
    cr.set_source_rgb(*BG); cr.set_line_width(2.5)
    for cx in (px0 + 40, px0 + 150, px1 - 60):
        cr.move_to(cx, top + 8); cr.line_to(cx + 10, top + 20); cr.line_to(cx + 4, top + h - 6); cr.stroke()
    return top, px0, px1

def rock_y(x, x0, x1, gy, h=40, slope=60):
    """Standing height on a rock_mound at x (gy off the rock)."""
    if x <= x0 or x >= x1: return gy
    if x < x0 + slope: return gy - h * smooth_(x, x0, x0 + slope)
    if x > x1 - slope: return gy - h * (1 - smooth_(x, x1 - slope, x1))
    return gy - h

def smooth_(x, a, b):
    u = clamp((x - a) / (b - a)); return u * u * (3 - 2 * u)

def sand(cr, x0, x1, gy, n=70):
    cr.set_source_rgb(*INK)
    for k in range(n):
        cr.arc(x0 + (k * 97) % (x1 - x0), gy + 9 + (k * 31) % 40, 1.5, 0, 2 * math.pi); cr.fill()
    cr.set_line_width(2)
    for k in range(5):
        x = x0 + 30 + k * (x1 - x0 - 60) / 4
        cr.move_to(x, gy - 1); cr.curve_to(x + 10, gy - 6, x + 26, gy - 6, x + 36, gy - 1); cr.stroke()

HOUSE_W, HOUSE_H, HOUSE_ROOF = 150, 110, 55
def small_house(cr, x, base_y, built=1.0, tilt=0.0, sink=0.0, collapse=0.0, light=0.0):
    """Silhouette house, x = centre, base_y = floor. built 0..1 rises from the floor; tilt in degrees;
    collapse 0..1 breaks it into a rubble heap (left wall, right wall, roof, beams fall at staggered times)."""
    w, h, r = HOUSE_W, HOUSE_H, HOUSE_ROOF
    if built <= 0: return
    cr.save()
    cr.rectangle(x - 400, base_y - 400, 800, 400 + 0.5); cr.clip()   # nothing shows below the floor
    cr.translate(x, base_y + sink)
    if collapse <= 0:
        cr.rotate(math.radians(tilt))
        reveal = (h + r) * built
        cr.save(); cr.rectangle(-w, -reveal, 2 * w, reveal + 1); cr.clip()
        cr.set_source_rgb(*INK)
        cr.rectangle(-w / 2, -h, w, h); cr.fill()
        cr.move_to(-w / 2 - 14, -h + 1); cr.line_to(0, -h - r); cr.line_to(w / 2 + 14, -h + 1); cr.close_path(); cr.fill()
        # door + window cut-outs (lit when light > 0)
        dc = tuple(lerp(BG[j], (1, 0.85, 0.45)[j], light) for j in range(3))
        cr.set_source_rgb(*dc); cr.rectangle(-w / 2 + 22, -62, 32, 62); cr.fill()
        cr.rectangle(w / 2 - 56, -82, 32, 30); cr.fill()
        cr.set_source_rgb(*INK); cr.set_line_width(3); cr.move_to(w / 2 - 40, -82); cr.line_to(w / 2 - 40, -52); cr.stroke()
        cr.restore()
    else:
        cr.rotate(math.radians(tilt))
        # pieces: (polygon, pivot, final_dx, final_dy, final_rot_deg, delay)
        P = [
            ([(-w/2, -h), (-w/2 + 26, -h), (-w/2 + 26, 0), (-w/2, 0)], (-w/2, 0), -40, 0, -90, 0.10),   # left wall
            ([(w/2 - 26, -h), (w/2, -h), (w/2, 0), (w/2 - 26, 0)], (w/2, 0), 30, 0, 90, 0.00),          # right wall
            ([(-w/2 + 26, -h), (w/2 - 26, -h), (w/2 - 26, -h + 24), (-w/2 + 26, -h + 24)], (0, -h), 10, h - 24, 12, 0.25),  # beam
            ([(-w/2 - 14, -h + 1), (0, -h - r), (w/2 + 14, -h + 1)], (0, -h), 25, h - 2, -18, 0.18),    # roof
            ([(-w/2 + 26, -70), (w/2 - 26, -70), (w/2 - 26, 0), (-w/2 + 26, 0)], (0, 0), 0, 0, 0, 0.0),   # rubble core (shrinks)
        ]
        cr.set_source_rgb(*INK)
        for k, (poly, pv, fdx, fdy, frot, dl) in enumerate(P):
            u = smooth_(collapse, dl, dl + 0.7)
            u2 = u * u
            cr.save()
            if k == 4:
                cr.translate(0, 0); cr.scale(1, max(0.3, 1 - 0.7 * u))
            else:
                cr.translate(pv[0] + fdx * u, pv[1] + fdy * u2); cr.rotate(math.radians(frot * u)); cr.translate(-pv[0], -pv[1])
            cr.move_to(*poly[0])
            for p in poly[1:]: cr.line_to(*p)
            cr.close_path(); cr.fill(); cr.restore()
    cr.restore()

def rain(cr, y0, ph, t, amount=1.0, slant=0.35, n=90, seed=9):
    if amount <= 0: return
    import random as _r
    r = _r.Random(seed); cr.set_source_rgba(*SOFT, 0.75 * amount); cr.set_line_width(2)
    for k in range(int(n * amount)):
        x0 = r.uniform(-200, W + 100); sp = r.uniform(700, 950); ph0 = r.uniform(0, ph); L = r.uniform(18, 30)
        y = y0 + ((ph0 + t * sp) % ph); x = x0 + slant * (y - y0)
        cr.move_to(x, y); cr.line_to(x + slant * L, y + L); cr.stroke()

def warm_glow(cr, x, y, r, amount):
    if amount <= 0: return
    g = cairo.RadialGradient(x, y, 0, x, y, r)
    g.add_color_stop_rgba(0, 1, 0.86, 0.48, 0.55 * amount); g.add_color_stop_rgba(1, 1, 0.86, 0.48, 0)
    cr.set_source(g); cr.rectangle(x - r, y - r, 2 * r, 2 * r); cr.fill()

def sheep(cr, x, gy, s=1.0, face=1, graze=0.0, step=0.0, color=INK):
    """Silhouette sheep standing on gy. graze 0..1 lowers the head; step = walk phase (radians), 0 = still."""
    cr.save(); cr.translate(x, gy); cr.scale(face * s, s)
    cr.set_source_rgb(*color); cr.set_line_width(5); cr.set_line_cap(cairo.LINE_CAP_ROUND)
    for k, lx in enumerate((-20, -12, 14, 22)):
        sw = 7 * math.sin(step + (0 if k in (0, 3) else math.pi)) if step else 0
        cr.move_to(lx, -24); cr.line_to(lx + sw, 0); cr.stroke()
    cr.save(); cr.translate(0, -34); cr.scale(32, 17); cr.arc(0, 0, 1, 0, 2 * math.pi); cr.restore(); cr.fill()
    for bx, by, br in ((-22, -42, 11), (-8, -48, 12), (8, -48, 12), (22, -43, 11), (-30, -32, 9)):
        cr.arc(bx, by, br, 0, 2 * math.pi); cr.fill()
    hx, hy = lerp(36, 36, graze), lerp(-48, -14, graze)
    cr.set_line_width(10); cr.move_to(24, -38); cr.line_to(hx - 4, hy + 2); cr.stroke()
    cr.save(); cr.translate(hx, hy); cr.rotate(lerp(0.35, 1.2, graze)); cr.scale(12, 7.5); cr.arc(0, 0, 1, 0, 2 * math.pi); cr.restore(); cr.fill()
    cr.save(); cr.translate(hx - 6, hy - 6); cr.rotate(-0.6); cr.scale(7, 3); cr.arc(0, 0, 1, 0, 2 * math.pi); cr.restore(); cr.fill()
    cr.restore()

def staff(cr, x, top_y, bottom_y, color=INK):
    cr.set_source_rgb(*color); cr.set_line_width(5); cr.set_line_cap(cairo.LINE_CAP_ROUND)
    cr.move_to(x, bottom_y); cr.line_to(x, top_y); cr.stroke()
    cr.arc(x + 12, top_y, 12, math.pi, 2 * math.pi); cr.stroke()

def thornbush(cr, x, gy, s=1.0, color=INK):
    cr.set_source_rgb(*color); cr.set_line_width(3.5); cr.set_line_cap(cairo.LINE_CAP_ROUND)
    for k, (a, L) in enumerate(((-1.2, 70), (-0.7, 95), (-0.25, 110), (0.2, 100), (0.65, 90), (1.1, 70))):
        ex, ey = x + math.sin(a) * L * s, gy - math.cos(a) * L * s * 0.9
        cr.move_to(x, gy); cr.curve_to(x + (ex - x) * 0.3, gy - 30 * s, ex - (ex - x) * 0.2, ey + 20 * s, ex, ey); cr.stroke()
        for j in range(1, 4):
            u = j / 4.0; px, py = lerp(x, ex, u), lerp(gy, ey, u * 1.05)
            d = 1 if j % 2 else -1
            cr.move_to(px, py); cr.line_to(px + d * 11 * s, py - 6 * s); cr.stroke()

# ---- props added by worker 0 ----
def coin_bag(cr, x, y, s=1.0, fill=1.0, color=INK):
    """Money pouch; (x, y) = the tie at its neck. fill 0..1 shrinks it as it empties."""
    f = 0.45 + 0.55 * fill
    cr.set_source_rgb(*color)
    cr.save(); cr.translate(x, y + 16 * s * f); cr.scale(15 * s * f, 15 * s * f); cr.arc(0, 0, 1, 0, 2 * math.pi); cr.restore(); cr.fill()
    cr.move_to(x - 6 * s, y + 4 * s); cr.line_to(x - 9 * s, y - 6 * s); cr.line_to(x + 9 * s, y - 6 * s); cr.line_to(x + 6 * s, y + 4 * s); cr.close_path(); cr.fill()

def pig(cr, x, gy, s=1.0, face=1, graze=0.0, color=INK):
    """Silhouette pig standing on gy; graze 0..1 lowers the snout."""
    cr.save(); cr.translate(x, gy); cr.scale(face * s, s)
    cr.set_source_rgb(*color); cr.set_line_width(7); cr.set_line_cap(cairo.LINE_CAP_ROUND)
    for lx in (-22, -12, 14, 24):
        cr.move_to(lx, -20); cr.line_to(lx, -2); cr.stroke()
    cr.save(); cr.translate(0, -32); cr.scale(38, 20); cr.arc(0, 0, 1, 0, 2 * math.pi); cr.restore(); cr.fill()
    hy = lerp(-36, -18, graze)
    cr.save(); cr.translate(36, hy); cr.scale(16, 13); cr.arc(0, 0, 1, 0, 2 * math.pi); cr.restore(); cr.fill()
    cr.rectangle(46, hy - 6 + 2 * graze, 10, 12); cr.fill()                       # snout
    cr.move_to(30, hy - 10); cr.line_to(36, hy - 22); cr.line_to(40, hy - 10); cr.fill()   # ear
    cr.set_line_width(2.5); cr.move_to(-38, -36); cr.curve_to(-48, -44, -42, -54, -50, -50); cr.stroke()  # tail
    cr.restore()

def _leaf_blob(cr, x, y, r):
    cr.arc(x, y, r, 0, 2 * math.pi); cr.fill()

def mustard_tree(cr, x, gy, grow, sway=0.0, color=INK):
    """grow 0..1: seedling (<0.15) up to a broad tree ~290px tall. Returns perch points [(x, y)] on the branches."""
    cr.set_source_rgb(*color); cr.set_line_cap(cairo.LINE_CAP_ROUND)
    if grow <= 0: return []
    if grow < 0.15:
        u = grow / 0.15
        cr.set_line_width(3); cr.move_to(x, gy); cr.line_to(x, gy - 30 * u); cr.stroke()
        for d in (-1, 1):
            cr.save(); cr.translate(x, gy - 30 * u); cr.rotate(d * 0.9); cr.scale(8 * u, 3.5 * u)
            cr.arc(d * 1.0, 0, 1, 0, 2 * math.pi); cr.restore(); cr.fill()
        return []
    g = (grow - 0.15) / 0.85
    H = 30 + 210 * g; tw = 4 + 14 * g
    sw = sway * g
    cr.move_to(x - tw / 2, gy); cr.line_to(x - tw * 0.3 + sw * 0.3, gy - H * 0.55); cr.line_to(x + tw * 0.3 + sw * 0.3, gy - H * 0.55)
    cr.line_to(x + tw / 2, gy); cr.close_path(); cr.fill()
    perches = []
    tips = []
    cr.set_line_width(max(2.5, 7 * g))
    for d, hy, L, up in ((-1, 0.5, 0.8, 0.35), (1, 0.55, 0.8, 0.4), (-1, 0.7, 0.5, 0.55), (1, 0.75, 0.5, 0.5), (0, 0.55, 0.45, 1.0)):
        bx, by = x + sw * 0.3, gy - H * hy
        ex, ey = bx + d * H * L * 0.62 + sw, by - H * L * up
        cr.move_to(bx, by); cr.curve_to(bx + (ex - bx) * 0.3, by - 10 * g, ex - (ex - bx) * 0.3, ey + 15 * g, ex, ey); cr.stroke()
        tips.append((ex, ey))
        if d != 0: perches.append((lerp(bx, ex, 0.5), lerp(by, ey, 0.4) + 2))
    # leaf clusters at the branch tips (open, so birds stay visible)
    r = 0.13 * H * min(1, g * 1.3)
    for (ex, ey) in tips:
        for dx, dy, f in ((0, -0.4, 1.0), (-0.8, 0.1, 0.75), (0.8, 0.1, 0.75)):
            _leaf_blob(cr, ex + dx * r, ey + dy * r, r * f)
    return perches

def mountain(cr, x, gy, w=380, h=210, color=INK):
    """Two-peaked mountain whose base spans x .. x+w."""
    cr.set_source_rgb(*color)
    cr.move_to(x, gy + 2); cr.line_to(x + w * 0.32, gy - h); cr.line_to(x + w * 0.46, gy - h * 0.72)
    cr.line_to(x + w * 0.62, gy - h * 0.86); cr.line_to(x + w, gy + 2); cr.close_path(); cr.fill()
    cr.set_source_rgb(*BG); cr.set_line_width(3)
    cr.move_to(x + w * 0.32, gy - h + 6); cr.line_to(x + w * 0.28, gy - h * 0.7); cr.stroke()
    cr.move_to(x + w * 0.62, gy - h * 0.86 + 6); cr.line_to(x + w * 0.66, gy - h * 0.6); cr.stroke()

def stool(cr, x, gy, h=44, w=56, color=INK):
    cr.set_source_rgb(*color); cr.rectangle(x - w / 2, gy - h, w, 8); cr.fill()
    cr.set_line_width(5)
    for d in (-1, 1): cr.move_to(x + d * (w / 2 - 6), gy - h + 6); cr.line_to(x + d * (w / 2 - 2), gy); cr.stroke()

def cook_pot(cr, x, gy, t=0.0, fire=1.0, steam=1.0, color=INK):
    """Round pot on three stones over a small fire; x = centre."""
    cr.set_source_rgb(*color)
    for d in (-28, 0, 28): cr.arc(x + d, gy - 7, 8, math.pi, 2 * math.pi); cr.fill()
    if fire > 0:
        for k, d in enumerate((-12, 0, 12)):
            f = 1 + 0.2 * math.sin(t * 11 + k * 2)
            cr.set_source_rgba(1, 0.62, 0.2, 0.95 * fire); cr.save(); cr.translate(x + d, gy - 18); cr.scale(6, 11 * f)
            cr.arc(0, 0, 1, 0, 2 * math.pi); cr.restore(); cr.fill()
    cr.set_source_rgb(*color)
    cr.save(); cr.translate(x, gy - 52); cr.scale(36, 28); cr.arc(0, 0, 1, 0, math.pi); cr.restore(); cr.fill()
    cr.rectangle(x - 40, gy - 58, 80, 8); cr.fill()
    if steam > 0:
        cr.set_source_rgba(*SOFT, 0.7 * steam); cr.set_line_width(3)
        for k in range(3):
            u = ((t * 0.6 + k / 3.0) % 1.0); yy = gy - 66 - u * 70; xx = x - 16 + k * 16
            cr.move_to(xx, yy); cr.curve_to(xx + 8, yy - 8, xx - 8, yy - 16, xx, yy - 24); cr.stroke()

def bowl(cr, x, y, w=26, color=INK):
    """Small bowl; (x, y) = rim centre."""
    cr.set_source_rgb(*color); cr.save(); cr.translate(x, y); cr.scale(w / 2, w / 3); cr.arc(0, 0, 1, 0, math.pi); cr.restore(); cr.fill()
    cr.rectangle(x - w / 2 - 2, y - 2, w + 4, 4); cr.fill()

def low_table(cr, x, gy, w=110, h=50, color=INK):
    cr.set_source_rgb(*color); cr.rectangle(x - w / 2, gy - h, w, 8); cr.fill()
    cr.set_line_width(6)
    for d in (-1, 1): cr.move_to(x + d * (w / 2 - 10), gy - h + 6); cr.line_to(x + d * (w / 2 - 10), gy); cr.stroke()
    return gy - h

def sycamore_tree(cr, x, gy, h=300, sway=0.0, color=INK):
    """Broad tree with a strong low branch reaching left. Returns the seat point (x, y) on that branch."""
    cr.set_source_rgb(*color); cr.set_line_cap(cairo.LINE_CAP_ROUND)
    cr.move_to(x - 16, gy); cr.curve_to(x - 10, gy - h * 0.3, x - 12, gy - h * 0.5, x - 8, gy - h * 0.7)
    cr.line_to(x + 8, gy - h * 0.7); cr.curve_to(x + 10, gy - h * 0.5, x + 12, gy - h * 0.3, x + 18, gy); cr.close_path(); cr.fill()
    by = gy - h * 0.40
    cr.set_line_width(11); cr.move_to(x - 4, by + 10); cr.curve_to(x - 50, by, x - 100, by - 4, x - 135, by - 18); cr.stroke()
    cr.set_line_width(8); cr.move_to(x + 4, gy - h * 0.62); cr.curve_to(x + 40, gy - h * 0.68, x + 70, gy - h * 0.72, x + 95, gy - h * 0.82); cr.stroke()
    cy = gy - h * 0.9
    for dx, dy, r in ((-95, 6, 34), (-60, -24, 46), (-10, -40, 54), (50, -26, 50), (95, 4, 38), (-30, 10, 40), (40, 14, 42)):
        _leaf_blob(cr, x + dx + sway * (1 + dy / -40.0), cy + dy, r)
    return (x - 92, by - 6)

def stone_gate(cr, x, gy, gap=60, h=150, post=26, color=INK):
    """Gateway: two square posts and a lintel; the opening is gap wide and h tall, centred on x."""
    cr.set_source_rgb(*color)
    for sx in (x - gap / 2 - post, x + gap / 2):
        cr.rectangle(sx, gy - h, post, h); cr.fill()
    cr.rectangle(x - gap / 2 - post - 10, gy - h - 22, gap + 2 * post + 20, 22); cr.fill()
    cr.set_source_rgb(*BG); cr.set_line_width(2)
    for sx in (x - gap / 2 - post, x + gap / 2):
        for k in range(1, int(h / 40) + 1):
            cr.move_to(sx + 3, gy - k * 40); cr.line_to(sx + post - 3, gy - k * 40); cr.stroke()

def lily(cr, x, gy, bloom=1.0, h=70, sway=0.0, color=INK):
    """Field lily; bloom 0..1 grows the stem then opens the flower."""
    if bloom <= 0: return
    g = clamp(bloom * 1.6); o = clamp((bloom - 0.55) / 0.45)
    hh = h * g; tx = x + sway * hh * 0.1; ty = gy - hh
    cr.set_source_rgb(*color); cr.set_line_width(3)
    cr.move_to(x, gy); cr.curve_to(x, gy - hh * 0.5, tx, ty + hh * 0.3, tx, ty); cr.stroke()
    if hh > 25:
        for d, f in ((-1, 0.3), (1, 0.45)):
            ly = gy - hh * f; cr.move_to(x, ly); cr.curve_to(x + d * 10, ly - 10, x + d * 18, ly - 18, x + d * 20, ly - 30); cr.stroke()
    if o <= 0:
        cr.save(); cr.translate(tx, ty - 6); cr.scale(4, 9); cr.arc(0, 0, 1, 0, 2 * math.pi); cr.restore(); cr.fill(); return
    for a in (-1, -0.35, 0.35, 1):
        ang = a * (0.25 + 0.9 * o)
        cr.save(); cr.translate(tx, ty); cr.rotate(ang); cr.move_to(0, 0)
        cr.curve_to(-7, -8, -6, -20, 0, -24 - 4 * o); cr.curve_to(6, -20, 7, -8, 0, 0); cr.fill(); cr.restore()

def moon(cr, x, y, r=26, color=(0.98, 0.94, 0.80)):
    """Crescent moon (light colour, for night scenes; draw after darkness)."""
    cr.save(); cr.push_group()
    cr.set_source_rgb(*color); cr.arc(x, y, r, 0, 2 * math.pi); cr.fill()
    cr.set_operator(cairo.OPERATOR_CLEAR); cr.arc(x + r * 0.45, y - r * 0.25, r * 0.85, 0, 2 * math.pi); cr.fill()
    cr.pop_group_to_source(); cr.paint(); cr.restore()

def salt_pouch(cr, x, y, color=INK):
    """Small open salt pouch held at (x, y)."""
    cr.set_source_rgb(*color); cr.save(); cr.translate(x, y + 10); cr.scale(12, 12); cr.arc(0, 0, 1, 0, 2 * math.pi); cr.restore(); cr.fill()
    cr.move_to(x - 10, y + 2); cr.line_to(x - 13, y - 6); cr.line_to(x + 13, y - 6); cr.line_to(x + 10, y + 2); cr.close_path(); cr.fill()

def salt_heap(cr, x, gy, amount=1.0, trampled=0.0, color=(0.40, 0.38, 0.35)):
    """A little heap of grey salt grains on the road; trampled 0..1 flattens and scatters it."""
    if amount <= 0: return
    cr.set_source_rgb(*color)
    h = 20 * amount * (1 - 0.8 * trampled); w = 40 + 40 * trampled
    cr.move_to(x - w, gy); cr.curve_to(x - w * 0.4, gy - h, x + w * 0.4, gy - h, x + w, gy); cr.close_path(); cr.fill()
    for k in range(int(14 * amount)):
        cr.arc(x - w - 10 + (k * 37) % int(2 * w + 20), gy - 2 - (k * 13) % 5, 1.8, 0, 2 * math.pi); cr.fill()

def hill_city(cr, x, gy, w=420, h=150, light=0.0, color=INK):
    """A hill (base x .. x+w) with a little walled city on top; light 0..1 lights its windows and a halo."""
    top = gy - h; cx = x + w * 0.55
    if light > 0:
        g = cairo.RadialGradient(cx, top - 40, 0, cx, top - 40, 260 * light)
        g.add_color_stop_rgba(0, 1, 0.86, 0.48, 0.7 * light); g.add_color_stop_rgba(1, 1, 0.86, 0.48, 0)
        cr.set_source(g); cr.rectangle(cx - 300, top - 300, 600, 600); cr.fill()
    cr.set_source_rgb(*color)
    cr.move_to(x, gy + 2); cr.curve_to(x + w * 0.25, gy - h * 0.4, cx - 120, top, cx - 90, top)
    cr.line_to(cx + 90, top); cr.curve_to(cx + 120, top, x + w * 0.85, gy - h * 0.4, x + w, gy + 2); cr.close_path(); cr.fill()
    blds = [(-88, 46, 40), (-46, 34, 64), (-10, 44, 50), (36, 30, 78), (68, 26, 44)]
    for bx, bw, bh in blds:
        cr.set_source_rgb(*color); cr.rectangle(cx + bx, top - bh, bw, bh + 2); cr.fill()
    cr.rectangle(cx + 44, top - 96, 14, 20); cr.fill()                     # tower top
    wc = tuple(lerp(BG[j], (1, 0.82, 0.38)[j], light) for j in range(3))
    cr.set_source_rgb(*wc)
    for bx, bw, bh in blds:
        for k in range(int(bh / 26)):
            cr.rectangle(cx + bx + bw / 2 - 5, top - bh + 10 + k * 24, 10, 12); cr.fill()

def crown(cr, head, s=1.0, face=1, color=INK):
    """Crown on a draw_figure head (pass J['head'])."""
    hx, hy = head; cr.set_source_rgb(*color)
    b = hy - 12 * s
    cr.move_to(hx - 12 * s, b + 2 * s); cr.line_to(hx - 13 * s, b - 14 * s); cr.line_to(hx - 6 * s, b - 6 * s); cr.line_to(hx, b - 16 * s)
    cr.line_to(hx + 6 * s, b - 6 * s); cr.line_to(hx + 13 * s, b - 14 * s); cr.line_to(hx + 12 * s, b + 2 * s); cr.close_path(); cr.fill()

def throne(cr, x, gy, face=1, color=INK):
    """Seat (height 46) with a tall back behind a figure facing `face`; x = seat centre."""
    cr.set_source_rgb(*color)
    cr.rectangle(x - 34, gy - 50, 68, 10); cr.fill()
    cr.rectangle(x - 30, gy - 42, 60, 42); cr.fill()
    bx = x - face * 34
    cr.rectangle(bx - 7, gy - 170, 14, 130); cr.fill()
    cr.arc(bx, gy - 172, 10, 0, 2 * math.pi); cr.fill()

def debt_scroll(cr, x, y, tear=0.0, fall=0.0, gy=None, color=INK):
    """Scroll held open at (x, y) (centre); tear 0..1 rips it in two; fall 0..1 drops the halves to gy."""
    cr.set_source_rgb(*color)
    for d in (-1, 1):
        dx = d * 6 * tear + d * 30 * fall; dy = (gy - y - 6) * fall * fall if gy else 0
        rot = d * (0.25 * tear + 1.2 * fall)
        cr.save(); cr.translate(x + dx, y + dy); cr.rotate(rot)
        cr.rectangle(min(0, d * 22), -18, 22, 36); cr.fill()
        cr.set_source_rgb(*BG); cr.set_line_width(1.6)
        for k in range(4):
            cr.move_to(d * 4, -10 + k * 7); cr.line_to(d * 18, -10 + k * 7); cr.stroke()
        cr.set_source_rgb(*color)
        cr.rectangle(d * 22 - (3 if d > 0 else 3), -21, 6, 42); cr.fill()
        cr.restore()

# ---- props added by worker 1 ----
from engine import draw_figure
STONE = (0.74, 0.71, 0.65)        # light rock tone (so black silhouettes read in front of it)

def rock_cave(cr, x, gy, w=330, h=190, mouth=0.38, mw=90, mh=120, color=STONE):
    """Rocky hill from x to x+w with an arched cave mouth. mouth = mouth centre as a fraction of w.
    Returns (mouth_cx, mw, mh)."""
    cx = x + w * mouth
    cr.set_source_rgb(*color)
    cr.move_to(x, gy + 2)
    cr.curve_to(x + w * 0.05, gy - h * 0.7, x + w * 0.25, gy - h, x + w * 0.5, gy - h)
    cr.curve_to(x + w * 0.78, gy - h, x + w * 0.95, gy - h * 0.6, x + w, gy + 2)
    cr.close_path(); cr.fill_preserve()
    cr.set_source_rgb(*INK); cr.set_line_width(4); cr.stroke()
    cr.set_line_width(2.5)
    for (fx, fy, dx, dy) in ((0.62, 0.72, 18, 22), (0.80, 0.45, -14, 26), (0.18, 0.40, 16, 18), (0.55, 0.30, 22, 10)):
        px, py = x + w * fx, gy - h * fy
        cr.move_to(px, py); cr.line_to(px + dx * 0.5, py + dy * 0.6); cr.line_to(px + dx, py + dy); cr.stroke()
    cr.set_source_rgb(*INK)
    cr.move_to(cx - mw / 2, gy); cr.line_to(cx - mw / 2, gy - mh + mw / 2)
    cr.arc(cx, gy - mh + mw / 2, mw / 2, math.pi, 2 * math.pi); cr.line_to(cx + mw / 2, gy); cr.close_path(); cr.fill()
    return (cx, mw, mh)

def round_stone(cr, x, gy, r=62, rot=0.0, color=INK):
    """Rolling tomb stone resting on gy; rot in radians (shows as turning crack lines)."""
    cr.set_source_rgb(*color); cr.arc(x, gy - r, r, 0, 2 * math.pi); cr.fill()
    cr.set_source_rgb(*BG); cr.set_line_width(3)
    cr.arc(x, gy - r, r * 0.72, 0, 2 * math.pi); cr.stroke()
    for k in range(3):
        a = rot + k * 2 * math.pi / 3
        cr.move_to(x + math.cos(a) * r * 0.2, gy - r + math.sin(a) * r * 0.2)
        cr.line_to(x + math.cos(a) * r * 0.55, gy - r + math.sin(a) * r * 0.55); cr.stroke()

def wrapped_figure(cr, x, gy, p, s=1.0, face=1, wrap=1.0, color=INK):
    """A figure bound in grave bands: light diagonal bands drawn only over the silhouette. wrap 0..1."""
    cr.push_group()
    J = draw_figure(cr, x, gy, p, s=s, face=face, color=color)
    if wrap > 0:
        cr.set_operator(cairo.OPERATOR_ATOP)
        cr.set_source_rgba(0.93, 0.90, 0.84, 0.95 * wrap); cr.set_line_width(6 * s)
        top = gy - 200 * s
        for k in range(22):
            yy = top + k * 11 * s
            cr.move_to(x - 60 * s, yy); cr.line_to(x + 60 * s, yy - 22 * s); cr.stroke()
        cr.set_operator(cairo.OPERATOR_OVER)
    cr.pop_group_to_source(); cr.paint()
    return J

def tears(cr, x, y, t, amount=1.0, face=1):
    """Small drops falling from a point near the face."""
    if amount <= 0: return
    for k in range(3):
        u = ((t * 0.9) + k / 3.0) % 1.0
        cr.set_source_rgba(*INK, amount * (1 - u))
        xx, yy = x + face * (3 + k * 2), y + u * 46
        cr.move_to(xx, yy - 5); cr.curve_to(xx + 3, yy, xx + 3, yy + 4, xx, yy + 4)
        cr.curve_to(xx - 3, yy + 4, xx - 3, yy, xx, yy - 5); cr.fill()

def cry_lines(cr, x, y, face=1, amount=1.0, size=1.0, t=0.0):
    """Short arcs radiating from a head (shouting / calling out)."""
    if amount <= 0: return
    cr.set_line_width(3.5 * size); cr.set_line_cap(cairo.LINE_CAP_ROUND)
    for k in range(3):
        r = (22 + k * 13) * size + 3 * math.sin(t * 10 + k)
        cr.set_source_rgba(*INK, amount * (1 - 0.2 * k))
        if face > 0: cr.arc(x, y, r, -0.55, 0.45)
        else: cr.arc(x, y, r, math.pi - 0.45, math.pi + 0.55)
        cr.stroke()

def hush_mark(cr, x, y, amount=1.0):
    """'Shh' gesture lines (a small downward zigzag) beside a head."""
    if amount <= 0: return
    cr.set_source_rgba(*SOFT, amount); cr.set_line_width(3)
    cr.move_to(x, y); cr.line_to(x + 8, y + 6); cr.line_to(x, y + 12); cr.line_to(x + 8, y + 18); cr.stroke()

def cane(cr, x, top_y, bottom_y, lean=0.0, color=INK):
    cr.set_source_rgb(*color); cr.set_line_width(4.5); cr.set_line_cap(cairo.LINE_CAP_ROUND)
    cr.move_to(x + lean, bottom_y); cr.line_to(x, top_y); cr.stroke()

def light_rays(cr, x, y, amount, r0=26, r1=60, n=12, t=0.0):
    """Warm rays around a point (sight restored, glory)."""
    if amount <= 0: return
    warm_glow(cr, x, y, 200 * amount, amount)
    cr.set_source_rgba(1, 0.78, 0.3, 0.9 * amount); cr.set_line_width(3)
    for k in range(n):
        a = k * 2 * math.pi / n + t * 0.3
        cr.move_to(x + math.cos(a) * r0, y + math.sin(a) * r0)
        cr.line_to(x + math.cos(a) * (r0 + (r1 - r0) * amount), y + math.sin(a) * (r0 + (r1 - r0) * amount)); cr.stroke()

def fishing_boat(cr, x, y, w=440, mast=110):
    """Low open boat (no tall sail), hull centred at x, gunwale at y."""
    cr.set_source_rgb(*INK)
    cr.move_to(x - w / 2 - 20, y - 12); cr.line_to(x - w / 2 + 8, y); cr.line_to(x + w / 2 - 8, y); cr.line_to(x + w / 2 + 20, y - 12)
    cr.curve_to(x + w / 2, y + 40, x + w / 3, y + 48, x, y + 48)
    cr.curve_to(x - w / 3, y + 48, x - w / 2, y + 40, x - w / 2 - 20, y - 12); cr.close_path(); cr.fill()
    if mast > 0:
        cr.set_line_width(5); cr.move_to(x + 20, y); cr.line_to(x + 20, y - mast); cr.stroke()
        cr.set_line_width(4); cr.move_to(x - 30, y - mast + 14); cr.line_to(x + 70, y - mast + 4); cr.stroke()

def splash(cr, x, y, amount, t, n=9, spread=70, seed=3):
    """Spray droplets thrown up from a point."""
    if amount <= 0: return
    import random as _r
    r = _r.Random(seed); cr.set_source_rgba(*INK, 0.8 * amount)
    for k in range(n):
        ph = (t * 1.4 + r.uniform(0, 1)) % 1.0
        vx = r.uniform(-1, 1) * spread; vy = r.uniform(80, 150)
        xx = x + vx * ph; yy = y - vy * ph + 160 * ph * ph
        cr.arc(xx, yy, r.uniform(2.5, 4.5) * (1 - 0.5 * ph), 0, 2 * math.pi); cr.fill()

def great_fish(cr, x, y, s=1.0, face=-1, mouth=0.0, tail=0.0, color=INK):
    """Large fish silhouette centred at (x, y); face -1 = head to the left; mouth 0..1 opens the jaw."""
    cr.save(); cr.translate(x, y); cr.scale(-face * s, s)   # drawn with head on the left
    cr.set_source_rgb(*color)
    m = 0.55 * mouth
    cr.move_to(-120, -6 - 40 * m)
    cr.curve_to(-100, -70, 40, -78, 110, -12)
    cr.line_to(110, 12)
    cr.curve_to(40, 70, -100, 62, -120, 6 + 40 * m)
    cr.line_to(-70, 0); cr.close_path(); cr.fill()
    tw = 10 * math.sin(tail)
    cr.move_to(100, 0); cr.line_to(170, -48 + tw); cr.line_to(155, 0); cr.line_to(170, 48 + tw); cr.close_path(); cr.fill()
    cr.move_to(10, -60); cr.line_to(50, -88); cr.line_to(60, -46); cr.close_path(); cr.fill()
    cr.set_source_rgb(*BG); cr.arc(-80, -26, 6, 0, 2 * math.pi); cr.fill()
    cr.set_line_width(3); cr.arc(-45, 0, 30, -0.9, 0.9); cr.stroke()
    cr.restore()

def city_skyline(cr, x, gy, s=1.0, color=INK):
    """Walled city ~270*s wide, x = left edge; open gate centred at x + 150*s. Returns gate centre x."""
    cr.save(); cr.translate(x, gy); cr.scale(s, s); cr.set_source_rgb(*color)
    cr.rectangle(0, -95, 270, 95); cr.fill()
    for bx in range(0, 270, 22): cr.rectangle(bx, -107, 12, 13); cr.fill()
    for (tx, tw, th) in ((10, 46, 165), (205, 52, 150)):
        cr.rectangle(tx, -th, tw, th); cr.fill()
        for bx in range(0, tw, 14): cr.rectangle(tx + bx, -th - 11, 9, 12); cr.fill()
    cr.rectangle(85, -140, 50, 50); cr.fill(); cr.arc(110, -140, 25, math.pi, 2 * math.pi); cr.fill()
    cr.set_source_rgb(*BG)
    cr.move_to(128, 0); cr.line_to(128, -44); cr.arc(150, -44, 22, math.pi, 2 * math.pi); cr.line_to(172, 0); cr.close_path(); cr.fill()
    for (wx, wy) in ((26, -130), (224, -118), (104, -125)): cr.rectangle(wx, wy, 10, 16); cr.fill()
    cr.restore()
    return x + 150 * s

def brook(cr, x0, x1, gy):
    """A shallow stream crossing the ground line."""
    cr.set_source_rgb(*BG); cr.rectangle(x0, gy - 3, x1 - x0, 8); cr.fill()
    cr.set_source_rgb(*INK); cr.set_line_width(3)
    cr.move_to(x0 - 10, gy); cr.curve_to(x0, gy, x0 + 4, gy + 10, x0 + 18, gy + 12)
    cr.line_to(x1 - 18, gy + 12); cr.curve_to(x1 - 4, gy + 10, x1, gy, x1 + 10, gy); cr.stroke()
    cr.set_line_width(2)
    for k in range(3):
        xx = x0 + 22 + k * (x1 - x0 - 50) / 3
        cr.move_to(xx, gy + 6); cr.curve_to(xx + 6, gy + 2, xx + 12, gy + 2, xx + 18, gy + 6); cr.stroke()

def pebble(cr, x, y, r=5, color=INK):
    cr.set_source_rgb(*color); cr.save(); cr.translate(x, y); cr.scale(r, r * 0.78)
    cr.arc(0, 0, 1, 0, 2 * math.pi); cr.restore(); cr.fill()

def sling(cr, hx, hy, ang, L=46, loaded=True):
    """Sling cords hanging/swinging from a hand at (hx, hy); ang = cord angle (radians, 0 = straight down)."""
    px, py = hx + math.sin(ang) * L, hy + math.cos(ang) * L
    cr.set_source_rgb(*INK); cr.set_line_width(2)
    nx, ny = math.cos(ang) * 6, -math.sin(ang) * 6
    cr.move_to(hx, hy); cr.line_to(px + nx, py + ny); cr.stroke()
    cr.move_to(hx, hy); cr.line_to(px - nx, py - ny); cr.stroke()
    if loaded: pebble(cr, px, py, 6)
    return (px, py)

def giant_gear(cr, J, s=1.0, face=1, spear_up=1.0, shield=True, spear=True):
    """Helmet, round shield on the far arm and a spear in the near hand of a figure (J from draw_figure)."""
    hx, hy = J["head"]
    cr.set_source_rgb(*INK)
    cr.save(); cr.translate(hx, hy); cr.scale(face, 1)
    cr.move_to(-15 * s, -4 * s); cr.curve_to(-15 * s, -24 * s, 15 * s, -24 * s, 15 * s, -4 * s); cr.close_path(); cr.fill()
    cr.rectangle(-3 * s, -36 * s, 6 * s, 14 * s); cr.fill()
    cr.move_to(-2 * s, -34 * s); cr.curve_to(-18 * s, -40 * s, -26 * s, -30 * s, -30 * s, -18 * s); cr.set_line_width(5 * s); cr.stroke()
    cr.restore()
    if shield:
        sx, sy = J["lhand_mid"]
        cr.arc(sx + face * 8 * s, sy + 10 * s, 26 * s, 0, 2 * math.pi); cr.fill()
        cr.set_source_rgb(*BG); cr.arc(sx + face * 8 * s, sy + 10 * s, 7 * s, 0, 2 * math.pi); cr.fill(); cr.set_source_rgb(*INK)
    if not spear: return
    rx, ry = J["rhand"]
    L = 150 * s; a = math.radians(lerp(10, 0, spear_up))
    cr.set_line_width(5 * s); cr.move_to(rx - face * math.sin(a) * L * 0.25, ry + L * 0.35)
    tx, ty = rx + face * math.sin(a) * L * 0.75, ry - L * 0.65
    cr.line_to(tx, ty); cr.stroke()
    cr.move_to(tx - 7 * s, ty + 4 * s); cr.line_to(tx, ty - 22 * s); cr.line_to(tx + 7 * s, ty + 4 * s); cr.close_path(); cr.fill()

def ark(cr, x, y, w=420, color=INK):
    """Noah's ark: hull centred at x with its waterline at y; cabin with a window. Returns window centre."""
    cr.set_source_rgb(*color)
    cr.move_to(x - w / 2 - 30, y - 70); cr.line_to(x + w / 2 + 30, y - 70)
    cr.curve_to(x + w / 2 + 10, y - 10, x + w / 2 - 20, y + 30, x + w / 2 - 50, y + 30)
    cr.line_to(x - w / 2 + 50, y + 30)
    cr.curve_to(x - w / 2 + 20, y + 30, x - w / 2 - 10, y - 10, x - w / 2 - 30, y - 70); cr.close_path(); cr.fill()
    cw = w * 0.55
    cr.rectangle(x - cw / 2, y - 140, cw, 72); cr.fill()
    cr.move_to(x - cw / 2 - 18, y - 138); cr.line_to(x, y - 178); cr.line_to(x + cw / 2 + 18, y - 138); cr.close_path(); cr.fill()
    cr.set_source_rgb(*BG); cr.set_line_width(2.5)
    for k in range(1, 3):
        yy = y - 70 + k * 28; cr.move_to(x - w / 2 + 10 - (2 - k) * 10, yy); cr.line_to(x + w / 2 - 10 + (2 - k) * 10, yy); cr.stroke()
    wx, wy = x + cw / 2 - 40, y - 108
    cr.rectangle(wx - 18, wy - 16, 36, 32); cr.fill()
    return (wx, wy)

def rainbow(cr, cx, cy, r, amount=1.0, band=9):
    """Soft pastel arc centred at (cx, cy) (centre usually below the horizon); amount 0..1 sweeps it in."""
    if amount <= 0: return
    cols = [(0.86, 0.45, 0.42), (0.90, 0.66, 0.40), (0.90, 0.83, 0.45), (0.55, 0.76, 0.52), (0.48, 0.66, 0.82), (0.62, 0.54, 0.78)]
    a1 = math.pi + math.pi * clamp(amount)
    cr.set_line_width(band)
    for k, c in enumerate(cols):
        cr.set_source_rgba(*c, 0.85); cr.arc(cx, cy, r - k * band, math.pi, a1); cr.stroke()

def olive_sprig(cr, x, y, s=1.0, rot=0.0):
    cr.save(); cr.translate(x, y); cr.rotate(rot); cr.scale(s, s)
    cr.set_source_rgb(*INK); cr.set_line_width(2); cr.move_to(0, 0); cr.line_to(22, 0); cr.stroke()
    for (lx, d) in ((7, -1), (12, 1), (17, -1), (22, 1)):
        cr.save(); cr.translate(lx, d * 3); cr.rotate(d * 0.6); cr.scale(6, 2.4); cr.arc(0, 0, 1, 0, 2 * math.pi); cr.restore(); cr.fill()
    cr.restore()

def sea_wall(cr, x0, x1, base_y, h, t, color=None):
    """A standing wall of water from x0 to x1 rising h px above base_y, with curling crests."""
    if h <= 1: return
    col = color or (0.62, 0.70, 0.74)
    top = []
    for x in range(int(x0), int(x1) + 1, 12):
        top.append((x, base_y - h + 6 * math.sin(x * 0.05 + t * 2.0) + 4 * math.sin(x * 0.13 - t * 2.6)))
    cr.set_source_rgba(*col, 0.85); cr.move_to(x0, base_y)
    for p in top: cr.line_to(*p)
    cr.line_to(x1, base_y); cr.close_path(); cr.fill()
    cr.set_source_rgb(*INK); cr.set_line_width(3.5); cr.move_to(*top[0])
    for p in top[1:]: cr.line_to(*p)
    cr.stroke()
    cr.set_line_width(2.5); cr.set_source_rgba(*INK, 0.55)
    rows = max(1, int(h / 38))
    for j in range(rows):
        for k in range(int((x1 - x0) / 90)):
            xx = x0 + 30 + k * 90 + (j % 2) * 45 + 10 * math.sin(t * 1.5 + k + j)
            yy = base_y - h + 34 + j * 38
            if yy > base_y - 10 or xx > x1 - 30: continue
            cr.move_to(xx, yy); cr.curve_to(xx + 10, yy - 7, xx + 22, yy - 7, xx + 32, yy); cr.stroke()

def dust_cloud(cr, x, gy, amount, t, spears=True):
    """Rolling dust of an approaching army at x (right edge of the cloud), with spear tips poking out."""
    if amount <= 0: return
    cr.set_source_rgba(*SOFT, 0.75 * amount)
    for k in range(9):
        r = 26 + (k % 3) * 10 + 3 * math.sin(t * 3 + k)
        cr.arc(x - 20 - k * 30, gy - 24 - (k % 2) * 26 - (k % 3) * 8, r, 0, 2 * math.pi); cr.fill()
    if spears:
        cr.set_source_rgba(*INK, amount); cr.set_line_width(3)
        for k in range(6):
            sx = x - 30 - k * 38 + 3 * math.sin(t * 6 + k); top = gy - 120 - (k % 3) * 12
            cr.move_to(sx, top + 70); cr.line_to(sx, top); cr.stroke()
            cr.move_to(sx - 5, top + 4); cr.line_to(sx, top - 12); cr.line_to(sx + 5, top + 4); cr.close_path(); cr.fill()

def flames(cr, x, gy, h, t, w=1.0, seed=1):
    """Flickering silhouette fire of height h at x (base on gy); w widens it."""
    if h <= 2: return
    cr.set_source_rgba(0.85, 0.42, 0.18, 0.95)
    for k in range(5):
        dx = (k - 2) * 16 * w; hh = h * (0.55 + 0.45 * math.sin(k * 1.7 + seed) ** 2) * (0.85 + 0.15 * math.sin(t * 11 + k * 2 + seed))
        sw = 4 * math.sin(t * 7 + k + seed)
        cr.move_to(x + dx - 14 * w, gy)
        cr.curve_to(x + dx - 16 * w, gy - hh * 0.5, x + dx + sw - 4, gy - hh * 0.8, x + dx + sw, gy - hh)
        cr.curve_to(x + dx + sw + 4, gy - hh * 0.8, x + dx + 16 * w, gy - hh * 0.5, x + dx + 14 * w, gy); cr.close_path(); cr.fill()
    cr.set_source_rgba(1.0, 0.78, 0.35, 0.9)
    for k in range(3):
        dx = (k - 1) * 16 * w; hh = h * 0.45 * (0.85 + 0.15 * math.sin(t * 13 + k + seed))
        cr.move_to(x + dx - 8 * w, gy); cr.curve_to(x + dx - 8 * w, gy - hh * 0.6, x + dx, gy - hh * 0.8, x + dx, gy - hh)
        cr.curve_to(x + dx, gy - hh * 0.8, x + dx + 8 * w, gy - hh * 0.6, x + dx + 8 * w, gy); cr.close_path(); cr.fill()

def rock_chunk(cr, x, y, r, rot=0.0, color=INK):
    cr.set_source_rgb(*color); cr.save(); cr.translate(x, y); cr.rotate(rot)
    pts = [(1.0, 0.1), (0.6, 0.85), (-0.3, 0.95), (-0.95, 0.35), (-0.8, -0.5), (-0.1, -0.9), (0.75, -0.65)]
    cr.move_to(pts[0][0] * r, pts[0][1] * r)
    for (a, b) in pts[1:]: cr.line_to(a * r, b * r)
    cr.close_path(); cr.fill(); cr.restore()

def breeze(cr, x, y, t, amount=1.0, length=260):
    """A single gentle curling breath of air drifting right."""
    if amount <= 0: return
    cr.set_source_rgba(*SOFT, 0.9 * amount); cr.set_line_width(3); cr.set_line_cap(cairo.LINE_CAP_ROUND)
    for k in range(2):
        yy = y + k * 26; xx = x + k * 40
        cr.move_to(xx, yy)
        for j in range(1, 21):
            u = j / 20.0
            cr.line_to(xx + u * length, yy + 8 * math.sin(u * 7 + t * 2.0 + k))
        cr.stroke()
    ex = x + length; ey = y + 8 * math.sin(7 + t * 2.0)
    cr.arc(ex - 10, ey - 10, 10, math.pi / 2, 2.2 * math.pi); cr.stroke()

def olive_tree(cr, x, gy, h=120, s=1.0, leaves=1.0, color=INK):
    """Small rounded tree; leaves 0..1 scales the canopy."""
    cr.set_source_rgb(*color); cr.set_line_width(9 * s); cr.set_line_cap(cairo.LINE_CAP_ROUND)
    cr.move_to(x, gy); cr.curve_to(x - 6 * s, gy - h * 0.4, x + 8 * s, gy - h * 0.6, x, gy - h * 0.75); cr.stroke()
    if leaves > 0:
        for (dx, dy, r) in ((-30, -0.78, 26), (0, -0.95, 30), (30, -0.80, 26), (-14, -0.66, 20), (16, -0.64, 20)):
            cr.arc(x + dx * s, gy + dy * h, r * s * leaves, 0, 2 * math.pi); cr.fill()

# ---- props added by worker 2 ----
def fig_tree(cr, x, gy, s=1.0, leaves=0.5, figs=0.0, fall=0.0, color=INK):
    """Fig tree; trunk base at (x, gy). leaves/figs 0..1 grow foliage/fruit. fall = degrees the cut trunk
    has toppled (+ = to the right) about a stump 18px tall. Returns list of branch-tip points (unfallen)."""
    cr.set_source_rgb(*color); cr.set_line_cap(cairo.LINE_CAP_ROUND)
    stump = 18 * s
    cr.save(); cr.rectangle(x - 600, gy - 700, 1200, 700); cr.clip()
    cr.set_line_width(16 * s); cr.move_to(x, gy); cr.line_to(x, gy - stump); cr.stroke()
    cr.save(); cr.translate(x, gy - stump); cr.rotate(math.radians(fall))
    cr.set_line_width(15 * s); cr.move_to(0, 2); cr.line_to(0, -100 * s); cr.stroke()
    br = ((-62, 62, 40), (58, 58, 46), (-38, 82, 70), (34, 86, 80), (-12, 76, 100), (14, 70, 100))
    tips = []
    for a, L, h0 in br:
        r = math.radians(a); sx, sy = 0, -h0 * s
        ex, ey = sx + math.sin(r) * L * s, sy - math.cos(r) * L * s
        cr.set_line_width(7 * s); cr.move_to(sx, sy); cr.curve_to(sx, sy - 20 * s, ex - math.sin(r) * 20 * s, ey + 10 * s, ex, ey); cr.stroke()
        cr.set_line_width(3 * s)
        for d in (-1, 1):
            cr.move_to(ex - math.sin(r) * 18 * s, ey + math.cos(r) * 18 * s)
            cr.line_to(ex - math.sin(r) * 18 * s + d * 14 * s, ey + math.cos(r) * 18 * s - 12 * s); cr.stroke()
        tips.append((ex, ey))
    if leaves > 0:
        for k, (ex, ey) in enumerate(tips):
            for j, (dx, dy, rot) in enumerate(((-10, -4, -0.6), (10, -6, 0.5), (0, -14, 0.0), (-16, 8, -1.2), (16, 6, 1.1))):
                lf = leaves * (1.0 if j < 3 else clamp(leaves * 1.6 - 0.6))
                if lf <= 0: continue
                cr.save(); cr.translate(ex + dx * s * leaves, ey + dy * s * leaves); cr.rotate(rot)
                cr.scale(17 * s * lf, 11 * s * lf); cr.arc(0, 0, 1, 0, 2 * math.pi); cr.restore(); cr.fill()
    if figs > 0:
        for k, (ex, ey) in enumerate(tips):
            for d in (-1, 1):
                fx, fy = ex + d * 12 * s, ey + 34 * s
                rr = 8 * s * figs
                cr.set_line_width(2.5 * s); cr.move_to(ex + d * 6 * s, ey + 14 * s); cr.line_to(fx, fy - rr * 1.4); cr.stroke()
                cr.arc(fx, fy, rr, 0, 2 * math.pi); cr.fill()
                cr.move_to(fx - rr * 0.5, fy - rr * 0.6); cr.line_to(fx, fy - rr * 1.7); cr.line_to(fx + rr * 0.5, fy - rr * 0.6); cr.fill()
    cr.restore(); cr.restore()
    return [(x + tx, gy - stump + ty) for tx, ty in tips]

def axe(cr, hx, hy, ang, s=1.0, color=INK):
    """Axe held at (hx, hy); ang = screen direction of the handle in degrees (0 = up, 90 = right)."""
    r = math.radians(ang); dx, dy = math.sin(r), -math.cos(r)
    cr.set_source_rgb(*color); cr.set_line_cap(cairo.LINE_CAP_ROUND); cr.set_line_width(5 * s)
    cr.move_to(hx - dx * 10 * s, hy - dy * 10 * s); cr.line_to(hx + dx * 62 * s, hy + dy * 62 * s); cr.stroke()
    cr.save(); cr.translate(hx + dx * 56 * s, hy + dy * 56 * s); cr.rotate(r)
    cr.move_to(-3 * s, -9 * s); cr.line_to(20 * s, -14 * s); cr.curve_to(25 * s, -6 * s, 25 * s, 4 * s, 20 * s, 10 * s)
    cr.line_to(-3 * s, 3 * s); cr.close_path(); cr.fill(); cr.restore()

def spade(cr, gx, gyy, tx, ty, s=1.0, color=INK):
    """Spade from grip (gx, gyy) to blade tip (tx, ty)."""
    cr.set_source_rgb(*color); cr.set_line_cap(cairo.LINE_CAP_ROUND)
    L = math.hypot(tx - gx, ty - gyy) or 1; ux, uy = (tx - gx) / L, (ty - gyy) / L
    bx, by = tx - ux * 30 * s, ty - uy * 30 * s
    cr.set_line_width(5 * s); cr.move_to(gx, gyy); cr.line_to(bx, by); cr.stroke()
    cr.set_line_width(4 * s); cr.move_to(gx - uy * 9 * s, gyy + ux * 9 * s); cr.line_to(gx + uy * 9 * s, gyy - ux * 9 * s); cr.stroke()
    px, py = -uy, ux
    cr.move_to(bx + px * 11 * s, by + py * 11 * s); cr.line_to(bx - px * 11 * s, by - py * 11 * s)
    cr.line_to(tx - px * 7 * s, ty - py * 7 * s); cr.line_to(tx + px * 7 * s, ty + py * 7 * s); cr.close_path(); cr.fill()

def grapevine(cr, x, gy, h=170, color=INK):
    """Gnarled vine stock on a post; returns the branch attachment point."""
    cr.set_source_rgb(*color); cr.set_line_cap(cairo.LINE_CAP_ROUND)
    cr.set_line_width(5); cr.move_to(x - 14, gy); cr.line_to(x - 14, gy - h - 20); cr.stroke()
    cr.set_line_width(14)
    cr.move_to(x, gy); cr.curve_to(x + 14, gy - h * 0.3, x - 12, gy - h * 0.6, x + 4, gy - h); cr.stroke()
    cr.set_line_width(4)
    for k in range(3):
        yy = gy - h * (0.25 + 0.25 * k)
        cr.arc(x - 6, yy, 9, math.pi * 0.2, math.pi * 1.1); cr.stroke()
    return (x + 4, gy - h)

def vine_leaf(cr, x, y, r, rot=0.0):
    cr.save(); cr.translate(x, y); cr.rotate(rot)
    for a in (-0.9, 0, 0.9):
        cr.arc(math.sin(a) * r * 0.55, -math.cos(a) * r * 0.55, r * 0.5, 0, 2 * math.pi); cr.fill()
    cr.arc(0, 0, r * 0.5, 0, 2 * math.pi); cr.fill(); cr.restore()

def vine_branch(cr, ax, ay, rot=0.0, L=230, grow=1.0, grapes=0.0, wither=0.0):
    """Vine branch starting at (ax, ay) growing to the right; rot in degrees about its base.
    grapes 0..1 swells the clusters; wither 0..1 fades, droops and shrivels it."""
    if grow <= 0: return
    col = tuple(lerp(INK[j], SOFT[j], wither) for j in range(3))
    cr.save(); cr.translate(ax, ay); cr.rotate(math.radians(rot + 14 * wither))
    cr.set_source_rgb(*col); cr.set_line_cap(cairo.LINE_CAP_ROUND)
    Lg = L * grow; sag = 18 + 26 * wither
    cr.set_line_width(7 - 2 * wither); cr.move_to(0, 0); cr.curve_to(Lg * 0.35, -14, Lg * 0.7, sag * 0.5, Lg, sag); cr.stroke()
    def pt(u):
        return (Lg * u, (-14 * 3 * u * (1 - u) ** 2) + (sag * 0.5 * 3 * u * u * (1 - u)) + sag * u ** 3)
    for k, u in enumerate((0.25, 0.45, 0.65, 0.85)):
        if u > grow + 0.05: continue
        px, py = pt(u); lr = 15 * (1 - 0.45 * wither) * min(1, grow * 1.4)
        d = -1 if k % 2 == 0 else 1
        vine_leaf(cr, px + 4, py + d * (lr + 2) + (wither * 10 if d > 0 else 0), lr, rot=(0.3 * d + wither * 1.4))
        cr.set_line_width(2.5); cr.move_to(px, py); cr.curve_to(px + 6, py - 6, px + 12, py - 10, px + 10, py - 18); cr.stroke()
    if grapes > 0:
        for k, u in enumerate((0.38, 0.62, 0.9)):
            if u > grow: continue
            px, py = pt(u); g = grapes * (1 - 0.55 * wither)
            cr.set_line_width(2); cr.move_to(px, py); cr.line_to(px, py + 8 * g); cr.stroke()
            rows = (4, 3, 3, 2, 1) if grapes > 0.6 else (3, 2, 1)
            rr = 4.6 * g + 0.6
            for ri, n in enumerate(rows):
                for c in range(n):
                    cr.arc(px + (c - (n - 1) / 2) * rr * 1.9, py + 10 * g + ri * rr * 1.7, rr, 0, 2 * math.pi); cr.fill()
    cr.restore()

def fire(cr, x, gy, size, t, logs=True):
    """Campfire on gy; size 0..1."""
    cr.set_source_rgb(*INK); cr.set_line_cap(cairo.LINE_CAP_ROUND)
    if logs:
        cr.set_line_width(9)
        cr.move_to(x - 40, gy - 3); cr.line_to(x + 34, gy - 16); cr.stroke()
        cr.move_to(x + 40, gy - 3); cr.line_to(x - 34, gy - 16); cr.stroke()
    if size <= 0: return
    g = cairo.RadialGradient(x, gy - 40 * size, 0, x, gy - 40 * size, 170 * size)
    g.add_color_stop_rgba(0, 1, 0.75, 0.3, 0.5 * size); g.add_color_stop_rgba(1, 1, 0.75, 0.3, 0)
    cr.set_source(g); cr.rectangle(x - 200, gy - 220, 400, 220); cr.fill()
    for k, (dx, hh, w, c) in enumerate(((-16, 60, 18, (0.95, 0.45, 0.15)), (14, 70, 18, (0.95, 0.45, 0.15)),
                                         (0, 95, 24, (0.97, 0.55, 0.18)), (-4, 55, 13, (1, 0.82, 0.35)), (6, 48, 11, (1, 0.82, 0.35)))):
        f = 1 + 0.15 * math.sin(t * 11 + k * 2.1) + 0.08 * math.sin(t * 23 + k)
        h = hh * size * f; ww = w * size; sw = 6 * math.sin(t * 7 + k) * size
        cr.set_source_rgb(*c)
        cr.move_to(x + dx - ww, gy - 8)
        cr.curve_to(x + dx - ww, gy - 8 - h * 0.5, x + dx + sw - ww * 0.2, gy - 8 - h * 0.7, x + dx + sw, gy - 8 - h)
        cr.curve_to(x + dx + sw + ww * 0.2, gy - 8 - h * 0.7, x + dx + ww, gy - 8 - h * 0.5, x + dx + ww, gy - 8)
        cr.close_path(); cr.fill()

def wolf(cr, x, gy, s=1.0, face=-1, step=0.0, crouch=0.0, color=INK):
    """Silhouette wolf standing on gy (x = body centre). step = gait phase (0 = still); crouch 0..1 lowers it to snarl."""
    cr.save(); cr.translate(x, gy); cr.scale(face * s, s)
    cr.set_source_rgb(*color); cr.set_line_cap(cairo.LINE_CAP_ROUND); cr.set_line_join(cairo.LINE_JOIN_ROUND)
    by = -46 + 12 * crouch
    cr.set_line_width(6)
    for k, (lx, ph) in enumerate(((-30, 0), (-20, math.pi), (24, math.pi), (34, 0))):
        sw = 11 * math.sin(step + ph) if step else 0
        kx = lx + sw * 0.5 + (4 if lx < 0 else -3)
        cr.move_to(lx, by + 4); cr.line_to(kx, (by + 4) * 0.45); cr.line_to(lx + sw, 0); cr.stroke()
    cr.save(); cr.translate(0, by); cr.scale(42, 15); cr.arc(0, 0, 1, 0, 2 * math.pi); cr.restore(); cr.fill()
    cr.save(); cr.translate(22, by - 6); cr.scale(20, 15); cr.arc(0, 0, 1, 0, 2 * math.pi); cr.restore(); cr.fill()
    # neck + head
    hx, hy = 52, by - 16 + 14 * crouch
    cr.move_to(28, by - 14); cr.line_to(hx - 4, hy - 10); cr.line_to(hx + 4, hy + 8); cr.line_to(34, by + 8); cr.close_path(); cr.fill()
    cr.save(); cr.translate(hx, hy); cr.scale(13, 10); cr.arc(0, 0, 1, 0, 2 * math.pi); cr.restore(); cr.fill()
    cr.move_to(hx + 6, hy - 6); cr.line_to(hx + 30, hy + 2); cr.line_to(hx + 28, hy + 6); cr.line_to(hx + 4, hy + 8); cr.close_path(); cr.fill()
    cr.move_to(hx - 8, hy - 6); cr.line_to(hx - 6, hy - 22); cr.line_to(hx + 2, hy - 8); cr.close_path(); cr.fill()
    cr.move_to(hx - 1, hy - 7); cr.line_to(hx + 3, hy - 21); cr.line_to(hx + 8, hy - 6); cr.close_path(); cr.fill()
    # bushy tail
    cr.move_to(-38, by - 6); cr.curve_to(-60, by - 4 + 8 * crouch, -70, by + 14, -74, by + 26)
    cr.curve_to(-62, by + 22, -50, by + 10, -36, by + 6); cr.close_path(); cr.fill()
    cr.restore()

def tare(cr, x, gy, h, sway=0.0, color=INK):
    """A weed (thistle-like) standing among the wheat: jagged leaves and a spiky head."""
    if h <= 1: return
    cr.set_source_rgb(*color); cr.set_line_cap(cairo.LINE_CAP_ROUND); cr.set_line_width(3.5)
    tx = x + sway * h * 0.1; ty = gy - h
    cr.move_to(x, gy); cr.curve_to(x, gy - h * 0.5, tx, ty + h * 0.3, tx, ty); cr.stroke()
    for f, d in ((0.25, 1), (0.42, -1), (0.6, 1)):
        if h < 30: break
        lx, ly = x + sway * h * 0.1 * f, gy - h * f; L = min(26, h * 0.3)
        cr.move_to(lx, ly)
        for j in range(1, 5):
            u = j / 4.0
            cr.line_to(lx + d * L * u, ly - L * 0.5 * u + (7 if j % 2 else -5) * min(1, h / 60))
        cr.stroke()
    r = min(13, h * 0.12)
    if r > 2:
        cr.arc(tx, ty, r, 0, 2 * math.pi); cr.fill()
        cr.set_line_width(2.5)
        for k in range(9):
            a = math.pi * (0.9 + k * 1.2 / 8)
            cr.move_to(tx + math.cos(a) * r, ty + math.sin(a) * r); cr.line_to(tx + math.cos(a) * r * 2.0, ty + math.sin(a) * r * 2.0); cr.stroke()

def sheaf(cr, x, gy, s=1.0, color=INK, weed=False):
    """Bound bundle of stalks standing on gy (weed=True draws spiky heads instead of grain)."""
    cr.set_source_rgb(*color); cr.set_line_cap(cairo.LINE_CAP_ROUND); cr.set_line_width(3 * s)
    for k in range(-4, 5):
        bx = x + k * 4 * s; tx = x + k * 9 * s; ty = gy - 78 * s + abs(k) * 3 * s
        cr.move_to(bx, gy); cr.line_to(x + k * 2 * s, gy - 38 * s); cr.line_to(tx, ty); cr.stroke()
        if weed:
            cr.arc(tx, ty, 5 * s, 0, 2 * math.pi); cr.fill()
        else:
            cr.save(); cr.translate(tx, ty - 5 * s); cr.rotate(k * 0.08); cr.scale(4 * s, 10 * s); cr.arc(0, 0, 1, 0, 2 * math.pi); cr.restore(); cr.fill()
    cr.set_line_width(7 * s); cr.move_to(x - 12 * s, gy - 38 * s); cr.line_to(x + 12 * s, gy - 38 * s); cr.stroke()

def treasure_chest(cr, x, gy, open_=0.0, glow=0.0, s=1.0):
    """Chest centred at x sitting on gy; open_ 0..1 swings the lid back; glow 0..1 shines from inside."""
    w, h = 64 * s, 36 * s
    if glow > 0:
        g = cairo.RadialGradient(x, gy - h, 0, x, gy - h, 260 * glow * s)
        g.add_color_stop_rgba(0, 1, 0.86, 0.45, 0.75 * glow); g.add_color_stop_rgba(1, 1, 0.86, 0.45, 0)
        cr.set_source(g); cr.rectangle(x - 300, gy - 300, 600, 300); cr.fill()
        cr.set_source_rgba(1, 0.8, 0.35, 0.9 * glow * open_); cr.set_line_width(3)
        for k in range(7):
            a = math.pi + (k + 0.5) * math.pi / 7
            cr.move_to(x + math.cos(a) * 46 * s, gy - h + math.sin(a) * 40 * s)
            cr.line_to(x + math.cos(a) * (70 + 40 * glow) * s, gy - h + math.sin(a) * (64 + 40 * glow) * s); cr.stroke()
    cr.set_source_rgb(*INK)
    cr.rectangle(x - w / 2, gy - h, w, h); cr.fill()
    cr.save(); cr.translate(x - w / 2, gy - h); cr.rotate(-math.radians(105) * open_)
    cr.move_to(0, 0); cr.line_to(w, 0); cr.curve_to(w, -16 * s, w * 0.8, -22 * s, w / 2, -22 * s)
    cr.curve_to(w * 0.2, -22 * s, 0, -16 * s, 0, 0); cr.close_path(); cr.fill(); cr.restore()
    cr.set_source_rgb(*BG); cr.set_line_width(2.5 * s)
    cr.move_to(x - w / 2 + 3, gy - h + 10 * s); cr.line_to(x + w / 2 - 3, gy - h + 10 * s); cr.stroke()
    cr.rectangle(x - 5 * s, gy - h + 6 * s, 10 * s, 10 * s); cr.fill()
    if open_ > 0.3:
        for k in range(5):
            cr.set_source_rgba(1, 0.82, 0.4, clamp((open_ - 0.3) * 2))
            cr.arc(x - 22 * s + k * 11 * s, gy - h - 2 * s - (k % 2) * 4 * s, 6 * s, 0, 2 * math.pi); cr.fill()

def barn(cr, x, gy, w=180, h=120, built=1.0, color=INK):
    """Gabled barn centred at x, rising from gy as built goes 0..1 (run backwards to tear it down)."""
    if built <= 0: return
    roof = w * 0.38
    cr.save(); reveal = (h + roof) * built
    cr.rectangle(x - w, gy - reveal, 2 * w, reveal + 1); cr.clip()
    cr.set_source_rgb(*color)
    cr.rectangle(x - w / 2, gy - h, w, h); cr.fill()
    cr.move_to(x - w / 2 - 14, gy - h + 1); cr.line_to(x, gy - h - roof); cr.line_to(x + w / 2 + 14, gy - h + 1); cr.close_path(); cr.fill()
    dw, dh = w * 0.42, h * 0.62
    cr.set_source_rgb(*BG); cr.set_line_width(3)
    cr.rectangle(x - dw / 2, gy - dh, dw, dh); cr.stroke()
    cr.move_to(x - dw / 2, gy - dh); cr.line_to(x + dw / 2, gy); cr.move_to(x + dw / 2, gy - dh); cr.line_to(x - dw / 2, gy); cr.stroke()
    cr.move_to(x, gy - dh); cr.line_to(x, gy); cr.stroke()
    cr.arc(x, gy - h - roof * 0.4, roof * 0.17, 0, 2 * math.pi); cr.fill()
    cr.restore()

def grain_sack(cr, x, gy, s=1.0, color=INK):
    cr.set_source_rgb(*color)
    cr.move_to(x - 16 * s, gy); cr.curve_to(x - 22 * s, gy - 22 * s, x - 14 * s, gy - 38 * s, x - 5 * s, gy - 40 * s)
    cr.line_to(x + 5 * s, gy - 40 * s); cr.curve_to(x + 14 * s, gy - 38 * s, x + 22 * s, gy - 22 * s, x + 16 * s, gy); cr.close_path(); cr.fill()
    cr.move_to(x - 4 * s, gy - 39 * s); cr.line_to(x - 9 * s, gy - 50 * s); cr.line_to(x + 9 * s, gy - 50 * s); cr.line_to(x + 4 * s, gy - 39 * s); cr.fill()

def candle(cr, x, y, lit=1.0, t=0.0, smoke=0.0):
    """Candle on a small dish; (x, y) = base. Returns flame position."""
    cr.set_source_rgb(*INK)
    cr.save(); cr.translate(x, y - 3); cr.scale(18, 4); cr.arc(0, 0, 1, 0, 2 * math.pi); cr.restore(); cr.fill()
    cr.rectangle(x - 6, y - 40, 12, 38); cr.fill()
    cr.set_line_width(2); cr.move_to(x, y - 40); cr.line_to(x, y - 46); cr.stroke()
    fx, fy = x, y - 56
    if lit > 0:
        f = 1 + 0.1 * math.sin(t * 13) + 0.06 * math.sin(t * 31)
        cr.save(); cr.translate(fx, fy); cr.scale(5.5 * lit * f, 11 * lit * f)
        cr.set_source_rgba(1, 0.75, 0.25, 1); cr.arc(0, 0, 1, 0, 2 * math.pi); cr.restore(); cr.fill()
    if smoke > 0:
        cr.set_source_rgba(*SOFT, 0.8 * smoke * (1 - smoke * 0.3)); cr.set_line_width(2.5)
        cr.move_to(x, y - 46)
        for k in range(1, 7):
            cr.line_to(x + 6 * math.sin(k * 1.3 + t * 3), y - 46 - k * 9 * (0.5 + smoke))
        cr.stroke()
    return (fx, fy)

def plain_stool(cr, x, gy, h=44, w=56, color=INK):
    cr.set_source_rgb(*color); cr.set_line_width(5); cr.set_line_cap(cairo.LINE_CAP_ROUND)
    cr.rectangle(x - w / 2, gy - h - 6, w, 8); cr.fill()
    cr.move_to(x - w / 2 + 6, gy - h); cr.line_to(x - w / 2 + 2, gy); cr.stroke()
    cr.move_to(x + w / 2 - 6, gy - h); cr.line_to(x + w / 2 - 2, gy); cr.stroke()
    return gy - h - 6

def judge_seat(cr, x, gy, face=-1, color=INK):
    """Raised dais with a high-backed seat; seat faces `face`. Returns (seat_floor_y, seat_top_y)."""
    cr.set_source_rgb(*color)
    cr.rectangle(x - 95, gy - 26, 190, 26); cr.fill()
    cr.rectangle(x - 105, gy - 32, 210, 8); cr.fill()
    fy = gy - 32
    bx = x - face * 30
    cr.rectangle(bx - 6, fy - 150, 12, 150); cr.fill()
    cr.arc(bx, fy - 150, 10, 0, 2 * math.pi); cr.fill()
    cr.rectangle(min(bx, x + face * 22) - 4, fy - 48, abs(x + face * 22 - bx) + 8, 8); cr.fill()
    cr.set_line_width(5); cr.move_to(x + face * 18, fy - 44); cr.line_to(x + face * 22, fy); cr.stroke()
    return fy, fy - 48

def crescent_moon(cr, x, y, r=22, alpha=1.0, color=BG):
    """Crescent crescent_moon (draw after darkness())."""
    if alpha <= 0: return
    cr.push_group()
    cr.set_source_rgb(*color); cr.arc(x, y, r, 0, 2 * math.pi); cr.fill()
    cr.set_operator(cairo.OPERATOR_DEST_OUT); cr.arc(x + r * 0.45, y - r * 0.2, r * 0.85, 0, 2 * math.pi); cr.fill()
    cr.set_operator(cairo.OPERATOR_OVER)
    cr.pop_group_to_source(); cr.paint_with_alpha(alpha)

def held_angle(p, face=1, arm="r"):
    """Screen angle (degrees, 0 = up, 90 = right) of a figure's forearm, for aiming held tools (axe etc.)."""
    a = math.radians(p[arm + "s"] + p[arm + "e"])
    return math.degrees(math.atan2(face * math.sin(a), -math.cos(a)))

def grape_cluster(cr, x, y, s=1.0, color=INK):
    """Loose bunch of grapes hanging from (x, y)."""
    cr.set_source_rgb(*color); cr.set_line_width(2.5 * s); cr.move_to(x, y); cr.line_to(x, y + 8 * s); cr.stroke()
    rr = 5.2 * s
    for ri, n in enumerate((4, 4, 3, 2, 1)):
        for c in range(n):
            cr.arc(x + (c - (n - 1) / 2) * rr * 1.9, y + 12 * s + ri * rr * 1.7, rr, 0, 2 * math.pi); cr.fill()

def pearl(cr, x, y, r=12, glow=0.0):
    """Shining pearl centred at (x, y)."""
    if glow > 0:
        g = cairo.RadialGradient(x, y, 0, x, y, r * 12 * glow)
        g.add_color_stop_rgba(0, 1, 0.95, 0.8, 0.8 * glow); g.add_color_stop_rgba(1, 1, 0.95, 0.8, 0)
        cr.set_source(g); cr.arc(x, y, r * 12 * glow, 0, 2 * math.pi); cr.fill()
    cr.set_source_rgb(1, 0.98, 0.93); cr.arc(x, y, r, 0, 2 * math.pi); cr.fill()
    cr.set_source_rgb(*INK); cr.set_line_width(2.5); cr.arc(x, y, r, 0, 2 * math.pi); cr.stroke()
    cr.set_source_rgba(*SOFT, 0.7); cr.arc(x + r * 0.25, y + r * 0.25, r * 0.5, 0, 2 * math.pi); cr.fill()
    cr.set_source_rgb(1, 1, 1); cr.arc(x - r * 0.35, y - r * 0.35, r * 0.22, 0, 2 * math.pi); cr.fill()

def dirt_mound(cr, x, gy, w=60, h=14, color=INK):
    if h <= 0.5: return
    cr.set_source_rgb(*color); cr.save(); cr.translate(x, gy); cr.scale(w / 2, h)
    cr.arc(0, 0, 1, math.pi, 2 * math.pi); cr.restore(); cr.fill()

# ---- props added by worker 3 ----
from engine import pose as _pose

def sit_pose(**over):
    """Seated on a bench/stool about 45px high (thighs forward, shins down)."""
    p = _pose("stand", lt=90, lk=90, rt=84, rk=84, ls=40, le=30, rs=35, re=40); p.update(over); return p

def bench(cr, x0, x1, gy, h=44):
    cr.set_source_rgb(*INK); cr.rectangle(x0, gy - h, x1 - x0, 9); cr.fill()
    cr.set_line_width(6)
    for lx in (x0 + 12, x1 - 12):
        cr.move_to(lx, gy - h); cr.line_to(lx, gy); cr.stroke()

def meal_table(cr, x0, x1, gy, h=58):
    cr.set_source_rgb(*INK); cr.rectangle(x0, gy - h, x1 - x0, 10); cr.fill()
    cr.set_line_width(7)
    for lx in (x0 + 16, x1 - 16):
        cr.move_to(lx, gy - h); cr.line_to(lx, gy); cr.stroke()
    return gy - h

def cup(cr, x, y, s=1.0):
    """Goblet standing on y."""
    cr.set_source_rgb(*INK)
    cr.move_to(x - 11*s, y - 34*s); cr.curve_to(x - 10*s, y - 16*s, x + 10*s, y - 16*s, x + 11*s, y - 34*s); cr.close_path(); cr.fill()
    cr.set_line_width(3*s); cr.move_to(x, y - 20*s); cr.line_to(x, y - 2*s); cr.stroke()
    cr.move_to(x - 8*s, y - 1*s); cr.line_to(x + 8*s, y - 1*s); cr.stroke()

def basin(cr, x, gy, w=74, water_lvl=0.0):
    """Shallow bowl resting on gy, centred at x; water_lvl 0..1 shows a pale water line."""
    cr.set_source_rgb(*INK)
    cr.move_to(x - w/2, gy - 18); cr.line_to(x + w/2, gy - 18)
    cr.curve_to(x + w/2 - 4, gy - 4, x + w/4, gy, x, gy); cr.curve_to(x - w/4, gy, x - w/2 + 4, gy - 4, x - w/2, gy - 18)
    cr.close_path(); cr.fill()
    if water_lvl > 0:
        cr.set_source_rgba(0.55, 0.7, 0.8, water_lvl); cr.set_line_width(3)
        cr.move_to(x - w/2 + 6, gy - 16); cr.line_to(x + w/2 - 6, gy - 16); cr.stroke()

def pitcher(cr, x, y, tilt=0.0, face=1):
    """Jug standing with its base centre at (x, y); tilt in degrees pours toward face. Returns spout (x, y)."""
    cr.save(); cr.translate(x, y); cr.scale(face, 1); cr.rotate(math.radians(tilt))
    cr.set_source_rgb(*INK)
    cr.move_to(-9, 0); cr.curve_to(-19, -12, -16, -30, -7, -36); cr.line_to(-7, -44); cr.line_to(8, -46)
    cr.line_to(16, -50); cr.line_to(9, -38); cr.curve_to(18, -28, 19, -12, 9, 0); cr.close_path(); cr.fill()
    cr.set_line_width(3.5); cr.move_to(-8, -40); cr.curve_to(-24, -40, -24, -18, -14, -14); cr.stroke()
    sp = cr.user_to_device(16, -50); cr.restore()
    return sp

def cape(cr, J, face=1, s=1.0):
    """Outer mantle hanging from the shoulders down the back (draw before the figure)."""
    sx, sy = J["sh"]; hx, hy = J["hip"]
    cr.set_source_rgb(*INK)
    cr.move_to(sx + face*6*s, sy - 2*s); cr.line_to(sx - face*14*s, sy + 4*s)
    cr.curve_to(sx - face*30*s, sy + 50*s, hx - face*34*s, hy + 30*s, hx - face*30*s, hy + 52*s)
    cr.line_to(hx + face*4*s, hy + 52*s); cr.line_to(hx + face*4*s, hy); cr.close_path(); cr.fill()

def folded_cloth(cr, x, y, w=56, h=13):
    """Folded garment lying on a surface at y."""
    cr.set_source_rgb(*INK); r = 5
    cr.new_sub_path(); cr.arc(x + w/2 - r, y - h + r, r, -math.pi/2, 0); cr.line_to(x + w/2, y)
    cr.line_to(x - w/2, y); cr.arc(x - w/2 + r, y - h + r, r, math.pi, 3*math.pi/2); cr.close_path(); cr.fill()
    cr.set_source_rgb(*BG); cr.set_line_width(1.5); cr.move_to(x - w/2 + 6, y - h/2); cr.line_to(x + w/2 - 6, y - h/2); cr.stroke()

def hanging_cloth(cr, x, y, L=46, sway=0.0):
    """Cloth dangling from a hand at (x, y)."""
    cr.set_source_rgb(*INK)
    cr.move_to(x - 6, y); cr.curve_to(x - 10 + sway, y + L*0.5, x - 14 + sway*2, y + L*0.8, x - 12 + sway*2, y + L)
    cr.line_to(x + 12 + sway*2, y + L); cr.curve_to(x + 10 + sway*2, y + L*0.6, x + 8 + sway, y + L*0.3, x + 6, y); cr.close_path(); cr.fill()

def towel_wrap(cr, J, face=1, s=1.0, amount=1.0):
    """Pale towel girded round the waist with one end hanging (draw after the figure)."""
    if amount <= 0: return
    hx, hy = J["hip"]; sx, sy = J["sh"]
    u = 0.22; cx, cy = lerp(hx, sx, u), lerp(hy, sy, u)
    cr.save(); cr.translate(cx, cy); cr.rotate(math.atan2(sx - hx, hy - sy))
    cr.set_source_rgba(*BG, amount); cr.rectangle(-17*s, -6*s, 34*s, 12*s); cr.fill()
    cr.move_to(face*6*s, 4*s); cr.line_to(face*16*s, 4*s); cr.line_to(face*13*s, 30*s); cr.line_to(face*4*s, 28*s); cr.close_path(); cr.fill()
    cr.set_source_rgba(*INK, amount); cr.set_line_width(1.5)
    cr.move_to(-17*s, 0); cr.line_to(17*s, 0); cr.stroke()
    cr.restore()

def campfire(cr, x, gy, t, s=1.0, lit=1.0):
    """Small fire of coals/sticks; flames flicker in warm colour."""
    cr.set_source_rgb(*INK); cr.set_line_width(7*s); cr.set_line_cap(cairo.LINE_CAP_ROUND)
    cr.move_to(x - 30*s, gy - 3); cr.line_to(x + 22*s, gy - 15*s); cr.stroke()
    cr.move_to(x + 30*s, gy - 3); cr.line_to(x - 22*s, gy - 15*s); cr.stroke()
    for k in range(5):
        cr.arc(x - 34*s + k*17*s, gy - 3*s, 6*s, math.pi, 2*math.pi); cr.fill()
    if lit <= 0: return
    for k, (dx, hh, ph) in enumerate(((-12, 34, 0.0), (10, 30, 1.7), (0, 48, 3.1))):
        f = 1 + 0.18*math.sin(t*11 + ph) + 0.1*math.sin(t*23 + ph*2)
        h = hh * s * lit * f; bx = x + dx*s; by = gy - 12*s; sw = 3*s*math.sin(t*7 + ph)
        col = (1, 0.55, 0.15) if k < 2 else (1, 0.72, 0.25)
        cr.set_source_rgba(*col, 0.95)
        cr.move_to(bx - 11*s*lit, by); cr.curve_to(bx - 13*s*lit, by - h*0.5, bx + sw, by - h*0.8, bx + sw, by - h)
        cr.curve_to(bx + sw, by - h*0.8, bx + 13*s*lit, by - h*0.5, bx + 11*s*lit, by); cr.close_path(); cr.fill()
    return (x, gy - 30*s)

def rooster(cr, x, gy, s=1.0, face=1, crow=0.0, color=INK):
    """Rooster standing on gy. crow 0..1 stretches the neck up and opens the beak."""
    cr.save(); cr.translate(x, gy); cr.scale(face*s, s)
    cr.set_source_rgb(*color); cr.set_line_width(3.5); cr.set_line_cap(cairo.LINE_CAP_ROUND)
    for lx in (-4, 6):
        cr.move_to(lx, -26); cr.line_to(lx, 0); cr.stroke(); cr.move_to(lx - 6, 0); cr.line_to(lx + 7, 0); cr.stroke()
    cr.save(); cr.translate(0, -38); cr.scale(22, 15); cr.arc(0, 0, 1, 0, 2*math.pi); cr.restore(); cr.fill()
    for k, a in enumerate((-0.2, 0.25, 0.7)):   # tail plumes
        cr.set_line_width(6 - k)
        cr.move_to(-16, -40); cr.curve_to(-30, -60 - 10*k, -44, -58 + 14*k, -40 + 4*k, -30 + 10*k); cr.stroke()
    nx, ny = lerp(16, 20, crow), lerp(-62, -74, crow)
    cr.set_line_width(11); cr.move_to(12, -44); cr.line_to(nx, ny); cr.stroke()
    cr.arc(nx + 2, ny - 4, 8, 0, 2*math.pi); cr.fill()
    for k in range(3):   # comb
        cr.arc(nx - 4 + k*5, ny - 13 + abs(k - 1)*2, 3.6, 0, 2*math.pi); cr.fill()
    cr.save(); cr.translate(nx + 4, ny + 6); cr.scale(3, 5); cr.arc(0, 0, 1, 0, 2*math.pi); cr.restore(); cr.fill()  # wattle
    op = 0.5 * crow; bx, by = nx + 9, ny - 4
    cr.move_to(bx, by - 2); cr.line_to(bx + 11, by - 2 - 8*op); cr.line_to(bx, by + 1); cr.fill()
    cr.move_to(bx, by + 1); cr.line_to(bx + 10, by + 3 + 8*op); cr.line_to(bx, by + 3); cr.fill()
    if crow > 0.3:   # crow lines
        a = (crow - 0.3) / 0.7
        cr.set_source_rgba(*color, a); cr.set_line_width(3)
        for k in range(3):
            r = 20 + k*12
            cr.arc(bx + 6, by, r, -0.5, 0.5); cr.stroke()
    cr.restore()

def fish(cr, x, y, s=1.0, face=1, color=INK):
    cr.save(); cr.translate(x, y); cr.scale(face*s, s); cr.set_source_rgb(*color)
    cr.move_to(16, 0); cr.curve_to(8, -10, -8, -10, -14, 0); cr.curve_to(-8, 10, 8, 10, 16, 0); cr.fill()
    cr.move_to(-12, 0); cr.line_to(-24, -9); cr.line_to(-24, 9); cr.close_path(); cr.fill()
    cr.set_source_rgb(*BG); cr.arc(9, -2, 1.8, 0, 2*math.pi); cr.fill()
    cr.restore()

def stone_seat(cr, x, gy, w=64, h=46):
    """Rounded rock to sit on (top at gy - h)."""
    cr.set_source_rgb(*INK)
    cr.move_to(x - w/2, gy + 1); cr.curve_to(x - w/2, gy - h*0.8, x - w/4, gy - h, x, gy - h)
    cr.curve_to(x + w/4, gy - h, x + w/2, gy - h*0.8, x + w/2, gy + 1); cr.close_path(); cr.fill()

def courtyard_wall(cr, x0, x1, gy, h=95):
    cr.set_source_rgb(*INK); cr.rectangle(x0, gy - h, x1 - x0, h); cr.fill()
    cr.rectangle(x0 - 8, gy - h - 10, x1 - x0 + 16, 12); cr.fill()
    cr.set_source_rgb(*SOFT); cr.set_line_width(1.5)
    for r in range(1, 4):
        y = gy - h + r * h / 4; cr.move_to(x0, y); cr.line_to(x1, y); cr.stroke()
        for k in range(int((x1 - x0) / 46) + 1):
            xx = x0 + k * 46 + (23 if r % 2 else 0)
            if x0 < xx < x1: cr.move_to(xx, y); cr.line_to(xx, y - h / 4); cr.stroke()

def bread_half(cr, x, y, face=1):
    """Half of a broken loaf; the broken edge faces `face`."""
    cr.set_source_rgb(*INK); cr.save(); cr.translate(x, y); cr.scale(face, 1)
    cr.move_to(4, -9); cr.curve_to(-10, -10, -14, -2, -12, 4); cr.curve_to(-8, 9, 2, 9, 4, 8)
    cr.line_to(1, 4); cr.line_to(5, 0); cr.line_to(1, -4); cr.close_path(); cr.fill(); cr.restore()

def food_basket(cr, x, y, w=52, h=32, loaves=0, fishes=0, full=0.0):
    """Upright woven basket with its base centre at (x, y). loaves/fishes peek over the rim; full 0..1 heaps it."""
    cr.set_source_rgb(*INK)
    if full > 0:
        for k in range(4):
            cr.arc(x - w*0.33 + k * w*0.22, y - h - 2, w*0.16 * full, math.pi, 2*math.pi); cr.fill()
    for k in range(int(loaves)):
        cr.save(); cr.translate(x - w*0.25 + k * w*0.5 / max(1, loaves - 1) if loaves > 1 else x, y - h - 2)
        cr.scale(9, 6); cr.arc(0, 0, 1, math.pi, 2*math.pi); cr.restore(); cr.fill()
    for k in range(int(fishes)):
        fish(cr, x + (k - 0.5) * 14, y - h - 4 - k * 3, s=0.5, face=1 if k % 2 else -1)
    cr.set_source_rgb(*INK)
    cr.move_to(x - w/2, y - h); cr.line_to(x + w/2, y - h); cr.line_to(x + w/2 - 7, y); cr.line_to(x - w/2 + 7, y); cr.close_path(); cr.fill()
    cr.set_source_rgb(*BG); cr.set_line_width(1.6)
    for k in range(1, 3):
        yy = y - h + k * h / 3; cr.move_to(x - w/2 + 3 + k*2, yy); cr.line_to(x + w/2 - 3 - k*2, yy); cr.stroke()

def ground_sit_pose(**over):
    """Sitting on the ground with legs stretched forward."""
    p = _pose("stand", lt=84, lk=-4, rt=78, rk=6, lean=-4, ls=20, le=40, rs=25, re=45); p.update(over); return p

def yoke(cr, x1, y1, x2, y2, s=1.0):
    """Wooden yoke beam resting across two shoulders, with neck bows."""
    cr.set_source_rgb(*INK); cr.set_line_cap(cairo.LINE_CAP_ROUND)
    cr.set_line_width(11*s); cr.move_to(x1 - 18*s, y1 - 6*s); cr.line_to(x2 + 18*s, y2 - 6*s); cr.stroke()
    cr.set_line_width(4*s)
    for (x, y) in ((x1, y1), (x2, y2)):
        cr.arc(x, y - 4*s, 13*s, 0.15, math.pi - 0.15); cr.stroke()

def _rough_f(x):
    return 30 * math.sin(x * 0.029) + 18 * math.sin(x * 0.071 + 1.3) + 10 * math.sin(x * 0.17 + 0.4)

def rough_y(x, x0, gy, rough):
    """Height of a rough_ground surface at x (gy where flat / before x0)."""
    if x <= x0: return gy
    ramp = clamp((x - x0) / 60.0)
    return gy - rough * ramp * (_rough_f(x) - _rough_f(x0) * (1 - ramp))

def rough_ground(cr, x0, x1, gy, rough):
    """Broken, uneven ground from x0 to x1; rough 0 = a straight level path."""
    cr.set_source_rgb(*INK); cr.set_line_width(4); cr.set_line_join(cairo.LINE_JOIN_ROUND)
    cr.move_to(x0, gy)
    x = x0
    while x <= x1:
        cr.line_to(x, rough_y(x, x0, gy, rough)); x += 6
    cr.stroke()
    if rough > 0.05:   # jagged rocks on the broken ground
        for rx in (520, 700, 905):
            if x0 < rx < x1:
                ry = rough_y(rx, x0, gy, rough)
                cr.set_source_rgba(*INK, min(1, rough * 1.5))
                cr.move_to(rx - 22 * rough, ry + 2); cr.line_to(rx - 6, ry - 30 * rough); cr.line_to(rx + 8, ry - 18 * rough)
                cr.line_to(rx + 20 * rough, ry + 2); cr.close_path(); cr.fill()

def held_map(cr, x, y, w=46, h=34, ang=0.0, fold=0.0, alpha=1.0):
    """Paper map held at (x, y); fold 0..1 closes it."""
    w = w * (1 - 0.6 * fold)
    cr.save(); cr.translate(x, y); cr.rotate(ang)
    cr.set_source_rgba(*BG, alpha); cr.rectangle(-w/2, -h/2, w, h); cr.fill()
    cr.set_source_rgba(*INK, alpha); cr.set_line_width(2.5); cr.rectangle(-w/2, -h/2, w, h); cr.stroke()
    cr.set_line_width(1.2)
    for k in (1, 2):
        xx = -w/2 + k * w / 3; cr.move_to(xx, -h/2); cr.line_to(xx, h/2); cr.stroke()
    if fold < 0.5:
        cr.set_dash([3, 3]); cr.set_line_width(1.6)
        cr.move_to(-w/2 + 5, h/2 - 6); cr.curve_to(-w/6, -h/2, w/6, h/2, w/2 - 5, -h/2 + 6); cr.stroke(); cr.set_dash([])
    cr.restore()

def grass_tuft(cr, x, gy, h, sway=0.0):
    """Clump of grass blades h px tall."""
    if h <= 1: return
    cr.set_source_rgb(*INK); cr.set_line_width(2.6); cr.set_line_cap(cairo.LINE_CAP_ROUND)
    for k, d in enumerate((-1.0, -0.5, 0.0, 0.45, 0.9)):
        hh = h * (0.7 + 0.3 * ((k * 7) % 3) / 2)
        tx = x + d * 9 + (d * 6 + sway * 4) * hh / 30
        cr.move_to(x + d * 4, gy); cr.curve_to(x + d * 5, gy - hh * 0.5, tx, gy - hh * 0.8, tx, gy - hh); cr.stroke()

def cliff(cr, x_edge, gy, h, side=1, top=None):
    """Jagged rock wall. side=-1: wall fills to the left of x_edge; side=1: to the right."""
    far = -60 if side < 0 else W + 60
    pts = [(x_edge, gy)]
    n = 6
    for k in range(1, n + 1):
        u = k / n
        jag = (14 if k % 2 else -10)
        pts.append((x_edge + side * (u * 120 + jag), gy - h * min(1, 0.25 + u) + (12 if k % 2 else 0)))
    pts.append((far, gy - h)); pts.append((far, gy + 2))
    cr.set_source_rgb(*INK); cr.move_to(*pts[0])
    for p in pts[1:]: cr.line_to(*p)
    cr.close_path(); cr.fill()

def anchor(cr, x, gy, h=140, glow=0.0):
    """Upright anchor (sign of hope) standing on gy."""
    if glow > 0: warm_glow(cr, x, gy - h * 0.6, 220, glow)
    s = h / 140.0
    cr.set_source_rgb(*INK); cr.set_line_cap(cairo.LINE_CAP_ROUND); cr.set_line_width(9 * s)
    cr.move_to(x, gy - 12 * s); cr.line_to(x, gy - h + 22 * s); cr.stroke()
    cr.set_line_width(6 * s); cr.arc(x, gy - h + 12 * s, 11 * s, 0, 2 * math.pi); cr.stroke()
    cr.set_line_width(8 * s); cr.move_to(x - 30 * s, gy - h + 46 * s); cr.line_to(x + 30 * s, gy - h + 46 * s); cr.stroke()
    cr.arc(x, gy - 58 * s, 50 * s, math.radians(20), math.radians(160)); cr.stroke()
    for d in (-1, 1):
        ex = x + d * 47 * s; ey = gy - 58 * s + 17 * s
        cr.move_to(ex - d * 2 * s, ey - 16 * s); cr.line_to(ex + d * 8 * s, ey + 6 * s); cr.line_to(ex - d * 14 * s, ey + 2 * s); cr.close_path(); cr.fill()

def heart(cr, x, gy, h=120, glow=0.0):
    """Heart (sign of charity) resting on its point at (x, gy)."""
    if glow > 0: warm_glow(cr, x, gy - h * 0.55, 300, glow)
    w = h * 0.55
    cr.set_source_rgb(*INK)
    cr.move_to(x, gy)
    cr.curve_to(x - w * 0.35, gy - h * 0.3, x - w * 1.05, gy - h * 0.55, x - w * 0.95, gy - h * 0.82)
    cr.curve_to(x - w * 0.85, gy - h * 1.08, x - w * 0.15, gy - h * 1.08, x, gy - h * 0.82)
    cr.curve_to(x + w * 0.15, gy - h * 1.08, x + w * 0.85, gy - h * 1.08, x + w * 0.95, gy - h * 0.82)
    cr.curve_to(x + w * 1.05, gy - h * 0.55, x + w * 0.35, gy - h * 0.3, x, gy)
    cr.close_path(); cr.fill()

# ---- props added by worker 4 ----
WATER_C = (0.50, 0.62, 0.72)     # water tint for jars / pouring
WINE_C = (0.50, 0.10, 0.18)      # wine tint

def veil_drape(cr, J, s=1.0, face=1, color=INK):
    """Head veil for a woman (Mary etc.). Call right after draw_figure with its joints J; same s/face/color."""
    hx, hy = J["head"]; sx, sy = J["sh"]; HR = 12.5 * s
    cr.set_source_rgb(*color)
    cr.save(); cr.translate(hx, hy); cr.scale(1.0, 1.15); cr.arc(0, 0, HR + 3 * s, 0, 2 * math.pi); cr.restore(); cr.fill()
    cr.move_to(hx + face * HR * 0.4, hy - HR * 1.15)
    cr.curve_to(hx - face * HR * 1.7, hy - HR * 1.0, hx - face * HR * 2.0, sy, hx - face * HR * 1.6, sy + 36 * s)
    cr.line_to(sx - face * 3 * s, sy + 24 * s)
    cr.line_to(sx + face * 4 * s, sy)
    cr.close_path(); cr.fill()

def angel_wings(cr, x, y, s=1.0, face=1, spread=1.0, color=INK):
    """Two wings rooted at shoulder point (x, y), sweeping up and behind (away from face). spread 0..1 opens them."""
    far = tuple(min(1, c + 0.14) for c in color)
    for col, dx, dy, rot in ((far, 10, -8, -0.18), (color, 0, 0, 0.0)):
        cr.save(); cr.translate(x - face * (14 - dx) * s, y + (8 + dy) * s); cr.scale(-face * s * 0.85, s * 0.85)
        cr.rotate(rot - 0.12 + 0.55 * (1 - spread))
        cr.set_source_rgb(*col)
        cr.move_to(0, 0)
        cr.curve_to(8, -62, 58, -122, 122, -142)
        prev = (122, -142)
        for (tx, ty) in ((114, -98), (100, -58), (80, -24), (54, 4), (24, 20)):
            mx, my = (prev[0] + tx) / 2, (prev[1] + ty) / 2
            dx, dy = ty - prev[1], -(tx - prev[0]); L = math.hypot(dx, dy) or 1
            cr.curve_to(mx + dx / L * 16, my + dy / L * 16, mx + dx / L * 16, my + dy / L * 16, tx, ty)
            prev = (tx, ty)
        cr.line_to(4, 12); cr.close_path(); cr.fill(); cr.restore()

def angel_figure(cr, x, gy, p, s=1.0, face=1, alpha=1.0, spread=1.0):
    """Robed winged silhouette (no face), drawn as one group so it can fade in/out with alpha."""
    if alpha <= 0.01: return None
    cr.push_group(); J = draw_figure_(cr, x, gy, p, s=s, face=face, prop="robe"); cr.pop_group()   # joints only
    cr.push_group()
    angel_wings(cr, J["sh"][0], J["sh"][1], s=s, face=face, spread=spread)
    draw_figure_(cr, x, gy, p, s=s, face=face, prop="robe")
    cr.pop_group_to_source(); cr.paint_with_alpha(alpha)
    return J

def draw_figure_(*a, **k):
    from engine import draw_figure
    return draw_figure(*a, **k)

def watering_jug(cr, hx, hy, tilt=0.0, face=1, s=1.0, color=INK):
    """Jug carried by its handle at the hand (hx, hy); tilt (deg) > 0 tips the spout forward/down. Returns spout tip."""
    cr.save(); cr.translate(hx, hy); cr.scale(face * s, s); cr.rotate(math.radians(tilt))
    cr.set_source_rgb(*color)
    cr.set_line_width(4); cr.arc(4, 8, 9, math.pi, 2 * math.pi); cr.stroke()
    cr.save(); cr.translate(6, 26); cr.scale(17, 15); cr.arc(0, 0, 1, 0, 2 * math.pi); cr.restore(); cr.fill()
    cr.rectangle(-2, 8, 14, 8); cr.fill()
    cr.move_to(16, 20); cr.line_to(38, 4); cr.line_to(40, 8); cr.line_to(20, 28); cr.close_path(); cr.fill()
    tip = cr.user_to_device(40, 5)
    cr.restore()
    return tip

def pour_drops(cr, x, y, y1, t, amount=1.0, color=WATER_C, drift=6):
    """Falling droplets from (x, y) down to y1."""
    if amount <= 0: return
    cr.set_source_rgba(*color, 0.95 * amount)
    for k in range(9):
        u = (t * 2.6 + k / 9.0) % 1.0
        cr.save(); cr.translate(x + drift * u, y + u * (y1 - y)); cr.scale(2.4, 5.0)
        cr.arc(0, 0, 1, 0, 2 * math.pi); cr.restore(); cr.fill()

def stone_water_jar(cr, x, gy, fill=0.0, fill_color=WATER_C, w=58, h=96):
    """Large outlined stone jar standing on gy; fill 0..1 shows the liquid level in fill_color."""
    def path():
        cr.move_to(x - w * 0.28, gy)
        cr.curve_to(x - w * 0.64, gy - h * 0.35, x - w * 0.56, gy - h * 0.8, x - w * 0.3, gy - h * 0.88)
        cr.line_to(x - w * 0.36, gy - h); cr.line_to(x + w * 0.36, gy - h); cr.line_to(x + w * 0.3, gy - h * 0.88)
        cr.curve_to(x + w * 0.56, gy - h * 0.8, x + w * 0.64, gy - h * 0.35, x + w * 0.28, gy)
        cr.close_path()
    path(); cr.set_source_rgb(*BG); cr.fill_preserve()
    if fill > 0:
        cr.save(); cr.clip_preserve()
        cr.set_source_rgb(*fill_color); cr.rectangle(x - w, gy - h * 0.92 * fill, 2 * w, h); cr.fill(); cr.restore()
    cr.new_path(); path(); cr.set_source_rgb(*INK); cr.set_line_width(5); cr.stroke()

def wine_goblet(cr, x, y, s=1.0, wine=0.0):
    """Small cup; (x, y) = foot. wine 0..1 shows red at the rim."""
    cr.set_source_rgb(*INK)
    cr.save(); cr.translate(x, y - 2 * s); cr.scale(8 * s, 2.5 * s); cr.arc(0, 0, 1, 0, 2 * math.pi); cr.restore(); cr.fill()
    cr.rectangle(x - 1.5 * s, y - 14 * s, 3 * s, 12 * s); cr.fill()
    cr.move_to(x - 10 * s, y - 28 * s); cr.line_to(x + 10 * s, y - 28 * s)
    cr.curve_to(x + 10 * s, y - 16 * s, x + 4 * s, y - 13 * s, x, y - 13 * s)
    cr.curve_to(x - 4 * s, y - 13 * s, x - 10 * s, y - 16 * s, x - 10 * s, y - 28 * s); cr.fill()
    if wine > 0:
        cr.set_source_rgba(*WINE_C, wine)
        cr.save(); cr.translate(x, y - 27 * s); cr.scale(8 * s, 2.6 * s); cr.arc(0, 0, 1, 0, 2 * math.pi); cr.restore(); cr.fill()

def feast_table(cr, x0, x1, gy, h=64):
    cr.set_source_rgb(*INK)
    cr.rectangle(x0, gy - h, x1 - x0, 10); cr.fill()
    cr.move_to(x0 - 6, gy - h); cr.line_to(x1 + 6, gy - h); cr.line_to(x1, gy - h + 22); cr.line_to(x0, gy - h + 22); cr.close_path(); cr.fill()
    for lx in (x0 + 14, x1 - 14):
        cr.rectangle(lx - 4, gy - h, 8, h); cr.fill()

def sweep_broom(cr, hx, hy, bx, gy):
    """Broom held at the hand (hx, hy) with its bristles on the floor at bx."""
    cr.set_source_rgb(*INK); cr.set_line_width(4); cr.set_line_cap(cairo.LINE_CAP_ROUND)
    by = gy - 28
    tx, ty = hx + (hx - bx) * 0.25, hy + (hy - by) * 0.25
    cr.move_to(tx, ty); cr.line_to(bx, by); cr.stroke()
    cr.move_to(bx - 6, by - 2); cr.line_to(bx + 6, by - 2); cr.line_to(bx + 17, gy); cr.line_to(bx - 17, gy); cr.close_path(); cr.fill()

def rising_wall(cr, x, gy, rise, w=64, h=180):
    """Brick wall column centred at x that grows up out of the ground (rise 0..1)."""
    if rise <= 0: return
    top = gy - h * rise
    cr.set_source_rgb(*INK); cr.rectangle(x - w / 2, top, w, gy - top); cr.fill()
    cr.set_source_rgb(*BG); cr.set_line_width(2)
    row = 0; y = gy - 18
    while y > top + 4:
        cr.move_to(x - w / 2, y); cr.line_to(x + w / 2, y); cr.stroke()
        off = 0 if row % 2 else w / 2
        cr.move_to(x - w / 2 + off / 2 + w / 4, y); cr.line_to(x - w / 2 + off / 2 + w / 4, y + 18); cr.stroke()
        y -= 18; row += 1

def coin_glint(cr, x, y, amount, t=0.0, r=26):
    """Golden four-point sparkle (a found coin catching the light)."""
    if amount <= 0: return
    rr = r * amount * (1 + 0.15 * math.sin(t * 9))
    cr.save(); cr.translate(x, y); cr.rotate(0.3 * math.sin(t * 2))
    cr.set_source_rgba(1, 0.80, 0.30, 0.95 * amount)
    for k in range(4):
        cr.save(); cr.rotate(k * math.pi / 2)
        cr.move_to(0, -rr); cr.line_to(rr * 0.18, -rr * 0.18); cr.line_to(0, 0); cr.line_to(-rr * 0.18, -rr * 0.18); cr.close_path(); cr.fill()
        cr.restore()
    cr.restore()

def arched_window(cr, x, y, w=80, h=120, light=0.0):
    """Arched window outline; (x, y) = bottom-left. light 0..1 fills the glass warm."""
    r = w / 2
    def path():
        cr.move_to(x, y); cr.line_to(x, y - h + r); cr.arc(x + r, y - h + r, r, math.pi, 2 * math.pi); cr.line_to(x + w, y); cr.close_path()
    if light > 0:
        path(); cr.set_source_rgba(1, 0.9, 0.6, light); cr.fill()
    path(); cr.set_source_rgb(*INK); cr.set_line_width(5); cr.stroke()
    cr.set_line_width(3); cr.move_to(x + r, y - h); cr.line_to(x + r, y); cr.stroke()
    cr.move_to(x, y - h * 0.45); cr.line_to(x + w, y - h * 0.45); cr.stroke()
    cr.set_line_width(6); cr.move_to(x - 10, y + 3); cr.line_to(x + w + 10, y + 3); cr.stroke()

def door_frame_lit(cr, x, gy, open_=0.0, light=0.0, w=78, h=165):
    """Interior doorway (x = left edge). open_ 0..1 swings the leaf in; light fills the opening."""
    if light > 0:
        cr.set_source_rgba(1, 0.95, 0.75, light); cr.rectangle(x, gy - h, w, h); cr.fill()
    cr.set_source_rgb(*INK); cr.set_line_width(5); cr.rectangle(x, gy - h, w, h); cr.stroke()
    lw = w * (1 - 0.85 * open_)
    cr.rectangle(x + w - lw, gy - h, lw, h); cr.fill()

# ---- Day 29: healing through the roof / let the children come ----
INTERIOR = (0.875, 0.845, 0.785)

def cutaway_house(cr, x0, x1, gy, h=200, door=(0, 0), hole=None, open_=0.0, slab=16, wall=12):
    """Flat-roofed house drawn as a cutaway (interior visible). door=(dx0, dx1) gap in the left wall
    (absolute x; (0,0) = none). hole=(hx0, hx1): roof section that opens from its centre, open_ 0..1.
    Returns roof top y. Draw anything 'behind' the house before calling, anything inside after."""
    ry = gy - h
    cr.set_source_rgb(*INTERIOR); cr.rectangle(x0, ry, x1 - x0, h); cr.fill()
    cr.set_source_rgb(*INK)
    # walls
    dx0, dx1 = door
    if dx1 > dx0:
        cr.rectangle(x0, ry, wall, h - 150); cr.fill()      # wall above the door (door 150 high)
    else:
        cr.rectangle(x0, ry, wall, h); cr.fill()
    cr.rectangle(x1 - wall, ry, wall, h); cr.fill()
    # roof slab with optional opening
    if hole and open_ > 0:
        hx0, hx1 = hole; c = (hx0 + hx1) / 2; half = (hx1 - hx0) / 2 * open_
        cr.rectangle(x0 - 10, ry, (c - half) - (x0 - 10), slab); cr.fill()
        cr.rectangle(c + half, ry, (x1 + 10) - (c + half), slab); cr.fill()
        # beam ends showing in the cut
        cr.set_source_rgb(*SOFT); cr.set_line_width(2)
        for xx in (c - half, c + half):
            cr.move_to(xx, ry + 3); cr.line_to(xx, ry + slab - 3); cr.stroke()
    else:
        cr.rectangle(x0 - 10, ry, x1 - x0 + 20, slab); cr.fill()
    return ry

def roof_tiles_pile(cr, x, ry, n):
    """Small heap of removed roof slabs sitting on the roof at x (n = 0..6 pieces)."""
    cr.set_source_rgb(*INK)
    for k in range(int(n)):
        row, col = divmod(k, 3)
        cr.rectangle(x + col * 15 - 22 + row * 7, ry - 9 - row * 9, 13, 8); cr.fill()

def stretcher(cr, ax, ay, bx, by, w=7, color=INK):
    """Mat/stretcher as a thick bar from (ax, ay) to (bx, by), with short handle ends."""
    cr.set_source_rgb(*color); cr.set_line_cap(cairo.LINE_CAP_ROUND)
    cr.set_line_width(w); cr.move_to(ax, ay); cr.line_to(bx, by); cr.stroke()

def rope(cr, ax, ay, bx, by, sag=0.0, color=INK):
    cr.set_source_rgb(*color); cr.set_line_width(2.4)
    mx, my = (ax + bx) / 2 + sag, (ay + by) / 2
    cr.move_to(ax, ay); cr.curve_to(mx, my, mx, my, bx, by); cr.stroke()

def rolled_mat(cr, x, y, ang=0.0, L=70, color=INK):
    """A rolled-up sleeping mat (carried under the arm / over the shoulder). (x, y) = centre."""
    cr.save(); cr.translate(x, y); cr.rotate(math.radians(ang)); cr.set_source_rgb(*color)
    cr.set_line_cap(cairo.LINE_CAP_ROUND); cr.set_line_width(13); cr.move_to(-L/2, 0); cr.line_to(L/2, 0); cr.stroke()
    cr.set_source_rgb(*BG); cr.set_line_width(1.6)
    for k in (-L/4, L/4): cr.move_to(k, -6); cr.line_to(k, 6); cr.stroke()
    cr.restore()

def stop_hand(cr, J, face=1, s=1.0, color=INK):
    """Flat raised palm at the right hand (a 'stop' gesture)."""
    hx, hy = J["rhand"]; cr.set_source_rgb(*color)
    cr.save(); cr.translate(hx, hy); cr.scale(1.0, 1.5); cr.arc(0, -3 * s, 6 * s, 0, 2 * math.pi); cr.restore(); cr.fill()
