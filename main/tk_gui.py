from tkinter import *

tk = Tk()
tk.attributes("-topmost", True)

canvas = Canvas(tk, width=500, height=500)
canvas.pack()

canvas.create_rectangle(150, 150, 350, 350, fill='')


# def run():
#     tk.mainloop()
#
#
# if __name__ == '__main__':
#     run()