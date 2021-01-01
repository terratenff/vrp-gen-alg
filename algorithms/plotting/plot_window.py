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
    """
    An implementation of a tkinter-based window that displays figures
    drawn using matplotlib. An instance of it displays
    one figure at a time, and if there are multiple figures,
    they can be browsed with next/previous buttons.

    Whenever an instance of this is active, console execution
    is halted: that will continue once the window is closed.

    This implementation utilizes PlotFrame-objects (based on
    Frame-objects) and PlotData-objects (see "plot_data.py") that
    act as containers for the necessary data.
    """

    def __init__(self, *args, **kwargs):
        """
        Constructor for a PlotWindow.
        """

        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "vrp-gen-alg - MatPlotLib-Figure Viewer")
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.plot_list = []
        self.plot_tracker = 0

    def get_container(self):
        """
        Getter for PlotWindow container.
        @return: Container.
        """

        return self.container

    def show_next_frame(self):
        """
        Displays the next PlotFrame in the list of them.
        PlotFrames have the contents of the window.
        """

        if self.plot_tracker < len(self.plot_list) - 1:
            self.plot_tracker += 1
            self.show_frame()

    def show_previous_frame(self):
        """
        Displays the previous PlotFrame in the list of them.
        PlotFrames have the contents of the window.
        """

        if self.plot_tracker > 0:
            self.plot_tracker -= 1
            self.show_frame()

    def show_frame(self):
        """
        Displays currently selected PlotFrame.
        PlotFrames have the contents of the window.
        """

        frame = self.plot_list[self.plot_tracker]
        frame.tkraise()

    def add_frame(self, plot_function, plot_data):
        """
        Adds a PlotFrame into the list of them. Consequently,
        another figure is added; however, figure numbers have to be
        updated separately.
        @param plot_function: Function that draws the figure.
        It must return a Figure and Axes.
        @param plot_data: PlotData-object that acts as a container
        for data that is necessary for drawing the figure.
        """

        frame = PlotFrame(self.container, self, plot_function, plot_data)
        self.plot_list.append(frame)
        frame.grid(row=0, column=0, sticky="nsew")

    def get_frame_count(self):
        """
        Getter for the number for PlotFrames that this PlotWindow has.
        @return: Total number of PlotFrames.
        """

        return len(self.plot_list)


class PlotFrame(tk.Frame):
    """
    Implementation of tkinter-based Frame-class that specializes
    in displaying matplotlib-figures and the means of navigating
    between other figures.

    This implementation utilizes PlotWindow-implementation of
    tkinter-based window and PlotData-objects that act as
    containers for data that is necessary for drawing figures.
    """

    def __init__(self, parent, controller, plot_function, plot_data):
        """
        Constructor for a PlotFrame-object.
        @param controller: The entity that controls this frame.
        This is expected to be a PlotWindow-object.
        @param plot_function: Function that draws the figure.
        It must return a Figure and Axes.
        @param plot_data: PlotData-object that contains the
        necessary data for drawing the figure.
        """

        tk.Frame.__init__(self, parent)

        button_next = ttk.Button(self, text="Next", command=controller.show_next_frame)
        button_previous = ttk.Button(self, text="Previous", command=controller.show_previous_frame)
        tracking_text = "Figure {} / {}".format(plot_data.current_plot_count, plot_data.expected_plot_count)
        tracking_label = tk.Label(self, text=tracking_text)

        button_previous.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)
        button_next.pack(side=tk.RIGHT, fill=tk.BOTH, expand=False)
        tracking_label.pack(side=tk.TOP, fill=tk.BOTH, expand=False)

        figure, axes = plot_function(plot_data)

        canvas = FigureCanvasTkAgg(figure, self)
        canvas.draw()

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        # noinspection PyProtectedMember
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
