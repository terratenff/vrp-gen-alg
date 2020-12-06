#!/usr/bin/env python

"""
param_builder.py:

Contains functions for setting necessary parameters.
"""

import numpy as np
import algorithms.matrix_builder as matrix_builder


def set_vrp_parameters(vrp_params):
    """
    Interactive function that requests the user to provide
    parameters when asked.
    :param vrp_params: Subject VRP parameters.
    """

    print("(Input N to skip to the next input)")
    print("(Input Q to abort and save any changes)")

    try:
        user_input = input("VRP - Vehicle Count\n- Current: {}\n- Default: 3\n> "
                           .format(vrp_params.vrp_vehicle_count))
        if user_input == "Q":
            return
        elif user_input != "N":
            vrp_params.vrp_vehicle_count = int(user_input)

        # -----------------------------------------------------------------------

        user_input = input("VRP - Node Service Times\n- Current: {}\n- Default: None\nInput File Name > "
                           .format(vrp_params.node_service_times_name))
        if user_input == "Q":
            return
        elif user_input != "N":
            vrp_params.vrp_node_service_time = \
                list(np.loadtxt("variables/node_service_times/" + user_input + ".txt",
                                dtype=int))
            vrp_params.node_service_times_name = user_input

        # -----------------------------------------------------------------------

        user_input = input("VRP - Maximum Route Time\n- Current: {}\n- Default: None\n> "
                           .format(vrp_params.vrp_maximum_route_time))
        if user_input == "Q":
            return
        elif user_input != "N":
            vrp_params.vrp_maximum_route_time = int(user_input)

        # -----------------------------------------------------------------------

        user_input = input("VRP - Maximum Route Distance\n- Current: {}\n- Default: None\n> "
                           .format(vrp_params.vrp_maximum_route_distance))
        if user_input == "Q":
            return
        elif user_input != "N":
            vrp_params.vrp_maximum_route_distance = int(user_input)

        # -----------------------------------------------------------------------

        user_input = input("VRP - Distance-to-Time Ratio\n- Current: {}\n- Default: 1\n"
                           "Positive integer: 'n' distance units to 1 time unit\n"
                           "Negative integer: 1 distance unit to 'n' time units\n"
                           "0: 'n' distance units to 0 time units\n> "
                           .format(vrp_params.vrp_distance_time_ratio))
        if user_input == "Q":
            return
        elif user_input != "N":
            vrp_params.vrp_distance_time_ratio = int(user_input)

        # -----------------------------------------------------------------------

        user_input = input("VRP - Time-to-Cost Ratio\n- Current: {}\n- Default: 1\n"
                           "Positive integer: 'n' time units to 1 cost unit\n"
                           "Negative integer: 1 time unit to 'n' cost units\n"
                           "0: 'n' time units to 0 cost units\n> "
                           .format(vrp_params.vrp_time_cost_ratio))
        if user_input == "Q":
            return
        elif user_input != "N":
            vrp_params.vrp_time_cost_ratio = int(user_input)

        # -----------------------------------------------------------------------

        user_input = input("VRP - Distance-to-Cost Ratio\n- Current: {}\n- Default: 1\n"
                           "Positive integer: 'n' distance units to 1 cost unit\n"
                           "Negative integer: 1 distance unit to 'n' cost units\n"
                           "0: 'n' distance units to 0 cost units\n> "
                           .format(vrp_params.vrp_distance_cost_ratio))
        if user_input == "Q":
            return
        elif user_input != "N":
            vrp_params.vrp_distance_cost_ratio = int(user_input)

        # -----------------------------------------------------------------------

        user_input = input("CVRP - Vehicle Capacity\n- Current: {}\n- Default: 0\n> "
                           .format(vrp_params.cvrp_vehicle_capacity))
        if user_input == "Q":
            return
        elif user_input != "N":
            vrp_params.cvrp_vehicle_capacity = int(user_input)

        # -----------------------------------------------------------------------

        user_input = input("CVRP - Node Demands\n- Current: {}\n- Default: None\nInput File Name > "
                           .format(vrp_params.node_demands_name))
        if user_input == "Q":
            return
        elif user_input != "N":
            vrp_params.cvrp_node_demand = \
                list(np.loadtxt("variables/node_demands/" + user_input + ".txt",
                                dtype=int))
            vrp_params.node_demands_name = user_input

        # -----------------------------------------------------------------------

        user_input = input("OVRP - Enable Open Routes\n- Current: {}\n- Default: False\n(True/False) > "
                           .format(vrp_params.ovrp_enabled))
        if user_input == "Q":
            return
        elif user_input != "N":
            vrp_params.ovrp_enabled = bool(user_input)

        # -----------------------------------------------------------------------

        user_input = input("VRPP - Node Profits\n- Current: {}\n- Default: None\nInput File Name > "
                           .format(vrp_params.node_profits_name))
        if user_input == "Q":
            return
        elif user_input != "N":
            vrp_params.vrpp_node_profit = \
                list(np.loadtxt("variables/node_profits/" + user_input + ".txt",
                                dtype=int))
            vrp_params.node_profits_name = user_input

        # -----------------------------------------------------------------------

        user_input = input("VRPP - Exclude Travel Costs\n- Current: {}\n- Default: False\n(True/False) > "
                           .format(vrp_params.vrpp_exclude_travel_costs))
        if user_input == "Q":
            return
        elif user_input != "N":
            vrp_params.vrpp_exclude_travel_costs = bool(user_input)

        # -----------------------------------------------------------------------

        user_input = input("VRPP - Optional Nodes\n- Current: {}\n- Default: None\n"
                           "Input Nodes separated by whitespace (Example: '0 1 2')\n> "
                           .format(vrp_params.vrpp_optional_node))
        if user_input == "Q":
            return
        elif user_input != "N":
            vrp_params.vrpp_optional_node = [int(i) for i in user_input.split(" ")]

        # -----------------------------------------------------------------------

        user_input = input("MDVRP - Depot Nodes\n- Current: {}\n- Default: 0\n"
                           "Input Nodes separated by whitespace (Example: '0 1 2')\n> "
                           .format(vrp_params.mdvrp_depot_node))
        if user_input == "Q":
            return
        elif user_input != "N":
            vrp_params.mdvrp_depot_node = [int(i) for i in user_input.split(" ")]

        # -----------------------------------------------------------------------

        user_input = input("MDVRP - Optimize Depot Nodes\n- Current: {}\n- Default: False\n(True/False) > "
                           .format(vrp_params.mdvrp_optimize_depot_nodes))
        if user_input == "Q":
            return
        elif user_input != "N":
            vrp_params.mdvrp_optimize_depot_nodes = bool(user_input)

        # -----------------------------------------------------------------------

        user_input = input("VRPTW - Node Time Windows\n- Current: {}\n- Default: None\n"
                           "Input File Name (or 'None') > "
                           .format(vrp_params.node_time_windows_name))
        if user_input == "Q":
            return
        elif user_input != "N":
            if user_input.upper() == "NONE":
                vrp_params.vrptw_node_time_window = None
            else:
                vrp_params.vrptw_node_time_window = \
                    list(map(tuple, np.loadtxt("variables/node_time_windows/" + user_input + ".txt",
                                               dtype=int)))
                vrp_params.node_time_windows_name = user_input

        # -----------------------------------------------------------------------

        user_input = input("VRPTW - Node Penalty Coefficients\n- Current: {}\n- Default: None\n"
                           "Input File Name (or 'None') > "
                           .format(vrp_params.node_penalties_name))
        if user_input == "Q":
            return
        elif user_input != "N":
            if user_input.upper() == "NONE":
                vrp_params.vrptw_node_penalty = None
            else:
                vrp_params.vrptw_node_penalty = \
                    list(np.loadtxt("variables/node_penalties/" + user_input + ".txt",
                                    dtype=float))
                vrp_params.node_penalties_name = user_input

        # -----------------------------------------------------------------------

        user_input = input("VRPTW - Hard Time Windows\n- Current: {}\n- Default: False\n(True/False) > "
                           .format(vrp_params.vrptw_hard_windows))
        if user_input == "Q":
            return
        elif user_input != "N":
            vrp_params.vrptw_hard_windows = bool(user_input)

    except ValueError:
        print("Invalid value. Aborting...")


