import time
from collections import namedtuple
import sys
from enum import Enum

import mouse
import keyboard
import pyautogui
from tkinter import *
import tkinter

from windows_gui import get_pixel_colour


class ColorPickerAreaCoords(Enum):
    X1 = 50
    Y1 = 50
    X2 = 250
    Y2 = 250


class PickedPixelCoordsInfoTextCoords(Enum):
    X1 = 100
    Y1 = 300


class PickedPixelColorInfoTextCoords(Enum):
    X1 = 100
    Y1 = 350

CurrentMouseCursorCoords = namedtuple('CurrentMouseCursorCoords', 'x y')

CURRENT_MOUSE_COORDS = CurrentMouseCursorCoords(0, 0)

PICKED_PIXEL_COORDS = tuple()
PICKED_PIXEL_COLOR = tuple()
QUIT = False
SPIN_COUNT = 10

tk = Tk()
tk.attributes("-topmost", True)

canvas = Canvas(tk, width=750, height=750)
canvas.pack()


canvas_1 = Canvas(tk, width=250, height=250)
canvas.pack()

color_picker_area_id = canvas.create_rectangle(
    ColorPickerAreaCoords.X1.value,
    ColorPickerAreaCoords.Y1.value,
    ColorPickerAreaCoords.X2.value,
    ColorPickerAreaCoords.Y2.value,
    fill=''
)

coords_info_id = canvas.create_text(PickedPixelCoordsInfoTextCoords.X1.value, PickedPixelCoordsInfoTextCoords.Y1.value, text=f'X: - ; Y: - ')
color_info_id = canvas.create_text(PickedPixelColorInfoTextCoords.X1.value, PickedPixelColorInfoTextCoords.Y1.value, text=f'R: - ; G: - ; B: - ')
autoclick_chain_info_id = canvas.create_text(450, 50, text='')


def set_rectangle_color(rgb_color=(0, 0, 0)):
    color = "#%02x%02x%02x" % rgb_color
    canvas.itemconfig(color_picker_area_id, fill=color)


def set_picked_pixel_coords_text():
    if PICKED_PIXEL_COORDS:
        text = f'X: {PICKED_PIXEL_COORDS[0]} ; Y: {PICKED_PIXEL_COORDS[1]}'
    else:
        text = f'X: - ; Y: - '
    canvas.itemconfig(coords_info_id, text=text)


def show_autoclick_chain():
    print('INSIDE FUNCTION!')
    canvas.itemconfig(autoclick_chain_info_id, text=f'{click_sequence}')
    # from itertools import count
    # c = count(1)
    # text = ''
    # for click in click_sequence:
    #     text += f'{next(c)}. Click on x: {click[0]}, y: {click[1]}'
    #     canvas.itemconfig(autoclick_chain_info_id, text=text)


def set_picked_pixel_color_text():
    if PICKED_PIXEL_COLOR:
        text = f'R: {PICKED_PIXEL_COLOR[0]}; G: {PICKED_PIXEL_COLOR[1]}; B: {PICKED_PIXEL_COLOR[2]}'
    else:
        text = 'R: - ; G: - ; B: - '
    canvas.itemconfig(color_info_id, text=text)


COLOR_PICKER_WAS_ACTIVATED = False


def track_pointer(event: tkinter.Event):
    global COLOR_PICKER_WAS_ACTIVATED
    pointer_is_in_color_picker_area = ColorPickerAreaCoords.X2.value >= event.x >= ColorPickerAreaCoords.X1.value and ColorPickerAreaCoords.Y2.value >= event.y >= ColorPickerAreaCoords.Y1.value
    left_mouse_button_pressed = event.state == 8 and event.num == 1
    left_mouse_button_released = event.state == 264 and event.num == 1
    if pointer_is_in_color_picker_area and left_mouse_button_pressed:
        tk.config(cursor="crosshair")
        mouse.hook(color_changer)
        COLOR_PICKER_WAS_ACTIVATED = True
    elif left_mouse_button_released and COLOR_PICKER_WAS_ACTIVATED:
        tk.config(cursor="arrow")
        try:
            COLOR_PICKER_WAS_ACTIVATED = False
            mouse.unhook(color_changer)
        except ValueError:
            print('Trying to unhook the func, which was not hooked. Error handled.')


def set_autoclick_chain():
    print('SET')


def color_changer_trigger(event):
    if isinstance(event, mouse.ButtonEvent) and event.event_type == 'down':
        mouse.hook(color_changer)
    elif isinstance(event, mouse.ButtonEvent) and event.event_type == 'up':
        mouse.unhook(color_changer)


def color_changer(event):
    global PICKED_PIXEL_COLOR, PICKED_PIXEL_COORDS
    # if isinstance(event, mouse.ButtonEvent) and event.event_type == 'up':
    if isinstance(event, mouse.MoveEvent):
        click_point = pyautogui.position()
        # print(click_point.x, click_point.y)
        # picked_color = get_pixel_colour(click_point.x, click_point.y)
        picked_color = get_pixel_colour(event.x, event.y)
        # print(f'Picked color is {picked_color}')
        PICKED_PIXEL_COLOR = picked_color
        PICKED_PIXEL_COORDS = click_point
        set_rectangle_color(picked_color)
        set_picked_pixel_coords_text()
        set_picked_pixel_color_text()


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
    if PICKED_PIXEL_COLOR and PICKED_PIXEL_COORDS:
        current_pixel_color = get_pixel_colour(*PICKED_PIXEL_COORDS)
        if current_pixel_color != PICKED_PIXEL_COLOR:
            print('CURRENT PIXEL COLOR IS DIFFERENT!')
            QUIT = True


