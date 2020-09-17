#!/usr/bin/env python

"""
params.py:

Class instances for general VRP parameters and algorithm-specific parameters.
"""

import numpy as np


class ParamsVRP:
    """
    General parameters for the subject problem.
    """

    def __init__(self,
                 vrp_contents,
                 vrp_path_table_override=None,
                 vrp_depot_node=0,
                 vrp_vehicle_count=3,
                 vrp_vehicle_variance=0,
                 vrp_node_service_time=0,
                 cvrp_vehicle_capacity=0,
                 cvrp_node_demand=0,
                 ovrp_enabled=False,
                 vrpp_node_profit=None,
                 vrptw_node_time_window=None,
                 vrptw_node_penalty=0
                 ):
        """
        Constructor for general VRP parameters.
        :param vrp_contents: Contents of the VRP. Either a path table or a list of node positions.
        Provide a path table as a NumPy square matrix, preferably with integer elements, since
        floats will be rounded to integers.
        List of node positions can be given with a list of tuples. [(x1,y1), (x2,y2), (x3,y3), ...]
        Support for drawing a map is available for the latter content format.
        :param vrp_path_table_override: Contents that are to be used in the VRP - ONLY IF
        node coordinates are provided as well.
        :param vrp_depot_node: Index of the depot.
        :param vrp_vehicle_count: Number of initial vehicles available for the problem.
        :param vrp_vehicle_variance: Variance of available vehicles for mutations.
        For example, if vehicle count is 4 and vehicle variance is 2, then the number
        of vehicles used for the problem is allowed to vary between the range [4 - 2, 4 + 2].
        :param vrp_node_service_time: Time taken to supply the nodes upon vehicle arrival.
        If given as a single value, every node will have the same service time.
        If given as a list, its length must match total number of nodes, including depot node.
        List index is a node, and the value within is that node's service time.
        :param cvrp_vehicle_capacity: Maximum supply capacity of each vehicle.
        If given as a single value, every vehicle will have the same capacity.
        If given as a list, its length must match total number of vehicles.
        List index is a vehicle, and the value within is that vehicle's supply capacity.
        :param cvrp_node_demand: Supply demand of each node. This is ignored with the depot node.
        If given as a single value, every node will have the same supply demand.
        :param ovrp_enabled: Flag that determines whether the vehicles have to return to the depot
        once they complete their rounds.
        If True, the problem becomes "open", letting vehicles stop at their final destinations.
        If False, the problem is "closed", forcing vehicles to go back to the depot.
        :param vrpp_node_profit: Profit gained from visiting nodes.
        If set to None, VRPP nature of the problem is disabled.
        If given as a single value, every vehicle will yield the same profit.
        If given as a list, its length must match total number of nodes, including depot node.
        List index is a node, and the value within is that node's profit value.
        :param vrptw_node_time_window: Time frames at which a vehicle is expected to visit the node.
        If set to None, this is ignored. TODO: Look into VRPTW.
        :param vrptw_node_penalty: TODO: Look into VRPTW.
        """

        self.vrp_path_table = None
        self.vrp_coordinates = None
        self.set_contents(vrp_contents, path_table_override=vrp_path_table_override)

        self.vrp_vehicle_count = vrp_vehicle_count
        self.vrp_depot_node = vrp_depot_node
        self.vrp_vehicle_variance = vrp_vehicle_variance
        self.vrp_node_service_time = vrp_node_service_time
        self.cvrp_vehicle_capacity = cvrp_vehicle_capacity
        self.cvrp_node_demand = cvrp_node_demand
        self.ovrp_enabled = ovrp_enabled
        self.vrpp_node_profit = vrpp_node_profit
        self.vrptw_node_time_window = vrptw_node_time_window
        self.vrptw_node_penalty = vrptw_node_penalty

    def set_contents(self, contents, path_table_override=None):
        """
        Dedicated setter for VRP contents. This function should always be used
        instead of directly assigning the contents to the member variable 'path_table'.
        :param contents: NumPy array or list of tuples. See constructor comment.
        :param path_table_override: Overriding path table, if list of xy-coordinates
        is given as contents. See constructor comment.
        """

        if isinstance(contents, np.ndarray):
            self.vrp_path_table = contents
            self.vrp_coordinates = None
        elif isinstance(contents, list):
            self.vrp_coordinates = contents
            if path_table_override is not None:
                self.vrp_path_table = path_table_override
            else:
                self.calculate_path_table()
        else:
            raise ValueError("Invalid data type given for 'contents'")

    def calculate_path_table(self):
        """
        Calculates path table from xy-coordinates.
        """

        try:
            nodes = len(self.vrp_coordinates)
            self.vrp_path_table = np.zeros([nodes, nodes], dtype=int)
            for i in range(nodes):
                xy1 = self.vrp_coordinates[i]
                for j in range(nodes):
                    xy2 = self.vrp_coordinates[j]
                    dx = xy2[0] - xy1[0]
                    dy = xy2[1] - xy1[1]
                    self.vrp_path_table[i][j] = np.sqrt(np.square(dx) + np.square(dy), dtype=int)
        except (ValueError, TypeError, IndexError):
            raise ValueError("Invalid data format / Flawed coordinate structure.\n"
                             "Expecting structure of type [(x1,y1), (x2,y2), ...]")

    def print(self):
        """
        Convenience function for printing VRP parameters.
        """

        print("- Instance Parameters ----------------------------------------------------")
        print("VRP   - Node Count                | " + str(len(self.path_table)))
        print("VRP   - Using XY-Coordinates      | " + str(self.coordinates is not None))
        print("VRP   - Vehicle Count             | " + str(self.vehicle_count))
        print("VRP   - Depot Node                | " + str(self.depot_node))
        print("VRP   - Vehicle Variance          | " + str(self.vehicle_variance))
        print("VRP   - Node Service Time         | " + str(self.vrp_node_service_time))
        print("CVRP  - Vehicle Supply Capacity   | " + str(self.cvrp_vehicle_capacity))
        print("CVRP  - Node Supply Demand        | " + str(self.cvrp_node_demand))
        print("OVRP  - Enabled                   | " + str(self.ovrp_enabled))
        print("VRPP  - Node Profit               | " + str(self.vrpp_node_profit))
        print("VRPTW - Node Time Window          | " + str(self.vrptw_node_time_window))
        print("VRPTW - Node Penalty              | " + str(self.vrptw_node_penalty))


