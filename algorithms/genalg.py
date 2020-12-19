#!/usr/bin/env python

"""
genalg.py:

Runner of the genetic algorithm.
"""

from instances.params import ParamsVRP, ParamsGENALG
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

    # GA Initialization, Step 9: Create variables relating to termination criteria.
    global_timer = Timer(alg_params.cpu_total_limit)
    individual_timer = Timer(alg_params.cpu_individual_limit)
    upper_bound = alg_params.fitness_upper_bound
    lower_bound = alg_params.fitness_lower_bound
    threshold = alg_params.fitness_threshold
    generation_count_min = alg_params.generation_count_min
    generation_count_max = alg_params.generation_count_max

    # -----------------------------------------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------
    # ----- Genetic Algorithm starts here -----------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------
    # -----------------------------------------------------------------------------------------------------------------

    # TODO: Test module functions.

    print("TODO")
