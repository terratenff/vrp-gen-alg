#!/usr/bin/env python

"""
crossover_operators.py:

Collection of functions that are used to breed individuals via crossover in the population.
"""

from copy import deepcopy
from random import randint, sample


def one_point(vrp1, vrp2):
    """
    A common point among two chromosomes is selected, and the contents
    after the point are swapped to produce offspring.

    Chromosomes are classified into primary and secondary chromosomes.
    - Primary chromosome is the one whose contents are kept intact
    during the crossover.
    - Secondary chromosome is the one that has to readjust its
    contents so as to accommodate for the primary chromosome.

    A chromosome is selected to be primary if one of two conditions apply:
    1. It is longer than the other (caused by optional nodes).
    2. It is presented as the first parameter.

    :param vrp1: Individual 1 selected from the population to be a parent
    for the crossover.
    :param vrp2: Individual 2 selected from the population to be a parent
    for the crossover.
    :return: Two individuals created via crossover from selected individuals.
    Generated offspring have to be validated and evaluated separately.
    """

    depot_list = vrp1.depot_node_list
    optional_list = vrp1.optional_node_list

    # Step 1: Determine dominant parent.
    # - Dominant parent is the one with the longest solution.
    # - If both are of equal size, the first parent is selected.
    if len(vrp1.solution) >= len(vrp2.solution):
        parent1 = deepcopy(vrp1.solution)
        parent2 = deepcopy(vrp2.solution)
        offspring1 = deepcopy(vrp1)
        offspring2 = deepcopy(vrp2)
    else:
        parent1 = deepcopy(vrp2.solution)
        parent2 = deepcopy(vrp1.solution)
        offspring1 = deepcopy(vrp2)
        offspring2 = deepcopy(vrp1)

    depot_indices = [i for i, x in enumerate(parent1) if x in depot_list]
    depot_indices_active = deepcopy(depot_indices)

    offspring1.assign_id()
    offspring2.assign_id()

    # Step 2: Add None elements to the parent with the shorter solution.
    # This step is skipped if solutions are of equal size.
    for i in range(len(parent1) - len(parent2)):
        parent2.append(None)

    # Step 3: Determine a cutoff-point for the crossover.
    # First two elements and last element are skipped to avoid ineffective
    # cutoff points.
    cutoff = randint(2, len(parent1) - 2)

    # Cut lists keep track of which nodes are located where.
    parent1_cut1 = parent1[:cutoff]
    parent1_cut2 = parent1[cutoff:]

    # Step 4: Keep track of list-wise number of optional nodes on cut lists.
    parent1_cut1_optional_count = 0
    parent1_cut2_optional_count = 0
    for i in parent1_cut1:
        parent1_cut1_optional_count += 1 if i in optional_list or i is None else 0
    for i in parent1_cut2:
        parent1_cut2_optional_count += 1 if i in optional_list or i is None else 0

    # Step 5: Generate convenience lists for accessing cut lists.
    shortcut = [0] * len(parent1_cut1) + [1] * len(parent1_cut2)
    cut_list = [parent1_cut1, parent1_cut2]
    optional_count = [parent1_cut1_optional_count, parent1_cut2_optional_count]

    # Step 6: Rearrange parent 2 in such a way that cut lists contain
    # the same elements (exact required nodes and any depot/optional nodes).
    i = 0
    while i < len(parent2):
        # Case 1a: Is selected spot reserved for a depot node?
        if i in depot_indices:
            if parent2[i] in depot_list:
                # Current node is a depot node. Carry on.
                i += 1
                continue
        # Case 1b: Is selected node a depot node?
        elif parent2[i] in depot_list:
            if i in depot_indices:
                # Current spot is reserved for a depot node. Carry on.
                i += 1
                continue
        # Case 2: Is selected node an optional node?
        elif parent2[i] is None or parent2[i] in optional_list:
            if optional_count[shortcut[i]] > 0:
                # Sufficient number of optional nodes are accounted for.
                optional_count[shortcut[i]] -= 1
                i += 1
                continue
        # Case 3: Is selected node in the respective cut list?
        elif parent2[i] in cut_list[shortcut[i]]:
            # Selected element is in the cut list. Continue.
            i += 1
            continue
        # Case 4: If selected node is not in the respective cut list,
        # start a new iteration that seeks a node that is in said list.
        # Then swap them.
        j = i + 1
        while j < len(parent2):
            if i in depot_indices_active:
                if parent2[j] in depot_list:
                    # Current node is a depot node. Perform a swap.
                    parent2[i], parent2[j] = parent2[j], parent2[i]
                    # Now that a depot node is in place, it is disregarded
                    # for the rest of the run.
                    depot_indices_active.remove(i)
                    i -= 1
                    break
            elif parent2[i] in depot_list:
                if j in depot_indices_active:
                    # Current spot is reserved for a depot node.
                    # Perform a swap.
                    parent2[i], parent2[j] = parent2[j], parent2[i]
                    # Now that a depot node is in place, it is disregarded
                    # for the rest of the run.
                    depot_indices_active.remove(j)
                    i -= 1
                    break
            elif parent2[j] in depot_list:
                # Sub-iteration comes across a depot node.
                # It may be in its correct or incorrect position,
                # for which reason it should be left alone for now.
                pass
            elif parent2[j] is None or parent2[j] in optional_list:
                if optional_count[shortcut[i]] > 0:
                    # Sufficient number of optional nodes are accounted for.
                    # Perform a swap.
                    optional_count[shortcut[i]] -= 1
                    parent2[i], parent2[j] = parent2[j], parent2[i]
                    break
            elif parent2[j] in cut_list[shortcut[i]]:
                # Selected element is in the cut list. Perform a swap.
                parent2[i], parent2[j] = parent2[j], parent2[i]
                break
            j += 1
        i += 1

    # Step 7: Perform the flip on the cutoff point.
    parent1[cutoff:], parent2[cutoff:] = parent2[cutoff:], parent1[cutoff:]

    # Step 8: Remove all None elements.
    parent1 = [i for i in parent1 if i is not None]
    parent2 = [i for i in parent2 if i is not None]

    # Step 9: Upon performing the flip, there is a possibility that
    # there are now duplicates of optional nodes, since None nodes
    # are treated as such. To combat this, any duplicates are removed.
    duplicate_list1, duplicate_list2 = [], []
    for i in range(len(parent1)):
        x1 = parent1[i]
        x2 = parent2[i]
        if x1 is not None:
            if x1 in depot_list:
                pass
            elif parent1.count(x1) > 1 and x1 not in duplicate_list1:
                duplicate_list1.append(x1)
        if x2 is not None:
            if x2 in depot_list:
                pass
            elif parent2.count(x2) > 1 and x2 not in duplicate_list2:
                duplicate_list2.append(x2)

    for x in duplicate_list1:
        for i in range(parent1.count(x) - 1):
            parent1.remove(x)
    for x in duplicate_list2:
        for i in range(parent2.count(x) - 1):
            parent2.remove(x)

    offspring1.assign_solution(parent1)
    offspring2.assign_solution(parent2)

    return offspring1, offspring2


