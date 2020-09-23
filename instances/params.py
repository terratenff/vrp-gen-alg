#!/usr/bin/env python

"""
params.py:

Class instances for general VRP parameters and genetic algorithm parameters.
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
                 vrp_node_service_time=None,
                 vrp_distance_time_ratio=1,
                 cvrp_vehicle_capacity=0,
                 cvrp_node_demand=None,
                 ovrp_enabled=False,
                 vrpp_node_profit=None,
                 vrptw_node_time_window=None,
                 vrptw_node_penalty=None
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
        :param vrp_distance_time_ratio: Conversion rate from distance to time.
        Example values: Ratio 1 converts 1 distance unit to 1 time unit.
        Ratio 5 converts every 5 distance units to 1 time unit. Integer division by 5 is performed.
        Ratio -10 converts 1 distance unit into 10 time units. Integer multiplication by 10 is performed.
        Use integers only. If set to zero, distance units do not convert to time; in other words,
        any amount of distance converts to 0 time units.
        :param cvrp_vehicle_capacity: Maximum supply capacity of each vehicle.
        If given as a single value, every vehicle will have the same capacity.
        If given as a list, its length must match total number of vehicles.
        List index is a vehicle, and the value within is that vehicle's supply capacity.
        :param cvrp_node_demand: Supply demand of each node. This is ignored with the depot node.
        A single integer value is expected: it is assumed that every vehicle has the same capacity.
        :param ovrp_enabled: Flag that determines whether the vehicles have to return to the depot
        once they complete their rounds.
        If True, the problem becomes "open", letting vehicles stop at their final destinations.
        If False, the problem is "closed", forcing vehicles to go back to the depot.
        :param vrpp_node_profit: Profit gained from visiting nodes.
        If set to None, VRPP nature of the problem is disabled.
        If given as a single value, every vehicle will yield the same profit.
        If given as a list, its length must match total number of nodes, including depot node.
        List index is a node, and the value within is that node's profit value.
        :param vrptw_node_time_window: Time frames at which a vehicle is expected to visit the node:
        if a vehicle arrives too early, it will have to wait for the time window to take place.
        If time windows are to be used, provide a list of tuples, totaling to the number of nodes,
        including the depot node (recommended time window for depot node is between 0 and maximum time
        that a vehicle is allowed to be out for).
        Expected tuple-list format: [(start0, end0), (start1, end1), (start2, end2), ...]
        If set to None, this is ignored.
        :param vrptw_node_penalty: Coefficient that determines the scale of the penalty value.
        Penalty value is based on how late a vehicle arrives at a node.
        This is used ONLY IF time windows are being used.
        If given as a single value, every node will have the same penalty coefficient.
        If given as a list, its length must match total number of nodes, including the depot node.
        List index is a node, and the value within is that node's penalty coefficient.
        """

        self.coordinates_name = None
        self.cost_matrices_name = "undefined"
        self.node_demands_name = None
        self.node_penalties_name = None
        self.node_profits_name = None
        self.node_service_times_name = None
        self.node_time_windows_name = None

        self.vrp_path_table = None
        self.vrp_coordinates = None
        self.set_contents(vrp_contents, path_table_override=vrp_path_table_override)

        self.vrp_vehicle_count = vrp_vehicle_count
        self.vrp_depot_node = vrp_depot_node
        self.vrp_vehicle_variance = vrp_vehicle_variance
        self.vrp_node_service_time = vrp_node_service_time
        self.vrp_distance_time_ratio = vrp_distance_time_ratio
        self.cvrp_vehicle_capacity = cvrp_vehicle_capacity
        self.cvrp_node_demand = cvrp_node_demand
        self.ovrp_enabled = ovrp_enabled
        self.vrpp_node_profit = vrpp_node_profit
        self.vrptw_node_time_window = vrptw_node_time_window
        self.vrptw_node_penalty = vrptw_node_penalty

    def set_contents(self, contents, path_table_override=None, name=None):
        """
        Dedicated setter for VRP contents. This function should always be used
        instead of directly assigning the contents to the member variable 'path_table'.
        :param contents: NumPy array or list of tuples. See constructor comment.
        :param path_table_override: Overriding path table, if list of xy-coordinates
        is given as contents. See constructor comment.
        :param name: A name to call the contents by. Cosmetic.
        """

        if contents.shape[0] == contents.shape[1]:
            self.vrp_path_table = contents
            self.vrp_coordinates = None
            if name is not None:
                self.cost_matrices_name = name
            else:
                self.cost_matrices_name = "undefined"
        elif contents.shape[1] == 2 and contents.shape[0] != contents.shape[1]:
            self.vrp_coordinates = contents
            if path_table_override is not None:
                self.vrp_path_table = path_table_override
                self.cost_matrices_name = name
            else:
                self.calculate_path_table()
                self.cost_matrices_name = "undefined"
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
                    self.vrp_path_table[i][j] = round(np.sqrt([dx * dx + dy * dy])[0])
        except (ValueError, TypeError, IndexError):
            raise ValueError("Invalid data format / Flawed coordinate structure.\n"
                             "Expecting structure of type [(x1,y1), (x2,y2), ...]")

    def print(self):
        """
        Convenience function for printing VRP parameters.
        """

        if self.vrp_node_service_time is None:
            nst_str = None
        else:
            nst_str = self.vrp_node_service_time.tolist()

        if self.cvrp_node_demand is None:
            nd_str = None
        else:
            nd_str = self.cvrp_node_demand.tolist()

        if self.vrpp_node_profit is None:
            np_str = None
        else:
            np_str = self.vrpp_node_profit.tolist()

        if self.vrptw_node_time_window is None:
            ntw_str = None
        else:
            ntw_str = list(map(tuple, self.vrptw_node_time_window))

        if self.vrptw_node_penalty is None:
            np2_str = None
        else:
            np2_str = self.vrptw_node_penalty.tolist()

        if self.vrp_distance_time_ratio > 0:
            conversion_str = "{} to 1".format(str(self.vrp_distance_time_ratio))
        elif self.vrp_distance_time_ratio < 0:
            conversion_str = "1 to {}".format(str(self.vrp_distance_time_ratio * (-1)))
        else:
            conversion_str = "Does not convert to time"

        print("- Problem Parameters ----------------------------------------------------")
        print("VRP   - Node Count                | {}".format(len(self.vrp_path_table)))
        print("VRP   - Using XY-Coordinates      | {}".format(self.vrp_coordinates is not None))
        print("VRP   - Vehicle Count             | {}".format(self.vrp_vehicle_count))
        print("VRP   - Depot Node                | {}".format(self.vrp_depot_node))
        print("VRP   - Vehicle Variance          | {}".format(self.vrp_vehicle_variance))
        print("VRP   - Node Service Time         | {}".format(nst_str))
        print("VRP   - Distance-to-Time Ratio    | {}".format(conversion_str))
        print("CVRP  - Vehicle Supply Capacity   | {}".format(self.cvrp_vehicle_capacity))
        print("CVRP  - Node Supply Demand        | {}".format(nd_str))
        print("OVRP  - Enabled                   | {}".format(self.ovrp_enabled))
        print("VRPP  - Node Profit               | {}".format(np_str))
        print("VRPTW - Node Time Window          | {}".format(ntw_str))
        print("VRPTW - Node Penalty Coefficient  | {}".format(np2_str))


