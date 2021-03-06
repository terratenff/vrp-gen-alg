#!/usr/bin/env python

"""
vrp.py:

Class implementation for the population individual that represents a solution
to the VRP.
"""

import numpy as np


class VRP:
    """
    Implementation for the individual that contains the solution to the VRP
    and some of its extensions. The behaviour of the individuals are defined
    in modules that define population initializers, evaluators, parent selectors,
    crossover operators, mutation operators and validators.
    """

    population_initializer = None
    validator = None
    evaluator = None
    parent_selector = None
    crossover_operator = None
    mutation_operator = None
    invalidity_corrector = None

    id_counter = 0

    def __init__(self,
                 node_count,
                 vehicle_count,
                 depot_node_list,
                 optional_node_list):
        """
        Constructor for an individual of the population. It is upon creation uninitialized.
        :param node_count: Number of nodes considered in the problem. Depot nodes are included.
        :param vehicle_count: Number of vehicles that are used for the problem.
        :param depot_node_list: List of nodes that represent the depot nodes.
        :param optional_node_list: List of nodes that represent optional nodes, ones that
        do not have to be visited.
        """

        self.individual_id = -1
        self.assign_id()

        self.node_count = node_count
        self.vehicle_count = vehicle_count
        self.depot_node_list = depot_node_list
        self.optional_node_list = optional_node_list

        # Problem solution is presented as a list. List elements represent nodes.
        # - Solution starts with a depot node. It also represents the start of a route.
        # - Of any consecutive depot nodes only the rightmost one is considered.
        # - A depot node (or a consecutive collection of them) at the end of the list are not considered.
        self.solution = None

        # In VRPP, optional nodes can remain unvisited. Those are kept here.
        self.unvisited_optional_nodes = optional_node_list

        # Used optional nodes are maintained here.
        self.visited_optional_nodes = []

        # Fitness value of the individual, evaluated by some other module.
        self.fitness = np.inf
        
        # Total profits collected by servicing (usually) optional nodes.
        self.profits = 0

        # With some constraints present, some solutions may not be valid.
        # Validity is check by some other module, and it leaves its mark here.
        self.valid = False

        # For route validity overseeing.
        self.route_distances = []
        self.route_times = []
        self.route_capacities = []

        # Specifically for tracking times at which vehicles depart.
        self.route_start_times = []

        # Waiting times caused by lower-bound time windows are kept here.
        self.route_waiting_times = []

        # Whenever soft time windows are used, incurred penalties are saved here.
        self.route_penalties = []

    def __str__(self):
        return "(VRP ID = {}, Fitness = {}, Valid = {})".format(self.individual_id, self.fitness, self.valid)

    def assign_id(self):
        self.individual_id = VRP.id_counter
        VRP.id_counter += 1

    def assign_solution(self, solution):
        """
        Assigns a solution to the individual. In so doing, potential optional nodes
        are taken into consideration. Validation and evaluation must be done separately.
        :param solution: Proposed solution to the problem.
        """

        self.solution = solution
        self.unvisited_optional_nodes = [i for i in self.optional_node_list if i not in self.solution]
        self.visited_optional_nodes = [i for i in self.optional_node_list if i in self.solution]
        self.fitness = np.inf
        self.valid = False
        self.route_distances = []
        self.route_times = []
        self.route_capacities = []
        self.route_start_times = []
        self.route_waiting_times = []
        self.route_penalties = []

    def get_route_list(self):
        """
        Converts individual's solution into a list of routes that it consists of.
        :return: List of vehicle routes, in which the first element represents the depot node being used.
        """

        vehicle_count = self.vehicle_count
        solution = self.solution
        depot_nodes = self.depot_node_list
        depot_indices = [i for i, x in enumerate(solution) if x in depot_nodes]

        route_list = []
        for i in range(1, vehicle_count):
            route_start = depot_indices[i - 1]
            route_end = depot_indices[i]
            route = solution[route_start:route_end]
            route_list.append(route)

        route_list.append(solution[depot_indices[vehicle_count - 1]:])
        return route_list

    def print(self):
        """
        Prints unique information about the individual.
        """

        route_set = []
        depot_indices = [i for i, x in enumerate(self.solution) if x in self.depot_node_list]
        depot_indices.append(len(self.solution))
        for i in range(1, len(depot_indices)):
            route_j = self.solution[depot_indices[i - 1]:depot_indices[i]]
            if len(route_j) > 1:
                route_set.append(route_j)

        print("-------------------------------------------------")
        print("Individual ID: {} ".format(self.individual_id if self.individual_id is not None else "None"))
        print("- Solution: {}".format(self.solution))
        for i in range(1, len(route_set) + 1):
            print("  - Route {}: {}".format(i, route_set[i - 1]))
            if len(self.route_times) == len(route_set):
                print("    - Time Taken:       {:0.2f}".format(self.route_times[i - 1]))
            if len(self.route_distances) == len(route_set):
                print("    - Total Distance:   {:0.2f}".format(self.route_distances[i - 1]))
            if len(self.route_capacities) != 0:
                if len(self.route_capacities[0]) == len(route_set):
                    appendix_str = " | ".join(["{:0.2f}".format(cap_list[i - 1]) for cap_list in self.route_capacities])
                    print("    - Route Capacity:   {}".format(appendix_str))
            if len(self.route_start_times) == len(route_set):
                if max(self.route_start_times) > 0:
                    print("    - Route Start Time: {:0.2f}".format(self.route_start_times[i - 1]))
            if len(self.route_waiting_times) == len(route_set):
                waiting_str = "    - Waiting Time:"
                waiting_dict = self.route_waiting_times[i - 1]
                print_waiting_times = False
                for key in waiting_dict:
                    if key == route_set[i - 1][1]:
                        # The first node subject to visit involved waiting.
                        # This waiting time was ignored in the final fitness value, so it will be skipped.
                        continue
                    print_waiting_times = True
                    key_value = waiting_dict[key]
                    waiting_str += "\n      - [{}: {:0.2f}]".format(key, key_value)
                if print_waiting_times:
                    print(waiting_str)
            if len(self.route_penalties) == len(route_set):
                penalty_str = "    - Penalties:"
                penalty_dict = self.route_penalties[i - 1]
                print_penalties = False
                for key in penalty_dict:
                    print_penalties = True
                    key_value = penalty_dict[key]
                    penalty_str += "\n      - [{}: {:0.2f}]".format(key, key_value)
                if print_penalties:
                    print(penalty_str)
        print("- Fitness: {:0.2f}".format(self.fitness))
        if self.profits > 0:
            print("- Collected Profits: {:0.2f}".format(self.profits))
        print("- Valid: {}".format(self.valid))
