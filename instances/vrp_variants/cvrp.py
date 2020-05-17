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
        if self.params.vehicle_count * self.vehicle_capacity < self.vrp_size:
            # Vehicle count / capacity is too low.
            # (Design decision) Vehicle capacity will be adjusted properly.
            old_capacity = self.vehicle_capacity
            while self.params.vehicle_count * self.vehicle_capacity < self.vrp_size:
                self.vehicle_capacity += 1
            print("NOTE: Vehicle capacity was changed from {0} to {0} to match problem size."
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

    def transfer_node(self):
        # TODO: Take vehicle capacity into account.
        super(CVRP, self).transfer_node()

    def merge_two_routes(self):
        # TODO: Take vehicle capacity into account.
        super(CVRP, self).merge_two_routes()
