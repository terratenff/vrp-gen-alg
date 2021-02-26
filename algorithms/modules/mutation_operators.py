#!/usr/bin/env python

"""
mutation_operators.py:

Collection of functions that are used to mutate individuals in the population.
"""

from random import sample, shuffle, randint


def allele_swap(vrp):
    """
    Mutates an individual by swapping the positions of two random alleles.
    :param vrp: Subject individual.

    Once the individual has been mutated, it has to be validated and evaluated
    again.
    """
    
    # Solution length must be greater than 2.
    if len(vrp.solution) <= 2:
        return

    solution = vrp.solution
    swap_indices = sample(range(1, len(solution)), 2)
    swap_indices.sort()
    solution[swap_indices[0]], solution[swap_indices[1]] = \
        solution[swap_indices[1]], solution[swap_indices[0]]

    vrp.assign_solution(solution)


def sequence_inversion(vrp):
    """
    Mutates an individual by inverting a random gene within the chromosome.
    :param vrp: Subject individual.

    Once the individual has been mutated, it has to be validated and evaluated
    again.
    """
    
    # Solution length must be greater than 2.
    if len(vrp.solution) <= 2:
        return

    solution = vrp.solution
    gene_border = sample(range(1, len(solution) + 1), 2)
    gene_border.sort()
    solution[gene_border[0]:gene_border[1]] = \
        solution[gene_border[0]:gene_border[1]][::-1]

    vrp.assign_solution(solution)


def sequence_shuffle(vrp):
    """
    Mutates an individual by shuffling a random gene within the chromosome.
    :param vrp: Subject individual.

    Once the individual has been mutated, it has to be validated and evaluated
    again.
    """
    
    # Solution length must be greater than 2.
    if len(vrp.solution) <= 2:
        return

    solution = vrp.solution
    gene_border = sample(range(1, len(solution) + 1), 2)
    gene_border.sort()
    subject_gene = solution[gene_border[0]:gene_border[1]]
    shuffle(subject_gene)
    solution[gene_border[0]:gene_border[1]] = subject_gene

    vrp.assign_solution(solution)


def sequence_relocation(vrp):
    """
    Mutates an individual by shifting a random gene to another position within
    the chromosome.
    :param vrp: Subject individual.

    Once the individual has been mutated, it has to be validated and evaluated
    again.
    """
    
    # Solution length must be greater than 2.
    if len(vrp.solution) <= 2:
        return

    solution = vrp.solution
    gene_border = sample(range(1, len(solution) + 1), 2)
    gene_border.sort()
    subject_gene = solution[gene_border[0]:gene_border[1]]
    del solution[gene_border[0]:gene_border[1]]

    destination = randint(1, len(solution))
    for allele in subject_gene[::-1]:
        solution.insert(destination, allele)

    vrp.assign_solution(solution)


def vehicle_diversification(vrp):
    """
    Mutates an individual by relocating depot nodes in such a manner
    that every single vehicle has a route to follow. This function
    assumes that there are more non-depot nodes than vehicles.

    :param vrp: Subject individual.

    Once the individual has been mutated, it has to be validated and evaluated
    again.
    """

    solution = vrp.solution
    used_depot_nodes = [node for node in solution if node in vrp.depot_node_list]
    solution = [node for node in solution if node not in set(used_depot_nodes)]
    increment = (len(solution) // len(used_depot_nodes)) + 1
    i = 0
    for node in used_depot_nodes:
        solution.insert(i, node)
        i += increment

    vrp.assign_solution(solution)


def add_optional_node(vrp):
    """
    Mutates an individual by adding 1-5 optional nodes to the solution.
    If all of the optional nodes are being used, remove some from the solution instead.
    Applicable for VRPP instances only.
    :param vrp: Subject individual.

    Once the individual has been mutated, it has to be validated and evaluated
    again.
    """

    solution = vrp.solution
    unused_nodes = vrp.unvisited_optional_nodes
    if len(unused_nodes) == 0:
        # All of the optional nodes are being used. Proceed to remove some instead.
        remove_optional_node(vrp)
        return
    
    node_count = min(randint(1, 5), len(unused_nodes))

    for _ in range(node_count):
        node_selector = randint(0, len(unused_nodes) - 1)
        subject_node = unused_nodes[node_selector]
        del unused_nodes[node_selector]
        destination = randint(1, len(solution))
        solution.insert(destination, subject_node)

    vrp.assign_solution(solution)


def remove_optional_node(vrp):
    """
    Mutates an individual by removing 1-5 optional nodes from the solution.
    If none of the optional nodes are being used, add some to the solution instead.
    Applicable for VRPP instances only.
    :param vrp: Subject individual.

    Once the individual has been mutated, it has to be validated and evaluated
    again.
    """

    solution = vrp.solution
    used_nodes = vrp.visited_optional_nodes
    if len(used_nodes) == 0:
        # None of the optional nodes are being used. Proceed to add some instead.
        add_optional_node(vrp)
        return
    
    node_count = min(randint(1, 5), len(used_nodes))

    for _ in range(node_count):
        node_selector = randint(0, len(used_nodes) - 1)
        subject_node = used_nodes[node_selector]
        del used_nodes[node_selector]
        solution.remove(subject_node)

    vrp.assign_solution(solution)


def change_depot(vrp):
    """
    Mutates an individual by changing a depot node with another. Applicable for
    MDVRP instances only.
    :param vrp: Subject individual.

    Once the individual has been mutated, it has to be validated and evaluated
    again.
    """

    solution = vrp.solution
    depot_nodes = vrp.depot_node_list
    subject_node = depot_nodes[randint(0, len(depot_nodes) - 1)]
    depot_indices = [i for i, x in enumerate(solution) if x in depot_nodes]
    target_node = depot_indices[randint(0, len(depot_indices) - 1)]
    solution[target_node] = subject_node

    vrp.assign_solution(solution)
