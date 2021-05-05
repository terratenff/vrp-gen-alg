#!/usr/bin/env python

"""
plot_manager.py:

Uses plot data and plot window to create plots themselves.
"""

import numpy as np
from copy import deepcopy
from operator import attrgetter

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


def plot_population_initializer(population, details):
    """
    Compiles data from the population in such a manner that
    a line graph could be plotted. The line graph demonstrates
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
        "title": "GA - Population Initialization",
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
            "Population Size: {}".format(len(population)),
            "Simulated Annealing",
            "$n_{max} = " + str(iteration_count) + "$",
            "$T^{(1)} = " + str(initial_temperature) + "$",
            "$p = " + str(annealing_coefficient) + "$"
        ]
    else:
        misc_list = [
            "Population Size: {}".format(len(population)),
            population_initializer
        ]

    plot_dict["misc"] = misc_list

    plot_functions = [plot_data.plot_graph]
    plot_list = [plot_data.PlotData(xy_data, [population_initializer], plot_dict)]
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

    population_count = details["population_count"]
    parent_selector = details["parent_selector"]
    crossover_operator = details["crossover_operator"]
    tournament_probability = details["tournament_probability"]
    crossover_probability = details["crossover_probability"]
    mutation_probability = details["mutation_probability"]

    selected_populations = []
    generation_str = []

    # - Selects initial population, next early populations and the final population.
    selected_populations.append(population_collection[0])
    
    generation_str.append("Initialization")
    line_count = min(5, len(population_collection) - 2)
    if line_count == 5:
        if 25 in population_collection.keys():
            line_list = [5, 10, 15, 20, 25]
        else:
            line_list = [1, 2, 3, 4, 5]
    else:
        line_list = list(range(1, line_count))
    
    for i in line_list:
        selected_populations.append(population_collection[i])
        generation_str.append("Generation {}".format(i))
    
    selected_populations.append(population_collection[max(population_collection.keys())])
    generation_str.append("Generation {}".format(max(population_collection.keys())))

    fitness_lists = []
    for population in selected_populations:
        fitness_lists.append([individual.fitness for individual in population])

    population_tracker = list(range(1, population_count + 1))

    xy_data = np.array([population_tracker, fitness_lists[0]])

    if parent_selector == "Tournament Selection":
        parent_selector_str = parent_selector + " ($p_t = " + str(tournament_probability) + "$)"
    else:
        parent_selector_str = parent_selector
    plot_dict = {
        "legend": True,
        "title": "GA - Population Development",
        "xlabel": "Population Individuals (best to worst)",
        "ylabel": "Fitness",
        "expected_plot_count": 1,
        "current_plot_count": 1,
        "misc": [
            "Population Size: {}".format(population_count),
            parent_selector_str,
            crossover_operator,
            "$p_c = " + str(crossover_probability) + "$",
            "$p_m = " + str(mutation_probability) + "$"
        ]
    }

    plot_data_object = plot_data.PlotData(xy_data, [generation_str[0]], plot_dict)
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

    if parent_selector == "Tournament Selection":
        parent_selector_str = parent_selector + " ($p_t = " + str(tournament_probability) + "$)"
    else:
        parent_selector_str = parent_selector
    plot_dict = {
        "legend": False,
        "title": "GA - Optimal Individual, Generation-Wise",
        "xlabel": "Generation",
        "ylabel": "Fitness",
        "expected_plot_count": 1,
        "current_plot_count": 1,
        "misc": [
            "Population Size: {}".format(population_count),
            parent_selector_str,
            crossover_operator,
            "$p_c = " + str(crossover_probability) + "$",
            "$p_m = " + str(mutation_probability) + "$"
        ]
    }

    plot_functions = [plot_data.plot_graph]
    plot_list = [plot_data.PlotData(xy_data, [""], plot_dict)]
    return plot_functions, plot_list


def plot_best_individual_fitness_time(best_time_individual_history, time_collection, details):
    """
    Compiles data from the population in such a manner that
    the fitness values of the best individuals can be plotted
    into a single line graph with respect to time.
    @param best_time_individual_history: List of individuals
    that were found to be the best find at the time of the search.
    @param time_collection: List of instances of time.
    @param details: Dictionary that contains relevant
    information about the development of the best individual, such as
    parameters used in the genetic algorithm.
    @return: List of plotting functions that are to be used,
    and a list of plot data objects that are to be used in
    the plotting.
    """

    fitness_list = [individual.fitness for individual in best_time_individual_history]

    population_count = details["population_count"]
    parent_selector = details["parent_selector"]
    crossover_operator = details["crossover_operator"]
    tournament_probability = details["tournament_probability"]
    crossover_probability = details["crossover_probability"]
    mutation_probability = details["mutation_probability"]

    xy_data = np.array([time_collection, fitness_list])

    if parent_selector == "Tournament Selection":
        parent_selector_str = parent_selector + " ($p_t = " + str(tournament_probability) + "$)"
    else:
        parent_selector_str = parent_selector
    plot_dict = {
        "legend": False,
        "title": "GA - Optimal Individual, Time-Wise",
        "xlabel": "Time (ms)",
        "ylabel": "Fitness",
        "expected_plot_count": 1,
        "current_plot_count": 1,
        "misc": [
            "Population Size: {}".format(population_count),
            parent_selector_str,
            crossover_operator,
            "$p_c = " + str(crossover_probability) + "$",
            "$p_m = " + str(mutation_probability) + "$"
        ]
    }

    plot_functions = [plot_data.plot_graph]
    plot_list = [plot_data.PlotData(xy_data, [""], plot_dict)]
    return plot_functions, plot_list


def plot_best_individual_initial_solution(best_initial_individual, details):
    """
    Compiles data for plotting a map of the best individual's solution that
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
    optional_nodes = best_initial_individual.optional_node_list
    depot_nodes = best_initial_individual.depot_node_list
    population_initializer = details["population_initializer"]
    population_count = details["population_count"]

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
            "Population Size: {}".format(population_count),
            "Simulated Annealing",
            "Fitness: {}".format(int(np.ceil(fitness))),
            "$n_{max} = " + str(iteration_count) + "$",
            "$T^{(1)} = " + str(initial_temperature) + "$",
            "$p = " + str(annealing_coefficient) + "$"
        ]
    else:
        misc_list = [
            "Population Size: {}".format(population_count),
            population_initializer,
            "Fitness: {}".format(int(np.ceil(fitness)))
        ]

    plot_dict["misc"] = misc_list

    plot_data_object = plot_data.PlotData(xy_data, ["Node Locations"], plot_dict)
    plot_data_object.set_node_data(node_count, optional_nodes, depot_nodes)
    plot_data_object.set_route_data(route_list, open_routes)

    plot_functions = [plot_data.plot_map]
    plot_list = [plot_data_object]
    return plot_functions, plot_list


