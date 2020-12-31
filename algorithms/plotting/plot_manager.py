#!/usr/bin/env python

"""
plot_manager.py:

Uses plot data and plot window to create plots themselves.
"""

import numpy as np
from copy import deepcopy

from algorithms.plotting import plot_data, plot_window


def summon_window(plot_function_list, plot_data_list):
    """
    Opens a window that shows figures based on provided data
    and functions. Once the window is closed, program execution
    continues.
    @param plot_function_list: List of plotting functions that
    are to be used. Matching indices are used to indicate which
    functions are used with which data.
    @param plot_data_list: List of plot data that are to be used.
    Matching indices are used to indicate which functions are used
    with which data.
    """

    if len(plot_function_list) != len(plot_data_list):
        print("(Plot Manager) List sizes do not match.")
        return

    app = plot_window.PlotWindow()
    for i in range(len(plot_data_list)):
        app.add_frame(plot_function_list[i], plot_data_list[i])

    app.show_frame()
    app.mainloop()


def test_plot_creation():
    x = np.linspace(0, 2, 100)
    y1 = x
    y2 = x**2
    y3 = x**3
    y = np.array([y1, y2, y3])
    plot_dict1 = {
        "legend": False,
        "title": "Genetic Algorithm - Best Individual",
        "xlabel": "Generation Count",
        "ylabel": "Fitness",
        "expected_plot_count": 3,
        "current_plot_count": 1,
        "misc": [
            "Simulated Annealing",
            "$n_{max} = 300$",
            "$T^{(1)} = 300$",
            "$p = 1.15$"
        ]
    }
    plot_dict2 = deepcopy(plot_dict1)
    plot_dict3 = deepcopy(plot_dict1)
    plot_dict2["current_plot_count"] = 2
    plot_dict3["current_plot_count"] = 3
    plot_dict2["legend"] = True
    plot_dict3["legend"] = True
    data_labels = ["Linear", "Quadratic", "Cubic"]
    data_set = np.array([x, y[0]])

    plot_data1 = plot_data.PlotData(data_set, ["Linear"], plot_dict1)
    plot_data2 = plot_data.PlotData(data_set, ["Linear"], plot_dict2)
    plot_data3 = plot_data.PlotData(data_set, ["Linear"], plot_dict3)

    appended_data1 = np.array([x, y[1]])
    appended_data2 = np.array([x, y[2]])

    plot_data2.add_data(appended_data1, data_labels[1])
    plot_data3.add_data(appended_data1, data_labels[1])
    plot_data3.add_data(appended_data2, data_labels[2])

    plot_functions = [
        plot_data.plot_graph,
        plot_data.plot_graph,
        plot_data.plot_graph
    ]
    plot_list = [plot_data1, plot_data2, plot_data3]

    print("Close plot window to continue.")

    summon_window(plot_functions, plot_list)


def test_map_creation():
    x = np.array([4,  7,  3,  5,  3,  5, -3, -8,  8, -9])
    y = np.array([4,  5,  3, -9,  6,  5,  4,  5,  8,  9])
    data_set = np.array([x, y]).T
    route_list1 = [[0, 1, 2, 3], [0, 4, 5, 6], [0, 7, 8, 9]]
    route_list2 = [[9, 8, 0], [9, 3, 5], [9, 6, 1], [9, 4, 2], [9, 7]]
    route_list3 = [[1, 6, 9, 4], [2, 8, 0, 7, 3, 5]]
    open_routes1 = False
    open_routes2 = True
    open_routes3 = False
    node_count = 10
    optional_nodes1 = []
    optional_nodes2 = [6, 7, 8]
    optional_nodes3 = [3, 6, 9]
    depot_nodes1 = [0]
    depot_nodes2 = [9]
    depot_nodes3 = [1, 2]
    plot_dict1 = {
        "legend": True,
        "title": "Genetic Algorithm - Individual Route Set",
        "xlabel": "X-Coordinate",
        "ylabel": "Y-Coordinate",
        "expected_plot_count": 3,
        "current_plot_count": 1,
        "misc": [
            "Simulated Annealing",
            "$n_{max} = 300$",
            "$T^{(1)} = 300$",
            "$p = 1.15$"
        ]
    }
    plot_dict2 = deepcopy(plot_dict1)
    plot_dict3 = deepcopy(plot_dict1)
    plot_dict2["current_plot_count"] = 2
    plot_dict3["current_plot_count"] = 3
    data_labels = ["Node Locations"]

    plot_data1 = plot_data.PlotData(data_set, data_labels, plot_dict1)
    plot_data1.set_node_data(node_count, optional_nodes1, depot_nodes1)
    plot_data1.set_route_data(route_list1, open_routes1)

    plot_data2 = plot_data.PlotData(data_set, data_labels, plot_dict2)
    plot_data2.set_node_data(node_count, optional_nodes2, depot_nodes2)
    plot_data2.set_route_data(route_list2, open_routes2)

    plot_data3 = plot_data.PlotData(data_set, data_labels, plot_dict3)
    plot_data3.set_node_data(node_count, optional_nodes3, depot_nodes3)
    plot_data3.set_route_data(route_list3, open_routes3)

    plot_functions = [
        plot_data.plot_map,
        plot_data.plot_map,
        plot_data.plot_map
    ]
    plot_list = [plot_data1, plot_data2, plot_data3]

    print("Close plot window to continue.")

    summon_window(plot_functions, plot_list)


