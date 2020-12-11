#!/usr/bin/env python

"""
population_initializers.py:

Collection of functions that are used to initialize a population for the Genetic Algorithm.
"""

from random import randint, sample, shuffle, random as random_float
from itertools import permutations
from math import factorial, exp, floor
from copy import deepcopy
from operator import attrgetter
from algorithms.timer import Timer
from instances.vrp import VRP


def random_solution(**kwargs):
    """
    Generates a random solution to the VRP, although it should be
    noted that its validity is not determined here.

    :param kwargs: Dictionary of expected parameters:
    - (int) 'node_count': Number of nodes used in the problem. Includes depot nodes and optional nodes.
    - (list<int>) 'depot_nodes': List of depot nodes used in the problem.
    - (list<int>) 'optional_nodes': List of optional nodes used in the problem.
    - (int) 'vehicle_count': Number of vehicles used in the problem.

    :return: List representation of a random solution to the problem,
    waiting to be assigned to a population individual.
    """

    # Generating a random solution, step 0: Required Variables
    nodes = list(range(kwargs["node_count"]))
    depot_nodes = kwargs["depot_nodes"]
    optional_nodes = kwargs["optional_nodes"]
    vehicle_count = kwargs["vehicle_count"]
    solution = []

    # Generating a random solution, step 1: Depot Nodes
    selected_depots = [
        depot_nodes[randint(0, len(depot_nodes) - 1)]
        for i in range(vehicle_count)
        ]

    solution = solution + selected_depots

    # Generating a random solution, step 2: Required Nodes
    required_nodes = [i for i in nodes if
                      i not in depot_nodes and
                      i not in optional_nodes]

    solution = solution + required_nodes

    # Generating a random solution, step 3: Optional Nodes
    list_size = max(0, floor((len(optional_nodes) / 2) - (len(required_nodes) / 4)))
    add_list = sample(optional_nodes, list_size)
    solution = solution + add_list

    # Generating a random solution, step 4: Shuffle
    shuffle(solution)

    # Generating a random solution, step 5: Move nearest Depot Node to Start
    first_depot = None
    for i in range(len(solution)):
        for j in range(len(depot_nodes)):
            if depot_nodes[j] == solution[i]:
                first_depot = i
                break
        if first_depot is not None:
            break

    solution[0], solution[first_depot] = \
        solution[first_depot], solution[0]

    return solution


def random(**kwargs):
    """
    Creates a population of randomly generated individuals that are also validated and evaluated.

    :param kwargs: Dictionary of expected parameters:
    - (int) 'node_count': Number of nodes used in the problem. Includes depot nodes and optional nodes.
    - (list<int>) 'depot_nodes': List of depot nodes used in the problem.
    - (list<int>) 'optional_nodes': List of optional nodes used in the problem.
    - (int) 'vehicle_count': Number of vehicles used in the problem.
    - (int) 'population_count': Number of individuals in the population.
    - (int) 'minimum_cpu_time': CPU time that is allotted for the initialization of an individual solution.
      The purpose of this is to stop the algorithm if that is unable to create a valid individual
      (or it takes too long).

    :return: List of randomly generated individuals, representing the population. (list<VRP>)
    """

    population = []

    node_count = kwargs["node_count"]
    depot_nodes = kwargs["depot_nodes"]
    optional_nodes = kwargs["optional_nodes"]
    vehicle_count = kwargs["vehicle_count"]
    population_count = kwargs["population_count"]
    minimum_cpu_time = kwargs["minimum_cpu_time"]

    # Set up two timers: one for measuring population initialization,
    # and another for measuring individual initializations.
    population_timer = Timer()
    individual_timer = Timer(goal=minimum_cpu_time)

    # If minimum CPU time is set to None, it is to be ignored.
    if minimum_cpu_time is None:
        def check_goal(vrp): return False
    else:
        def check_goal(vrp): return vrp.past_goal()

    population_timer.start()
    individual_timer.start()
    for i in range(population_count):

        valid_individual = False
        candidate_individual = None
        while valid_individual is False:

            candidate_solution = random_solution(
                node_count=node_count,
                depot_nodes=depot_nodes,
                optional_nodes=optional_nodes,
                vehicle_count=vehicle_count
            )

            # Create an individual so that a solution can be assigned, validated and evaluated.
            candidate_individual = VRP(node_count, vehicle_count, depot_nodes, optional_nodes)
            candidate_individual.assign_solution(candidate_solution)
            VRP.validator(candidate_individual)

            # If the solution is invalid, restart the process.
            valid_individual = candidate_individual.valid

            # Should solution-finding take too long, it is halted here.
            if check_goal(candidate_individual):
                return population, "(Random) Individual initialization is taking too long."

        # Once the solution is valid, evaluate it.
        VRP.evaluator(candidate_individual)

        # With an individual both validated and evaluated, it is good to go.
        population.append(candidate_individual)

        # Reset individual timer, since an individual has been created successfully.
        individual_timer.reset()

    population_timer.stop()
    individual_timer.stop()

    return population, "(Random) Population initialization OK (Time taken: {} ms)".format(population_timer.elapsed())