def two_point(vrp1, vrp2):
    """
    Two common points among two chromosomes are selected, and the contents
    between them are swapped to produce offspring.

    Chromosomes are classified into primary and secondary chromosomes.
    - Primary chromosome is the one whose contents are kept intact
    during the crossover.
    - Secondary chromosome is the one that has to readjust its
    contents so as to accommodate for the primary chromosome.

    A chromosome is selected to be primary if one of two conditions apply:
    1. It is longer than the other (caused by optional nodes).
    2. It is presented as the first parameter.

    :param vrp1: Individual 1 selected from the population to be a parent
    for the crossover.
    :param vrp2: Individual 2 selected from the population to be a parent
    for the crossover.
    :return: Two individuals created via crossover from selected individuals.
    Generated offspring have to be validated and evaluated separately.
    """

    depot_list = vrp1.depot_node_list
    optional_list = vrp1.optional_node_list

    # Step 1: Determine dominant parent.
    # - Dominant parent is the one with the longest solution.
    # - If both are of equal size, the first parent is selected.
    if len(vrp1.solution) >= len(vrp2.solution):
        parent1 = deepcopy(vrp1.solution)
        parent2 = deepcopy(vrp2.solution)
        offspring1 = deepcopy(vrp1)
        offspring2 = deepcopy(vrp2)
    else:
        parent1 = deepcopy(vrp2.solution)
        parent2 = deepcopy(vrp1.solution)
        offspring1 = deepcopy(vrp2)
        offspring2 = deepcopy(vrp1)

    depot_indices = [i for i, x in enumerate(parent1) if x in depot_list]
    depot_indices_active = deepcopy(depot_indices)

    offspring1.assign_id()
    offspring2.assign_id()

    # Step 2: Add None elements to the parent with the shorter solution.
    # This step is skipped if solutions are of equal size.
    for i in range(len(parent1) - len(parent2)):
        parent2.append(None)

    # Step 3: Determine a cutoff-point for the crossover.
    # First two elements and last element are skipped to avoid ineffective
    # cutoff points.
    cutoff = sample(range(2, len(parent1) - 1), 2)
    cutoff.sort()

    # Cut lists keep track of which nodes are located where.
    parent1_cut1 = parent1[:cutoff[0]]
    parent1_cut2 = parent1[cutoff[0]:cutoff[1]]
    parent1_cut3 = parent1[cutoff[1]:]

    # Step 4: Keep track of list-wise number of optional nodes on cut lists.
    parent1_cut1_optional_count = 0
    parent1_cut2_optional_count = 0
    parent1_cut3_optional_count = 0
    for i in parent1_cut1:
        parent1_cut1_optional_count += 1 if i in optional_list or i is None else 0
    for i in parent1_cut2:
        parent1_cut2_optional_count += 1 if i in optional_list or i is None else 0
    for i in parent1_cut3:
        parent1_cut3_optional_count += 1 if i in optional_list or i is None else 0

    # Step 5: Generate convenience lists for accessing cut lists.
    shortcut = [0] * len(parent1_cut1) + [1] * len(parent1_cut2) + [2] * len(parent1_cut3)
    cut_list = [parent1_cut1, parent1_cut2, parent1_cut3]
    optional_count = [
        parent1_cut1_optional_count,
        parent1_cut2_optional_count,
        parent1_cut3_optional_count
    ]

    # Step 6: Rearrange parent 2 in such a way that cut lists contain
    # the same elements (exact required nodes and any depot/optional nodes).
    i = 0
    while i < len(parent2):
        # Case 1a: Is selected spot reserved for a depot node?
        if i in depot_indices:
            if parent2[i] in depot_list:
                # Current node is a depot node. Carry on.
                i += 1
                continue
        # Case 1b: Is selected node a depot node?
        elif parent2[i] in depot_list:
            if i in depot_indices:
                # Current spot is reserved for a depot node. Carry on.
                i += 1
                continue
        # Case 2: Is selected node an optional node?
        elif parent2[i] is None or parent2[i] in optional_list:
            if optional_count[shortcut[i]] > 0:
                # Sufficient number of optional nodes are accounted for.
                optional_count[shortcut[i]] -= 1
                i += 1
                continue
        # Case 3: Is selected node in the respective cut list?
        elif parent2[i] in cut_list[shortcut[i]]:
            # Selected element is in the cut list. Continue.
            i += 1
            continue
        # Case 4: If selected node is not in the respective cut list,
        # start a new iteration that seeks a node that is in said list.
        # Then swap them.
        j = i + 1
        while j < len(parent2):
            if i in depot_indices_active:
                if parent2[j] in depot_list:
                    # Current node is a depot node. Perform a swap.
                    parent2[i], parent2[j] = parent2[j], parent2[i]
                    # Now that a depot node is in place, it is disregarded
                    # for the rest of the run.
                    depot_indices_active.remove(i)
                    i -= 1
                    break
            elif parent2[i] in depot_list:
                if j in depot_indices_active:
                    # Current spot is reserved for a depot node.
                    # Perform a swap.
                    parent2[i], parent2[j] = parent2[j], parent2[i]
                    # Now that a depot node is in place, it is disregarded
                    # for the rest of the run.
                    depot_indices_active.remove(j)
                    i -= 1
                    break
            elif parent2[j] in depot_list:
                # Sub-iteration comes across a depot node.
                # It may be in its correct or incorrect position,
                # for which reason it should be left alone for now.
                j += 1
                continue
            elif parent2[j] is None or parent2[j] in optional_list:
                if optional_count[shortcut[i]] > 0:
                    # Sufficient number of optional nodes are accounted for.
                    # Perform a swap.
                    optional_count[shortcut[i]] -= 1
                    parent2[i], parent2[j] = parent2[j], parent2[i]
                    break
            elif parent2[j] in cut_list[shortcut[i]]:
                # Selected element is in the cut list. Perform a swap.
                parent2[i], parent2[j] = parent2[j], parent2[i]
                break
            j += 1
        i += 1

    # Step 7: Perform the flip on the cutoff point.
    parent1[cutoff[0]:cutoff[1]], parent2[cutoff[0]:cutoff[1]] = \
        parent2[cutoff[0]:cutoff[1]], parent1[cutoff[0]:cutoff[1]]

    # Step 8: Remove all None elements.
    parent1 = [i for i in parent1 if i is not None]
    parent2 = [i for i in parent2 if i is not None]

    # Step 9: Upon performing the flip, there is a possibility that
    # there are now duplicates of optional nodes, since None nodes
    # are treated as such. To combat this, any duplicates are removed.
    duplicate_list1, duplicate_list2 = [], []
    for i in range(len(parent1)):
        x1 = parent1[i]
        x2 = parent2[i]
        if x1 is not None:
            if x1 in depot_list:
                pass
            elif parent1.count(x1) > 1 and x1 not in duplicate_list1:
                duplicate_list1.append(x1)
        if x2 is not None:
            if x2 in depot_list:
                pass
            elif parent2.count(x2) > 1 and x2 not in duplicate_list2:
                duplicate_list2.append(x2)

    for x in duplicate_list1:
        for i in range(parent1.count(x) - 1):
            parent1.remove(x)
    for x in duplicate_list2:
        for i in range(parent2.count(x) - 1):
            parent2.remove(x)

    offspring1.assign_solution(parent1)
    offspring2.assign_solution(parent2)

    return offspring1, offspring2