def set_algorithm_parameters(alg_params):
    """
    Interactive function that requests the user to provide
    parameters when asked.
    :param alg_params: Subject Algorithm parameters.
    """

    print("(Input N to skip to the next input)")
    print("(Input Q to abort and save any changes)")

    try:
        user_input = input("Population Count\n- Current: {}\n- Default: 100\n> "
                           .format(alg_params.population_count))
        if user_input == "Q":
            return
        elif user_input != "N":
            alg_params.population_count = int(user_input)

        # -----------------------------------------------------------------------

        user_input = input("Population Initializer\n"
                           "- 0 = Random\n"
                           "- 1 = Allele Mutation\n"
                           "- 2 = Gene Permutation\n"
                           "- 3 = Simulated Annealing\n"
                           "- Current: {}\n- Default: 0\n> "
                           .format(alg_params.population_initializer))
        if user_input == "Q":
            return
        elif user_input != "N":
            if int(user_input) < 0 or int(user_input) > 3:
                while int(user_input) < 0 or int(user_input) > 3:
                    print("Input value is outside expected range.")
                    user_input = input("> ")
            alg_params.population_initializer = int(user_input)

        # -----------------------------------------------------------------------

        user_input = input("Minimum Generation Count\n- Current: {}\n- Default: 100\n> "
                           .format(alg_params.generation_count_min))
        if user_input == "Q":
            return
        elif user_input != "N":
            alg_params.generation_count_min = int(user_input)

        # -----------------------------------------------------------------------

        user_input = input("Maximum Generation Count\n- Current: {}\n- Default: 1500\n> "
                           .format(alg_params.generation_count_max))
        if user_input == "Q":
            return
        elif user_input != "N":
            alg_params.generation_count_max = int(user_input)

        # -----------------------------------------------------------------------

        user_input = input("Individual CPU Time Limit\n- Current: {} ms\n- Default: 5000 ms\nms > "
                           .format(alg_params.cpu_individual_limit))
        if user_input == "Q":
            return
        elif user_input != "N":
            alg_params.cpu_individual_limit = int(user_input)

        # -----------------------------------------------------------------------

        user_input = input("Total CPU Time Limit\n- Current: {} ms\n- Default: 60000 ms\nms > "
                           .format(alg_params.cpu_total_limit))
        if user_input == "Q":
            return
        elif user_input != "N":
            alg_params.cpu_total_limit = int(user_input)

        # -----------------------------------------------------------------------

        user_input = input("Fitness Lower Bound\n- Current: {}\n- Default: None\n> "
                           .format(alg_params.fitness_lower_bound))
        if user_input == "Q":
            return
        elif user_input != "N":
            alg_params.fitness_lower_bound = int(user_input)

        # -----------------------------------------------------------------------

        user_input = input("Fitness Upper Bound\n- Current: {}\n- Default: None\n> "
                           .format(alg_params.fitness_upper_bound))
        if user_input == "Q":
            return
        elif user_input != "N":
            alg_params.fitness_upper_bound = int(user_input)

        # -----------------------------------------------------------------------

        user_input = input("Fitness Threshold\n- Current: {}\n- Default: 0\n> "
                           .format(alg_params.fitness_threshold))
        if user_input == "Q":
            return
        elif user_input != "N":
            alg_params.fitness_threshold = int(user_input)

        # -----------------------------------------------------------------------

        user_input = input("Parent Candidate Count\n- Current: {}\n- Default: 5\n> "
                           .format(alg_params.parent_candidate_count))
        if user_input == "Q":
            return
        elif user_input != "N":
            alg_params.parent_candidate_count = int(user_input)

        # -----------------------------------------------------------------------

        user_input = input("Parent Selection Function\n"
                           "- 0 = Best Fitness\n"
                           "- 1 = Roulette Selection\n"
                           "- 2 = Tournament Selection\n"
                           "- Current: {}\n- Default: 0\n> "
                           .format(alg_params.parent_selection_function))
        if user_input == "Q":
            return
        elif user_input != "N":
            if int(user_input) < 0 or int(user_input) > 2:
                while int(user_input) < 0 or int(user_input) > 2:
                    print("Input value is outside expected range.")
                    user_input = input("> ")
            alg_params.parent_selection_function = int(user_input)

        # -----------------------------------------------------------------------

        user_input = input("Tournament Probability\n- Current: {:0.2f}\n- Default: 0.75\n"
                           "Input Range: [0.00, 1.00]\n"
                           "This parameter applies only if Tournament Selection is used.\n> "
                           .format(alg_params.tournament_probability))
        if user_input == "Q":
            return
        elif user_input != "N":
            alg_params.tournament_probability = float(user_input)

        # -----------------------------------------------------------------------

        user_input = input("Crossover Operator\n"
                           "- 0 = 1-Point\n"
                           "- 1 = 2-Point\n"
                           "- 2 = Order Crossover\n"
                           "- 3 = Vehicle Crossover\n"
                           "- Current: {}\n- Default: 0\n> "
                           .format(alg_params.crossover_operator))
        if user_input == "Q":
            return
        elif user_input != "N":
            if int(user_input) < 0 or int(user_input) > 3:
                while int(user_input) < 0 or int(user_input) > 3:
                    print("Input value is outside expected range.")
                    user_input = input("> ")
            alg_params.crossover_operator = int(user_input)

        # -----------------------------------------------------------------------

        user_input = input("Crossover Probability\n- Current: {:0.2f}\n- Default: 0.90\n"
                           "Input Range: [0.00, 1.00] > "
                           .format(alg_params.crossover_probability))
        if user_input == "Q":
            return
        elif user_input != "N":
            alg_params.crossover_probability = float(user_input)

        # -----------------------------------------------------------------------

        user_input = input("Mutation Probability\n- Current: {:0.2f}\n- Default: 0.10\n"
                           "Input Range: [0.00, 1.00] > "
                           .format(alg_params.mutation_probability))
        if user_input == "Q":
            return
        elif user_input != "N":
            alg_params.mutation_probability = float(user_input)

        # -----------------------------------------------------------------------

        if alg_params.filtration_frequency <= 0:
            filtration_fr_str = "Never"
        elif alg_params.filtration_frequency == 1:
            filtration_fr_str = "Every Generation"
        else:
            filtration_fr_str = "Every {} Generations".format(alg_params.filtration_frequency)
        user_input = input("Filtration Frequency\n"
                           "- Current: {}\n"
                           "- Default: Never\n"
                           "Input in terms of 'once every x generations'. Input <= 0 for 'Never'.\n> "
                           .format(filtration_fr_str))
        if user_input == "Q":
            return
        elif user_input != "N":
            alg_params.filtration_frequency = int(user_input)

        # -----------------------------------------------------------------------

        user_input = input("SA - Iteration Count\n- Current: {}\n- Default: 300\n"
                           "This parameter applies only if Simulated Annealing is used.\n> "
                           .format(alg_params.sa_iteration_count))
        if user_input == "Q":
            return
        elif user_input != "N":
            alg_params.sa_iteration_count = int(user_input)

        # -----------------------------------------------------------------------

        user_input = input("SA - Initial Temperature\n- Current: {}\n- Default: 300\n"
                           "This parameter applies only if Simulated Annealing is used.\n> "
                           .format(alg_params.sa_initial_temperature))
        if user_input == "Q":
            return
        elif user_input != "N":
            alg_params.sa_initial_temperature = int(user_input)

        # -----------------------------------------------------------------------

        user_input = input("SA - Annealing Coefficient\n- Current: {:0.2f}\n- Default: 1.15\n"
                           "Recommended Input Range: (1.00, 2.00]\n"
                           "This parameter applies only if Simulated Annealing is used.\n> "
                           .format(alg_params.sa_p_coeff))
        if user_input == "Q":
            return
        elif user_input != "N":
            alg_params.sa_p_coeff = float(user_input)
    except ValueError:
        print("Invalid value. Aborting...")