def allele_mutation(**kwargs):
    """
    Creates a random individual from which a population is generated by randomly mutating it over and over.

    :param kwargs: Dictionary of expected parameters:
    - (int) 'node_count': Number of nodes used in the problem. Includes depot nodes and optional nodes.
    - (list<int>) 'depot_nodes': List of depot nodes used in the problem.
    - (list<int>) 'optional_nodes': List of optional nodes used in the problem.
    - (int) 'vehicle_count': Number of vehicles used in the problem.
    - (int) 'population_count': Number of individuals in the population.
    - (int) 'minimum_cpu_time': CPU time that is allotted for the initialization of an individual solution.
      The purpose of this is to stop the algorithm if that is unable to create a valid individual
      (or it takes too long).

    :return: List of randomly generated individuals, representing the population. (list<VRP>)
    """

    population = []

    node_count = kwargs["node_count"]
    depot_nodes = kwargs["depot_nodes"]
    optional_nodes = kwargs["optional_nodes"]
    vehicle_count = kwargs["vehicle_count"]
    population_count = kwargs["population_count"]
    minimum_cpu_time = kwargs["minimum_cpu_time"]

    # Set up two timers: one for measuring population initialization,
    # and another for measuring individual initializations.
    population_timer = Timer()
    individual_timer = Timer(goal=minimum_cpu_time)

    # If minimum CPU time is set to None, it is to be ignored.
    if minimum_cpu_time is None:
        def check_goal(vrp): return False
    else:
        def check_goal(vrp): return vrp.past_goal()

    population_timer.start()
    individual_timer.start()

    # Start off with a completely random individual.
    candidate_solution = random(
        node_count=node_count,
        depot_nodes=depot_nodes,
        optional_nodes=optional_nodes,
        vehicle_count=vehicle_count
    )
    candidate_individual = VRP(node_count, vehicle_count, depot_nodes, optional_nodes)
    candidate_individual.assign_solution(candidate_solution)

    for i in range(population_count):

        valid_individual = False
        while valid_individual is False:
            # Mutate the individual, creating a new solution. Then validate it.
            VRP.mutation_operator(candidate_individual)
            VRP.validator(candidate_individual)

            # If the solution is invalid, mutate it again.
            valid_individual = candidate_individual.valid

            # Should solution-finding via mutations take too long, it is halted here.
            if check_goal(candidate_individual):
                return population, "(Allele Mutation) Individual initialization is taking too long."

        # Once the solution is valid, evaluate it.
        VRP.evaluator(candidate_individual)

        # With an individual both validated and evaluated, it is good to go.
        population.append(candidate_individual)
        candidate_individual = deepcopy(candidate_individual)
        candidate_individual.assign_id()

        # Reset individual timer, since an individual has been created successfully.
        individual_timer.reset()

    population_timer.stop()
    individual_timer.stop()

    return population, "(Allele Mutation) Population initialization OK (Time taken: {} ms)" \
        .format(population_timer.elapsed())


