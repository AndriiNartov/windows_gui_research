import time
from collections import namedtuple
import sys

import mouse
import keyboard
import pyautogui
from tkinter import *

from windows_gui import get_pixel_colour


CurrentMouseCursorCoords = namedtuple('CurrentMouseCursorCoords', 'x y')

CURRENT_MOUSE_COORDS = CurrentMouseCursorCoords(0, 0)

PICKED_PIXEL_COORDS = tuple()
PICKED_PIXEL_COLOR = tuple()
QUIT = False

tk = Tk()
tk.attributes("-topmost", True)

canvas = Canvas(tk, width=500, height=500)
canvas.pack()
id = canvas.create_rectangle(150, 150, 350, 350, fill='')


def set_rectangle_color(rgb_color=(0, 0, 0)):
    color = "#%02x%02x%02x" % rgb_color
    canvas.itemconfig(id, fill=color)


def run():
    mouse.hook(color_changer_trigger)
    tk.mainloop()


def color_changer_trigger(event):
    if isinstance(event, mouse.ButtonEvent) and event.event_type == 'down':
        mouse.hook(color_changer)
    elif isinstance(event, mouse.ButtonEvent) and event.event_type == 'up':
        mouse.unhook(color_changer)


def color_changer(event):
    # if isinstance(event, mouse.ButtonEvent) and event.event_type == 'up':
    if isinstance(event, mouse.MoveEvent):
        click_point = pyautogui.position()
        print(click_point.x, click_point.y)
        # picked_color = get_pixel_colour(click_point.x, click_point.y)
        picked_color = get_pixel_colour(event.x, event.y)
        print(f'Picked color is {picked_color}')
        set_rectangle_color(picked_color)



def color_picker(event):
    global PICKED_PIXEL_COLOR, PICKED_PIXEL_COORDS
    if isinstance(event, mouse.ButtonEvent) and event.event_type == 'up':
        click_point = pyautogui.position()
        print(click_point.x, click_point.y)
        PICKED_PIXEL_COLOR = get_pixel_colour(click_point.x, click_point.y)
        PICKED_PIXEL_COORDS = click_point.x, click_point.y
        print(f'Picked color is {PICKED_PIXEL_COLOR}')


def waiting_for_color_picking():
    global PICKED_COLOR
    print('Please, pick the pixel you want to track')
    mouse.hook(color_picker)
    mouse.wait(target_types='up')
    mouse.unhook(color_picker)


def track_picked_pixel_color_change():
    global QUIT
    global PICKED_PIXEL_COLOR, PICKED_PIXEL_COORDS
    current_pixel_color = get_pixel_colour(*PICKED_PIXEL_COORDS)
    if current_pixel_color != PICKED_PIXEL_COLOR:
        print('CURRENT PIXEL COLOR IS DIFFERENT!')
        QUIT = True


def track_picked_pixel_color_change_1():
    global QUIT
    global PICKED_PIXEL_COLOR, PICKED_PIXEL_COORDS, SPIN_COUNT
    current_pixel_color = get_pixel_colour(*PICKED_PIXEL_COORDS)
    if current_pixel_color != PICKED_PIXEL_COLOR:
        SPIN_COUNT -= 1
        print('CURRENT PIXEL COLOR IS DIFFERENT!')
    if SPIN_COUNT == 0:
        QUIT = True


click_sequence = []


def click_tracker(event):
    global click_sequence
    if isinstance(event, mouse.ButtonEvent) and event.event_type == 'down':
        click_point = pyautogui.position()
        click_sequence.append((click_point.x, click_point.y))
        print(click_sequence)


def play_sequence():
    for click in click_sequence:
        print(click)
        mouse.move(*click, duration=0.5)
        mouse.click()


def quit(event):
    global QUIT
    if isinstance(event, keyboard.KeyboardEvent) and event.event_type == 'down' and event.name == 'q':
        QUIT = True


def set_sequence():
    global QUIT
    print('Please, set the mouse click sequence. After setting the sequence press "ESC" button to run the sequence.')
    mouse.hook(click_tracker)
    keyboard.wait('ESC')
    mouse.unhook(click_tracker)
    keyboard.hook(quit)
    while True:
        if not QUIT:
            track_picked_pixel_color_change()
            play_sequence()
            track_picked_pixel_color_change()
        else:
            break
    print('Running stoped')


def main():
    waiting_for_color_picking()
    set_sequence()


if __name__ == '__main__':
    try:
        run()
        # main()
    except KeyboardInterrupt:
        exit()
