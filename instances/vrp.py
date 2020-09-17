#!/usr/bin/env python

"""
vrp.py:

Class instance for the base VRP.
"""

import numpy as np
from random import shuffle

from instances.params import InstanceParams


class VRP:
    """
    VRP - Vehicle Routing Problem. The base problem.
    
    Problem description:
    There are n number of cities (nodes) and one depot.
    Each city has to be visited. The travels start and end at the depot.
    You have m number of trucks at your disposal, for the purpose of
    visiting the cities. Which trucks should visit where so that total
    time taken for the trucks is as optimal as possible?
    """

    def __init__(self, path_table, params=None):
        """
        Constructor for the base problem.
        :param path_table: Integer matrix of costs between nodes.
        :param params: InstanceParams object, contains general problem parameters.
        """

        # Distances between nodes.
        self.path_table = path_table

        # Path table name. Purely cosmetic.
        self.table_name = "sample"

        # Instance parameters. Use default values if not provided/valid.
        self.params = params
        if self.params is None or isinstance(self.params, InstanceParams) is False:
            self.params = InstanceParams()

        # Node count.
        self.vrp_size = len(self.path_table)

        # Fitness value.
        self.fitness = 0

        # Route costs of the proposed solution.
        self.route_costs = []

        # List of routes that describe the proposed solution with nodes.
        self.routes = []

        # Initialize proposed solution with empty routes.
        for i in range(0, self.params.vehicle_count):
            self.routes.append([])

        # Collect a list of target nodes, excluding depot node, and shuffle them.
        unused_nodes = list(range(0, self.vrp_size))
        unused_nodes.remove(self.params.depot_node)
        shuffle(unused_nodes)

        # Distribute shuffled nodes into empty routes, creating a solution.
        for i in range(0, self.vrp_size - 1):
            self.routes[i % self.params.vehicle_count].append(unused_nodes[0])
            del unused_nodes[0]
            if len(unused_nodes) == 0:
                break
        self.refresh()

    def print(self):
        """
        Prints unique, problem-specific details about itself.
        """

        print("- Vehicle Routing Problem - General Information --------------------------")
        print("Problem Type:    VRP")
        print("Problem Size:    {0}".format(self.vrp_size))
        print("Path Table Name: {0}".format(self.table_name))
        print("- Vehicle Routing Problem - Problem-specific Parameters ------------------")
        print("None")

    def set_path_table(self, matrix):
        """
        Appropriate setter for the path table.
        :param matrix: Path table
        """

        self.path_table = matrix
        self.vrp_size = len(self.path_table)

        # Invariant: number of vehicles should not exceed VRP size (excluding depot).
        if self.vrp_size - 1 < self.params.vehicle_count:
            old_value = self.params.vehicle_count
            self.params.vehicle_count = self.vrp_size - 1
            print("NOTE: Vehicle count changed from {0} to {1} to match node count.".format(old_value,
                                                                                            self.params.vehicle_count))
        self.refresh(reset=True)

    def set_params(self, params):
        """
        Appropriate setter for problem parameters.
        :param params: InstanceParams-object. If not, default parameters are set.
        """

        self.params = params
        if self.params is None or isinstance(self.params, InstanceParams) is False:
            self.params = InstanceParams()

        # Invariant: number of vehicles should not exceed VRP size (excluding depot).
        if self.vrp_size - 1 < self.params.vehicle_count:
            old_value = self.params.vehicle_count
            self.params.vehicle_count = self.vrp_size - 1
            print("NOTE: Vehicle count changed from {0} to {1} to match node count.".format(old_value,
                                                                                            self.params.vehicle_count))
        self.refresh(reset=True)

    def refresh(self, reset=False):
        """
        Calculates the fitness value of the proposed solution.
        :param reset: Flag for further initializations.
        """

        # Perform extra initializations if reset is set to True.
        if reset is True:
            # List of routes that describe the proposed solution with nodes.
            self.routes = []

            # Initialize proposed solution with empty routes.
            for i in range(0, self.params.vehicle_count):
                self.routes.append([])

            # Collect a list of target nodes, excluding depot node, and shuffle them.
            unused_nodes = list(range(0, self.vrp_size))
            unused_nodes.remove(self.params.depot_node)
            shuffle(unused_nodes)

            # Distribute shuffled nodes into empty routes, creating a solution.
            for i in range(0, self.vrp_size - 1):
                self.routes[i % self.params.vehicle_count].append(unused_nodes[0])
                del unused_nodes[0]
                if len(unused_nodes) == 0:
                    break

        # Reset route costs and fitness.
        self.route_costs = []
        self.fitness = 0

        # Evaluate every route of the proposed solution.
        for i in range(0, len(self.routes)):

            # Zero cost at the beginning.
            self.route_costs.append(0)

            # Select a route (list of nodes) to iterate.
            route_list = self.routes[i]

            # Placeholder variable.
            prev = 0

            # Iterate selected route.
            for j in range(0, len(route_list) + 1):
                if j == len(route_list):
                    # Reached the end of the route.
                    self.route_costs[i] += self.path_table[prev][self.params.depot_node]
                    continue
                k = route_list[j]
                if j == 0:
                    # The beginning of the route.
                    self.route_costs[i] += self.path_table[self.params.depot_node][k]
                else:
                    # Elsewhere in the route.
                    self.route_costs[i] += self.path_table[prev][k]
                prev = k

        # The fitness value is the highest individual cost of all the routes.
        self.fitness = max(self.route_costs)

    def print_solution(self):
        """
        Convenient function for printing the proposed solution.
        """

        # Refresh object instance in case it is out-of-date.
        if self.fitness is None:
            self.refresh()

        print("Fitness: " + str(self.fitness))
        vehicle = 1  # Index 0 is vehicle 1.

        # Iterate every route for the printing.
        for i in range(0, len(self.routes)):
            vehicle_route = self.routes[i]
            route_cost = self.route_costs[i]
            print("Vehicle {0}: ({1} Nodes) {2} (Cost: {3})".format(vehicle,
                                                                    len(vehicle_route),
                                                                    vehicle_route,
                                                                    route_cost))
            vehicle += 1

    def _select_mutation(self, max_choices):
        """
        Acts as a selector for a mutation function.
        :param max_choices: Number of available mutation functions.
        :return: Integer representing a randomly selected mutation function.
        """

        # Proposed solution is going to be mutated: fitness value should be reset.
        self.fitness = None

        # Determine what kind of mutation should be done.
        action = np.random.randint(0, max_choices)
        return action

    def mutate(self):
        """
        Mutates the proposed solution.
        """

        # Start by selecting mutation function.
        action = self._select_mutation(5)  # Five different mutation functions for basic VRP.
        if action == 0:

            # Mutation function 1: Swap two nodes within a route.
            self.swap_nodes_one_route()

        elif action == 1:

            # Mutation function 2: Swap two nodes between two routes.
            self.swap_nodes_two_routes()

        elif action == 2:

            # Mutation function 3: Transfer a node to another route.
            self.transfer_node()

        elif action == 3:

            # Mutation function 4: Either 4a or 4b.
            if len(self.routes) == self.params.vehicle_count - self.params.vehicle_variance:

                # Mutation function 4a: Swap two nodes between two routes 3 times.
                for i in range(0, 3):
                    self.swap_nodes_two_routes()

            else:

                # Mutation function 4b: Merge two routes into one. Non-zero vehicle variance required.
                self.merge_two_routes()

        elif action == 4:

            # Mutation function 5: Either 5a or 5b.
            if len(self.routes) == self.params.vehicle_count + self.params.vehicle_variance:

                # Mutation function 5a: Shuffle a route.
                self.shuffle_route()

            else:

                # Mutation function 5b: Split a route into two. Non-zero vehicle variance required.
                self.split_to_two_routes()

        # Refresh to update fitness.
        self.refresh()

    def swap_nodes_one_route(self):
        """
        Selects two nodes randomly within a randomly selected route,
        and swaps their places. Mutation function.
        """

        print("Mutation: 'swap_nodes_one_route'")

        # Select random route.
        path = np.random.randint(0, len(self.routes))

        # Select random nodes in selected route.
        i1 = np.random.randint(0, len(self.routes[path]))
        i2 = np.random.randint(0, len(self.routes[path]))

        # Check if selected nodes are the same.
        if i1 == i2:
            # Select the next node in the route.
            i2 = (i2 + 1) % len(self.routes[path])

        # Swap selected nodes.
        self.routes[path][i1], self.routes[path][i2] = self.routes[path][i2], self.routes[path][i1]

    def swap_nodes_two_routes(self):
        """
        Selects random two routes and one node from each,
        and swaps their places. Mutation function.
        """

        print("Mutation: 'swap_nodes_two_routes'")

        # Select random routes.
        path1 = np.random.randint(0, len(self.routes))
        path2 = np.random.randint(0, len(self.routes))

        # Check if the routes are the same.
        if path1 == path2:
            # Select the next route in the proposed solution.
            path2 = (path2 + 1) % len(self.routes)

        # Select one random node from each selected route.
        i1 = np.random.randint(0, len(self.routes[path1]))
        i2 = np.random.randint(0, len(self.routes[path2]))

        # Swap selected nodes.
        self.routes[path1][i1], self.routes[path2][i2] = self.routes[path2][i2], self.routes[path1][i1]

    def transfer_node(self):
        """
        Selects a random node from a random route,
        and places it to another random route. Mutation function.
        """

        print("Mutation: 'transfer_node'")

        # Select two random routes.
        path1 = np.random.randint(0, len(self.routes))

        # Check if path 1 has any nodes to transfer.
        if len(self.routes[path1]) == 1:
            # Only one node. Transferring that elsewhere is equivalent to merging.
            # Determine highest number of nodes in one.
            longest_path = max((self.routes[i_path] for i_path in range(len(self.routes))), key=len)

            # Check the size.
            if len(longest_path) > 1:
                # Mutation goes on!
                path1 = self.routes.index(longest_path)
            else:
                # Mutation is cancelled.
                print("NOTE: Mutation 'transfer_node' was skipped.")
                return

        path2 = np.random.randint(0, len(self.routes))

        # Check if the routes are the same.
        if path1 == path2:
            # Select the next route in the proposed solution.
            path2 = (path2 + 1) % len(self.routes)

        # Select two random indexes.
        i1 = np.random.randint(0, len(self.routes[path1]))
        i2 = np.random.randint(0, len(self.routes[path2]))

        # Get the node of the first index.
        subject = self.routes[path1][i1]

        # Transfer the node into the route specified by the second index.
        self.routes[path2].insert(i2, subject)
        self.routes[path1].remove(subject)

    def merge_two_routes(self):
        """
        Selects two random routes and combines them into one.
        Mutation function. Non-zero vehicle variance required.
        """

        print("Mutation: 'merge_two_routes'")

        # Select two random routes.
        path1 = np.random.randint(0, len(self.routes))
        path2 = np.random.randint(0, len(self.routes))

        # Check if the routes are the same.
        if path1 == path2:
            # Select the next route in the proposed solution.
            path2 = (path2 + 1) % len(self.routes)

        # Merge selected routes by appending them.
        appended_list = self.routes[path1] + self.routes[path2]

        # Assign appended route into one and delete the other.
        self.routes[path1] = appended_list
        del self.routes[path2]

    def split_to_two_routes(self):
        """
        Selects a random route and splits it into two.
        Mutation Function. Non-zero vehicle variance required.
        """

        print("Mutation: 'split_to_two_routes'")

        # Select a random route.
        path = np.random.randint(0, len(self.routes))

        # Check if the route consists of only one node (which cannot be split)
        if len(self.routes[path]) == 1:
            # Select the longest existing route.
            longest_path = max(len(self.routes[i_path]) for i_path in range(0, len(self.routes)))

            # Check again. If a suitable route could not be found, mutation process is skipped.
            if len(self.routes[longest_path]) != 1:
                # Set a point where the splitting is done.
                divider = longest_path
            else:
                print("NOTE: Mutation 'split_to_two_routes' was skipped.")
                return
        else:
            # Set a point where the splitting is done.
            divider = np.random.randint(1, len(self.routes[path]))

        # Collect two smaller routes from the target route.
        sub_path1 = self.routes[path][:divider]
        sub_path2 = self.routes[path][divider:]

        # Replace route with two smaller ones.
        del self.routes[path]
        self.routes.append(sub_path1)
        self.routes.append(sub_path2)

    def shuffle_route(self):
        """
        Shuffles a random route. Mutation function.
        """

        print("Mutation: 'shuffle_route'")

        path = np.random.randint(0, len(self.routes))
        shuffle(self.routes[path])