def gene_permutation(**kwargs):
    """
    Creates a random individual from which a population is generated by generating gene permutations of it.

    :param kwargs: Dictionary of expected parameters:
    - (int) 'node_count': Number of nodes used in the problem. Includes depot nodes and optional nodes.
    - (list<int>) 'depot_nodes': List of depot nodes used in the problem.
    - (list<int>) 'optional_nodes': List of optional nodes used in the problem.
    - (int) 'vehicle_count': Number of vehicles used in the problem.
    - (int) 'population_count': Number of individuals in the population.
    - (int) 'minimum_cpu_time': CPU time that is allotted for the initialization of an individual solution.
      The purpose of this is to stop the algorithm if that is unable to create a valid individual
      (or it takes too long).

    :return: List of randomly generated individuals, representing the population. (list<VRP>)
    """

    population = []

    node_count = kwargs["node_count"]
    depot_nodes = kwargs["depot_nodes"]
    optional_nodes = kwargs["optional_nodes"]
    vehicle_count = kwargs["vehicle_count"]
    population_count = kwargs["population_count"]
    minimum_cpu_time = kwargs["minimum_cpu_time"]

    # Set up two timers: one for measuring population initialization,
    # and another for measuring individual initializations.
    population_timer = Timer()
    individual_timer = Timer(goal=minimum_cpu_time)

    # If minimum CPU time is set to None, it is to be ignored.
    if minimum_cpu_time is None:
        def check_goal(vrp): return False
    else:
        def check_goal(vrp): return vrp.past_goal()

    population_timer.start()
    individual_timer.start()

    # Factorials spike in value very quickly, for which reason the number of genes split
    # from the chromosome has to be set accordingly.
    if population_count <= 24:
        gene_count = 4
    elif 24 < population_count <= 120:
        gene_count = 5
    else:
        gene_count = 6

    permutation_count = factorial(gene_count)
    permutation_tracker = factorial(gene_count)
    permutation_list = []
    for i in range(population_count):

        valid_individual = False
        candidate_individual = None
        while valid_individual is False:
            if permutation_tracker >= permutation_count:
                # All of the permutations in the list have been used. More is to be made.
                # Generate a random solution along with indexes representing gene beginnings.
                permutation_tracker = 0
                candidate_solution = random(
                    node_count=node_count,
                    depot_nodes=depot_nodes,
                    optional_nodes=optional_nodes,
                    vehicle_count=vehicle_count
                )

                # Collection of indices that indicate the beginnings of the genes subject to permutations.
                gene_indices = [0,
                                *list(sample(range(1, len(candidate_solution) - 1), gene_count - 1)),
                                len(candidate_solution)]

                # Sort the indices in ascending order to avoid overlapping genes.
                gene_indices.sort()

                # The first element of the solution is kept untouched. We'll keep track of it here.
                start_node = candidate_solution[0]

                # Gene list is to contain the solution as randomly cut genes.
                gene_list = []

                # Collecting the genes from the solution, excluding the first allele.
                for j in range(len(gene_indices) - 1):
                    gene_start = gene_indices[j]
                    gene_finish = gene_indices[j + 1]
                    gene_list.append(list(candidate_solution[gene_start + 1:gene_finish + 1]))

                # Now that the genes have been generated, their permutations can be created.
                permutation_indices = list(permutations(range(gene_count)))
                permutation_list = []
                for permutation in permutation_indices:
                    permutation_candidate = [start_node]
                    for index in permutation:
                        permutation_candidate = permutation_candidate + gene_list[index]
                    permutation_list.append(permutation_candidate)

            # Create an individual so that a solution can be assigned, validated and evaluated.
            candidate_individual = VRP(node_count, vehicle_count, depot_nodes, optional_nodes)
            candidate_individual.assign_solution(permutation_list[permutation_tracker])
            VRP.validator(candidate_individual)

            # If the solution is invalid, restart the process.
            valid_individual = candidate_individual.valid

            # Since a permutation has been used, it is now discarded.
            permutation_tracker += 1

            # Should solution-finding via mutations take too long, it is halted here.
            if check_goal(candidate_individual):
                return population, "(Allele Mutation) Individual initialization is taking too long."

        # Once the solution is valid, evaluate it.
        VRP.evaluator(candidate_individual)

        # With an individual both validated and evaluated, it is good to go.
        population.append(candidate_individual)
        candidate_individual = deepcopy(candidate_individual)
        candidate_individual.assign_id()

        # Reset individual timer, since an individual has been created successfully.
        individual_timer.reset()

    population_timer.stop()
    individual_timer.stop()

    return population, "(Allele Mutation) Population initialization OK (Time taken: {} ms)" \
        .format(population_timer.elapsed())


