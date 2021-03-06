#!/usr/bin/env python

"""
genalg.py:

Core of the genetic algorithm.
"""

from copy import deepcopy
from operator import attrgetter
import numpy as np

from instances.vrp import VRP
from algorithms.timer import Timer

import algorithms.plotting.plot_manager as plot_manager
from algorithms.plotting.plot_data import PlotData
import algorithms.modules.population_initializers as population_initializers
import algorithms.modules.validators as validators
import algorithms.modules.evaluators as evaluators
import algorithms.modules.parent_selectors as parent_selectors
import algorithms.modules.crossover_operators as crossover_operators
import algorithms.modules.mutation_operators as mutation_operators
import algorithms.modules.invalidity_correction_functions as invalidity_correction


def run_gen_alg(vrp_params, alg_params):
    """
    Runs the Genetic Algorithm on selected VRP types.

    :param vrp_params: Parameters for the specified VRP.
    :param alg_params: Parameters for the genetic algorithm.
    :return: Computed solution for the specified VRP.
    """
    # GA Initialization, Step 0: Reset ID Counter.
    VRP.id_counter = 0

    # GA Initialization, Step 1: Detecting which extensions are being solved.

    # CVRP: List of customer capacities.
    using_cvrp = vrp_params.cvrp_node_demand is not None

    # OVRP: Toggled (True/False -flag)
    using_ovrp = vrp_params.ovrp_enabled

    # VRPP: List of optional nodes.
    using_vrpp = vrp_params.vrpp_optional_node is not None

    # MDVRP: More than one depot node detected.
    using_mdvrp = len(vrp_params.mdvrp_depot_node) > 1

    # VRPTW: List of customer time windows.
    using_vrptw = vrp_params.vrptw_node_time_window is not None

    # Maximization: Determined via VRPP.
    maximize = using_vrpp

    # Exclude Travel Costs: Toggled (True/False -flag) (Switch between TOP and PTP)
    exclude_travel_costs = vrp_params.vrpp_exclude_travel_costs

    # Optimize Depot Nodes: Toggled (True/False -flag)
    optimize_depot_nodes = vrp_params.mdvrp_optimize_depot_nodes

    # Hard Time Windows: Toggled (True/False -flag)
    using_hard_time_windows = vrp_params.vrptw_hard_windows

    print("Using CVRP:  {}".format(using_cvrp))
    print("Using OVRP:  {}".format(using_ovrp))
    print("Using VRPP:  {}".format(using_vrpp))
    print("Using MDVRP: {}".format(using_mdvrp))
    print("Using VRPTW: {}".format(using_vrptw))
    print("Maximize Objective:   {}".format(maximize))
    print("Exclude Travel Costs: {}".format(exclude_travel_costs))
    print("Optimize Depot Nodes: {}".format(exclude_travel_costs))
    print("Hard Windows:         {}".format(using_hard_time_windows))

    # GA Initialization, Step 2: Selecting a population initialization function.
    population_initialization_collection = {
        0: population_initializers.random,
        1: population_initializers.allele_permutation,
        2: population_initializers.gene_permutation,
        3: population_initializers.simulated_annealing,
        4: population_initializers.nearest_neighbor_population
    }
    VRP.population_initializer = population_initialization_collection[alg_params.population_initializer]

    # GA Initialization, Step 3: Selecting suitable validation functions.
    validation_collection = {
        0: validators.validate_maximum_time,
        1: validators.validate_maximum_distance,
        2: validators.validate_capacity,
        3: validators.validate_time_windows
    }
    validation_functions = []
    if vrp_params.vrp_maximum_route_time is not None:
        validation_functions.append(validation_collection[0])
    if vrp_params.vrp_maximum_route_distance is not None:
        validation_functions.append(validation_collection[1])
    if using_cvrp:
        validation_functions.append(validation_collection[2])
    if using_vrptw and using_hard_time_windows:
        validation_functions.append(validation_collection[3])

    # Add a dummy validation function if none were selected.
    if len(validation_functions) == 0:
        validation_functions.append(lambda target_individual, **kwargs: (True, "No validation functions were used."))
    VRP.validator = validation_functions

    # GA Initialization, Step 4: Selecting an individual evaluation function.
    evaluation_collection = {
        0: evaluators.evaluate_travel_distance,
        1: evaluators.evaluate_travel_time,
        2: evaluators.evaluate_travel_cost,
        3: evaluators.evaluate_profits,
        4: evaluators.evaluate_profit_cost_difference,
        5: evaluators.optimize_depot_nodes
    }
    if using_vrpp and exclude_travel_costs:
        evaluation_function = evaluation_collection[3]
    elif using_vrpp:
        evaluation_function = evaluation_collection[4]
    else:
        evaluation_function = evaluation_collection[2]

    VRP.evaluator = evaluation_function

    # For maximization, a proper comparison function is needed.
    if maximize:
        def compare(vrp1, vrp2): return vrp1.fitness > vrp2.fitness
    else:
        def compare(vrp1, vrp2): return vrp1.fitness < vrp2.fitness

    # GA Initialization, Step 5: Selecting a parent selector function.
    selector_collection = {
        0: parent_selectors.best_fitness,
        1: parent_selectors.roulette_selection,
        2: parent_selectors.tournament_selection
    }
    VRP.parent_selector = selector_collection[alg_params.parent_selection_function]

    # GA Initialization, Step 6: Selecting a crossover operator.
    crossover_collection = {
        0: crossover_operators.one_point,
        1: crossover_operators.two_point,
        2: crossover_operators.order_crossover,
        3: crossover_operators.vehicle_crossover
    }
    VRP.crossover_operator = crossover_collection[alg_params.crossover_operator]

    # GA Initialization, Step 7: Selecting suitable mutation operators.
    mutation_collection = {
        0: mutation_operators.allele_swap,
        1: mutation_operators.sequence_inversion,
        2: mutation_operators.sequence_shuffle,
        3: mutation_operators.sequence_relocation,
        4: mutation_operators.add_optional_node,
        5: mutation_operators.remove_optional_node,
        6: mutation_operators.change_depot
    }
    mutation_functions = [
        mutation_collection[0],
        mutation_collection[1],
        mutation_collection[2],
        mutation_collection[3]
    ]
    
    # Optional node-wise mutation operators.
    if using_vrpp:
        mutation_functions.append(mutation_collection[4])
        mutation_functions.append(mutation_collection[5])
    
    if using_mdvrp and not optimize_depot_nodes:
        # Depot node mutation operator is used only if depot node optimization
        # is disabled.
        mutation_functions.append(mutation_collection[6])
    
    VRP.mutation_operator = mutation_functions
    mutation_function_count = len(mutation_functions)
    
    # GA Initialization, Step 8: Selecting an invalidity correction function.
    invalidity_correction_collection = {
        0: invalidity_correction.random_valid_individual,
        1: invalidity_correction.best_individual,
        2: invalidity_correction.neighbor_of_best_individual,
        3: invalidity_correction.indefinite_mutation,
        4: invalidity_correction.best_individual_and_mutation,
        5: invalidity_correction.retry
    }
    VRP.invalidity_corrector = invalidity_correction_collection[alg_params.invalidity_correction]

    # GA Initialization, Step 9: Create conversion functions between distance, time and cost.
    # Also create functions that conduct the filtration and replacement strategies.
    distance_time_var = max(0, vrp_params.vrp_distance_time_ratio)
    time_cost_var = max(0, vrp_params.vrp_time_cost_ratio)
    distance_cost_var = max(0, vrp_params.vrp_distance_cost_ratio)

    def distance_to_time(distance): return distance * distance_time_var
    def time_to_cost(time): return time * time_cost_var
    def distance_to_cost(distance): return distance * distance_cost_var
    
    # Filtration strategy.
    if alg_params.filtration_frequency <= 0:
        filtration_counter = float("inf")
    else:
        filtration_counter = alg_params.filtration_frequency

    def filtration(population_old, population_new, **kwargs):
        """
        Combines two most recent populations into one, takes the best half of
        individuals and replaces fitness-wise duplicates with completely random
        individuals.

        :param population_old: Population of generation n
        :param population_new: Population of generation n + 1
        :param kwargs: Dictionary of expected parameters:
        - (int) 'node_count': Number of nodes used in the problem. Includes depot nodes and optional nodes.
        - (list<int>) 'depot_nodes': List of depot nodes used in the problem.
        - (list<int>) 'optional_nodes': List of optional nodes used in the problem.
        - (int) 'vehicle_count': Number of vehicles used in the problem.
        - (bool) 'maximize': Flag that determines whether the objective to maximize or minimize.
        - (int) 'minimum_cpu_time': CPU time that is allotted for the initialization of an individual solution.
          The purpose of this is to stop the algorithm if that is unable to create a valid individual
          (or it takes too long).
        :return: Population containing the best of 2 recent populations and
        random individuals if there were duplicates.
        """
        
        fl_node_count = kwargs["node_count"]
        fl_depot_nodes = kwargs["depot_nodes"]
        fl_optional_nodes = kwargs["optional_nodes"]
        fl_vehicle_count = kwargs["vehicle_count"]
        fl_maximize = kwargs["maximize"]
        fl_minimum_cpu_time = kwargs["minimum_cpu_time"]

        def fl_check_goal(timer): return timer.past_goal()

        filtration_timer = Timer()
        filtration_timer.start()
        population_size = len(population_new)
        combined_population = population_old + population_new
        combined_population.sort(key=attrgetter("fitness"), reverse=fl_maximize)
        cut_population = combined_population[:population_size]
            
        # Multiple weak solutions can share the same fitness value.
        # However, with potentially optimal solutions, it is very
        # likely that solutions with the same fitness value
        # are the same. For that reason, it is assumed that solutions
        # that have the same fitness value are the same.
        replacement_indices = []
        previous_fitness = cut_population[0].fitness
        for fl_i in range(1, len(cut_population)):
            if cut_population[fl_i].fitness == previous_fitness:
                replacement_indices.append(fl_i)
            else:
                previous_fitness = cut_population[fl_i].fitness
            
        # Create random individuals to replace duplicates.
        fl_individual_timer = Timer(goal=fl_minimum_cpu_time)
        fl_individual_args = {
            "node_count": fl_node_count,
            "depot_nodes": fl_depot_nodes,
            "optional_nodes": fl_optional_nodes,
            "vehicle_count": fl_vehicle_count,
            "failure_msg": "(Filtration) Individual initialization is taking too long.",
            "individual_timer": fl_individual_timer,
            "check_goal": fl_check_goal,
            "validation_args": validation_args,
            "evaluation_args": evaluation_args
        }
        fl_individual_timer.start()
        for fl_i in range(len(replacement_indices)):
            fl_candidate_individual, error_msg = population_initializers.random_valid_individual(
                **fl_individual_args
            )
            if fl_candidate_individual is None:
                # Filtration strategy has failed due to taking too long in making a valid individual.
                # In such a case, the algorithm will fall back to original new population.
                return population_new, error_msg
            cut_population[replacement_indices[fl_i]] = fl_candidate_individual
            fl_individual_timer.reset()

        # Population has to be sorted again, since there could be random individuals
        # between fitness-wise good individuals.
        cut_population.sort(key=attrgetter("fitness"), reverse=fl_maximize)

        filtration_timer.stop()
        fl_msg = "Filtration operation OK (Time taken: {} ms)".format(filtration_timer.elapsed())
        return cut_population, fl_msg

    # Similar individual replacement strategy.
    if alg_params.replace_similar_individuals <= 0:
        replacement_counter = float("inf")
    else:
        replacement_counter = alg_params.replace_similar_individuals

    def similar_individual_replacement(target_population, **kwargs):
        """
        Looks for fitness-wise duplicates in specified population and replaces
        them with random individuals.

        :param target_population: Population subject to duplicate replacements.
        :param kwargs: Dictionary of expected parameters:
        - (int) 'node_count': Number of nodes used in the problem. Includes depot nodes and optional nodes.
        - (list<int>) 'depot_nodes': List of depot nodes used in the problem.
        - (list<int>) 'optional_nodes': List of optional nodes used in the problem.
        - (int) 'vehicle_count': Number of vehicles used in the problem.
        - (bool) 'maximize': Flag that determines whether the objective to maximize or minimize.
        - (int) 'minimum_cpu_time': CPU time that is allotted for the initialization of an individual solution.
          The purpose of this is to stop the algorithm if that is unable to create a valid individual
          (or it takes too long).
        :return: Population where duplicate individuals have been replaced
        with random individuals.
        """
        
        rp_node_count = kwargs["node_count"]
        rp_depot_nodes = kwargs["depot_nodes"]
        rp_optional_nodes = kwargs["optional_nodes"]
        rp_vehicle_count = kwargs["vehicle_count"]
        rp_maximize = kwargs["maximize"]
        rp_minimum_cpu_time = kwargs["minimum_cpu_time"]

        def rp_check_goal(timer): return timer.past_goal()

        replacement_timer = Timer()
        replacement_timer.start()

        replaced_population = deepcopy(target_population)

        # Multiple weak solutions can share the same fitness value.
        # However, with potentially optimal solutions, it is very
        # likely that solutions with the same fitness value
        # are the same. For that reason, it is assumed that solutions
        # that have the same fitness value are the same.
        replacement_indices = []
        previous_fitness = replaced_population[0].fitness
        for rp_i in range(1, len(replaced_population)):
            if replaced_population[rp_i].fitness == previous_fitness:
                replacement_indices.append(rp_i)
            else:
                previous_fitness = replaced_population[rp_i].fitness

        # Create random individuals to replace duplicates.
        rp_individual_timer = Timer(goal=rp_minimum_cpu_time)
        rp_individual_args = {
            "node_count": rp_node_count,
            "depot_nodes": rp_depot_nodes,
            "optional_nodes": rp_optional_nodes,
            "vehicle_count": rp_vehicle_count,
            "failure_msg": "(Similar Individual Replacement) Individual initialization is taking too long.",
            "individual_timer": rp_individual_timer,
            "check_goal": rp_check_goal,
            "validation_args": validation_args,
            "evaluation_args": evaluation_args
        }
        rp_individual_timer.start()
        for rp_i in range(len(replacement_indices)):
            rp_candidate_individual, error_msg = population_initializers.random_valid_individual(
                **rp_individual_args
            )
            if rp_candidate_individual is None:
                # Replacement operation has failed. Fall back to original population.
                return target_population, error_msg
            replaced_population[replacement_indices[rp_i]] = rp_candidate_individual
            rp_individual_timer.reset()

        # Since similar individuals have been replaced with completely random individuals,
        # the population has to be sorted again.
        replaced_population.sort(key=attrgetter("fitness"), reverse=rp_maximize)

        rp_msg = "Similar Individual Replacement operation OK (Time taken: {} ms)" \
            .format(replacement_timer.elapsed())

        return replaced_population, rp_msg

    # GA Initialization, Step 10: Create (and modify) variables that GA actively uses.
    path_table = deepcopy(vrp_params.vrp_path_table)
    path_table_mapping = deepcopy(vrp_params.vrp_path_table_mapping)
    coordinates = deepcopy(vrp_params.vrp_coordinates)
    node_count = len(path_table)
    vehicle_count = vrp_params.vrp_vehicle_count
    vehicle_capacity = vrp_params.cvrp_vehicle_capacity
    depot_node_list = list(set(vrp_params.mdvrp_depot_node))
    optional_node_list = list(set(vrp_params.vrpp_optional_node)) if vrp_params.vrpp_optional_node is not None else []

    # At least 1 vehicle is required.
    if vehicle_count < 1:
        print("Vehicle count must be at least 1.")
        return

    # In OVRP, vehicles do not return to the depots.
    # This is simulated by reducing all travels distances, where the destination is a depot, to zero.
    if using_ovrp:
        path_table[:, depot_node_list] = 0

    # If path table mapping is provided, the path table will be limited to mapped nodes only
    # and the node count will be modified to account for the mapping.
    if path_table_mapping is not None:

        # Path table mapping values cannot exceed the size of the original path table.
        if max(path_table_mapping) >= len(path_table):
            print("Path table mapping cannot contain integers greater than path table size ({} vs. {})."
                  .format(len(path_table), max(path_table_mapping)))
            return

        # Path table mapping values also cannot be negative.
        if min(path_table_mapping) < 0:
            print("Path table mapping cannot contain negative integers.")
            return

        # Adjust path table according to provided mapping.
        node_count = len(path_table_mapping)
        new_path_table = []
        for i in path_table_mapping:
            new_path_table_row = []
            for j in path_table_mapping:
                new_path_table_row.append(path_table[i, j])
            new_path_table.append(new_path_table_row)
        path_table = np.array(new_path_table)

    # Depot node list cannot contain nodes that go above node count.
    if max(depot_node_list) >= node_count:
        print("Depot node list cannot contain nodes that do not exist ({} vs. {})."
              .format(node_count, max(depot_node_list)))
        return

    # Depot node list also cannot contain negative integers.
    if min(depot_node_list) < 0:
        print("Depot node list cannot contain negative integers.")
        return

    # Optional node list cannot contain nodes that go above node count.
    if len(optional_node_list) > 0:
        if max(optional_node_list) >= node_count:
            print("Optional node list cannot contain nodes that do not exist ({} vs. {})."
                  .format(node_count, max(optional_node_list)))
            return
        # Optional node list also cannot contain negative integers.
        if min(optional_node_list) < 0:
            print("Optional node list cannot contain negative integers.")
            return

    # Set maximum time/distance constraints.
    maximum_time = vrp_params.vrp_maximum_route_time \
        if vrp_params.vrp_maximum_route_time is not None else float("inf")
    maximum_distance = vrp_params.vrp_maximum_route_distance \
        if vrp_params.vrp_maximum_route_distance is not None else float("inf")

    # Set node service times to 0 if they're not provided.
    node_service_time = deepcopy(vrp_params.vrp_node_service_time)
    if node_service_time is None:
        node_service_time = [0] * node_count
    else:
        # Depot nodes do not need servicing.
        for depot_node in depot_node_list:
            node_service_time[depot_node] = 0

    # Set node demands to 0 if they're not provided.
    node_demand_list = deepcopy(vrp_params.cvrp_node_demand)
    if node_demand_list is None:
        node_demand_list = np.array([[0] * node_count]).T
    if len(node_demand_list.shape) == 1:
        node_demand_list = np.array([node_demand_list]).T

    # If vehicle capacity was not specified, default capacities (0) are given.
    if vehicle_capacity is None:
        vehicle_capacity = [0] * node_demand_list.shape[1]

    # Depot nodes do not have supply demands associated with them.
    for depot_node in depot_node_list:
        node_demand_list[depot_node] = 0

    # Set time windows infinitely large if they're not provided.
    time_windows = deepcopy(vrp_params.vrptw_node_time_window)
    if time_windows is None:
        time_windows = [(0, float("inf"))] * node_count

    # Time windows of the depot nodes are the same as maximum time
    # unless it is specified. (Although it is pointless to set a time window
    # that is greater than maximum time: maximum time takes precedence over time windows)

    # Set penalty coefficients to 0 if they're not provided.
    node_penalty_list = deepcopy(vrp_params.vrptw_node_penalty)
    if node_penalty_list is None:
        node_penalty_list = [0] * node_count

    # Set profits to 0 if they're not provided.
    node_profit_list = deepcopy(vrp_params.vrpp_node_profit)
    if node_profit_list is None:
        node_profit_list = [0] * node_count

    # Depot nodes do not have profits associated with them.
    for depot_node in depot_node_list:
        node_profit_list[depot_node] = 0

    population_count = alg_params.population_count
    parent_candidate_count = alg_params.parent_candidate_count
    tournament_probability = alg_params.tournament_probability
    crossover_probability = alg_params.crossover_probability
    mutation_probability = alg_params.mutation_probability
    sa_iteration_count = alg_params.sa_iteration_count
    sa_initial_temperature = alg_params.sa_initial_temperature
    sa_p_coeff = alg_params.sa_p_coeff

    # GA Initialization, Step 11: Create variables relating to termination criteria.
    global_cpu_limit = alg_params.cpu_total_limit
    individual_cpu_limit = alg_params.cpu_individual_limit
    upper_bound = alg_params.fitness_upper_bound
    if upper_bound is None or not using_vrpp:
        upper_bound = float("inf")
    lower_bound = alg_params.fitness_lower_bound
    if lower_bound is None or using_vrpp:
        lower_bound = -float("inf")
    threshold = alg_params.fitness_threshold
    generation_count_min = alg_params.generation_count_min
    generation_count_max = alg_params.generation_count_max

    global_timer = Timer(global_cpu_limit)
    individual_timer = Timer(individual_cpu_limit)
    def check_goal(timer): return timer.past_goal()

    # GA Initialization, Step 12: Prepare keyword arguments for module functions.
    evaluation_args = {
        "path_table": path_table,
        "distance_time_converter": distance_to_time,
        "distance_cost_converter": distance_to_cost,
        "time_cost_converter": time_to_cost,
        "time_window": time_windows,
        "service_time": node_service_time,
        "penalty": node_penalty_list,
        "node_profit": node_profit_list,
        "ovrp": using_ovrp
    }
    validation_args = {
        "path_table": path_table,
        "capacity": vehicle_capacity,
        "demand": node_demand_list,
        "maximum_time": maximum_time,
        "maximum_distance": maximum_distance,
        "time_window": time_windows,
        "service_time": node_service_time,
        "distance_time_converter": distance_to_time,
        "ovrp": using_ovrp
    }
    population_args = {
        "node_count": node_count,
        "depot_nodes": depot_node_list,
        "optional_nodes": optional_node_list,
        "vehicle_count": vehicle_count,
        "population_count": population_count,
        "minimum_cpu_time": individual_cpu_limit,
        "sa_iteration_count": sa_iteration_count,
        "sa_initial_temperature": sa_initial_temperature,
        "sa_p_coeff": sa_p_coeff,
        "maximize": maximize,
        "validation_args": validation_args,
        "evaluation_args": evaluation_args
    }
    individual_args = {
        "node_count": node_count,
        "depot_nodes": depot_node_list,
        "optional_nodes": optional_node_list,
        "vehicle_count": vehicle_count,
        "failure_msg": "(Invalid Individual Replacement) Individual initialization is taking too long.",
        "individual_timer": individual_timer,
        "check_goal": check_goal,
        "validation_args": validation_args,
        "evaluation_args": evaluation_args
    }
    parent_selection_args = {
        "parent_candidate_count": parent_candidate_count,
        "maximize": maximize,
        "tournament_probability": tournament_probability
    }
    filtration_replacement_args = {
        "node_count": node_count,
        "depot_nodes": depot_node_list,
        "optional_nodes": optional_node_list,
        "vehicle_count": vehicle_count,
        "maximize": maximize,
        "minimum_cpu_time": individual_cpu_limit
    }
    # GA Initialization, Step 13: Miscellaneous collection of tests.

    # Capacity test: total capacity potential (vehicle_capacity * vehicle_capacity) is compared
    # to total required capacity (sum of every required node capacity).
    if len(vehicle_capacity) != node_demand_list.shape[1]:
        print("Number of Vehicle Capacity Types does not match with that of Node Demands.")
        return

    required_nodes = [i for i in range(node_count) if i not in optional_node_list and i not in depot_node_list]
    for demand_type in range(node_demand_list.shape[1]):

        # If there are no required nodes, this can be skipped.
        if len(required_nodes) == 0:
            break

        # Start by checking if individual demands are too high by themselves.
        highest_capacity_demand = max(node_demand_list[:, demand_type][required_nodes])
        if highest_capacity_demand > vehicle_capacity[demand_type]:
            print("Capacity requirements are too strict (Individual demand {} exceeds vehicle capacity {})"
                  .format(highest_capacity_demand, vehicle_capacity[demand_type]))
            return

        # Check if total demand is too high.
        capacity_potential = vehicle_capacity[demand_type] * vehicle_count
        required_capacity = 0
        for i in range(len(node_demand_list[:, demand_type])):
            if i not in optional_node_list:
                # Depot nodes do not have supply demands.
                node_capacity = node_demand_list[:, demand_type][i]
                required_capacity += node_capacity
        if required_capacity > capacity_potential:
            print("Capacity requirements are too strict ({} required, {} available)".format(required_capacity,
                                                                                            capacity_potential))
            # This test assumes that every node is a delivery node, while the depot nodes
            # are the pickup nodes, or every node is a pickup node, while the depot nodes
            # are delivery nodes.
            return

    # Valid depot test: optional nodes cannot be depot nodes. This will be checked here.
    offending_list = []
    for depot_node in depot_node_list:
        if depot_node in optional_node_list:
            offending_list.append(depot_node)
    if len(offending_list) > 0:
        print("Optional nodes cannot be depot nodes (Offending nodes: {})".format(offending_list))
        return

    # -----------------------------------------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------
    # ----- Genetic Algorithm starts here -----------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------

    population_history = {}                     # Used in drawing graph 3 / 7.
    population_history_tracker = [0, 1, 2, 3, 4, 5, 10, 15, 20, 25]
    best_generation_individual_history = []     # Used in drawing graph 4 / 7.
    best_time_individual_history = []           # Used in drawing graph 5 / 7.
    best_individual_time_tracker = []           # Used in drawing graph 5 / 7.
    best_overall_individual_history = []        # Used in drawing graph 6 / 7 and graph 7 / 7.
    best_overall_generation_tracker = []        # Used in drawing graph 6 / 7 and graph 7 / 7.

    current_generation = 0
    current_generation_min = 0

    print("Initializing generation 0 population...")
    population, msg = VRP.population_initializer(**population_args)

    # Population initialization can fail due to taking too long in creating a valid individual.
    # If this happens, GA execution is terminated, without results.
    if population is None:
        print(msg)
        print("Returning to menu...")
        return

    population.sort(key=attrgetter("fitness"), reverse=maximize)
    population_history[0] = deepcopy(population)
    initial_population = deepcopy(population)                   # Used in drawing graph 1 / 7.
    best_individual = deepcopy(population[0])
    best_initialized_individual = deepcopy(best_individual)     # Used in drawing graph 2 / 7.
    best_generation_individual_history.append(deepcopy(best_individual))
    best_overall_individual_history.append(deepcopy(best_individual))
    best_overall_generation_tracker.append(current_generation)
    print(msg)
    
    invalidity_correction_args = {
        "best_individual": best_individual,
        "individual_args": individual_args
    }

    timeout = False
    global_timer.start()

    # ------------------------------------------------------------------------------------------------------------------
    # - The Beginning of the Main Loop of the Genetic Algorithm. -------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    
    while not timeout \
            and lower_bound + threshold <= best_individual.fitness <= upper_bound - threshold \
            and current_generation < generation_count_max \
            and current_generation_min < generation_count_min:

        new_population = []
        while len(new_population) < population_count and not timeout:
            # Two new individuals are created for the new population in each loop.
            
            # Select two parents from current generation.
            parent1, parent2 = VRP.parent_selector(population, **parent_selection_args)

            # Perform crossover operation.
            crossover_check = np.random.random()
            if crossover_probability >= crossover_check:
                offspring1, offspring2 = VRP.crossover_operator(parent1, parent2)
            else:
                offspring1, offspring2 = deepcopy(parent1), deepcopy(parent2)

            offspring1.assign_id()
            offspring2.assign_id()

            # Perform mutation operation.
            mutation_check1, mutation_check2 = np.random.random(), np.random.random()
            if mutation_probability >= mutation_check1:
                mutation_selector = np.random.randint(0, mutation_function_count)
                VRP.mutation_operator[mutation_selector](offspring1)
            if mutation_probability >= mutation_check2:
                mutation_selector = np.random.randint(0, mutation_function_count)
                VRP.mutation_operator[mutation_selector](offspring2)

            # Optimize Depot Nodes if it has been requested.
            if using_mdvrp and optimize_depot_nodes:
                evaluation_collection[5](offspring1, path_table=path_table)
                evaluation_collection[5](offspring2, path_table=path_table)

            # Now that the offspring have been created, they must be validated
            # and evaluated before they are added to the population.
            add_offspring1 = True
            for validator in VRP.validator:
                offspring1.valid, validation_msg = validator(offspring1, **validation_args)
                if offspring1.valid is False:
                    add_offspring1 = False
                    # New individual is invalid. It is now subject to a correction operation.
                    individual_timer.start()
                    replacement, msg = VRP.invalidity_corrector(offspring1, **invalidity_correction_args)
                    individual_timer.stop()
                    if replacement is None:
                        if msg == "RETRY":
                            # Ignore invalidity correction process.
                            break
                        else:
                            # Minimum CPU Time Termination Criterion has been violated.
                            # GA will be concluded here, without results.
                            print(msg)
                            timeout = True
                    else:
                        # Replacement individual is valid. Evaluate and add to population.
                        replacement.fitness = VRP.evaluator(replacement, **evaluation_args)
                        new_population.append(replacement)
            
            # If offspring was found valid, it is added to the population here.
            if add_offspring1 and offspring1.valid:
                offspring1.fitness = VRP.evaluator(offspring1, **evaluation_args)
                new_population.append(offspring1)

            add_offspring2 = True
            for validator in VRP.validator:
                offspring2.valid, validation_msg = validator(offspring2, **validation_args)
                if offspring2.valid is False:
                    add_offspring2 = False
                    # New individual is deemed invalid. It is now subject to a correction operation.
                    individual_timer.start()
                    replacement, msg = VRP.invalidity_corrector(offspring2, **invalidity_correction_args)
                    individual_timer.stop()
                    if replacement is None:
                        if msg == "RETRY":
                            # Ignore invalidity correction process.
                            break
                        else:
                            # Minimum CPU Time Termination Criterion has been violated.
                            # GA will be concluded here, without results.
                            print(msg)
                            timeout = True
                    else:
                        # Replacement individual is valid. Evaluate and add to population.
                        replacement.fitness = VRP.evaluator(replacement, **evaluation_args)
                        new_population.append(replacement)
            
            # If offspring was found valid, it is added to the population here.
            if add_offspring2 and offspring2.valid:
                offspring2.fitness = VRP.evaluator(offspring2, **evaluation_args)
                new_population.append(offspring2)
            
            timeout = global_timer.past_goal()
            
            # - End of population loop -

        # If population count is set to an uneven number, chances are that
        # only one individual has to be removed.
        if len(new_population) > population_count:
            del new_population[np.random.randint(0, len(new_population))]

        # Check if GA termination has been requested.
        if timeout:
            break

        new_population.sort(key=attrgetter("fitness"), reverse=maximize)
        candidate_individual = new_population[0]

        # Filtration/Replacement Check.
        if current_generation % filtration_counter == 0:
            # Filtration Strategy: combine the two recent populations into one,
            # and throw away the worst individuals and replace duplicates with
            # random individuals, until population count matches.
            population, filtration_msg = filtration(population, new_population, **filtration_replacement_args)
        elif current_generation % replacement_counter == 0:
            # Similar Individual Replacement Strategy: check most recent population for
            # duplicates and replace them with completely random individuals.
            # Filtration Strategy does this as well, which is why the conjunction
            # of the two conditions is not separately checked.
            population, replacement_msg = similar_individual_replacement(new_population, **filtration_replacement_args)
        else:
            # No Filtration/Replacement performed: new population becomes current population.
            population = new_population

        # Check if next generation's best individual is the best overall.
        if compare(candidate_individual, best_individual):
            # New best individual takes over as the potential optimal solution.
            best_individual = deepcopy(candidate_individual)
            invalidity_correction_args["best_individual"] = best_individual

            # Add said individual into a separate list so that it could be plotted
            # later.
            best_overall_individual_history.append(deepcopy(candidate_individual))
            best_overall_generation_tracker.append(current_generation)

            # Since new best individual was discovered, minimum generation count
            # is now reset.
            current_generation_min = -1

        # Data collection for plotting purposes.
        if current_generation + 1 in population_history_tracker:
            population_history[current_generation + 1] = deepcopy(population)
        best_generation_individual_history.append(deepcopy(candidate_individual))
        best_time_individual_history.append(deepcopy(best_individual))
        best_individual_time_tracker.append(global_timer.elapsed())

        current_generation += 1
        current_generation_min += 1

        print("Generation {:> 5} / {:> 5} (Min: {:> 5} / {:> 5}) | "
              "Best Fitness (Generation / Overall): {:0.0f} / {:0.0f}"
              .format(
                current_generation,
                generation_count_max,
                current_generation_min,
                generation_count_min,
                candidate_individual.fitness,
                best_individual.fitness))

    # ------------------------------------------------------------------------------------------------------------------
    # - The End of the Main Loop of the Genetic Algorithm. -------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------

    global_timer.stop()
    population_history[current_generation] = deepcopy(population)

    print("Algorithm has finished. (Time taken: {} ms)".format(global_timer.elapsed()))
    print("Discovered an individual with the following details:")
    best_individual.print()

    print("Preparing data for drawing plots...")

    # ------------------------------------------------------------------------------------------------------------------
    # - Plot Drawing starts here. --------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------

    PlotData.select_unused_folder_name()

    plot_function_list = []
    plot_data_list = []

    # Graph 1 / 7
    # Line Graph that illustrates diversity of population created using a population initializer.
    details1 = {
        "population_initializer": alg_params.str_population_initializer[alg_params.population_initializer],
        "sa_iteration_count": sa_iteration_count,
        "sa_initial_temperature": sa_initial_temperature,
        "sa_p_coeff": sa_p_coeff
    }
    plot_function1, plot_data1 = plot_manager.plot_population_initializer(
        initial_population,
        details1
    )
    plot_function_list, plot_data_list = plot_function_list + plot_function1, plot_data_list + plot_data1

    # Graph 2 / 7
    # Scatter Graph (Map) that illustrates the solution of the best individual created by the population initializer.
    # This is drawn only if node coordinates are available, and if path table mapping is not used.
    if coordinates is not None and path_table_mapping is None:
        details2 = {
            "population_initializer": alg_params.str_population_initializer[alg_params.population_initializer],
            "population_count": population_count,
            "coordinates": coordinates,
            "open_routes": using_ovrp,
            "sa_iteration_count": sa_iteration_count,
            "sa_initial_temperature": sa_initial_temperature,
            "sa_p_coeff": sa_p_coeff
        }
        plot_function2, plot_data2 = plot_manager.plot_best_individual_initial_solution(
            best_initialized_individual,
            details2
        )
        plot_function_list, plot_data_list = plot_function_list + plot_function2, plot_data_list + plot_data2

    # Graph 3 / 7
    # Line Graph that illustrates the development of the population. Fitness values of every individual over
    # multiple generations are presented.
    details3 = {
        "population_count": population_count,
        "parent_selector": alg_params.str_parent_selection_function[alg_params.parent_selection_function],
        "crossover_operator": alg_params.str_crossover_operator[alg_params.crossover_operator],
        "tournament_probability": tournament_probability,
        "crossover_probability": crossover_probability,
        "mutation_probability": mutation_probability
    }
    plot_function3, plot_data3 = plot_manager.plot_population_development(
        population_history,
        details3
    )
    plot_function_list, plot_data_list = plot_function_list + plot_function3, plot_data_list + plot_data3

    # Graph 4 / 7
    # Line Graph that illustrates fitness development of the competing individuals of their generations.
    details4 = {
        "population_count": population_count,
        "parent_selector": alg_params.str_parent_selection_function[alg_params.parent_selection_function],
        "crossover_operator": alg_params.str_crossover_operator[alg_params.crossover_operator],
        "tournament_probability": tournament_probability,
        "crossover_probability": crossover_probability,
        "mutation_probability": mutation_probability
    }
    plot_function4, plot_data4 = plot_manager.plot_best_individual_fitness(
        best_generation_individual_history,
        details4
    )
    plot_function_list, plot_data_list = plot_function_list + plot_function4, plot_data_list + plot_data4

    # Graph 5 / 7
    # Line Graph that illustrates fitness development of the competing individuals with respect to time.
    details5 = {
        "population_count": population_count,
        "parent_selector": alg_params.str_parent_selection_function[alg_params.parent_selection_function],
        "crossover_operator": alg_params.str_crossover_operator[alg_params.crossover_operator],
        "tournament_probability": tournament_probability,
        "crossover_probability": crossover_probability,
        "mutation_probability": mutation_probability
    }
    plot_function5, plot_data5 = plot_manager.plot_best_individual_fitness_time(
        best_time_individual_history,
        best_individual_time_tracker,
        details5
    )
    plot_function_list, plot_data_list = plot_function_list + plot_function5, plot_data_list + plot_data5

    # Graph 6 / 7
    # Bar Graph that illustrates the development of the best individual in terms of its fitness.
    details6 = {
        "bar_count": 50 if len(best_overall_individual_history) > 50 else len(best_overall_individual_history),
        "population_count": population_count,
        "parent_selector": alg_params.str_parent_selection_function[alg_params.parent_selection_function],
        "crossover_operator": alg_params.str_crossover_operator[alg_params.crossover_operator],
        "tournament_probability": tournament_probability,
        "crossover_probability": crossover_probability,
        "mutation_probability": mutation_probability
    }
    plot_function6, plot_data6 = plot_manager.plot_best_individual_collection(
        best_overall_individual_history,
        best_overall_generation_tracker,
        details6
    )
    plot_function_list, plot_data_list = plot_function_list + plot_function6, plot_data_list + plot_data6

    # Graph 7 / 7
    # Collection of Scatter Graphs that illustrate the development of the solution of the best individual.
    # This is drawn only if node coordinates are available, and if path table mapping is not used.
    if coordinates is not None and path_table_mapping is None:
        details7 = {
            "max_plot_count": 10,
            "coordinates": coordinates,
            "open_routes": using_ovrp,
            "population_count": population_count,
            "parent_selector": alg_params.str_parent_selection_function[alg_params.parent_selection_function],
            "crossover_operator": alg_params.str_crossover_operator[alg_params.crossover_operator],
            "tournament_probability": tournament_probability,
            "crossover_probability": crossover_probability,
            "mutation_probability": mutation_probability
        }
        plot_function7, plot_data7 = plot_manager.plot_best_individual_solution(
            best_overall_individual_history,
            best_overall_generation_tracker,
            details7
        )
        plot_function_list, plot_data_list = plot_function_list + plot_function7, plot_data_list + plot_data7

    plot_manager.set_total_plot_count(plot_data_list)

    print("Drawing plots...")
    print("(Once a window appears, closing it resumes execution.)")

    plot_manager.summon_window(plot_function_list, plot_data_list)

    print("Returning to menu...")
