def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))

def rgb_to_hex(rgb):
    return '#{:02x}{:02x}{:02x}'.format(*rgb)

def average_color(planets):
    r_tot = g_tot = b_tot = 0
    count = len(planets)
    for planet in planets:
        r, g, b = hex_to_rgb(planet.color)
        r_tot += r
        g_tot += g
        b_tot += b
    return rgb_to_hex((r_tot // count, g_tot // count, b_tot // count))

def draw_planets(canvas, planets, show_radii=False):
    canvas.delete('all')
    drawn_groups = set()

    for planet in planets:
        group = frozenset(planet.connections.union({planet}))
        if group not in drawn_groups:
            drawn_groups.add(group)
            color = average_color(group)
            friend_list = list(group)
            for i in range(len(friend_list)):
                for j in range(i + 1, len(friend_list)):
                    x1, y1 = friend_list[i].get_position()
                    x2, y2 = friend_list[j].get_position()
                    canvas.create_line(x1, y1, x2, y2, fill=color, width=2)

    for planet in planets:
        x, y = planet.get_position()
        canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill=planet.color)
        if show_radii and planet.colonized:
            r = planet.detection_radius
            canvas.create_oval(x - r, y - r, x + r, y + r, outline='white')
