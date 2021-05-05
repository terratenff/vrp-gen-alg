#!/usr/bin/env python

"""
population_initializers.py:

Collection of functions that are used to initialize generation 0 population.
"""

from random import randint, sample, shuffle, random as random_float
from numpy import argmin
from itertools import permutations
from math import factorial, exp
from copy import deepcopy
from operator import attrgetter
from algorithms.timer import Timer
from algorithms.modules.mutation_operators import allele_swap, vehicle_diversification
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
    waiting to be assigned to a population individual and validated.
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
        for _ in range(vehicle_count)
        ]

    solution = solution + selected_depots

    # Generating a random solution, step 2: Required Nodes
    required_nodes = [i for i in nodes if
                      i not in depot_nodes and
                      i not in optional_nodes]

    solution = solution + required_nodes

    # Generating a random solution, step 3: Optional Nodes
    list_size = randint(0, len(optional_nodes))
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


def nearest_neighbor_solution(segment, path_table):
    """
    Generates a random solution segment as part of nearest neighbor heuristic
    population initialization.

    :param kwargs: Dictionary of expected parameters:
    - (list<int>) 'segment': List of nodes associated with the subproblem.
    - (numpy.ndarray) path_table: Square matrix that represents
      distances between nodes.

    :return: Segment sorted to fit as the solution to the subproblem.
    """
    
    solution = []
    if len(segment) < 2:
        return segment
    
    unused_nodes = segment[1:]
    start_node = segment[0]
    solution.append(start_node)
    
    for _ in range(len(segment) - 1):
        travel_costs = path_table[start_node][unused_nodes]
        travel_costs_indices = unused_nodes
        lowest_cost_index = argmin(travel_costs)
        target_node = travel_costs_indices[lowest_cost_index]
        solution.append(target_node)
        unused_nodes.remove(target_node)
        start_node = target_node
    
    return solution