def plot_population_initializer(population, details):
    """
    Compiles data from the population in such a manner that
    a bar graph could be plotted. The bar graph demonstrates
    population diversity in terms of fitness value.
    @param population: Population subject to plotting.
    @param details: Dictionary that contains relevant
    information about population initialization, such as
    used population initializer and other relevant parameters.
    @return: List of plotting functions that are to be used,
    and a list of plot data objects that are to be used in
    the plotting.
    """

    # TODO

    plot_functions = []
    plot_list = []
    return plot_functions, plot_list


def plot_population_development(population_collection, details):
    """
    Compiles data from the population in such a manner that
    a line graph could be plotted. The plot demonstrates
    population development from one generation to another.
    @param population_collection: List of populations
    from different generations.
    @param details: Dictionary that contains relevant
    information about provided populations, such as
    used parameters, maximum number of populations subject to
    plotting and the means of how said populations are selected.
    @return: List of plotting functions that are to be used,
    and a list of plot data objects that are to be used in
    the plotting.
    """

    # TODO

    plot_functions = []
    plot_list = []
    return plot_functions, plot_list


def plot_best_individual_fitness(best_individual_history, details):
    """
    Compiles data from the population in such a manner that
    the fitness value of the best individuals can be plotted
    over the course of generations.
    @param best_individual_history: List of individuals that were found
    to be the best in their generations.
    @param details: Dictionary that contains relevant
    information about the development of the best individual, such as
    parameters used in the genetic algorithm.
    @return: List of plotting functions that are to be used,
    and a list of plot data objects that are to be used in
    the plotting.
    """

    # TODO

    plot_functions = []
    plot_list = []
    return plot_functions, plot_list


def plot_best_individual_initial_solution(best_initial_individual, details):
    """
    Compiles data for plotting the best individual's solution that
    was generated during population initialization.
    @param best_initial_individual: The individual that was considered
    the best during initialization.
    @param details: Dictionary that contains relevant
    information about the development of the best individual, such as
    used population initializer and other parameters.
    @return: List of plotting functions that are to be used,
    and a list of plot data objects that are to be used in
    the plotting.
    """

    # TODO

    plot_functions = []
    plot_list = []
    return plot_functions, plot_list


def plot_best_individual_solution(best_unique_individual_history, details):
    """
    Compiles data from the population in such a manner that
    the solution of the best individuals can be plotted
    over the course of generations. Whenever a new best individual
    emerges, a plot representing its solution will be drawn.
    @param best_unique_individual_history: List of unique individuals
    that were found to be the best find during the search.
    @param details: Dictionary that contains relevant
    information about the development of the best individual, such as
    parameters used in the genetic algorithm.
    @return: List of plotting functions that are to be used,
    and a list of plot data objects that are to be used in
    the plotting.
    """

    # TODO

    plot_functions = []
    plot_list = []
    return plot_functions, plot_list
