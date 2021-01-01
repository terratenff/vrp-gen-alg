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
    @param population: Population subject to plotting. Note
    that the population is assumed to be already sorted.
    @param details: Dictionary that contains relevant
    information about population initialization, such as
    used population initializer and other relevant parameters.
    @return: List of plotting functions that are to be used,
    and a list of plot data objects that are to be used in
    the plotting.
    """

    fitness_list = [individual.fitness for individual in population]
    population_initializer = details["population_initializer"]

    individual_indices = list(range(len(fitness_list)))

    xy_data = np.array([individual_indices, fitness_list])

    plot_dict = {
        "legend": False,
        "title": "GA - Population Initialization ({} Individuals)".format(len(population)),
        "xlabel": "Population Individuals (best to worst)",
        "ylabel": "Fitness",
        "expected_plot_count": 1,
        "current_plot_count": 1
    }

    if population_initializer == "Simulated Annealing":
        iteration_count = details["sa_iteration_count"]
        initial_temperature = details["sa_initial_temperature"]
        annealing_coefficient = details["sa_p_coeff"]
        misc_list = [
            "Simulated Annealing",
            "$n_{max} = " + iteration_count + "$",
            "$T^{(1)} = " + initial_temperature + "$",
            "$p = " + annealing_coefficient + "$"
        ]
    else:
        misc_list = [population_initializer]

    plot_dict["misc"] = misc_list

    plot_functions = [plot_data.plot_graph]
    plot_list = [plot_data.PlotData(xy_data, population_initializer, plot_dict)]
    return plot_functions, plot_list


def plot_population_development(population_collection, details):
    """
    Compiles data from the population in such a manner that
    a line graph could be plotted. The plot demonstrates
    population development from one generation to another.
    @param population_collection: List of populations
    from different generations. They are assumed to be
    already sorted.
    @param details: Dictionary that contains relevant
    information about provided populations, such as used
    parameters and maximum number of populations to plot.
    @return: List of plotting functions that are to be used,
    and a list of plot data objects that are to be used in
    the plotting.
    """

    line_count = details["line_count"]
    generation_count = len(population_collection)
    population_count = details["population_count"]
    parent_selector = details["parent_selector"]
    crossover_operator = details["crossover_operator"]
    tournament_probability = details["tournament_probability"]
    crossover_probability = details["crossover_probability"]
    mutation_probability = details["mutation_probability"]

    selected_populations = []
    generation_str = []
    incrementer = generation_count // (line_count + 1)
    index = incrementer
    for i in range(1, line_count + 1):
        selected_populations.append(population_collection[index])
        generation_str.append("Generation {}".format(index))
        index += incrementer

    fitness_lists = []
    for population in selected_populations:
        fitness_lists.append([individual.fitness for individual in population])

    population_tracker = list(range(1, population_count + 1))

    xy_data = np.array([population_tracker, fitness_lists[0]])

    if parent_selector == "Tournament":
        parent_selector_str = parent_selector + "($p_t = " + tournament_probability + "$)"
    else:
        parent_selector_str = parent_selector
    plot_dict = {
        "legend": True,
        "title": "GA - Population Development ({} Individuals)".format(population_count),
        "xlabel": "Population Individuals (best to worst)",
        "ylabel": "Fitness",
        "expected_plot_count": 1,
        "current_plot_count": 1,
        "misc": [
            parent_selector_str,
            crossover_operator,
            "$p_c = " + crossover_probability + "$",
            "$p_m = " + mutation_probability + "$"
        ]
    }

    plot_data_object = plot_data.PlotData(xy_data, generation_str[0], plot_dict)
    for i in range(1, len(generation_str)):
        plot_data_object.add_data(np.array([population_tracker, fitness_lists[i]]), generation_str[i])

    plot_functions = [plot_data.plot_graph]
    plot_list = [plot_data_object]
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

    generation_count = len(best_individual_history)
    population_count = details["population_count"]
    parent_selector = details["parent_selector"]
    crossover_operator = details["crossover_operator"]
    tournament_probability = details["tournament_probability"]
    crossover_probability = details["crossover_probability"]
    mutation_probability = details["mutation_probability"]

    fitness_values = [individual.fitness for individual in best_individual_history]
    generation_tracker = list(range(1, generation_count + 1))

    xy_data = np.array([generation_tracker, fitness_values])

    if parent_selector == "Tournament":
        parent_selector_str = parent_selector + "($p_t = " + tournament_probability + "$)"
    else:
        parent_selector_str = parent_selector
    plot_dict = {
        "legend": False,
        "title": "GA - Optimal Individual ({} Individuals)".format(population_count),
        "xlabel": "Generation",
        "ylabel": "Fitness",
        "expected_plot_count": 1,
        "current_plot_count": 1,
        "misc": [
            parent_selector_str,
            crossover_operator,
            "$p_c = " + crossover_probability + "$",
            "$p_m = " + mutation_probability + "$"
        ]
    }

    plot_functions = [plot_data.plot_graph]
    plot_list = [plot_data.PlotData(xy_data, "", plot_dict)]
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

    xy_data = details["coordinates"]
    route_list = best_initial_individual.get_route_list()
    fitness = best_initial_individual.fitness
    open_routes = details["open_routes"]
    node_count = best_initial_individual.node_count
    optional_nodes = best_initial_individual.optional_nodes
    depot_nodes = best_initial_individual.depot_nodes
    population_initializer = details["population_initializer"]

    plot_dict = {
        "legend": True,
        "title": "GA - Best Initialization Individual",
        "xlabel": "X-Coordinate",
        "ylabel": "Y-Coordinate",
        "expected_plot_count": 1,
        "current_plot_count": 1
    }

    if population_initializer == "Simulated Annealing":
        iteration_count = details["sa_iteration_count"]
        initial_temperature = details["sa_initial_temperature"]
        annealing_coefficient = details["sa_p_coeff"]
        misc_list = [
            "Simulated Annealing",
            "Fitness: {}".format(fitness),
            "$n_{max} = " + iteration_count + "$",
            "$T^{(1)} = " + initial_temperature + "$",
            "$p = " + annealing_coefficient + "$"
        ]
    else:
        misc_list = [population_initializer, "Fitness: {}".format(fitness)]

    plot_dict["misc"] = misc_list

    plot_data_object = plot_data.PlotData(xy_data, "Node Locations", plot_dict)
    plot_data_object.set_node_data(node_count, optional_nodes, depot_nodes)
    plot_data_object.set_route_data(route_list, open_routes)

    plot_functions = [plot_data.plot_map]
    plot_list = [plot_data_object]
    return plot_functions, plot_list


def plot_best_individual_solution(best_unique_individual_history, generation_history, details):
    """
    Compiles data from the population in such a manner that
    the solution of the best individuals can be plotted
    over the course of generations. Whenever a new best individual
    emerges, a plot representing its solution will be drawn.
    @param best_unique_individual_history: List of unique individuals
    that were found to be the best find during the search.
    @param generation_history: List of generation numbers during which
    best individuals were discovered.
    @param details: Dictionary that contains relevant
    information about the development of the best individual, such as
    parameters used in the genetic algorithm.
    @return: List of plotting functions that are to be used,
    and a list of plot data objects that are to be used in
    the plotting.
    """

    xy_data = details["coordinates"]
    open_routes = details["open_routes"]
    node_count = best_unique_individual_history[0].node_count
    optional_nodes = best_unique_individual_history[0].optional_nodes
    depot_nodes = best_unique_individual_history[0].depot_nodes

    population_count = details["population_count"]
    parent_selector = details["parent_selector"]
    crossover_operator = details["crossover_operator"]
    tournament_probability = details["tournament_probability"]
    crossover_probability = details["crossover_probability"]
    mutation_probability = details["mutation_probability"]

    if parent_selector == "Tournament":
        parent_selector_str = parent_selector + "($p_t = " + tournament_probability + "$)"
    else:
        parent_selector_str = parent_selector
    plot_dict = {
        "legend": True,
        "title": "GA - Best Individual of Generation X (Among Y Individuals)",
        "xlabel": "X-Coordinate",
        "ylabel": "Y-Coordinate",
        "expected_plot_count": 1,
        "current_plot_count": 1,
        "misc": [
            "Individual Fitness: Z",
            parent_selector_str,
            crossover_operator,
            "$p_c = " + crossover_probability + "$",
            "$p_m = " + mutation_probability + "$"
        ]
    }

    plot_functions = []
    plot_list = []
    for i in range(len(best_unique_individual_history)):
        individual = best_unique_individual_history[i]
        generation = generation_history[i]
        route_list = individual.get_route_list()
        fitness = individual.fitness
        individual_dict = deepcopy(plot_dict)
        individual_title = "GA - Best Individual of Generation {} (Among {} Individuals)".format(generation,
                                                                                                 population_count)
        fitness_text = "Individual Fitness: {}".format(fitness)
        individual_dict["title"] = individual_title
        individual_dict["misc"][0] = fitness_text
        plot_data_object = plot_data.PlotData(xy_data, "Node Locations", individual_dict)
        plot_data_object.set_node_data(node_count, optional_nodes, depot_nodes)
        plot_data_object.set_route_data(route_list, open_routes)
        
        plot_functions.append(plot_data.plot_map)
        plot_list.append(plot_data_object)

    return plot_functions, plot_list


def set_total_plot_count(plot_list):
    """
    Updates PlotData objects by counting their total amount
    in the provided list. This function should be called
    as soon as all of the necessary PlotData objects
    have been created.
    @param plot_list: List of PlotData objects that are to
    be updated.
    """
    total = len(plot_list)
    i = 1
    for plot_data_item in plot_list:
        plot_data_item.expected_plot_count = total
        plot_data_item.current_plot_count = i
        i += 1