def save_params(filename, vrp_params, alg_params):
    """
    Saves current parameter settings into two identically named text files.
    :param filename: The name that is to be given for the file.
    :param vrp_params: VRP parameters to be saved.
    :param alg_params: Algorithmic parameters to be saved.
    """

    # ---------------------------------------------------------------
    # - VRP - Parameters --------------------------------------------
    # ---------------------------------------------------------------

    if vrp_params.vrp_coordinates is None:
        content_type = "matrix"
        content_name = vrp_params.cost_matrices_name
        overriding_content_name = "None"
    else:
        content_type = "coordinates"
        content_name = vrp_params.coordinates_name
        overriding_content_name = str(vrp_params.cost_matrices_name)
        if overriding_content_name == "undefined":
            overriding_content_name = "None"

    with open("variables/parameter_settings/vrp/" + filename + ".txt", "a") as file:
        file.write("vrp_contents={}={}\n".format(content_type, content_name))
        file.write("vrp_path_table_override={}\n".format(overriding_content_name))
        file.write("vrp_vehicle_count={}\n".format(str(vrp_params.vrp_vehicle_count)))
        file.write("vrp_node_service_time={}\n".format(str(vrp_params.node_service_times_name)))
        file.write("vrp_maximum_route_time={}\n".format(str(vrp_params.vrp_maximum_route_time)))
        file.write("vrp_maximum_route_distance={}\n".format(str(vrp_params.vrp_maximum_route_distance)))
        file.write("vrp_distance_time_ratio={}\n".format(str(vrp_params.vrp_distance_time_ratio)))
        file.write("vrp_time_cost_ratio={}\n".format(str(vrp_params.vrp_time_cost_ratio)))
        file.write("vrp_distance_cost_ratio={}\n".format(str(vrp_params.vrp_distance_cost_ratio)))
        file.write("cvrp_vehicle_capacity={}\n".format(str(vrp_params.cvrp_vehicle_capacity)))
        file.write("cvrp_node_demand={}\n".format(str(vrp_params.node_demands_name)))
        file.write("ovrp_enabled={}\n".format(str(vrp_params.ovrp_enabled)))
        file.write("vrpp_node_profit={}\n".format(str(vrp_params.node_profits_name)))
        file.write("vrpp_exclude_travel_costs={}\n".format(str(vrp_params.vrpp_exclude_travel_costs)))
        file.write("vrpp_optional_node={}\n".format(str(vrp_params.vrpp_optional_node)
                                                    .replace("[", "")
                                                    .replace("]", "")
                                                    .replace(",", "")))
        file.write("mdvrp_depot_node={}\n".format(str(vrp_params.mdvrp_depot_node)
                                                  .replace("[", "")
                                                  .replace("]", "")
                                                  .replace(",", "")))
        file.write("mdvrp_optimize_depot_nodes={}\n".format(str(vrp_params.mdvrp_optimize_depot_nodes)))
        file.write("vrptw_node_time_window={}\n".format(str(vrp_params.node_time_windows_name)))
        file.write("vrptw_node_penalty={}\n".format(str(vrp_params.node_penalties_name)))
        file.write("vrptw_hard_windows={}\n".format(str(vrp_params.vrptw_hard_windows)))

    # ---------------------------------------------------------------
    # - GENALG - Parameters -----------------------------------------
    # ---------------------------------------------------------------

    with open("variables/parameter_settings/genalg/" + filename + ".txt", "a") as file:
        file.write("population_count={}\n".format(alg_params.population_count))
        file.write("population_initializer={}\n".format(str(alg_params.population_initializer)))
        file.write("generation_count_min={}\n".format(str(alg_params.generation_count_min)))
        file.write("generation_count_max={}\n".format(str(alg_params.generation_count_max)))
        file.write("cpu_individual_limit={}\n".format(str(alg_params.cpu_individual_limit)))
        file.write("cpu_total_limit={}\n".format(str(alg_params.cpu_total_limit)))
        file.write("fitness_lower_bound={}\n".format(str(alg_params.fitness_lower_bound)))
        file.write("fitness_upper_bound={}\n".format(str(alg_params.fitness_upper_bound)))
        file.write("fitness_threshold={}\n".format(str(alg_params.fitness_threshold)))
        file.write("parent_candidate_count={}\n".format(str(alg_params.parent_candidate_count)))
        file.write("parent_selection_function={}\n".format(str(alg_params.parent_selection_function)))
        file.write("tournament_probability={}\n".format(str(alg_params.tournament_probability)))
        file.write("crossover_operator={}\n".format(str(alg_params.crossover_operator)))
        file.write("crossover_probability={}\n".format(str(alg_params.crossover_probability)))
        file.write("mutation_probability={}\n".format(str(alg_params.mutation_probability)))
        file.write("filtration_frequency={}\n".format(str(alg_params.filtration_frequency)))
        file.write("sa_iteration_count={}\n".format(str(alg_params.sa_iteration_count)))
        file.write("sa_initial_temperature={}\n".format(str(alg_params.sa_initial_temperature)))
        file.write("sa_p_coeff={}".format(str(alg_params.sa_p_coeff)))


