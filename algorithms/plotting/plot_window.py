#!/usr/bin/env python

"""
plot_window.py:

Implementation for the windows that contain the plots.
"""

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import tkinter as tk
from tkinter import ttk
import matplotlib
matplotlib.use("TkAgg")


class PlotWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "MatPlotLib Tester")
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.plot_list = []
        self.plot_tracker = 0

    def get_container(self):
        return self.container

    def show_next_frame(self):
        if self.plot_tracker < len(self.plot_list) - 1:
            self.plot_tracker += 1
            self.show_frame()

    def show_previous_frame(self):
        if self.plot_tracker > 0:
            self.plot_tracker -= 1
            self.show_frame()

    def show_frame(self):
        frame = self.plot_list[self.plot_tracker]
        frame.tkraise()

    def add_frame(self, plot_function, plot_data):
        frame = PlotFrame(self.container, self, plot_function, plot_data)
        self.plot_list.append(frame)
        frame.grid(row=0, column=0, sticky="nsew")

    def get_frame_count(self):
        return len(self.plot_list)


class PlotFrame(tk.Frame):
    def __init__(self, parent, controller, plot_function, plot_data):
        tk.Frame.__init__(self, parent)
        label_title = "Plot Viewer - Results from using the Genetic Algorithm"
        label = tk.Label(self, text=label_title)
        label.pack(side=tk.TOP, fill=tk.BOTH, padx=10, pady=10)

        figure, axes = plot_function(plot_data)

        canvas = FigureCanvasTkAgg(figure, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        button_next = ttk.Button(self, text="Next Figure", command=controller.show_next_frame)
        button_previous = ttk.Button(self, text="Previous Figure", command=controller.show_previous_frame)

        tracking_text = "Figure {} / {}".format(plot_data.current_plot_count, plot_data.expected_plot_count)
        tracking_label = tk.Label(self, text=tracking_text)

        button_previous.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tracking_label.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        button_next.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
