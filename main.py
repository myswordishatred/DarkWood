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

planets = []

def gCreate():
    global planets
    number = int(planets_number.get())
    planets = generate_planets(number)
    draw_planets(canvas, planets)

def animate():
    update_planets(planets, speed=0.01)
    draw_planets(canvas, planets)
    window.after(50, animate)

def gStart():
    animate()

create_btn = Button(text='Создать', command=gCreate)
create_btn.place(x=670, y=100)
start_btn = Button(text='Запустить', command=gStart)
start_btn.place(x=670, y=140)

window.mainloop()