def load_params(filename, vrp_params, alg_params):
    """
    Assigns parameters found in specified file to parameter instances.
    :param filename: Name of the subject file.
    :param vrp_params: VRP parameters.
    :param alg_params: Algorithmic parameters.
    """

    # ---------------------------------------------------------------
    # - VRP - Parameters --------------------------------------------
    # ---------------------------------------------------------------

    with open("variables/parameter_settings/vrp/" + filename + ".txt") as file:
        contents = file.readlines()

    coordinates = None
    overriding_matrix = None

    contents = [x.strip() for x in contents]
    for line in contents:
        key_value = line.split("=")

        if key_value[0] == "vrp_contents":
            file_type = key_value[1]
            file_name = key_value[2]
            if file_type == "matrix":
                matrix_builder.select_cost_matrix(vrp_params, name=file_name)
            elif file_type == "coordinates":
                coordinates = file_name
        elif key_value[0] == "vrp_path_table_override":
            overriding_matrix = key_value[1]

        elif key_value[0] == "vrp_vehicle_count":
            vrp_params.vrp_vehicle_count = int(key_value[1])
        elif key_value[0] == "vrp_node_service_time":
            matrix_builder.select_service_times_matrix(vrp_params, name=key_value[1])
        elif key_value[0] == "vrp_maximum_route_time":
            vrp_params.vrp_maximum_route_time = int(key_value[1])
        elif key_value[0] == "vrp_maximum_route_distance":
            vrp_params.vrp_maximum_route_distance = int(key_value[1])
        elif key_value[0] == "vrp_distance_time_ratio":
            vrp_params.vrp_distance_time_ratio = int(key_value[1])
        elif key_value[0] == "vrp_time_cost_ratio":
            vrp_params.vrp_time_cost_ratio = int(key_value[1])
        elif key_value[0] == "vrp_distance_cost_ratio":
            vrp_params.vrp_distance_cost_ratio = int(key_value[1])
        elif key_value[0] == "cvrp_vehicle_capacity":
            vrp_params.cvrp_vehicle_capacity = int(key_value[1])
        elif key_value[0] == "cvrp_node_demand":
            matrix_builder.select_demands_matrix(vrp_params, name=key_value[1])
        elif key_value[0] == "ovrp_enabled":
            vrp_params.ovrp_enabled = key_value[1] == "True"
        elif key_value[0] == "vrpp_node_profit":
            matrix_builder.select_profits_matrix(vrp_params, name=key_value[1])
        elif key_value[0] == "vrpp_exclude_travel_costs":
            vrp_params.vrpp_exclude_travel_costs = key_value[1] == "True"
        elif key_value[0] == "vrpp_optional_node":
            vrp_params.vrpp_optional_node = [int(i) for i in key_value[1].split(" ")]
        elif key_value[0] == "mdvrp_depot_node":
            vrp_params.mdvrp_depot_node = [int(i) for i in key_value[1].split(" ")]
        elif key_value[0] == "mdvrp_optimize_depot_nodes":
            vrp_params.mdvrp_optimize_depot_nodes = key_value[1] == "True"
        elif key_value[0] == "vrptw_node_time_window":
            matrix_builder.select_time_windows_matrix(vrp_params, name=key_value[1])
        elif key_value[0] == "vrptw_node_penalty":
            matrix_builder.select_penalties_matrix(vrp_params, name=key_value[1])
        elif key_value[0] == "vrptw_hard_windows":
            vrp_params.vrptw_hard_windows = key_value[1] == "True"

    if coordinates is not None:
        if overriding_matrix == "None":
            overriding_matrix = None
        matrix_builder.select_coordinates_matrix(
            vrp_params,
            name=coordinates,
            name_override=overriding_matrix
        )

    # ---------------------------------------------------------------
    # - GENALG - Parameters -----------------------------------------
    # ---------------------------------------------------------------

    with open("variables/parameter_settings/genalg/" + filename + ".txt") as file:
        contents = file.readlines()

    contents = [x.strip() for x in contents]
    for line in contents:
        key_value = line.split("=")
        if key_value[0] == "population_count":
            alg_params.population_count = int(key_value[1])
        elif key_value[0] == "population_initializer":
            alg_params.population_initializer = int(key_value[1])
        elif key_value[0] == "generation_count_min":
            alg_params.generation_count_min = int(key_value[1])
        elif key_value[0] == "generation_count_max":
            alg_params.generation_count_max = int(key_value[1])
        elif key_value[0] == "cpu_individual_limit":
            alg_params.cpu_individual_limit = int(key_value[1])
        elif key_value[0] == "cpu_total_limit":
            alg_params.cpu_total_limit = int(key_value[1])
        elif key_value[0] == "fitness_lower_bound":
            alg_params.fitness_lower_bound = None if key_value[1] == str(None) else int(key_value[1])
        elif key_value[0] == "fitness_upper_bound":
            alg_params.fitness_upper_bound = None if key_value[1] == str(None) else int(key_value[1])
        elif key_value[0] == "fitness_threshold":
            alg_params.fitness_threshold = int(key_value[1])
        elif key_value[0] == "parent_candidate_count":
            alg_params.parent_candidate_count = int(key_value[1])
        elif key_value[0] == "parent_selection_function":
            alg_params.parent_selection_function = int(key_value[1])
        elif key_value[0] == "tournament_probability":
            alg_params.tournament_probability = float(key_value[1])
        elif key_value[0] == "offspring_pair_count":
            alg_params.offspring_pair_count = int(key_value[1])
        elif key_value[0] == "crossover_operator":
            alg_params.crossover_operator = int(key_value[1])
        elif key_value[0] == "crossover_probability":
            alg_params.crossover_probability = float(key_value[1])
        elif key_value[0] == "mutation_probability":
            alg_params.mutation_probability = float(key_value[1])
        elif key_value[0] == "filtration_frequency":
            alg_params.filtration_frequency = int(key_value[1])
        elif key_value[0] == "sa_iteration_count":
            alg_params.sa_iteration_count = int(key_value[1])
        elif key_value[0] == "sa_initial_temperature":
            alg_params.sa_initial_temperature = int(key_value[1])
        elif key_value[0] == "sa_p_coeff":
            alg_params.sa_p_coeff = float(key_value[1])
