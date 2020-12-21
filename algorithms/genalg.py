#!/usr/bin/env python

"""
genalg.py:

Runner of the genetic algorithm.
"""

from copy import deepcopy
from operator import attrgetter

from instances.vrp import VRP
from algorithms.timer import Timer
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
    maximization = using_vrpp

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
    print("Maximize Objective:   {}".format(maximization))
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
    if using_vrpp:
        mutation_functions.append(mutation_collection[4])
        mutation_functions.append(mutation_collection[5])
    if using_mdvrp and not optimize_depot_nodes:
        mutation_functions.append(mutation_collection[6])
    VRP.mutation_operator = mutation_functions

    # GA Initialization, Step 8: Create conversion functions between distance, time and cost.
    # Also create a function that conducts the filtration strategy.
    distance_time_var = vrp_params.vrp_distance_time_ratio
    time_cost_var = vrp_params.vrp_time_cost_ratio
    distance_cost_var = vrp_params.vrp_distance_cost_ratio
    if distance_time_var > 0:
        def distance_to_time(distance):
            return distance / distance_time_var
    else:
        def distance_to_time(distance):
            return distance * distance_time_var * (-1)

    if time_cost_var > 0:
        def time_to_cost(time):
            return time / time_cost_var
    else:
        def time_to_cost(time):
            return time * time_cost_var * (-1)

    if distance_cost_var > 0:
        def distance_to_cost(distance):
            return distance / distance_cost_var
    else:
        def distance_to_cost(distance):
            return distance * distance_cost_var * (-1)
    
    # Filtration strategy.
    if alg_params.filtration_frequency <= 0:
        filtration_counter = float("inf")
        def filtration(population_old, population_new, **kwargs):
            return population_new, "Filtration operation skipped."
    else:
        filtration_counter = alg_params.filtration_frequency
        def filtration(population_old, population_new, **kwargs):
            node_count = kwargs["node_count"]
            depot_nodes = kwargs["depot_nodes"]
            optional_nodes = kwargs["optional_nodes"]
            vehicle_count = kwargs["vehicle_count"]
            maximize = kwargs["maximize"]
            minimum_cpu_time = kwargs["minimum_cpu_time"]
            
            # If minimum CPU time is set to None, it is to be ignored.
            if minimum_cpu_time is None:
                def check_goal(timer): return False
            else:
                def check_goal(timer): return timer.past_goal()
            
            filtration_timer = Timer()
            filtration_timer.start()
            population_size = len(population_new)
            combined_population = population_old + population_new
            combined_population.sort(key=attrgetter("fitness"), reverse=maximize)
            cut_population = combined_population[:population_size]
            
            # Multiple weak solutions can share the same fitness value.
            # However, with potentially optimal solutions, it is very
            # likely that solutions with the same fitness value
            # are the same. For that reason, it is assumed that solutions
            # that have the same fitness value are the same.
            replacement_indices = []
            previous_fitness = cut_population[0].fitness 
            for i in range(1, cut_population):
                if cut_population[i].fitness == previous_fitness:
                    replacement_indices.append(i)
                else:
                    previous_fitness = cut_population[i].fitness
            
            # Create random individuals to replace duplicates.
            individual_timer = Timer(goal=minimum_cpu_time)
            for i in range(len(replacement_indices)):
                individual_timer.start()
                
                valid_individual = False
                candidate_individual = None
                while valid_individual is False:

                    candidate_solution = population_initializers.random_solution(
                        node_count=node_count,
                        depot_nodes=depot_nodes,
                        optional_nodes=optional_nodes,
                        vehicle_count=vehicle_count
                    )

                    candidate_individual = VRP(node_count, vehicle_count, depot_nodes, optional_nodes)
                    candidate_individual.assign_solution(candidate_solution)
                    for validator in VRP.validator:
                        valid_individual, validation_msg = validator(candidate_individual, **validation_args)
                        if valid_individual is False:
                            break

                    candidate_individual.valid = valid_individual
                    if check_goal(individual_timer):
                        return cut_population, "(Filtration) Individual initialization is taking too long."

                candidate_individual.fitness = VRP.evaluator(candidate_individual, **evaluation_args)
                cut_population[replacement_indices[i]] = candidate_individual
                individual_timer.reset()
            
            filtration_timer.stop()
            msg = "Replacement operation OK (Time taken: {} ms)".format(filtration_timer.elapsed())
            return cut_population, msg

    # GA Initialization, Step 9: Create (and modify) variables that GA actively uses.
    # - Deep-copied variables are potentially subject to modifications.
    path_table = deepcopy(vrp_params.vrp_path_table)
    node_count = len(path_table)
    vehicle_count = vrp_params.vrp_vehicle_count
    vehicle_capacity = vrp_params.cvrp_vehicle_capacity
    depot_node_list = vrp_params.mdvrp_depot_node
    optional_node_list = vrp_params.vrpp_optional_node if vrp_params.vrpp_optional_node is not None else []

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
    time_windows = deepcopy(vrp_params.vrptw_node_time_window)
    if time_windows is None:
        time_windows = [(0, float("inf"))] * node_count
    node_penalty_list = deepcopy(vrp_params.vrptw_node_penalty)
    if node_penalty_list is None:
        node_penalty_list = [0] * node_count
    node_profit_list = deepcopy(vrp_params.vrpp_node_profit)
    if node_profit_list is None:
        node_profit_list = [0] * node_count

    population_count = alg_params.population_count
    parent_candidate_count = alg_params.parent_candidate_count
    tournament_probability = alg_params.tournament_probability
    crossover_probability = alg_params.crossover_probability
    mutation_probability = alg_params.mutation_probability
    filtration_frequency = alg_params.filtration_frequency
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
        "maximize": maximization,
        "validation_args": validation_args,
        "evaluation_args": evaluation_args
    }
    parent_selection_args = {
        "parent_candidate_count": parent_candidate_count,
        "maximize": maximization,
        "tournament_probability": tournament_probability
    }

    # -----------------------------------------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------
    # ----- Genetic Algorithm starts here -----------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------

    current_generation = 1

    # TODO: Test module functions.

    population, msg = VRP.population_initializer(**population_args)
    # population.sort(key=attrgetter("fitness"))
    print(msg)
    for individual in population:
        print("{:> 4} | {:> 5} | {}".format(individual.individual_id, individual.fitness, individual.solution))

    print("TODO")