def random_valid_individual(**kwargs):
    """
    Creates a random individual, the solution of which has been both validated
    and evaluated.

    :param kwargs: Dictionary of expected parameters:
    - (int) 'node_count': Number of nodes used in the problem. Includes depot nodes and optional nodes.
    - (list<int>) 'depot_nodes': List of depot nodes used in the problem.
    - (list<int>) 'optional_nodes': List of optional nodes used in the problem.
    - (int) 'vehicle_count': Number of vehicles used in the problem.
    - (str) 'failure_msg': Text to represent if individual creation is taking too long.
    - (Timer) 'individual_timer': Timer based on specified minimum CPU time. Should be started before
      calling this function.
    - (function) 'check_goal': Convenience function that checks whether minimum CPU time has passed.
    - (dict) 'validation_args': Dictionary of arguments that are used in individual validations. See
      validation functions for what is expected of them.
    - (dict) 'evaluation_args': Dictionary of arguments that are used in individual evaluations. See
      evaluation functions for what is expected of them.

    :return: Randomly generated individual that has been validated and evaluated.
    """
    node_count = kwargs["node_count"]
    depot_nodes = kwargs["depot_nodes"]
    optional_nodes = kwargs["optional_nodes"]
    vehicle_count = kwargs["vehicle_count"]
    failure_msg = kwargs["failure_msg"]
    individual_timer = kwargs["individual_timer"]
    check_goal = kwargs["check_goal"]
    validation_args = kwargs["validation_args"]
    evaluation_args = kwargs["evaluation_args"]

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

        # Mutate the individual with "vehicle diversification" 10% of the time.
        if random_float() <= 0.10:
            vehicle_diversification(candidate_individual)
        
        for validator in VRP.validator:
            valid_individual, validation_msg = validator(candidate_individual, **validation_args)
            # print("(Random Valid Individual) {}".format(validation_msg))
            if valid_individual is False:
                break

        # If the solution is invalid, the process is restarted.
        candidate_individual.valid = valid_individual
        
        # Should solution-finding take too long, it is halted here.
        if check_goal(individual_timer):
            return None, failure_msg

    # Once the solution is valid, it is evaluated.
    candidate_individual.fitness = VRP.evaluator(candidate_individual, **evaluation_args)

    # The individual is now ready for use.
    return candidate_individual, "Individual Creation OK (Time taken: {} ms)".format(individual_timer.elapsed())


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
    - (dict) 'validation_args': Dictionary of arguments that are used in individual validations. See
      validation functions for what is expected of them.
    - (dict) 'evaluation_args': Dictionary of arguments that are used in individual evaluations. See
      evaluation functions for what is expected of them.

    :return: List of randomly generated individuals, representing the population. (list<VRP>)
    """

    population = []

    node_count = kwargs["node_count"]
    depot_nodes = kwargs["depot_nodes"]
    optional_nodes = kwargs["optional_nodes"]
    vehicle_count = kwargs["vehicle_count"]
    population_count = kwargs["population_count"]
    minimum_cpu_time = kwargs["minimum_cpu_time"]
    validation_args = kwargs["validation_args"]
    evaluation_args = kwargs["evaluation_args"]

    population_timer = Timer()
    individual_timer = Timer(goal=minimum_cpu_time)

    def check_goal(timer): return timer.past_goal()

    population_timer.start()
    individual_timer.start()

    individual_args = {
        "node_count": node_count,
        "depot_nodes": depot_nodes,
        "optional_nodes": optional_nodes,
        "vehicle_count": vehicle_count,
        "failure_msg": "(Random) Individual initialization is taking too long.",
        "individual_timer": individual_timer,
        "check_goal": check_goal,
        "validation_args": validation_args,
        "evaluation_args": evaluation_args
    }
    for i in range(population_count):

        # Create a random, validated and evaluated individual.
        candidate_individual, individual_msg = random_valid_individual(**individual_args)
        if candidate_individual is None:
            return None, individual_msg

        # With an individual both validated and evaluated, it is good to go.
        population.append(candidate_individual)

        # Reset individual timer, since an individual has been created successfully.
        individual_timer.reset()

    population_timer.stop()
    individual_timer.stop()

    return population, "(Random) Population initialization OK (Time taken: {} ms)".format(population_timer.elapsed())


def allele_permutation(**kwargs):
    """
    Creates a random individual from which a population is generated by randomly mutating it over and over
    using the allele swap mutation operator.

    :param kwargs: Dictionary of expected parameters:
    - (int) 'node_count': Number of nodes used in the problem. Includes depot nodes and optional nodes.
    - (list<int>) 'depot_nodes': List of depot nodes used in the problem.
    - (list<int>) 'optional_nodes': List of optional nodes used in the problem.
    - (int) 'vehicle_count': Number of vehicles used in the problem.
    - (int) 'population_count': Number of individuals in the population.
    - (int) 'minimum_cpu_time': CPU time that is allotted for the initialization of an individual solution.
      The purpose of this is to stop the algorithm if that is unable to create a valid individual
      (or it takes too long).
    - (dict) 'validation_args': Dictionary of arguments that are used in individual validations. See
      validation functions for what is expected of them.
    - (dict) 'evaluation_args': Dictionary of arguments that are used in individual evaluations. See
      evaluation functions for what is expected of them.

    :return: List of randomly generated individuals, representing the population. (list<VRP>)
    """

    population = []

    node_count = kwargs["node_count"]
    depot_nodes = kwargs["depot_nodes"]
    optional_nodes = kwargs["optional_nodes"]
    vehicle_count = kwargs["vehicle_count"]
    population_count = kwargs["population_count"]
    minimum_cpu_time = kwargs["minimum_cpu_time"]
    validation_args = kwargs["validation_args"]
    evaluation_args = kwargs["evaluation_args"]
    
    if len(optional_nodes) > node_count - len(optional_nodes):
        print("(Allele Permutation) Note that this population initializer may not "\
              "work well with VRPP instances.")

    population_timer = Timer()
    individual_timer = Timer(goal=minimum_cpu_time)

    def check_goal(timer): return timer.past_goal()

    population_timer.start()
    individual_timer.start()

    # Start off with a completely random, unvalidated individual.
    candidate_solution = random_solution(
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
            allele_swap(candidate_individual)
            for validator in VRP.validator:
                valid_individual, validation_msg = validator(candidate_individual, **validation_args)
                if valid_individual is False:
                    break

            # If the solution is invalid, mutate it again.
            candidate_individual.valid = valid_individual

            # Should solution-finding via mutations take too long, it is halted here.
            if check_goal(individual_timer):
                return None, "(Allele Permutation) Individual initialization is taking too long."

        # Once the solution is valid, evaluate it.
        candidate_individual.fitness = VRP.evaluator(candidate_individual, **evaluation_args)

        # With an individual both validated and evaluated, it is good to go.
        population.append(candidate_individual)
        candidate_individual = deepcopy(candidate_individual)
        candidate_individual.assign_id()

        # Reset individual timer, since an individual has been created successfully.
        individual_timer.reset()

    population_timer.stop()
    individual_timer.stop()

    return population, "(Allele Permutation) Population initialization OK (Time taken: {} ms)" \
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
    - (dict) 'validation_args': Dictionary of arguments that are used in individual validations. See
      validation functions for what is expected of them.
    - (dict) 'evaluation_args': Dictionary of arguments that are used in individual evaluations. See
      evaluation functions for what is expected of them.

    :return: List of randomly generated individuals, representing the population. (list<VRP>)
    """

    population = []

    node_count = kwargs["node_count"]
    depot_nodes = kwargs["depot_nodes"]
    optional_nodes = kwargs["optional_nodes"]
    vehicle_count = kwargs["vehicle_count"]
    population_count = kwargs["population_count"]
    minimum_cpu_time = kwargs["minimum_cpu_time"]
    validation_args = kwargs["validation_args"]
    evaluation_args = kwargs["evaluation_args"]
    
    if node_count - len(depot_nodes) < 10:
        return None, "(Gene Permutation) Population Initialization halted: "\
        "arbitralily set requirement (10 customers or more) is not met."
    if len(optional_nodes) > node_count - len(optional_nodes):
        print("(Gene Permutation) Note that this population initializer may not "\
              "work well with VRPP instances.")

    population_timer = Timer()
    individual_timer = Timer(goal=minimum_cpu_time)

    def check_goal(timer): return timer.past_goal()

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
                
                # Select a random solution such that its length, excluding depot nodes,
                # is greater than or equal to 10.
                solution_size = 0
                while solution_size < 10:
                    candidate_solution = random_solution(
                        node_count=node_count,
                        depot_nodes=depot_nodes,
                        optional_nodes=optional_nodes,
                        vehicle_count=vehicle_count
                    )
                    solution_size = len(candidate_solution) - len(depot_nodes)

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
            for validator in VRP.validator:
                valid_individual, validation_msg = validator(candidate_individual, **validation_args)
                if valid_individual is False:
                    break

            # If the solution is invalid, restart the process.
            candidate_individual.valid = valid_individual

            # Since a permutation has been used, it is now discarded.
            permutation_tracker += 1

            # Should solution-finding via mutations take too long, it is halted here.
            if check_goal(individual_timer):
                return None, "(Gene Permutation) Individual initialization is taking too long."

        # Once the solution is valid, evaluate it.
        candidate_individual.fitness = VRP.evaluator(candidate_individual, **evaluation_args)

        # With an individual both validated and evaluated, it is good to go.
        population.append(candidate_individual)
        candidate_individual = deepcopy(candidate_individual)
        candidate_individual.assign_id()

        # Reset individual timer, since an individual has been created successfully.
        individual_timer.reset()

    population_timer.stop()
    individual_timer.stop()

    return population, "(Gene Permutation) Population initialization OK (Time taken: {} ms)" \
        .format(population_timer.elapsed())


