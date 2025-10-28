import math

def draw_planets(canvas, planets):
    canvas.delete('all')
    for theta, r in planets:
        x = 300 + 250 * r * math.cos(theta)
        y = 250 + 150 * r * math.sin(theta)
        canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill='yellow')
