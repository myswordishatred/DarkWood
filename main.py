from tkinter import *
from tkinter import ttk
from planet_generator import generate_planets
from planet_renderer import draw_planets
from animation import update_planets

window = Tk()
window.title("DarkWood")
window.geometry('1600x900')

canvas = Canvas(bg='black', width=1000, height=600)
canvas.place(x=10, y=20)

planets_number = Spinbox(from_=50, to=1000)
planets_number.place(x=1015, y=50)

Label(window, text="Шанс появления жизни").place(x=1015, y=80)
life_spawn_chance = DoubleVar(value=0.00001)
Spinbox(window, from_=0.0, to=1.0, increment=0.00001, textvariable=life_spawn_chance, format="%.5f").place(x=1015, y=100)

Label(window, text="Шанс агрессии").place(x=1015, y=130)
aggression_chance = DoubleVar(value=0.5)
Spinbox(window, from_=0.0, to=1.0, increment=0.01, textvariable=aggression_chance, format="%.2f").place(x=1015, y=150)

Label(window, text="Скорость моделирования (мс)").place(x=1015, y=180)
simulation_speed = IntVar(value=50)
Spinbox(window, from_=10, to=1000, increment=10, textvariable=simulation_speed).place(x=1015, y=200)

show_radii = BooleanVar(value=False)
checkbox = Checkbutton(text='Показать радиусы', variable=show_radii)
checkbox.place(x=1070, y=230)

log_text = Text(window, width=60, height=10, state=DISABLED)
log_text.place(x=1020, y=330)

tree = ttk.Treeview(window)

tree['columns'] = ('tech_level', 'friends', 'destroyed', 'detection_radius')

tree.heading('tech_level', text='Уровень технологии')
tree.heading('friends', text='Друзья')
tree.heading('destroyed', text='Уничтожила')
tree.heading('detection_radius', text='Радиус обнаружения')

tree.column('tech_level', width=100)
tree.column('friends', width=200)
tree.column('destroyed', width=200)
tree.column('detection_radius', width=120)

tree.place(x=10, y=650, width=1000, height=210)

planets = []

def log_event(message):
    log_text.config(state=NORMAL)
    log_text.insert(END, message + "\n")
    log_text.see(END)
    log_text.config(state=DISABLED)

def gCreate():
    global planets
    planets = generate_planets(int(planets_number.get()), aggression_chance.get())
    draw_planets_wrapper()
    update_tree()

def draw_planets_wrapper():
    draw_planets(canvas, planets, show_radii=show_radii.get())

def update_tree():
    tree.delete(*tree.get_children())
    for planet in planets:
        if planet.colonized:
            friends_names = ", ".join(sorted(friend.name for friend in planet.connections))
            destroyed_names = ", ".join(sorted(planet.destroyed_planets))
            tree.insert('', END, text=planet.name,
                        values=(f"{planet.tech_level:.2f}",
                                friends_names,
                                destroyed_names,
                                f"{planet.detection_radius:.1f}"))


def animate():
    update_planets(planets, canvas, log_event, speed=0.01, spawn_chance=life_spawn_chance.get())
    draw_planets_wrapper()
    update_tree()
    window.after(simulation_speed.get(), animate)

def gStart():
    animate()

paused = False  # глобальная переменная паузы

def toggle_pause():
    global paused
    paused = not paused
    if paused:
        pause_button.config(text='Продолжить')
    else:
        pause_button.config(text='Пауза')
        animate()

# Оставьте ваше определение функции animate, но добавьте проверку paused
def animate():
    if not paused:
        update_planets(planets, canvas, log_event, speed=0.01, spawn_chance=life_spawn_chance.get())
        draw_planets_wrapper()
        update_tree()
        window.after(simulation_speed.get(), animate)

# Создайте кнопку паузы, не меняя позиции существующих элементов
pause_button = Button(text='Пауза', command=toggle_pause)
# Например, разместить рядом с кнопками Создать и Запустить
pause_button.place(x=1170, y=260)

create_btn = Button(text='Создать', command=gCreate)
create_btn.place(x=1070, y=260)
start_btn = Button(text='Запустить', command=gStart)
start_btn.place(x=1070, y=300)

window.mainloop()
