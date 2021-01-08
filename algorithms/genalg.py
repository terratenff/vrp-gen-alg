#!/usr/bin/env python

"""
genalg.py:

Runner of the genetic algorithm.
"""

from copy import deepcopy
from operator import attrgetter
from threading import Thread, current_thread
from time import sleep
import numpy as np

from instances.vrp import VRP
from algorithms.timer import Timer

import algorithms.plotting.plot_manager as plot_manager
import algorithms.modules.population_initializers as population_initializers
import algorithms.modules.validators as validators
import algorithms.modules.evaluators as evaluators
import algorithms.modules.parent_selectors as parent_selectors
import algorithms.modules.crossover_operators as crossover_operators
import algorithms.modules.mutation_operators as mutation_operators


def run_gen_alg(vrp_params, alg_params):
    """
    Conducts the Genetic Algorithm on selected VRP type.

    :param vrp_params: Parameters for the VRP.
    :param alg_params: Parameters for the genetic algorithm.
    :return: Computed solution for the VRP.
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

    # Exclude Travel Costs: Toggled (True/False -flag)
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
    print("Travel Costs:         {}".format(exclude_travel_costs))
    print("Optimize Depot Nodes: {}".format(exclude_travel_costs))
    print("Hard Windows:         {}".format(using_hard_time_windows))

    # GA Initialization, Step 2: Selecting a population initialization function.
    population_initialization_collection = {
        0: population_initializers.random,
        1: population_initializers.allele_permutation,
        2: population_initializers.gene_permutation,
        3: population_initializers.simulated_annealing
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

    if len(validation_functions) == 0:
        validation_functions.append(lambda target_individual, **kwargs: (True, "No validation functions were used."))
    VRP.validator = validation_functions

    # GA Initialization, Step 4: Selecting suitable individual evaluation function.
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

    # GA Initialization, Step 5: Selecting suitable parent selector function.
    selector_collection = {
        0: parent_selectors.best_fitness,
        1: parent_selectors.roulette_selection,
        2: parent_selectors.tournament_selection
    }
    VRP.parent_selector = selector_collection[alg_params.parent_selection_function]

    # GA Initialization, Step 6: Selecting suitable crossover operator.
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
        4: mutation_operators.vehicle_diversification,
        5: mutation_operators.add_optional_node,
        6: mutation_operators.remove_optional_node,
        7: mutation_operators.change_depot
    }
    mutation_functions = [
        mutation_collection[0],
        mutation_collection[1],
        mutation_collection[2],
        mutation_collection[3],
        mutation_collection[4]
    ]
    if using_vrpp:
        mutation_functions.append(mutation_collection[5])
        mutation_functions.append(mutation_collection[6])
    if using_mdvrp and not optimize_depot_nodes:
        mutation_functions.append(mutation_collection[7])
    VRP.mutation_operator = mutation_functions
    mutation_function_count = len(mutation_functions)

    # GA Initialization, Step 8: Create conversion functions between distance, time and cost.
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
                # In such a case, the population is set to remain untouched.
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
                # Replacement operation has failed. Fall back to the original population.
                return target_population, error_msg
            replaced_population[replacement_indices[rp_i]] = rp_candidate_individual
            rp_individual_timer.reset()

        # Since similar individuals have been replaced with completely random individuals,
        # the population has to be sorted again.
        replaced_population.sort(key=attrgetter("fitness"), reverse=rp_maximize)

        rp_msg = "Similar Individual Replacement operation OK (Time taken: {} ms)" \
            .format(replacement_timer.elapsed())

        return replaced_population, rp_msg

    # GA Initialization, Step 9: Create (and modify) variables that GA actively uses.
    # - Deep-copied variables are potentially subject to modifications.
    path_table = deepcopy(vrp_params.vrp_path_table)
    coordinates = deepcopy(vrp_params.vrp_coordinates)
    node_count = len(path_table)
    vehicle_count = vrp_params.vrp_vehicle_count
    vehicle_capacity = vrp_params.cvrp_vehicle_capacity
    depot_node_list = vrp_params.mdvrp_depot_node
    optional_node_list = vrp_params.vrpp_optional_node if vrp_params.vrpp_optional_node is not None else []

    # In OVRP, vehicles do not return to the depots.
    # This is simulated by reducing all travels distances, where the destination is a depot, to zero.
    if using_ovrp:
        path_table[:, depot_node_list] = 0

    maximum_time = vrp_params.vrp_maximum_route_time \
        if vrp_params.vrp_maximum_route_time is not None else -1
    maximum_distance = vrp_params.vrp_maximum_route_distance \
        if vrp_params.vrp_maximum_route_distance is not None else -1

    node_service_time = deepcopy(vrp_params.vrp_node_service_time)
    if node_service_time is None:
        node_service_time = [0] * node_count

    node_demand_list = deepcopy(vrp_params.cvrp_node_demand)
    if node_demand_list is None:
        node_demand_list = [0] * node_count

    # Depot nodes do not have supply demands associated with them.
    for depot_node in depot_node_list:
        node_demand_list[depot_node] = 0

    time_windows = deepcopy(vrp_params.vrptw_node_time_window)
    if time_windows is None:
        time_windows = [(0, float("inf"))] * node_count

    # Time windows of the depot nodes are the same as maximum time
    # unless it is specified. (Although it is pointless to set a time window
    # that is greater than maximum time: maximum time takes precedence over time windows)

    node_penalty_list = deepcopy(vrp_params.vrptw_node_penalty)
    if node_penalty_list is None:
        node_penalty_list = [0] * node_count

    # Depot nodes can have penalty coefficients.

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

    # GA Initialization, Step 10: Create variables relating to termination criteria.
    global_cpu_limit = alg_params.cpu_total_limit
    individual_cpu_limit = alg_params.cpu_individual_limit
    upper_bound = alg_params.fitness_upper_bound
    if upper_bound is None:
        upper_bound = float("inf")
    lower_bound = alg_params.fitness_lower_bound
    if lower_bound is None:
        lower_bound = -float("inf")
    threshold = alg_params.fitness_threshold
    generation_count_min = alg_params.generation_count_min
    generation_count_max = alg_params.generation_count_max

    global_timer = Timer(global_cpu_limit)
    individual_timer = Timer(individual_cpu_limit)
    def check_goal(timer): return timer.past_goal()

    # GA Initialization, Step 11: Prepare keyword arguments for module functions.
    evaluation_args = {
        "path_table": path_table,
        "distance_time_converter": distance_to_time,
        "distance_cost_converter": distance_to_cost,
        "time_cost_converter": time_to_cost,
        "time_window": time_windows,
        "service_time": node_service_time,
        "penalty": node_penalty_list,
        "node_profit": node_profit_list
    }
    validation_args = {
        "path_table": path_table,
        "capacity": vehicle_capacity,
        "demand": node_demand_list,
        "maximum_time": maximum_time,
        "maximum_distance": maximum_distance,
        "time_window": time_windows,
        "service_time": node_service_time,
        "distance_time_converter": distance_to_time
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
    # GA Initialization, Step 12: Miscellaneous collection of tests.

    # Capacity test: total capacity potential (vehicle_capacity * vehicle_capacity) is compared
    # to total required capacity (sum of every required node capacity).
    capacity_potential = vehicle_capacity * vehicle_count
    required_capacity = 0
    for i in range(len(node_demand_list)):
        if i not in optional_node_list:
            # Depot nodes do not have supply demands.
            node_capacity = node_demand_list[i]
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

    population_history = []                     # Used in drawing graph 3 / 7.
    best_generation_individual_history = []     # Used in drawing graph 4 / 7.
    best_time_individual_history = []           # Used in drawing graph 5 / 7.
    best_individual_time_tracker = []           # Used in drawing graph 5 / 7.
    best_overall_individual_history = []        # Used in drawing graph 6 / 7 and graph 7 / 7.
    best_overall_generation_tracker = []        # Used in drawing graph 6 / 7 and graph 7 / 7.

    current_generation = 0
    current_generation_min = 0

    population, msg = VRP.population_initializer(**population_args)

    # Population initialization can fail due to taking too long in creating a valid individual.
    # If this happens, GA execution is terminated, without results.
    if population is None:
        print(msg)
        print("Returning to menu...")
        return

    population.sort(key=attrgetter("fitness"), reverse=maximize)
    population_history.append(deepcopy(population))
    initial_population = deepcopy(population)                   # Used in drawing graph 1 / 6.
    best_individual = deepcopy(population[0])
    best_initialized_individual = deepcopy(best_individual)     # Used in drawing graph 2 / 6.
    best_generation_individual_history.append(deepcopy(best_individual))
    best_overall_individual_history.append(deepcopy(best_individual))
    best_overall_generation_tracker.append(current_generation)
    print(msg)

    # for individual in population:
    #     print("{:> 4} | {:> 5} | {}".format(individual.individual_id, individual.fitness, individual.solution))

    timeout = False
    global_timer.start()

    # Start a thread that collects an instance of the best individual for each interval passed.
    def timed_collection():
        interval = 0.10  # Seconds.
        thread = current_thread()
        setattr(thread, "terminate", False)
        while not getattr(thread, "terminate", False):
            best_time_individual_history.append(deepcopy(best_individual))
            best_individual_time_tracker.append(global_timer.elapsed())
            sleep(interval)

    timed_collector = Thread(target=timed_collection)
    timed_collector.start()

    # ------------------------------------------------------------------------------------------------------------------
    # - The Beginning of the Main Loop of the Genetic Algorithm. -------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------

    while not timeout \
            and lower_bound + threshold <= best_individual.fitness <= upper_bound - threshold \
            and current_generation <= generation_count_max \
            and current_generation_min <= generation_count_min:

        print("Generation {:> 5} / {:> 5} (Min: {:> 5} / {:> 5}) | Best Fitness: {}".format(
            current_generation,
            generation_count_max,
            current_generation_min,
            generation_count_min,
            best_individual.fitness
        ))  # Test print.

        new_population = []
        while len(new_population) < population_count and not timeout:
            # Two new individuals are created for the new population in each loop.
            # 1. Select two parents from current generation.
            parent1, parent2 = VRP.parent_selector(population, **parent_selection_args)

            # 2. Perform crossover operation.
            crossover_check = np.random.random()
            if crossover_probability >= crossover_check:
                offspring1, offspring2 = VRP.crossover_operator(parent1, parent2)
            else:
                offspring1, offspring2 = deepcopy(parent1), deepcopy(parent2)

            offspring1.assign_id()
            offspring2.assign_id()

            # 3. Perform mutation operation.
            mutation_check1, mutation_check2 = np.random.random(), np.random.random()
            if mutation_probability >= mutation_check1:
                mutation_selector = np.random.randint(0, mutation_function_count)
                VRP.mutation_operator[mutation_selector](offspring1)
            if mutation_probability >= mutation_check2:
                mutation_selector = np.random.randint(0, mutation_function_count)
                VRP.mutation_operator[mutation_selector](offspring2)

            new_population.append(offspring1)
            new_population.append(offspring2)
            timeout = global_timer.past_goal()

        # If population count is set to an uneven number, chances are one individual
        # has to be removed.
        if len(new_population) > population_count:
            del new_population[np.random.randint(0, len(new_population))]

        # With the new population now created, its individuals now have to be
        # both validated and evaluated.
        for i in range(len(new_population)):
            for validator in VRP.validator:
                new_population[i].valid, validation_msg = validator(new_population[i], **validation_args)
                if new_population[i].valid is False:
                    # New individual is deemed invalid. It is now subject to a replacement
                    # with a completely random, but valid, individual.
                    individual_timer.start()
                    replacement, msg = population_initializers.random_valid_individual(**individual_args)
                    individual_timer.stop()
                    if replacement is None:
                        # Minimum CPU Time Termination Criterion has been violated.
                        # GA will be concluded here, with partial results.
                        print(msg)
                        timeout = True
                    else:
                        new_population[i] = replacement

            # A valid individual is then evaluated.
            new_population[i].fitness = VRP.evaluator(new_population[i], **evaluation_args)

            if timeout:
                break

        # If GA termination is requested in the middle of creating
        # a new population, the population in question is ignored.
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

        # Data collection for plotting purposes.
        population_history.append(deepcopy(population))
        best_generation_individual_history.append(deepcopy(candidate_individual))

        # Check if next generation's best individual is the best overall.
        if compare(candidate_individual, best_individual):
            # New best individual takes over as the potential optimal solution.
            best_individual = deepcopy(candidate_individual)

            # Add said individual into a separate list so that it could be plotted
            # later.
            best_overall_individual_history.append(deepcopy(candidate_individual))
            best_overall_generation_tracker.append(current_generation)

            # Since new best individual was discovered, minimum generation count
            # is now reset.
            current_generation_min = -1

        current_generation += 1
        current_generation_min += 1

    # ------------------------------------------------------------------------------------------------------------------
    # - The End of the Main Loop of the Genetic Algorithm. -------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------

    global_timer.stop()
    timed_collector.terminate = True
    if timeout:
        print("Algorithm has finished incomplete. (Time taken: {} ms)".format(global_timer.elapsed()))
    else:
        print("Algorithm has finished. (Time taken: {} ms)".format(global_timer.elapsed()))

    print("Discovered an individual with the following details:")
    best_individual.print()

    print("Preparing data for drawing plots...")

    # ------------------------------------------------------------------------------------------------------------------
    # - Plot Drawing starts here. --------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------

    plot_function_list = []
    plot_data_list = []

    # Graph 1 / 7
    # Bar Graph that illustrates diversity of population created using a population initializer.
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
    # Scatter Graph that illustrates the solution of the best individual created by the population initializer.
    # This is drawn only if node coordinates are available.
    if coordinates is not None:
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
    line_count, line_increment = 7, 5
    details3 = {
        "line_count": line_count if current_generation > line_count else current_generation,
        "line_increment": line_increment if current_generation > line_count * line_increment else 1,
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
    # Collection Scatter Graph that illustrate the development of the solution of the best individual.
    # This is drawn only if node coordinates are available.
    if coordinates is not None:
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
