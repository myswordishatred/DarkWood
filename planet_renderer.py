def draw_planets(canvas, planets, show_radii=False):
    canvas.delete('all')
    for planet in planets:
        for friend in planet.connections:
            x1, y1 = planet.get_position()
            x2, y2 = friend.get_position()
            canvas.create_line(x1, y1, x2, y2, fill='cyan', width=2)
    for planet in planets:
        x, y = planet.get_position()
        canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill=planet.color)
        if show_radii and planet.colonized:
            r = planet.detection_radius
            canvas.create_oval(x - r, y - r, x + r, y + r, outline='white')
