import tkinter as tk
from tkinter import OptionMenu, colorchooser, Frame, Checkbutton, IntVar, StringVar, Canvas
from tkinter.ttk import Scale

from PIL import ImageGrab


class DrawingApp:
    def __init__(self, master):
        self.eraser_var = None
        self.master = master
        self.master.grid_rowconfigure(1, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        self.color = "white"
        self.bg_color = "black"
        self.pen_size = 3
        self.draw = True
        self.brush_type = 'Pencil'

        self.canvas = Canvas(self.master, bg=self.bg_color)
        self.canvas.grid(row=1, column=0, sticky="nsew")

        self.previous_x = self.previous_y = 0
        self.canvas.bind("<B1-Motion>", self.draw_shape)
        self.canvas.bind("<ButtonRelease-1>", self.reset_position)
        self.master.bind("<Configure>", self.resize_canvas)
        self.create_widgets()

    def create_widgets(self):
        self.control_frame = Frame(self.master, height=50)
        self.control_frame.grid(row=0, column=0, sticky="ew")

        color_button = tk.Button(self.control_frame, text="Color", command=self.choose_color, font=('Times', 14),
                                 bg='light grey', fg='black')
        color_button.grid(row=0, column=0, sticky="nsew")

        brush_menu = OptionMenu(self.control_frame, StringVar(value=self.brush_type),
                                *['Pencil', 'Line', 'Rectangle', 'Oval', 'Arc'],
                                command=self.choose_brush)
        brush_menu.config(font=('Times', 14), bg='light grey', fg='black', padx=10, pady=5)
        brush_menu.grid(row=0, column=1)

        self.eraser_var = IntVar()
        eraser_button = Checkbutton(self.control_frame, text="Eraser", variable=self.eraser_var,
                                    command=self.use_eraser, font=('Times', 14), bg='light grey', fg='black', padx=10,
                                    pady=5)
        eraser_button.grid(row=0, column=2)

        clear_button = tk.Button(self.control_frame, text="Clear", command=self.clear_canvas, font=('Times', 14),
                                 bg='light grey', fg='black', padx=10, pady=5)
        clear_button.grid(row=0, column=3)

        bg_color_button = tk.Button(self.control_frame, text="BG Color", command=self.choose_bg_color,
                                    font=('Times', 14), bg='light grey', fg='black', padx=10, pady=5)
        bg_color_button.grid(row=0, column=4)

        save_button = tk.Button(self.control_frame, text="Save", command=self.save_canvas, font=('Times', 14),
                                bg='light grey', fg='black', padx=10, pady=5)
        save_button.grid(row=0, column=5)

        size_frame = Frame(self.master, width=50)
        size_frame.grid(row=0, column=1, sticky="ns")

        size_slider = Scale(size_frame, from_=1, to=30, orient="horizontal", command=self.update_size)
        size_slider.set(self.pen_size)
        size_slider.pack(fill="y")

    def choose_color(self):
        self.color = colorchooser.askcolor(color=self.color)[1]

    def choose_bg_color(self):
        self.bg_color = colorchooser.askcolor(color=self.bg_color)[1]
        self.canvas.configure(bg=self.bg_color)

    def update_size(self, value):
        self.pen_size = int(float(value))

    def choose_brush(self, brush_type):
        self.brush_type = brush_type

    def use_eraser(self):
        self.draw = not self.eraser_var.get()

    def clear_canvas(self):
        self.canvas.delete("all")

    def save_canvas(self):
        x = self.master.winfo_rootx() + self.canvas.winfo_x()
        y = self.master.winfo_rooty() + self.canvas.winfo_y()
        x1 = x + self.canvas.winfo_width()
        y1 = y + self.canvas.winfo_height()
        ImageGrab.grab().crop((x, y, x1, y1)).save("canvas_image.jpg")

    def resize_canvas(self, event):
        self.canvas.config(width=self.master.winfo_width(),
                           height=self.master.winfo_height() - self.control_frame.winfo_height())
        self.canvas.delete("bg")
        self.canvas.create_rectangle(0, 0, self.master.winfo_width(), self.master.winfo_height(), fill=self.bg_color,
                                     tags="bg")

    def draw_shape(self, event):
        if self.previous_x and self.previous_y:
            if self.brush_type == 'Pencil':
                self.canvas.create_line(self.previous_x, self.previous_y,
                                        event.x, event.y, width=self.pen_size,
                                        fill=self.color if self.draw else self.bg_color, capstyle="round")
            elif self.brush_type == 'Line':
                self.canvas.create_line(self.previous_x, self.previous_y,
                                        event.x, event.y, width=self.pen_size,
                                        fill=self.color, capstyle="Line")
            elif self.brush_type == 'Rectangle':
                self.canvas.create_rectangle(self.previous_x, self.previous_y,
                                             event.x, event.y, width=self.pen_size,
                                             outline=self.color)
            elif self.brush_type == 'Oval':
                self.canvas.create_oval(self.previous_x, self.previous_y,
                                        event.x, event.y, width=self.pen_size,
                                        outline=self.color)
            elif self.brush_type == 'Arc':
                self.canvas.create_arc(self.previous_x, self.previous_y,
                                       event.x, event.y, width=self.pen_size,
                                       outline=self.color)

        self.previous_x = event.x
        self.previous_y = event.y

    def reset_position(self, event):
        self.previous_x = self.previous_y = 0


def main():
    root = tk.Tk()
    app = DrawingApp(root)
    root.title("DraWall")
    root.mainloop()


main()
