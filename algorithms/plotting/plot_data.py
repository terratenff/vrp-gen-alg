#!/usr/bin/env python

"""
plot_data.py:

Implementation for plot data and various plotting functions.
"""

from os import mkdir, listdir
from os.path import exists

import numpy as np
from matplotlib.figure import Figure
from matplotlib.path import Path
from matplotlib.patches import PathPatch


class PlotData:
    """
    Represents the data aspect of the plot figure.
    """

    folder_tracker = "ResultSet1"
    base_destination = "variables/plot_data/"

    @staticmethod
    def select_unused_folder_name():
        """
        Creates a folder to which data of a collection of plot data is saved.
        """

        i = 1
        file_str = "ResultSet{}".format(i)
        file_list = listdir(PlotData.base_destination)
        existing_name = file_str in file_list
        while existing_name is True:
            i += 1
            file_str = "ResultSet{}".format(i)
            existing_name = file_str in file_list
        PlotData.folder_tracker = file_str

    def __init__(self, xy_datasets, data_labels, plot_details):
        """
        Constructor of the plot data container.

        @param xy_datasets: 3D-Matrix of size (m x n x 2), where
        m represents the number of xy-datasets and n is the number of data points
        in each dataset. First column is x-data, while the other column is y-data.
        @param data_labels: String labels for each set of xy-data. An exception
        is thrown if the size of this list does not match the number of xy-datasets.
        @param plot_details: Dictionary that contains details for the plot figure.
        The following key-value-pairs are expected:
        - 'title': (string) Title for the plot figure.
        - 'xlabel': (string) Title for the x-data in the xy-datasets.
        - 'ylabel': (string) Title for the y-data in the xy-datasets.
        - 'legend': (bool) Flag that determines whether a legend should be shown.
        - 'expected_plot_count': (int) Number of plot figures that are expected to be
          associated with this data.
        - 'current_plot_count': (int) Placement within associated plot figures.
        """

        if len(xy_datasets.shape) == 2:
            self.data = xy_datasets[np.newaxis]
        elif len(xy_datasets.shape) == 3 and xy_datasets.shape[2] == 2:
            self.data = xy_datasets
        else:
            raise ValueError("Expected shape (m x n x 2), got {}".format(xy_datasets.shape))

        self.dataset_count = xy_datasets.shape[0]
        self.labels = data_labels
        self.title = plot_details["title"]
        self.xlabel = plot_details["xlabel"]
        self.ylabel = plot_details["ylabel"]
        self.legend = plot_details["legend"]
        self.expected_plot_count = plot_details["expected_plot_count"]
        self.current_plot_count = plot_details["current_plot_count"]

        if "misc" in plot_details:
            self.misc = plot_details["misc"]
        else:
            self.misc = None

        # The following variables are only needed in making maps.
        # These are to be configured separately using methods
        # "set_node_data" and "set_route_data".
        self.route_list = None
        self.open_routes = None
        self.required_nodes = None
        self.optional_nodes = None
        self.depot_nodes = None

    def get_data(self, index):
        """
        Getter for specified XY-dataset.
        @param index: Selector value for a dataset. Range: [0, m)
        @return: n x 2 matrix and a string label that describes it.
        """
        return self.data[index], self.labels[index]

    def add_data(self, xy_data, label):
        """
        Adds an XY-dataset to the plot data object.
        @param xy_data: n x 2 matrix.
        @param label: String label that describes the dataset being added.
        """
        self.data = np.vstack((self.data, xy_data[np.newaxis]))
        self.labels.append(label)

    def remove_data(self, index):
        """
        Removes specified XY-dataset from the plot data object.
        @param index: Selector value for a dataset. Range: [0, n)
        """
        self.data = np.delete(self.data, index, 0)
        del self.labels[index]

    def set_node_data(self, node_count, optional_nodes, depot_nodes):
        """
        Setter for node data. Coordinates are provided via XY_datasets
        The nodes are split into three different categories:
        required nodes, optional nodes and depot nodes.
        @param node_count: Number of nodes that exist for the datasets.
        @param optional_nodes: List of nodes that are considered optional.
        @param depot_nodes: List of nodes that act as depots.
        """
        all_nodes = list(range(node_count))
        self.required_nodes = [i for i in all_nodes if i not in optional_nodes and i not in depot_nodes]
        self.optional_nodes = optional_nodes
        self.depot_nodes = depot_nodes

    def set_route_data(self, route_list, open_routes):
        """
        Setter for route data. This is needed to draw the lines between
        the nodes.
        @param route_list: List of routes that are to be drawn
        These represent the solution of an individual.
        @param open_routes: Flag that determines whether the routes are open.
        """
        self.route_list = route_list
        self.open_routes = open_routes

    def save_data(self):
        """
        Saves stored data into text files. Node and route data are excluded.
        """

        destination = PlotData.base_destination + PlotData.folder_tracker + "/"

        if exists(destination) is False:
            mkdir(destination)

        i = 1
        file_str = "R-{}".format(i)
        file_list = listdir(destination)
        existing_name = file_str in file_list
        while existing_name is True:
            i += 1
            file_str = "R-{}".format(i)
            existing_name = file_str in file_list
        folder_name = file_str

        new_destination = destination + folder_name + "/"
        mkdir(new_destination)

        with open(new_destination + "details.txt", "w") as detail_file:
            detail_file.write("Plot Title: {}\n".format(self.title))
            detail_file.write("X-axis:     {}\n".format(self.xlabel))
            detail_file.write("Y-axis:     {}\n".format(self.ylabel))
            if len(self.labels) > 1:
                detail_file.write("Legend:\n")
                for i in range(len(self.labels)):
                    label = self.labels[i]
                    detail_file.write("- results_{}.txt: {}\n".format(i + 1, label))

        if len(self.data.shape) == 2:
            np.savetxt(new_destination + "results.txt", self.data.T, fmt="%.8f")
        elif self.data.shape[0] == 1:
            np.savetxt(new_destination + "results.txt", self.data[0].T, fmt="%.8f")
        else:
            for i in range(self.data.shape[0]):
                temp_name = "results_{}.txt".format(i + 1)
                np.savetxt(new_destination + temp_name, self.data[i].T, fmt="%.8f")


