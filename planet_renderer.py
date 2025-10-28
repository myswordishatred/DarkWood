def draw_planets(canvas, planets):
    canvas.delete('all')
    for planet in planets:
        x, y = planet.get_position()
        # рисуем планету
        canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill=planet.color)
        # если выбран флаг отображения радиусов
        if show_radii.get() and planet.colonized:
            r = planet.detection_radius
            canvas.create_oval(
                x - r, y - r, x + r, y + r,
                outline='white'
            )
