def draw_planets(canvas, planets):
    canvas.delete('all')
    for planet in planets:
        x, y = planet.get_position()
        canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill=planet.color)