def plot_graph(plot_data):
    """
    Plots a regular graph based on provided data. Resulting figure
    has to be separately viewed. Supports multiple datasets.
    @param plot_data: Plot Data Object that contains everything
    necessary for the graph.
    @return: Figure and Figure Axes that encompass the graph.
    """

    title = plot_data.title
    xlabel = plot_data.xlabel
    ylabel = plot_data.ylabel
    draw_textbox = False
    textbox_details = ""

    # A textbox is created and placed to the top edge of the plot
    # if a string list under "misc" is defined.
    if plot_data.misc is not None:
        textbox_details = "\n".join(plot_data.misc)
        draw_textbox = True

    figure = Figure(figsize=(9.0, 6.8), dpi=100)
    figure_axes = figure.add_subplot(111)

    # Add data to the figure. Multiple datasets are added
    # to the same plot.
    lowest_x, highest_x = float("inf"), -float("inf")
    for i in range(len(plot_data.labels)):
        xy_data, data_label = plot_data.get_data(i)
        x = xy_data[0]
        y = xy_data[1]
        if x.size == 0 or y.size == 0:
            continue
        lowest_x, highest_x = min(lowest_x, min(x)), max(highest_x, max(x))
        figure_axes.plot(x, y, label=data_label, linewidth=3)

    if lowest_x != float("inf") and highest_x != float("inf"):
        figure_axes.set_xlim([lowest_x, highest_x])
    
    figure_axes.set_title(title)
    figure_axes.set_xlabel(xlabel)
    figure_axes.set_ylabel(ylabel)
    if plot_data.legend is True:
        figure_axes.legend()
    if draw_textbox is True:
        props = dict(boxstyle="round", facecolor="lightcyan", alpha=0.50)
        figure_axes.text(0.50, 0.95, textbox_details,
                         transform=figure_axes.transAxes,
                         fontsize=12,
                         verticalalignment="top",
                         horizontalalignment="center",
                         bbox=props)

    plot_data.save_data()

    return figure, figure_axes


def plot_bar(plot_data):
    """
    Plots a bar graph based on provided data. Resulting figure
    has to be separately viewed. Supports only one dataset.
    @param plot_data: Plot Data Object that contains everything
    necessary for the graph.
    @return: Figure and Figure Axes that encompass the graph.
    """

    title = plot_data.title
    xlabel = plot_data.xlabel
    ylabel = plot_data.ylabel
    draw_textbox = False
    textbox_details = ""

    # A textbox is created and placed to the top edge of the plot
    # if a string list under "misc" is defined.
    if plot_data.misc is not None:
        textbox_details = "\n".join(plot_data.misc)
        draw_textbox = True

    figure = Figure(figsize=(9.0, 6.8), dpi=100)
    figure_axes = figure.add_subplot(111)

    # With a bar graph only 1 set of data is expected.
    xy_data, data_label = plot_data.get_data(0)
    if xy_data.size != 0:
        low, high = min(xy_data[1, :]), max(xy_data[1, :])
        figure_axes.bar([str(int(gen)) for gen in xy_data[0, :]], xy_data[1, :], label=data_label)
        # figure_axes.set_xlim([min(xy_data[0, :]), max(xy_data[0, :])])
        figure_axes.set_ylim([np.ceil(low - 0.05*(high - low)), np.ceil(high + 0.05*(high - low))])

    figure_axes.set_title(title)
    figure_axes.set_xlabel(xlabel)
    figure_axes.set_ylabel(ylabel)
    figure_axes.tick_params(axis="x", which="both", labelsize="8", rotation=90)
    if plot_data.legend is True:
        figure_axes.legend()
    if draw_textbox is True:
        props = dict(boxstyle="round", facecolor="lightcyan", alpha=0.50)
        figure_axes.text(0.50, 0.95, textbox_details,
                         transform=figure_axes.transAxes,
                         fontsize=12,
                         verticalalignment="top",
                         horizontalalignment="center",
                         bbox=props)

    plot_data.save_data()

    return figure, figure_axes