class ParamsGEN:
    """
    General parameters for the genetic algorithm.
    """

    def __init__(self,
                 population_count=100,
                 population_initialization=0,
                 fitness_evaluation=0,
                 parent_candidate_count=2,
                 parent_selection_function=0,
                 offspring_pair_count=2,
                 crossover_operator=0,
                 elitism_operator=0):
        """
        Constructor for GA parameters.
        :param population_count: Number of instances that contain the solution for the problem.
        :param population_initialization:
        :param fitness_evaluation:
        :param parent_candidate_count:
        :param parent_selection_function:
        :param offspring_pair_count:
        :param crossover_operator:
        :param elitism_operator:
        """

        self.population_count = population_count
        self.population_initialization = population_initialization
        self.fitness_evaluation = fitness_evaluation
        self.parent_candidate_count = parent_candidate_count
        self.parent_selection_function = parent_selection_function
        self.offspring_pair_count = offspring_pair_count
        self.crossover_operator = crossover_operator
        self.elitism_operator = elitism_operator

        self.str_population_initialization = [
            "Random",
            "Semi-Nearest-Neighbor (depth)",
            "Semi-Nearest-Neighbor (breadth)",
            "1 instance to x mutated variants"
        ]

    def print(self):
        """
        Convenience function for printing GA parameters.
        """

        print("- Algorithm Parameters ---------------------------------------------------")
        print("GEN - Population Count          | " + str(self.population_count))
        print("GEN - Offspring Count           | " + str(self.offspring_count))
        print("GEN - Crossover Function        | " + str(self.crossover_functions[self.crossover_function]))
        print("GEN - Population Retention Rate | " + str(self.retention_rate) + "%")


class ParamsALG:
    """
    TODO
    """

    def __init__(self,
                 generation_count_min=100,
                 generation_count_max=1000,
                 generation_count_repeat=25,
                 goal_min=None,
                 goal_max=None,
                 goal_threshold=0,
                 selection_probability=0.75,
                 crossover_probability=0.90,
                 mutation_probability=0.05,
                 elitism_frequency=0):
        pass

    def print(self):
        print("TODO")
