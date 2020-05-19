#!/usr/bin/env python

"""
cvrp.py:

Class instance for the Capacitated VRP.
"""

import numpy as np
from random import shuffle

from instances.vrp import VRP


class CVRP(VRP):
    """
    CVRP - Capacitated Vehicle Routing Problem.

    Problem description:
    There are n number of cities (nodes) and one depot.
    Each city has to be visited. The travels start and end at the depot.
    You have m number of trucks at your disposal, for the purpose of
    visiting the cities. Each truck can make up to k visits.
    Which trucks should visit where so that total time taken for the
    trucks is as optimal as possible?

    NOTE! Modifying instance variables by directly accessing them is
    discouraged: use functions "set_params" or "set_path_table" instead.
    """

    def __init__(self, path_table, params=None, capacity=9999):
        """
        Constructor for capacitated variant of the problem.
        :param path_table: Integer matrix of costs between nodes.
        :param params: InstanceParams object, contains general problem parameters.
        :param capacity: Capacity for each truck. One unit represents one node,
        excluding the depot node. If given capacity is too low, then it will be
        adjusted to be sufficiently high.
        """

        super(CVRP, self).__init__(path_table, params)
        self.vehicle_capacity = capacity
        if self.params.vehicle_count * self.vehicle_capacity < self.vrp_size - 1:
            # Vehicle count / capacity is too low.
            # (Design decision) Vehicle capacity will be adjusted properly.
            old_capacity = self.vehicle_capacity
            while self.params.vehicle_count * self.vehicle_capacity < self.vrp_size - 1:
                self.vehicle_capacity += 1
            print("NOTE: Vehicle capacity was changed from {0} to {1} to match problem size."
                  .format(old_capacity, self.vehicle_capacity))

    def print(self):
        """
        Prints unique, problem-specific details about itself.
        """

        print("- Vehicle Routing Problem - General Information --------------------------")
        print("Problem Type:     CVRP")
        print("Problem Size:     {0}".format(self.vrp_size))
        print("Path Table Name:  {0}".format(self.table_name))
        print("- Vehicle Routing Problem - Problem-specific Parameters ------------------")
        print("Vehicle Capacity: {0}".format(self.vehicle_capacity))

    def set_path_table(self, matrix):
        # Upon setting a new path table, current vehicle capacity may not be enough.
        # That will be checked here.
        if self.params.vehicle_count * self.vehicle_capacity < len(matrix) - 1:
            # Vehicle count / capacity is too low.
            # (Design decision) Vehicle capacity will be adjusted properly.
            old_capacity = self.vehicle_capacity
            while self.params.vehicle_count * self.vehicle_capacity < len(matrix) - 1:
                self.vehicle_capacity += 1
            print("NOTE: Vehicle capacity was changed from {0} to {1} to match problem size."
                  .format(old_capacity, self.vehicle_capacity))
        super(CVRP, self).set_path_table(matrix)

    def set_params(self, params):
        # If vehicle count is lowered, then vehicle capacity may have
        # to be increased.
        if params.vehicle_count * self.vehicle_capacity < self.vrp_size - 1:
            # Vehicle capacity is too low.
            # (Design decision) Vehicle capacity will be adjusted properly.
            old_capacity = self.vehicle_capacity
            while params.vehicle_count * self.vehicle_capacity < self.vrp_size - 1:
                self.vehicle_capacity += 1
            print("NOTE: Vehicle capacity was changed from {0} to {1} to match problem size."
                  .format(old_capacity, self.vehicle_capacity))
        super(CVRP, self).set_params(params)

    def transfer_node(self):
        super(CVRP, self).transfer_node()

        # Node transfer has been performed, as usual.
        # Now we check if vehicle capacity has been exceeded.
        longest_path = max((self.routes[i_path] for i_path in range(len(self.routes))), key=len)
        if len(longest_path) > self.vehicle_capacity:
            # Vehicle capacity has exceeded. Default course of action is to
            # transfer a node from it to the one with the least nodes.
            print("NOTE (CVRP): Vehicle capacity exceeded. Another transfer was performed.")
            shortest_path = min((self.routes[i_path] for i_path in range(len(self.routes))), key=len)

            # Collect path indexes.
            long_index = self.routes.index(longest_path)
            short_index = self.routes.index(shortest_path)

            print("Vehicle {0}: ({1}) {2}".format(long_index + 1, len(longest_path), longest_path))
            print("Vehicle {0}: ({1}) {2}".format(short_index + 1, len(shortest_path), shortest_path))

            # Select two random indexes.
            i1 = np.random.randint(0, len(self.routes[long_index]))
            i2 = np.random.randint(0, len(self.routes[short_index]))

            # Get the node of the first index.
            subject = self.routes[long_index][i1]

            # Transfer the node into the route specified by the second index.
            self.routes[short_index].insert(i2, subject)
            self.routes[long_index].remove(subject)

    def merge_two_routes(self):
        print("Mutation: 'merge_two_routes'")

        # If given vehicle capacity is strict, merges should not usually
        # be possible. Here, a hard-coded number of merging attempts is made.
        attempt_count = 3
        for i in range(attempt_count):
            # Select two random routes.
            path1 = np.random.randint(0, len(self.routes))
            path2 = np.random.randint(0, len(self.routes))

            # Check if the routes are the same.
            if path1 == path2:
                # Select the next route in the proposed solution.
                path2 = (path2 + 1) % len(self.routes)

            # Check if proposed paths exceed vehicle capacity.
            if len(self.routes[path1]) + len(self.routes[path2]) <= self.vehicle_capacity:
                # Merge selected routes by appending them.
                appended_list = self.routes[path1] + self.routes[path2]

                # Assign appended route into one and delete the other.
                self.routes[path1] = appended_list
                del self.routes[path2]

                # Merging was successful. End procedure here.
                break
        print("NOTE (CVRP): Merging failed - too many unsuccessful attempts.")