class ParamsGENALG:
    """
    Parameters for the genetic algorithm.
    """

    def __init__(self,
                 population_count=100,
                 generation_count_min=10,
                 generation_count_max=100,
                 fitness_evaluator=0,
                 parent_candidate_count=2,
                 parent_selection_function=0,
                 selection_probability=0.75,
                 offspring_pair_count=1,
                 crossover_operator=0,
                 crossover_probability=0.90,
                 mutation_probability=0.05,
                 followup_probability=0.70,
                 elitism_operator=0,
                 elitism_frequency=0):
        """
        Constructor for GA parameters.
        :param population_count: Number of instances that contain the solution for the problem.
        :param generation_count_min: Number of generations that must be created before termination.
        :param generation_count_max: Number of generations that cannot be exceeded.
        :param fitness_evaluator: Objective fitness function.
        :param parent_candidate_count: Determines how many individuals are selected from the population
        as candidates to becoming parents of the next generation.
        :param parent_selection_function: Function that decides how individuals are chosen to be
        parents of the next generation.
        :param selection_probability: Probability of the leading candidate parent (in terms of fitness)
        to be selected. Relevant in 'Tournament' and 'Best Fitness'.
        :param offspring_pair_count: The number of offsprings (in terms of pairs) that are to be
        created by a single instance of parents. Once set number of pairs have been created, another
        set of parents are selected to create the same number of pairs.
        :param crossover_operator: Function that controls the crossover operation.
        :param crossover_probability: Probability of performing a crossover operation on the offspring
        of the selected parents. If crossover does not occur, offspring are exact replicas of the parents.
        :param mutation_probability: Probability of mutating an individual offspring upon its creation.
        The probability is for one node. If mutation does not occur, the node is skipped.
        Otherwise a followup check is performed.
        :param followup_probability: Probability of mutating a node instead of something else.
        If a roll favors a node, that is marked for mutation. If ultimately only one node was
        marked, another one will be marked at random. Marked nodes are then rearranged.
        If a roll does not favor a node, some other elements are modified, examples being
        changing vehicle counts, including/excluding nodes (VRPP)
        and changing vehicle departure times (VRPTW).
        :param elitism_operator: Function that does something to mitigate elitism (or not).
        :param elitism_frequency: Determines how frequently elitism is handled (for or against).
        Number represents generations: if set to 10, then for every 10 generations, elitism operator
        is requested. At 0 (or less), the matter is ignored.
        """

        self.population_count = population_count
        self.generation_count_min = generation_count_min
        self.generation_count_max = generation_count_max
        self.fitness_evaluator = fitness_evaluator
        self.parent_candidate_count = parent_candidate_count
        self.parent_selection_function = parent_selection_function
        self.selection_probability = selection_probability
        self.offspring_pair_count = offspring_pair_count
        self.crossover_operator = crossover_operator
        self.crossover_probability = crossover_probability
        self.mutation_probability = mutation_probability
        self.followup_probability = followup_probability
        self.elitism_operator = elitism_operator
        self.elitism_frequency = elitism_frequency

        self.str_fitness_evaluator = [
            "Total Cost",
            "Total Distance",
            "Longest Route"
        ]
        self.str_parent_selection_function = [
            "Best Fitness",
            "Roulette Wheel",
            "Tournament"
        ]
        self.str_crossover_operator = [
            "1-Point",
            "2-Point",
            "Uniform",
            "OE-Children"
        ]
        self.str_elitism_operator = [
            "None",
            "Retention",
            "Filtration"
        ]

    def print(self):
        """
        Convenience function for printing GA parameters.
        """

        fit_str = self.str_fitness_evaluator[self.fitness_evaluator]
        par_sel_str = self.str_parent_selection_function[self.parent_selection_function]
        cross_str = self.str_crossover_operator[self.crossover_operator]
        elite_str = self.str_elitism_operator[self.elitism_operator]

        if self.elitism_frequency <= 0:
            elite_fr_str = "Never"
        elif self.elitism_frequency == 1:
            elite_fr_str = "Every Generation"
        else:
            elite_fr_str = "Every {} Generations".format(self.elitism_frequency)

        print("- Genetic Algorithm Parameters ---------------------------------------------------")
        print("GEN - Population Count          | {}".format(self.population_count))
        print("GEN - Minimum Generation Count  | {}".format(self.generation_count_min))
        print("GEN - Maximum Generation Count  | {}".format(self.generation_count_max))
        print("ALG - Fitness Evaluator         | {}".format(fit_str))
        print("GEN - Parent Candidate Count    | {}".format(self.parent_candidate_count))
        print("ALG - Parent Selection Function | {}".format(par_sel_str))
        print("GEN - Selection Probability     | {:0.2f}".format(self.selection_probability))
        print("GEN - Offspring Pair Count      | {}".format(self.offspring_pair_count))
        print("ALG - Crossover Operator        | {}".format(cross_str))
        print("GEN - Crossover Probability     | {:0.2f}".format(self.crossover_probability))
        print("GEN - Mutation Probability      | {:0.2f}".format(self.mutation_probability))
        print("GEN - Followup Probability      | {:0.2f}".format(self.followup_probability))
        print("ALG - Elitism Managing Operator | {}".format(elite_str))
        print("GEN - Elitism Management Rate   | {}".format(elite_fr_str))