def plot_map(plot_data):
    """
    Plots a scatter graph with lines connecting the dots based on
    provided data. Resulting figure has to be separately viewed.
    Supports only one dataset.
    @param plot_data: Plot Data Object that contains everything
    necessary for the graph.
    @return: Figure and Figure Axes that encompass the graph.
    """

    title = plot_data.title
    xlabel = plot_data.xlabel
    ylabel = plot_data.ylabel

    route_list = plot_data.route_list
    vehicle_count = len(route_list)
    open_routes = plot_data.open_routes

    required_nodes = plot_data.required_nodes
    optional_nodes = plot_data.optional_nodes
    depot_nodes = plot_data.depot_nodes
    draw_textbox = False
    textbox_details = ""

    # A textbox is created and placed to the top edge of the plot
    # if a string list under "misc" is defined.
    if plot_data.misc is not None:
        textbox_details = "\n".join(plot_data.misc)
        draw_textbox = True

    figure = Figure(figsize=(9.0, 6.8), dpi=100)
    figure_axes = figure.add_subplot(111)

    # One dataset - that being node coordinates - is expected.
    all_vertices, data_label = plot_data.get_data(0)

    # Colors to separate different routes.
    color_collection = [
        "black", "red", "blue",
        "green", "yellow", "orange",
        "cyan", "magenta", "brown",
        "lime", "teal", "gold",
        "yellowgreen", "darkseagreen", "darkslateblue",
        "lightgrey", "grey", "darkgrey"
    ]
    if len(color_collection) < vehicle_count:
        # In case named colors are not enough.
        missing_count = vehicle_count - len(color_collection)
        for i in range(missing_count):
            color_collection.append(np.random.rand(3))

    # Lines connecting the dots represent routes.
    # They are added here.
    i_color = -1
    for i in range(vehicle_count):
        route_vertices = []
        route_codes = []
        route = route_list[i]
        if len(route) <= 1:
            continue
        i_color += 1
        route_codes.append(Path.MOVETO)
        depot_node = route[0]
        route_vertices.append(all_vertices[depot_node])

        for j in range(1, len(route)):
            route_codes.append(Path.LINETO)
            route_vertices.append(all_vertices[route[j]])

        # In OVRP, vehicle does not return to where it started.
        if open_routes is False:
            route_codes.append(Path.LINETO)
            route_vertices.append(all_vertices[depot_node])

        # Inserting PathPatch to the figure.
        path = Path(route_vertices, route_codes)
        patch = PathPatch(path, fill=False, lw=2, color=color_collection[i_color])
        figure_axes.add_patch(patch)

    # Add text to appropriate places to signify node locations.
    for i in range(len(all_vertices)):
        vertex = all_vertices[i]
        x = vertex[0]
        y = vertex[1]
        # y = y + np.ones(y.shape) * 5
        figure_axes.text(x, y, "{}".format(i), fontsize=18, ha="center", va="bottom")

    # Provided dataset is split into three categories: required nodes, optional nodes and depot nodes.
    if len(required_nodes) != 0:
        figure_axes.scatter(
            all_vertices[required_nodes, 0],
            all_vertices[required_nodes, 1],
            s=100,
            c="red",
            label="Required Nodes"
        )

    if len(optional_nodes) != 0:
        figure_axes.scatter(
            all_vertices[optional_nodes, 0],
            all_vertices[optional_nodes, 1],
            s=100,
            c="yellow",
            label="Optional Nodes"
        )

    if len(depot_nodes) != 0:
        figure_axes.scatter(
            all_vertices[depot_nodes, 0],
            all_vertices[depot_nodes, 1],
            s=100,
            c="lightgreen",
            label="Depot Nodes"
        )

    figure_axes.set_title(title)
    figure_axes.set_xlabel(xlabel)
    figure_axes.set_ylabel(ylabel)
    if plot_data.legend is True:
        figure_axes.legend()
    if draw_textbox is True:
        props = dict(boxstyle="round", facecolor="lightcyan", alpha=0.50)
        figure_axes.text(0.50, 0.95, textbox_details,
                         transform=figure_axes.transAxes,
                         fontsize=12,
                         verticalalignment="top",
                         horizontalalignment="center",
                         bbox=props)

    return figure, figure_axes