def order_crossover(vrp1, vrp2):
    """
    For both parent individuals, a random gene of random size is selected
    from their chromosomes. Upon crossover, these genes remain intact on
    their offspring: gene from parent 1 remains on offspring 1, and gene
    from parent 2 remains on offspring 2.

    Offspring 1 has a gene exactly preserved, structure and order, from
    parent 1. The rest of the alleles are taken from parent 2. They
    are placed in order of appearance, going from left to right. Any
    alleles that appear in parent 1 gene are ignored. Offspring 2 is
    generated in a similar fashion.

    :param vrp1: Individual 1 selected from the population to be a parent
    for the crossover.
    :param vrp2: Individual 2 selected from the population to be a parent
    for the crossover.
    :return: Two individuals created via crossover from selected individuals.
    Generated offspring have to be validated and evaluated separately.
    """

    depot_list = vrp1.depot_node_list
    parent1 = vrp1.solution
    parent2 = vrp2.solution

    offspring1_solution = []
    offspring2_solution = []
    offspring1 = deepcopy(vrp1)
    offspring2 = deepcopy(vrp2)
    offspring1.assign_id()
    offspring2.assign_id()

    # Step 1: Determine random gene for both parents, subject to preservation.
    gene1 = sample(range(2, len(parent1) - 1), 2)
    gene1.sort()
    gene1_start = gene1[0]
    gene1 = parent1[gene1[0]:gene1[1]]
    gene2 = sample(range(2, len(parent2) - 1), 2)
    gene2.sort()
    gene2_start = gene2[0]
    gene2 = parent2[gene2[0]:gene2[1]]

    # Step 2: Generate variables that keep track of the number of depot nodes.
    parent1_depot_count = 0
    parent2_depot_count = 0
    gene1_depot_count = 0
    gene2_depot_count = 0
    for i in parent1:
        parent1_depot_count += 1 if i in depot_list else 0
    for i in gene1:
        gene1_depot_count += 1 if i in depot_list else 0
    for i in parent2:
        parent2_depot_count += 1 if i in depot_list else 0
    for i in gene2:
        gene2_depot_count += 1 if i in depot_list else 0

    depot_count1 = parent2_depot_count - gene1_depot_count
    depot_count2 = parent1_depot_count - gene2_depot_count

    # Step 3a: Creating offspring 1.
    # - Gene from parent 1.
    # - The rest from parent 2.
    for i in parent2:
        if i in depot_list:
            if depot_count1 > 0:
                # Sufficient number of depot nodes are accounted for.
                # Add depot node to the offspring list.
                depot_count1 -= 1
            else:
                continue
        elif i in gene1:
            # Node is in the gene that will be added afterwards.
            # Skip current node.
            continue
        offspring1_solution.append(i)

    # Step 3b: Inserting gene into offspring 1.
    if gene1_start >= len(offspring1_solution):
        offspring1_solution = offspring1_solution + gene1
    else:
        for i in gene1[::-1]:
            offspring1_solution.insert(gene1_start, i)

    # Step 4a: Creating offspring 2.
    # - Gene from parent 2.
    # - The rest from parent 1.
    for i in parent1:
        if i in depot_list:
            if depot_count2 > 0:
                # Sufficient number of depot nodes are accounted for.
                # Add depot node to the offspring list.
                depot_count2 -= 1
            else:
                continue
        elif i in gene2:
            # Node is in the gene that will be added afterwards.
            # Skip current node.
            continue
        offspring2_solution.append(i)

    # Step 4b: Inserting gene into offspring 1.
    if gene2_start >= len(offspring2_solution):
        offspring2_solution = offspring2_solution + gene2
    else:
        for i in gene2[::-1]:
            offspring2_solution.insert(gene2_start, i)

    offspring1.assign_solution(offspring1_solution)
    offspring2.assign_solution(offspring2_solution)

    return offspring1, offspring2


