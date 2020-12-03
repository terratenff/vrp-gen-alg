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

    solution = vrp.solution
    swap_indices = sample(range(1, len(solution) - 1), 2)
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

    solution = vrp.solution
    gene_border = sample(range(1, len(solution)), 2)
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

    solution = vrp.solution
    gene_border = sample(range(1, len(solution)), 2)
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

    solution = vrp.solution
    gene_border = sample(range(1, len(solution)), 2)
    gene_border.sort()
    subject_gene = solution[gene_border[0]:gene_border[1]]
    for allele in subject_gene:
        solution.remove(allele)
    destination = randint(1, len(solution) - 1)
    for allele in subject_gene[::-1]:
        solution.insert(destination, allele)

    vrp.assign_solution(solution)


def add_optional_node(vrp):
    """
    Mutates an individual by adding an optional node to the solution. Applicable
    for VRPP instances only.
    :param vrp: Subject individual.

    Once the individual has been mutated, it has to be validated and evaluated
    again.
    """

    solution = vrp.solution
    unused_nodes = vrp.unvisited_optional_nodes
    subject_node = unused_nodes[randint(0, len(unused_nodes) - 1)]
    destination = randint(1, len(solution) - 1)
    solution.insert(destination, subject_node)

    vrp.assign_solution(solution)


def remove_optional_node(vrp):
    """
    Mutates an individual by removing an optional node from the solution.
    Applicable for VRPP instances only.
    :param vrp: Subject individual.

    Once the individual has been mutated, it has to be validated and evaluated
    again.
    """

    solution = vrp.solution
    used_nodes = vrp.visited_optional_nodes
    subject_node = used_nodes[randint(0, len(used_nodes) - 1)]
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