def simulated_annealing(**kwargs):
    """
    Creates a random individual from which simulated annealing is used to generate a population.

    :param kwargs: Dictionary of expected parameters:
    - (int) 'node_count': Number of nodes used in the problem. Includes depot nodes and optional nodes.
    - (list<int>) 'depot_nodes': List of depot nodes used in the problem.
    - (list<int>) 'optional_nodes': List of optional nodes used in the problem.
    - (int) 'vehicle_count': Number of vehicles used in the problem.
    - (int) 'population_count': Number of individuals in the population.
    - (int) 'minimum_cpu_time': CPU time that is allotted for the initialization of an individual solution.
      The purpose of this is to stop the algorithm if that is unable to create a valid individual
      (or it takes too long).
    - (int) 'sa_iteration_count': Number of iterations that SA is allowed to go for.
    - (int) 'sa_initial_temperature': Initial temperature, acts as how easily a solution could be accepted.
    - (float) 'sa_p_coeff': Annealing coefficient.
    - (bool) 'maximize': Flag that determines whether the objective to maximize or minimize.

    :return: List of randomly generated individuals, representing the population. (list<VRP>)
    """

    population = []

    node_count = kwargs["node_count"]
    depot_nodes = kwargs["depot_nodes"]
    optional_nodes = kwargs["optional_nodes"]
    vehicle_count = kwargs["vehicle_count"]
    population_count = kwargs["population_count"]
    minimum_cpu_time = kwargs["minimum_cpu_time"]
    sa_iteration_count = kwargs["sa_iteration_count"]
    sa_initial_temperature = kwargs["sa_initial_temperature"]
    sa_p_coeff = kwargs["sa_p_coeff"]

    if "maximize" in kwargs:
        if kwargs["maximize"] is True:
            reverse_sort = False
            max_factor = 1
        else:
            reverse_sort = True
            max_factor = -1
    else:
        reverse_sort = True
        max_factor = -1

    # Set up two timers: one for measuring population initialization,
    # and another for measuring individual initializations.
    population_timer = Timer()
    individual_timer = Timer(goal=minimum_cpu_time)

    # If minimum CPU time is set to None, it is to be ignored.
    if minimum_cpu_time is None:
        def check_goal(vrp): return False
    else:
        def check_goal(vrp): return vrp.past_goal()

    population_timer.start()
    individual_timer.start()

    # Start off with a completely random individual.
    candidate_solution = random(
        node_count=node_count,
        depot_nodes=depot_nodes,
        optional_nodes=optional_nodes,
        vehicle_count=vehicle_count
    )
    candidate_individual = VRP(node_count, vehicle_count, depot_nodes, optional_nodes)
    candidate_individual.assign_solution(candidate_solution)

    # Validate and evaluate the first individual so that it can be used as a guide for SA.
    while candidate_individual.valid is False:
        VRP.mutation_operator(candidate_individual)
        VRP.validator(candidate_individual)

    VRP.evaluator(candidate_individual)
    individual_timer.reset()

    population.append(candidate_individual)
    guide_individual = deepcopy(candidate_individual)
    guide_individual.assign_id()

    for n in range(1, sa_iteration_count):
        # Once all of the iterations have been exhausted, the state of the population is checked.
        # If the population quota is not met, random individuals are created to make up for it.

        valid_individual = False
        while valid_individual is False:
            # Usually only one change is considered in SA. In this case, there is a possibility
            # that one change can invalidate the individual. For that reason, we'll keep changing it
            # until it is valid.
            VRP.mutation_operator(candidate_individual)
            VRP.validator(candidate_individual)

            # If the solution is invalid, mutate it again.
            valid_individual = candidate_individual.valid

            # Should solution-finding via mutations take too long, it is halted here.
            if check_goal(candidate_individual):
                return population, "(Simulated Annealing) Individual initialization is taking too long."

        # Once the solution is valid, evaluate it.
        VRP.evaluator(candidate_individual)

        # Calculate temperature for current iteration and generate a "pass requirement".
        temperature = sa_initial_temperature * (1 - (n - 1) / (sa_iteration_count - 1)) ** sa_p_coeff
        pass_requirement = random_float()

        # With the fitness values of both guide and candidate, SA probability can be calculated.
        sa_probability = exp(max_factor * (candidate_individual.fitness - guide_individual.fitness) / temperature)

        if sa_probability >= pass_requirement:
            # Mutation has been selected as the new guide.
            population.append(candidate_individual)
            guide_individual = deepcopy(candidate_individual)
            guide_individual.assign_id()

        # Reset individual timer upon completing an iteration.
        individual_timer.reset()

    population_timer.stop()
    individual_timer.stop()

    msg = "(Simulated Annealing) Population initialization OK (Time taken: {} ms)" \
        .format(population_timer.elapsed())

    # Check the state of the population.
    # - If it is too large, sort by fitness in descending order and take an appropriate sublist.
    # - If it is too small, add missing individuals by generating random individuals.
    current_population_count = len(population)
    if current_population_count > population_count:
        population.sort(key=attrgetter("fitness"), reverse=reverse_sort)
        return population[:population_count], msg
    elif current_population_count < population_count:
        missing_population_count = population_count - current_population_count
        missing_population, msg0 = random(
            node_count=node_count,
            depot_nodes=depot_nodes,
            optional_nodes=optional_nodes,
            vehicle_count=vehicle_count,
            population_count=missing_population_count,
            minimum_cpu_time=minimum_cpu_time
        )
        return population + missing_population, msg

    return population, msg