def nearest_neighbor_population(**kwargs):
    """
    Creates a population of individuals by applying the nearest neighbor heuristic.

    :param kwargs: Dictionary of expected parameters:
    - (int) 'node_count': Number of nodes used in the problem. Includes depot nodes and optional nodes.
    - (list<int>) 'depot_nodes': List of depot nodes used in the problem.
    - (list<int>) 'optional_nodes': List of optional nodes used in the problem.
    - (int) 'vehicle_count': Number of vehicles used in the problem.
    - (int) 'population_count': Number of individuals in the population.
    - (int) 'minimum_cpu_time': CPU time that is allotted for the initialization of an individual solution.
      The purpose of this is to stop the algorithm if that is unable to create a valid individual
      (or it takes too long).
    - (dict) 'validation_args': Dictionary of arguments that are used in individual validations. See
      validation functions for what is expected of them.
    - (dict) 'evaluation_args': Dictionary of arguments that are used in individual evaluations. See
      evaluation functions for what is expected of them.

    :return: List of randomly generated individuals, directed by the
    nearest neighbor heuristic. (list<VRP>)
    """

    population = []

    node_count = kwargs["node_count"]
    nodes = list(range(node_count))
    path_table = kwargs["evaluation_args"]["path_table"]
    depot_nodes = kwargs["depot_nodes"]
    optional_nodes = kwargs["optional_nodes"]
    required_nodes = [i for i in nodes if i not in depot_nodes and i not in optional_nodes]
    vehicle_count = kwargs["vehicle_count"]
    population_count = kwargs["population_count"]
    minimum_cpu_time = kwargs["minimum_cpu_time"]
    validation_args = kwargs["validation_args"]
    evaluation_args = kwargs["evaluation_args"]

    population_timer = Timer()
    individual_timer = Timer(goal=minimum_cpu_time)

    def check_goal(timer): return timer.past_goal()

    population_timer.start()
    individual_timer.start()

    for i in range(population_count):

        valid_individual = False
        while valid_individual is False:
            # Collect a random portion of optional nodes.
            optional_sample_size = randint(0, len(optional_nodes))
            optional_sample = sample(optional_nodes, optional_sample_size)
            node_collection = required_nodes + optional_sample
            shuffle(node_collection)
            present_node_count = len(node_collection)
            
            # Create partitions for the nearest neighbor heuristic to handle.
            if present_node_count < 10:
                partition_count = 1
            else:
                partition_count = randint(1, present_node_count // 10)
            if partition_count == 1:
                candidate_solution = nearest_neighbor_solution(node_collection, path_table)
            else:
                candidate_solution = []
                partition_length = present_node_count // partition_count
                partition_list = [
                    node_collection[
                        x*partition_length
                        :
                        (x + 1) * partition_length]
                    for x in range(partition_count - 1)
                ]
                partition_list.append(node_collection[(partition_count - 1)*partition_length:])
                for partition in partition_list:
                    if len(partition) == 0:
                        continue
                    sorted_partition = nearest_neighbor_solution(partition, path_table)
                    candidate_solution = candidate_solution + sorted_partition
            
            # Add missing depot nodes.
            selected_depots = [
                depot_nodes[randint(0, len(depot_nodes) - 1)]
                for _ in range(vehicle_count)
            ]
            candidate_solution.insert(0, selected_depots[0])
            for depot in selected_depots[1:]:
                candidate_solution.insert(randint(0, len(candidate_solution) - 1), depot)
            
            candidate_individual = VRP(node_count, vehicle_count, depot_nodes, optional_nodes)
            candidate_individual.assign_solution(candidate_solution)
            for validator in VRP.validator:
                valid_individual, validation_msg = validator(candidate_individual, **validation_args)
                if valid_individual is False:
                    break

            # If the solution is invalid, try again.
            candidate_individual.valid = valid_individual

            # Should solution-finding take too long, it is halted here.
            if check_goal(individual_timer):
                return None, "(Nearest Neighbor) Individual initialization is taking too long."

        # Once the solution is valid, evaluate it.
        candidate_individual.fitness = VRP.evaluator(candidate_individual, **evaluation_args)

        # With an individual both validated and evaluated, it is good to go.
        population.append(candidate_individual)
        candidate_individual = deepcopy(candidate_individual)
        candidate_individual.assign_id()

        # Reset individual timer, since an individual has been created successfully.
        individual_timer.reset()

    population_timer.stop()
    individual_timer.stop()

    return population, "(Nearest Neighbor) Population initialization OK (Time taken: {} ms)" \
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
    - (dict) 'validation_args': Dictionary of arguments that are used in individual validations. See
      validation functions for what is expected of them.
    - (dict) 'evaluation_args': Dictionary of arguments that are used in individual evaluations. See
      evaluation functions for what is expected of them.
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
    validation_args = kwargs["validation_args"]
    evaluation_args = kwargs["evaluation_args"]
    sa_iteration_count = kwargs["sa_iteration_count"]
    sa_initial_temperature = kwargs["sa_initial_temperature"]
    sa_p_coeff = kwargs["sa_p_coeff"]

    if "maximize" in kwargs:
        if kwargs["maximize"] is True:
            reverse_sort = True
            max_factor = 1
        else:
            reverse_sort = False
            max_factor = -1
    else:
        reverse_sort = False
        max_factor = -1

    population_timer = Timer()
    individual_timer = Timer(goal=minimum_cpu_time)

    def check_goal(timer): return timer.past_goal()

    population_timer.start()
    individual_timer.start()

    individual_args = {
        "node_count": node_count,
        "depot_nodes": depot_nodes,
        "optional_nodes": optional_nodes,
        "vehicle_count": vehicle_count,
        "failure_msg": "(Simulated Annealing - Random) Individual initialization is taking too long.",
        "individual_timer": individual_timer,
        "check_goal": check_goal,
        "validation_args": validation_args,
        "evaluation_args": evaluation_args
    }
    candidate_individual, individual_msg = random_valid_individual(**individual_args)
    if candidate_individual is None:
        return None, individual_msg
    individual_timer.reset()

    population.append(candidate_individual)
    guide_individual = deepcopy(candidate_individual)
    candidate_individual = deepcopy(candidate_individual)
    guide_individual.assign_id()
    candidate_individual.assign_id()

    for n in range(1, sa_iteration_count):
        # Once all of the iterations have been exhausted, the state of the population is checked.
        # If the population quota is not met, random individuals are created to make up for it.

        valid_individual = False
        while valid_individual is False:
            # Usually only one change is considered in SA. In this case, there is a possibility
            # that one change can invalidate the individual. For that reason, we'll keep changing it
            # until it is valid.
            VRP.mutation_operator[randint(0, len(VRP.mutation_operator) - 1)](candidate_individual)
            for validator in VRP.validator:
                valid_individual, validation_msg = validator(candidate_individual, **validation_args)
                if valid_individual is False:
                    break

            # If the solution is invalid, mutate it again.
            candidate_individual.valid = valid_individual

            # Should solution-finding via mutations take too long, it is halted here.
            if check_goal(individual_timer):
                return None, "(Simulated Annealing) Individual initialization is taking too long."

        # Once the solution is valid, evaluate it.
        candidate_individual.fitness = VRP.evaluator(candidate_individual, **evaluation_args)

        # Calculate temperature for current iteration and generate a "pass requirement".
        temperature = sa_initial_temperature * (1 - (n - 1) / (sa_iteration_count - 1)) ** sa_p_coeff
        pass_requirement = random_float()

        # With the fitness values of both guide and candidate, SA probability can be calculated.
        try:
            sa_probability = exp(max_factor * (candidate_individual.fitness - guide_individual.fitness) / temperature)
        except OverflowError:
            sa_probability = float("inf")

        if sa_probability >= pass_requirement:
            # Mutation has been selected as the new guide.
            population.append(candidate_individual)
            
            # Delete old individuals if current population is too large.
            if len(population) > population_count:
                del population[0]
                
            guide_individual = deepcopy(candidate_individual)
            guide_individual.assign_id()
            candidate_individual = deepcopy(guide_individual)
            outcome_str = "Selected"
        else:
            # Mutation has been rejected. Revert to guide individual.
            candidate_individual = deepcopy(guide_individual)
            outcome_str = "Discarded"
        
        print("Iteration: {} |"
              " Fitness: {:> .5f} |"
              " Temperature: {:> .5f} |"
              " Selection Probability: {:> .5f} |"
              " Outcome: {}"
              .format(
            n,
            candidate_individual.fitness,
            temperature,
            sa_probability,
            outcome_str
        ))
        
        # Reset individual timer upon completing an iteration.
        individual_timer.reset()

    population_timer.stop()
    individual_timer.stop()

    msg = "(Simulated Annealing) Population initialization OK (Time taken: {} ms)\n" \
          "- Result Population Size: {}" \
        .format(population_timer.elapsed(), len(population))

    # If resulting population is too small, add missing individuals by
    # generating random individuals.
    if len(population) < population_count:
        missing_population_count = population_count - len(population)
        missing_population, msg0 = random(
            node_count=node_count,
            depot_nodes=depot_nodes,
            optional_nodes=optional_nodes,
            vehicle_count=vehicle_count,
            population_count=missing_population_count,
            minimum_cpu_time=minimum_cpu_time,
            validation_args=validation_args,
            evaluation_args=evaluation_args
        )
        population = population + missing_population

    population.sort(key=attrgetter("fitness"), reverse=reverse_sort)
    return population, msg
