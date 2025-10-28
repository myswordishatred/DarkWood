from tkinter import *
from planet_generator import generate_planets
from planet_renderer import draw_planets
from animation import update_planets

window = Tk()
window.title("DarkWood")
window.geometry('800x600')

canvas = Canvas(bg='black', width=600, height=500)
canvas.place(x=10, y=20)

planets_number = Spinbox(from_=50, to=1000)
planets_number.place(x=615, y=50)

show_radii = BooleanVar(value=False)  # Переменная для чекбокса

checkbox = Checkbutton(text='Показать радиусы', variable=show_radii)
checkbox.place(x=670, y=180)

planets = []

def gCreate():
    global planets
    number = int(planets_number.get())
    planets = generate_planets(number)
    draw_planets_wrapper()

def draw_planets_wrapper():
    # Вызываем функцию рисования с учетом состояния чекбокса
    canvas.delete('all')
    for planet in planets:
        x, y = planet.get_position()
        canvas.create_oval(x - 2, y - 2, x + 2, y + 2, fill=planet.color)
        if show_radii.get() and planet.colonized:
            r = planet.detection_radius
            canvas.create_oval(x - r, y - r, x + r, y + r, outline='white')

def animate():
    update_planets(planets, speed=0.01, spawn_chance=0.001)
    draw_planets_wrapper()
    window.after(50, animate)

def gStart():
    animate()

create_btn = Button(text='Создать', command=gCreate)
create_btn.place(x=670, y=100)
start_btn = Button(text='Запустить', command=gStart)
start_btn.place(x=670, y=140)

window.mainloop()
