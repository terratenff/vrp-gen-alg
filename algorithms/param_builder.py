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
        user_input = input("VRP - Depot Node\n- Current: {}\n- Default: 0\n> "
                           .format(vrp_params.vrp_depot_node))
        if user_input == "Q":
            return
        elif user_input != "N":
            vrp_params.vrp_depot_node = int(user_input)

        # -----------------------------------------------------------------------

        user_input = input("VRP - Vehicle Count\n- Current: {}\n- Default: 3\n> "
                           .format(vrp_params.vrp_vehicle_count))
        if user_input == "Q":
            return
        elif user_input != "N":
            vrp_params.vrp_vehicle_count = int(user_input)

        # -----------------------------------------------------------------------

        user_input = input("VRP - Vehicle Variance\n- Current: {}\n- Default: 3\n> "
                           .format(vrp_params.vrp_vehicle_variance))
        if user_input == "Q":
            return
        elif user_input != "N":
            vrp_params.vrp_vehicle_variance = int(user_input)

        # -----------------------------------------------------------------------

        user_input = input("VRP - Node Service Times\n- Current: {}\n- Default: None\nInput File Name > "
                           .format(vrp_params.vrp_node_service_time))
        if user_input == "Q":
            return
        elif user_input != "N":
            vrp_params.vrp_node_service_time = \
                list(np.loadtxt("variables/node_service_times/" + user_input + ".txt",
                                dtype=int))[0]

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

        user_input = input("CVRP - Vehicle Capacity\n- Current: {}\n- Default: 0\n> "
                           .format(vrp_params.cvrp_vehicle_capacity))
        if user_input == "Q":
            return
        elif user_input != "N":
            vrp_params.cvrp_vehicle_capacity = int(user_input)

        # -----------------------------------------------------------------------

        user_input = input("CVRP - Node Demands\n- Current: {}\n- Default: None\nInput File Name > "
                           .format(vrp_params.cvrp_node_demand))
        if user_input == "Q":
            return
        elif user_input != "N":
            vrp_params.cvrp_node_demand = \
                list(np.loadtxt("variables/node_demands/" + user_input + ".txt",
                                dtype=int))[0]

        # -----------------------------------------------------------------------

        user_input = input("OVRP - Enabled\n- Current: {}\n- Default: False\nTrue/False > "
                           .format(vrp_params.ovrp_enabled))
        if user_input == "Q":
            return
        elif user_input != "N":
            vrp_params.ovrp_enabled = bool(user_input)

        # -----------------------------------------------------------------------

        user_input = input("VRPP - Node Profits\n- Current: {}\n- Default: None\nInput File Name > "
                           .format(vrp_params.vrpp_node_profit))
        if user_input == "Q":
            return
        elif user_input != "N":
            vrp_params.vrpp_node_profit = \
                list(np.loadtxt("variables/node_profits/" + user_input + ".txt",
                                dtype=int))[0]

        # -----------------------------------------------------------------------

        user_input = input("VRPTW - Node Time Windows\n- Current: {}\n- Default: None\n"
                           "Input File Name (or 'None') > "
                           .format(vrp_params.vrptw_node_time_window))
        if user_input == "Q":
            return
        elif user_input != "N":
            if user_input.upper() == "NONE":
                vrp_params.vrptw_node_time_window = None
            else:
                vrp_params.vrptw_node_time_window = \
                    list(map(tuple, np.loadtxt("variables/node_time_windows/" + user_input + ".txt",
                                               dtype=int)))

        # -----------------------------------------------------------------------

        user_input = input("VRPTW - Node Penalty Coefficients\n- Current: {}\n- Default: None\n"
                           "Input File Name > "
                           .format(vrp_params.vrptw_node_penalty))
        if user_input == "Q":
            return
        elif user_input != "N":
            vrp_params.vrptw_node_penalty = \
                list(np.loadtxt("variables/node_penalties/" + user_input + ".txt",
                                dtype=float))[0]

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
        user_input = input("GEN - Population Count\n- Current: {}\n- Default: 100\n> "
                           .format(alg_params.population_count))
        if user_input == "Q":
            return
        elif user_input != "N":
            alg_params.population_count = int(user_input)

        # -----------------------------------------------------------------------

        user_input = input("ALG - Population Initializer\n"
                           "- 0 = Random\n"
                           "- 1 = Mutated Copies\n"
                           "- 2 = Gene Permutation\n"
                           "- 3 = Chromosome Permutation\n"
                           "- 4 = Sweep Algorithm\n"
                           "- Current: {}\n- Default: 0\n> "
                           .format(alg_params.fitness_evaluator))
        if user_input == "Q":
            return
        elif user_input != "N":
            if int(user_input) < 0 or int(user_input) > 4:
                while int(user_input) < 0 or int(user_input) > 4:
                    print("Input value is outside expected range.")
                    user_input = input("> ")
            alg_params.population_initializer = int(user_input)

        # -----------------------------------------------------------------------

        user_input = input("GEN - Minimum Generation Count\n- Current: {}\n- Default: 10\n> "
                           .format(alg_params.generation_count_min))
        if user_input == "Q":
            return
        elif user_input != "N":
            alg_params.generation_count_min = int(user_input)

        # -----------------------------------------------------------------------

        user_input = input("GEN - Maximum Generation Count\n- Current: {}\n- Default: 100\n> "
                           .format(alg_params.generation_count_max))
        if user_input == "Q":
            return
        elif user_input != "N":
            alg_params.generation_count_max = int(user_input)

        # -----------------------------------------------------------------------

        user_input = input("ALG - Fitness Evaluator\n"
                           "- 0 = Total Cost\n"
                           "- 1 = Total Distance\n"
                           "- 2 = Longest Route\n"
                           "- Current: {}\n- Default: 0\n> "
                           .format(alg_params.fitness_evaluator))
        if user_input == "Q":
            return
        elif user_input != "N":
            if int(user_input) < 0 or int(user_input) > 2:
                while int(user_input) < 0 or int(user_input) > 2:
                    print("Input value is outside expected range.")
                    user_input = input("> ")
            alg_params.fitness_evaluator = int(user_input)

        # -----------------------------------------------------------------------

        user_input = input("GEN - Parent Candidate Count\n- Current: {}\n- Default: 2\n> "
                           .format(alg_params.parent_candidate_count))
        if user_input == "Q":
            return
        elif user_input != "N":
            alg_params.parent_candidate_count = int(user_input)

        # -----------------------------------------------------------------------

        user_input = input("ALG - Parent Selection Function\n"
                           "- 0 = Best Fitness\n"
                           "- 1 = Roulette Wheel\n"
                           "- 2 = Tournament\n"
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

        user_input = input("GEN - Selection Probability\n- Current: {:0.2f}\n- Default: 0.75\n"
                           "Input Range: [0.00, 1.00] > "
                           .format(alg_params.selection_probability))
        if user_input == "Q":
            return
        elif user_input != "N":
            alg_params.selection_probability = float(user_input)

        # -----------------------------------------------------------------------

        user_input = input("GEN - Offspring Pair Count\n- Current: {}\n- Default: 1\n> "
                           .format(alg_params.offspring_pair_count))
        if user_input == "Q":
            return
        elif user_input != "N":
            alg_params.offspring_pair_count = int(user_input)

        # -----------------------------------------------------------------------

        user_input = input("ALG - Crossover Operator\n"
                           "- 0 = 1-Point\n"
                           "- 1 = 2-Point\n"
                           "- 2 = Uniform\n"
                           "- 3 = OE-Children\n"
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

        user_input = input("GEN - Crossover Probability\n- Current: {:0.2f}\n- Default: 0.90\n"
                           "Input Range: [0.00, 1.00] > "
                           .format(alg_params.crossover_probability))
        if user_input == "Q":
            return
        elif user_input != "N":
            alg_params.crossover_probability = float(user_input)

        # -----------------------------------------------------------------------

        user_input = input("GEN - Mutation Probability\n- Current: {:0.3f}\n- Default: 0.05\n"
                           "Input Range: [0.000, 1.000] > "
                           .format(alg_params.mutation_probability))
        if user_input == "Q":
            return
        elif user_input != "N":
            alg_params.mutation_probability = float(user_input)

        # -----------------------------------------------------------------------

        user_input = input("GEN - Followup Probability\n- Current: {:0.2f}\n- Default: 0.70\n"
                           "Input Range: [0.00, 1.00] > "
                           .format(alg_params.followup_probability))
        if user_input == "Q":
            return
        elif user_input != "N":
            alg_params.followup_probability = float(user_input)

        # -----------------------------------------------------------------------

        user_input = input("ALG - Elitism Managing Operator\n"
                           "- 0 = None\n"
                           "- 1 = Retention\n"
                           "- 2 = Filtration\n"
                           "- Current: {}\n- Default: 0\n> "
                           .format(alg_params.elitism_operator))
        if user_input == "Q":
            return
        elif user_input != "N":
            if int(user_input) < 0 or int(user_input) > 2:
                while int(user_input) < 0 or int(user_input) > 2:
                    print("Input value is outside expected range.")
                    user_input = input("> ")
            alg_params.elitism_operator = int(user_input)

        # -----------------------------------------------------------------------

        user_input = input("GEN - Elitism Management Rate\n- Current: {}\n- Default: 0\n"
                           "Integer represents how many generations must pass before\n"
                           "elitism managing operator is called.\n"
                           "> "
                           .format(alg_params.elitism_frequency))
        if user_input == "Q":
            return
        elif user_input != "N":
            alg_params.elitism_frequency = int(user_input)
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
        file.write("vrp_depot_node={}\n".format(str(vrp_params.vrp_depot_node)))
        file.write("vrp_vehicle_count={}\n".format(str(vrp_params.vrp_vehicle_count)))
        file.write("vrp_vehicle_variance={}\n".format(str(vrp_params.vrp_vehicle_variance)))
        file.write("vrp_node_service_time={}\n".format(str(vrp_params.node_service_times_name)))
        file.write("vrp_distance_time_ratio={}\n".format(str(vrp_params.vrp_distance_time_ratio)))
        file.write("cvrp_vehicle_capacity={}\n".format(str(vrp_params.cvrp_vehicle_capacity)))
        file.write("cvrp_node_demand={}\n".format(str(vrp_params.node_demands_name)))
        file.write("ovrp_enabled={}\n".format(str(vrp_params.ovrp_enabled)))
        file.write("vrpp_node_profit={}\n".format(str(vrp_params.node_profits_name)))
        file.write("vrptw_node_time_window={}\n".format(str(vrp_params.node_time_windows_name)))
        file.write("vrptw_node_penalty={}".format(str(vrp_params.node_penalties_name)))

    # ---------------------------------------------------------------
    # - GENALG - Parameters -----------------------------------------
    # ---------------------------------------------------------------

    with open("variables/parameter_settings/genalg/" + filename + ".txt", "a") as file:
        file.write("population_count={}\n".format(alg_params.population_count))
        file.write("generation_count_min={}\n".format(str(alg_params.generation_count_min)))
        file.write("generation_count_max={}\n".format(str(alg_params.generation_count_max)))
        file.write("fitness_evaluator={}\n".format(str(alg_params.fitness_evaluator)))
        file.write("parent_candidate_count={}\n".format(str(alg_params.parent_candidate_count)))
        file.write("parent_selection_function={}\n".format(str(alg_params.parent_selection_function)))
        file.write("selection_probability={}\n".format(str(alg_params.selection_probability)))
        file.write("offspring_pair_count={}\n".format(str(alg_params.offspring_pair_count)))
        file.write("crossover_operator={}\n".format(str(alg_params.crossover_operator)))
        file.write("crossover_probability={}\n".format(str(alg_params.crossover_probability)))
        file.write("mutation_probability={}\n".format(str(alg_params.mutation_probability)))
        file.write("followup_probability={}\n".format(str(alg_params.followup_probability)))
        file.write("elitism_operator={}\n".format(str(alg_params.elitism_operator)))
        file.write("elitism_frequency={}".format(str(alg_params.elitism_frequency)))


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

        elif key_value[0] == "vrp_depot_node":
            vrp_params.vrp_depot_node = int(key_value[1])
        elif key_value[0] == "vrp_vehicle_count":
            vrp_params.vrp_vehicle_count = int(key_value[1])
        elif key_value[0] == "vrp_vehicle_variance":
            vrp_params.vrp_vehicle_variance = int(key_value[1])
        elif key_value[0] == "vrp_node_service_time":
            matrix_builder.select_service_times_matrix(vrp_params, name=key_value[1])
        elif key_value[0] == "vrp_distance_time_ratio":
            vrp_params.vrp_distance_time_ratio = int(key_value[1])
        elif key_value[0] == "cvrp_vehicle_capacity":
            vrp_params.cvrp_vehicle_capacity = int(key_value[1])
        elif key_value[0] == "cvrp_node_demand":
            matrix_builder.select_demands_matrix(vrp_params, name=key_value[1])
        elif key_value[0] == "ovrp_enabled":
            vrp_params.ovrp_enabled = bool(key_value[1])
        elif key_value[0] == "vrpp_node_profit":
            matrix_builder.select_profits_matrix(vrp_params, name=key_value[1])
        elif key_value[0] == "vrptw_node_time_window":
            matrix_builder.select_time_windows_matrix(vrp_params, name=key_value[1])
        elif key_value[0] == "vrptw_node_penalty":
            matrix_builder.select_penalties_matrix(vrp_params, name=key_value[1])

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
        elif key_value[0] == "generation_count_min":
            alg_params.generation_count_min = int(key_value[1])
        elif key_value[0] == "generation_count_max":
            alg_params.generation_count_max = int(key_value[1])
        elif key_value[0] == "fitness_evaluator":
            alg_params.fitness_evaluator = int(key_value[1])
        elif key_value[0] == "parent_candidate_count":
            alg_params.parent_candidate_count = int(key_value[1])
        elif key_value[0] == "parent_selection_function":
            alg_params.parent_selection_function = int(key_value[1])
        elif key_value[0] == "selection_probability":
            alg_params.selection_probability = float(key_value[1])
        elif key_value[0] == "offspring_pair_count":
            alg_params.offspring_pair_count = int(key_value[1])
        elif key_value[0] == "crossover_operator":
            alg_params.crossover_operator = int(key_value[1])
        elif key_value[0] == "crossover_probability":
            alg_params.crossover_probability = float(key_value[1])
        elif key_value[0] == "mutation_probability":
            alg_params.mutation_probability = float(key_value[1])
        elif key_value[0] == "followup_probability":
            alg_params.followup_probability = float(key_value[1])
        elif key_value[0] == "elitism_operator":
            alg_params.elitism_operator = int(key_value[1])
        elif key_value[0] == "elitism_frequency":
            alg_params.elitism_frequency = int(key_value[1])