def vehicle_crossover(vrp1, vrp2):
    """
    For both parent individuals, a random vehicle route is selected
    from their chromosomes. Upon crossover, these routes remain intact on
    their offspring: route from parent 1 remains on offspring 1, and route
    from parent 2 remains on offspring 2.

    Vehicle Crossover is similar to Order Crossover. The difference between
    them is that in Order Crossover, a random gene is selected for
    preservation, while in Vehicle Crossover, a random vehicle route is
    selected instead.

    :param vrp1: Individual 1 selected from the population to be a parent
    for the crossover.
    :param vrp2: Individual 2 selected from the population to be a parent
    for the crossover.
    :return: Two individuals created via crossover from selected individuals.
    Generated offspring have to be validated and evaluated separately.
    """

    depot_list = vrp1.depot_node_list
    parent1 = vrp1.solution
    parent2 = vrp2.solution

    offspring1_solution = []
    offspring2_solution = []
    offspring1 = deepcopy(vrp1)
    offspring2 = deepcopy(vrp2)
    offspring1.assign_id()
    offspring2.assign_id()

    # Step 1: Determine a vehicle gene for both parents, subject to preservation.
    depot_indices1 = [i for i, x in enumerate(parent1) if x in depot_list]
    depot_indices2 = [i for i, x in enumerate(parent2) if x in depot_list]
    target_selector1 = randint(0, len(depot_indices1) - 1)
    target_selector2 = randint(0, len(depot_indices2) - 1)
    target_depot1 = depot_indices1[target_selector1]
    target_depot2 = depot_indices2[target_selector2]
    if target_selector1 == len(depot_indices1) - 1:
        gene1 = parent1[target_depot1:]
    else:
        checkpoint = depot_indices1[target_selector1 + 1]
        gene1 = parent1[target_depot1:checkpoint]
    if target_selector2 == len(depot_indices2) - 1:
        gene2 = parent2[target_depot2:]
    else:
        checkpoint = depot_indices2[target_selector2 + 1]
        gene2 = parent2[target_depot2:checkpoint]

    gene1_start = target_depot1
    gene2_start = target_depot2

    # Step 2: Generate variables to keep track of the number of depot nodes.
    parent1_depot_count = 0
    parent2_depot_count = 0
    gene1_depot_count = 0
    gene2_depot_count = 0
    for i in parent1:
        parent1_depot_count += 1 if i in depot_list else 0
    for i in gene1:
        gene1_depot_count += 1 if i in depot_list else 0
    for i in parent2:
        parent2_depot_count += 1 if i in depot_list else 0
    for i in gene2:
        gene2_depot_count += 1 if i in depot_list else 0

    depot_count1 = parent2_depot_count - gene1_depot_count
    depot_count2 = parent1_depot_count - gene2_depot_count

    # Step 3a: Creating offspring 1.
    # - Gene from parent 1.
    # - The rest from parent 2.
    for i in parent2:
        if i in depot_list:
            if depot_count1 > 0:
                # Sufficient number of depot nodes are accounted for.
                # Add depot node to the offspring list.
                depot_count1 -= 1
            else:
                continue
        elif i in gene1:
            # Node is in the gene that will be added afterwards.
            # Skip current node.
            continue
        offspring1_solution.append(i)

    # Step 3b: Inserting gene into offspring 1.
    if gene1_start >= len(offspring1_solution):
        offspring1_solution = offspring1_solution + gene1
    else:
        for i in gene1[::-1]:
            offspring1_solution.insert(gene1_start, i)

    # Step 4a: Creating offspring 2.
    # - Gene from parent 2.
    # - The rest from parent 1.
    for i in parent1:
        if i in depot_list:
            if depot_count2 > 0:
                # Sufficient number of depot nodes are accounted for.
                # Add depot node to the offspring list.
                depot_count2 -= 1
            else:
                continue
        elif i in gene2:
            # Node is in the gene that will be added afterwards.
            # Skip current node.
            continue
        offspring2_solution.append(i)

    # Step 4b: Inserting gene into offspring 1.
    if gene2_start >= len(offspring2_solution):
        offspring2_solution = offspring2_solution + gene2
    else:
        for i in gene2[::-1]:
            offspring2_solution.insert(gene2_start, i)

    offspring1.assign_solution(offspring1_solution)
    offspring2.assign_solution(offspring2_solution)

    return offspring1, offspring2