def run_auto_click_with_pixel_check(delay=0.5):
    global QUIT
    global PICKED_PIXEL_COLOR, PICKED_PIXEL_COORDS, SPIN_COUNT
    current_pixel_color = get_pixel_colour(*PICKED_PIXEL_COORDS)
    if current_pixel_color == PICKED_PIXEL_COLOR:
        play_sequence()
        time.sleep(delay)
        SPIN_COUNT -= 1
        print('CURRENT PIXEL COLOR IS DIFFERENT!', 'SPIN COUNT IS', SPIN_COUNT)
    if SPIN_COUNT == 0:
        QUIT = True


def run_auto_click_without_pixel_check(delay=0.5):
    global QUIT
    global SPIN_COUNT
    if SPIN_COUNT:
        play_sequence()
        time.sleep(delay)
        SPIN_COUNT -= 1
        print('CURRENT PIXEL COLOR IS DIFFERENT!', 'SPIN COUNT IS', SPIN_COUNT)
    if SPIN_COUNT == 0:
        QUIT = True


click_sequence = []


def click_tracker(event):
    global btn_1
    if isinstance(event, keyboard.KeyboardEvent) and event.name == 'esc':
        mouse.unhook(click_tracker)
        keyboard.unhook(click_tracker)
        btn_1['state'] = tkinter.ACTIVE
    global click_sequence
    if isinstance(event, mouse.ButtonEvent) and event.event_type == 'down':
        click_point = pyautogui.position()
        click_sequence.append((click_point.x, click_point.y))
        test_1(click_point)
        print(click_sequence)
        # mouse.unhook(click_tracker)


def click_tracker_tk(event):
    global click_sequence
    if event.state == 8:
        click_point = pyautogui.position()
        click_sequence.append((click_point.x, click_point.y))
        print(click_sequence)


def finish_track_click_tk(event):
    print(event)


def play_sequence():
    for click in click_sequence:
        print(click)
        mouse.move(*click, duration=1)
        mouse.click()


def quit(event):
    global QUIT
    if isinstance(event, keyboard.KeyboardEvent) and event.event_type == 'down' and event.name == 'q':
        QUIT = True


def test():
    c = len(click_sequence) + 1
    for click in click_sequence:
        text = f'{c}. Click on point: x: {click[0]}, y: {click[1]}'
        y = 50 + c * 20
        canvas.create_text(450, y, text=text)


TEXT_ID_LIST = []


def test_1(click):
    global TEXT_ID_LIST
    c = len(click_sequence)
    y = 50 + c * 20
    text = f'{c}. Click on point: x: {click[0]}, y: {click[1]}'
    id = canvas.create_text(450, y, text=text)
    TEXT_ID_LIST.append(id)


def test_2():
    print('Inside')
    global click_sequence, TEXT_ID_LIST
    for id in TEXT_ID_LIST:
        canvas.delete(id)
    TEXT_ID_LIST = []
    click_sequence = []
    print('DONE')


def set_sequence():
    # global click_sequence
    # click_sequence = []
    tk.unbind("<ButtonPress>")
    tk.unbind("<ButtonRelease>")
    test_2()
    print('Please, set the mouse click sequence. After setting the sequence press "ESC" button to run the sequence.')
    mouse.hook(click_tracker)
    keyboard.hook(click_tracker)
    # keyboard.wait('ESC')
    # mouse.unhook(click_tracker)
    # test()


def run_sequence():
    global SPIN_COUNT, PICKED_PIXEL_COLOR, QUIT
    QUIT = False
    keyboard.hook(quit)
    try:
        SPIN_COUNT = int(spin_count_entry_field.get())
        print(f'We will spin {spin_count_entry_field.get()} times')
    except Exception as e:
        print(e)
        print(f'We will spin {SPIN_COUNT} times')
    print('SPIN COUNT IS', SPIN_COUNT)
    if PICKED_PIXEL_COLOR:
        while True:
            if not QUIT:
                run_auto_click_with_pixel_check()
            else:
                keyboard.unhook(quit)
                break
    else:
        while True:
            if not QUIT:
                run_auto_click_without_pixel_check()
            else:
                keyboard.unhook(quit)
                break
    print('Running stopped')


btn = Button(tk, text='Set autoclick chain', command=set_sequence)
btn.pack()

btn_1 = Button(tk, text='Start', command=run_sequence, state=tkinter.DISABLED)
btn_1.pack()

spin_count_entry_field = Entry(tk)
spin_count_entry_field.pack()


def run():
    tk.bind("<ButtonPress>", track_pointer)
    tk.bind("<ButtonRelease>", track_pointer)
    tk.mainloop()


def main():
    waiting_for_color_picking()
    set_sequence()


if __name__ == '__main__':
    try:
        run()
        # main()
    except KeyboardInterrupt:
        exit()
