from tkinter import *
from pynput import mouse
import pyautogui

is_pressed = False
color_coordinates = {'x': 0, 'y': 0}
clicked_coordinates = []


class MyException(Exception):
    pass


def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb


def on_click(x, y, button, pressed):
    global is_pressed
    global color_coordinates
    is_pressed = not is_pressed
    print(x, y)
    color_coordinates['x'] = x
    color_coordinates['y'] = y
    return is_pressed


def one_click_coordinates():
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()


def get_color_under_mouse(x, y):
    pixel = pyautogui.screenshot(region=(x, y, 1, 1))
    return pixel.getcolors()[0][1]


def enter_color_data():
    global color_coordinates
    one_click_coordinates()
    print(f'Color coordinates: {color_coordinates}')
    color = get_color_under_mouse(color_coordinates['x'], color_coordinates['y'])
    print(color)
    color_frame.configure(bg=rgb_to_hex(color))


def enter_combination_data():
    print('Entered')


def enter_data():
    time_interval_value = time_interval.get()
    repetitions_number_value = repetitions_number.get()
    print(f'Time interval: {time_interval_value}')
    print(f'Number of repetitions: {repetitions_number_value}')


root = Tk()

root.title('ColorPicker')
root.wm_attributes('-alpha', 0.98)
root.geometry('300x250')

canvas = Canvas(root, height=300, width=250)
canvas.pack()

# Color picker set up

frame = Frame(root)
frame.place(relwidth=0.9, relheight=0.9, relx=0.05, rely=0.05)

btn = Button(frame, text='Enter color coordinates', bg='#fafafa', command=enter_color_data)
btn.pack()

color_frame = Frame(root, bg='#F9D312')
color_frame.place(relwidth=0.1, relheight=0.1, relx=0.15, rely=0.05)

# Time interval setup

frame = Frame(root)
frame.place(relwidth=0.9, relheight=0.9, relx=0.05, rely=0.2)

label = Label(frame, text=' - Enter time interval (sec)')
label.pack()

time_interval = Entry(root, bg='white')
time_interval.place(relwidth=0.1, relheight=0.1, relx=0.15, rely=0.2)


# Number of repetitions setup

frame = Frame(root)
frame.place(relwidth=0.9, relheight=0.9, relx=0.05, rely=0.35)

label = Label(frame, text=' - Enter repetitions amount')
label.pack()

repetitions_number = Entry(root, bg='white')
repetitions_number.place(relwidth=0.1, relheight=0.1, relx=0.15, rely=0.35)


# Combination set up

frame = Frame(root)
frame.place(relwidth=0.9, relheight=0.9, relx=0.05, rely=0.5)

btn = Button(frame, text='Enter combination (press Esc to exit)', bg='#fafafa', command=enter_combination_data)
btn.pack()


# Start button
frame = Frame(root)
frame.place(relwidth=0.9, relheight=0.9, relx=0.05, rely=0.65)

btn = Button(frame, text='Start', bg='#c9faac', command=enter_data)
btn.config(height=2, width=8)
btn.pack()

root.mainloop()