def plot_best_individual_collection(best_unique_individual_history, generation_history, details):
    """
    Compiles data from the population in such a manner that
    the fitness values of the best individuals can be plotted
    into a single bar graph over the course of generations.
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

    fitness_list = [individual.fitness for individual in best_unique_individual_history]

    bar_count = details["bar_count"]
    population_count = details["population_count"]
    parent_selector = details["parent_selector"]
    crossover_operator = details["crossover_operator"]
    tournament_probability = details["tournament_probability"]
    crossover_probability = details["crossover_probability"]
    mutation_probability = details["mutation_probability"]

    if len(generation_history) > bar_count:
        selected_indices = np.linspace(0, len(generation_history) - 1, bar_count, dtype=int)
        selected_generations = [generation_history[i] for i in selected_indices]
        selected_fitness_values = [fitness_list[i] for i in selected_indices]
        xy_data = np.array([selected_generations, selected_fitness_values])
    else:
        xy_data = np.array([generation_history, fitness_list])

    if parent_selector == "Tournament Selection":
        parent_selector_str = parent_selector + " ($p_t = " + str(tournament_probability) + "$)"
    else:
        parent_selector_str = parent_selector
    plot_dict = {
        "legend": False,
        "title": "GA - New Best Individuals",
        "xlabel": "Generation of Discovery",
        "ylabel": "Fitness",
        "expected_plot_count": 1,
        "current_plot_count": 1,
        "misc": [
            "Population Size: {}".format(population_count),
            parent_selector_str,
            crossover_operator,
            "$p_c = " + str(crossover_probability) + "$",
            "$p_m = " + str(mutation_probability) + "$"
        ]
    }

    plot_functions = [plot_data.plot_bar]
    plot_list = [plot_data.PlotData(xy_data, [""], plot_dict)]
    return plot_functions, plot_list


def plot_best_individual_solution(best_unique_individual_history, generation_history, details):
    """
    Compiles data from the population in such a manner that up to a fixed
    number of maps of the best individuals can be plotted over the course of
    the algorithm execution.
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

    max_plot_count = details["max_plot_count"]
    xy_data = details["coordinates"]
    open_routes = details["open_routes"]
    node_count = best_unique_individual_history[0].node_count
    optional_nodes = best_unique_individual_history[0].optional_node_list
    depot_nodes = best_unique_individual_history[0].depot_node_list

    population_count = details["population_count"]
    parent_selector = details["parent_selector"]
    crossover_operator = details["crossover_operator"]
    tournament_probability = details["tournament_probability"]
    crossover_probability = details["crossover_probability"]
    mutation_probability = details["mutation_probability"]

    if parent_selector == "Tournament Selection":
        parent_selector_str = parent_selector + " ($p_t = " + str(tournament_probability) + "$)"
    else:
        parent_selector_str = parent_selector
    plot_dict = {
        "legend": True,
        "title": "GA - New Best Individual from Generation X (Among Y Individuals)",
        "xlabel": "X-Coordinate",
        "ylabel": "Y-Coordinate",
        "expected_plot_count": 1,
        "current_plot_count": 1,
        "misc": [
            "Individual Fitness: Z",
            parent_selector_str,
            crossover_operator,
            "$p_c = " + str(crossover_probability) + "$",
            "$p_m = " + str(mutation_probability) + "$"
        ]
    }

    fitness_high = max(best_unique_individual_history, key=attrgetter("fitness")).fitness
    fitness_low = min(best_unique_individual_history, key=attrgetter("fitness")).fitness
    overall_fitness_difference = np.abs(fitness_high - fitness_low)
    fitness_increment = overall_fitness_difference / max_plot_count

    # An attempt is made here to select individuals fitness-wise as evenly as possible.
    # If every individual here is plotted, not only will it take a long time, there is
    # also the possibility of the application crashing while resizing figures.
    selected_individuals = []
    selected_generations = []
    plot_counter = 0
    fitness_previous = best_unique_individual_history[0].fitness
    for i in range(1, len(best_unique_individual_history)):
        subject_individual = best_unique_individual_history[i]
        fitness_difference = np.abs(fitness_previous - subject_individual.fitness)
        if fitness_difference > fitness_increment or i == len(best_unique_individual_history) - 1:
            selected_individuals.append(best_unique_individual_history[i])
            selected_generations.append(generation_history[i])
            fitness_previous = best_unique_individual_history[i].fitness
            plot_counter += 1
        if plot_counter >= max_plot_count:
            break

    plot_functions = []
    plot_list = []
    for i in range(len(selected_individuals)):
        individual = selected_individuals[i]
        generation = selected_generations[i]
        route_list = individual.get_route_list()
        fitness = individual.fitness
        individual_dict = deepcopy(plot_dict)
        individual_title = "GA - Best Individual of Generation {} (Among {} Individuals)".format(generation,
                                                                                                 population_count)
        fitness_text = "Individual Fitness: {}".format(int(np.ceil(fitness)))
        individual_dict["title"] = individual_title
        individual_dict["misc"][0] = fitness_text
        plot_data_object = plot_data.PlotData(xy_data, ["Node Locations"], individual_dict)
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
