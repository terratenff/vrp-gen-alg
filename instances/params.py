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
                 vrp_vehicle_count=3,
                 vrp_node_service_time=None,
                 vrp_maximum_route_time=None,
                 vrp_maximum_route_distance=None,
                 vrp_distance_time_ratio=1,
                 vrp_time_cost_ratio=1,
                 vrp_distance_cost_ratio=1,
                 cvrp_vehicle_capacity=0,
                 cvrp_node_demand=None,
                 ovrp_enabled=False,
                 vrpp_node_profit=None,
                 vrpp_optional_node=None,
                 vrpp_exclude_travel_costs=False,
                 mdvrp_depot_node=None,
                 vrptw_node_time_window=None,
                 vrptw_node_penalty=None,
                 vrptw_hard_windows=False
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

        :param vrp_vehicle_count: Number of vehicles that are to be used for the problem.

        :param vrp_node_service_time: Time taken to supply the nodes upon vehicle arrival.
        If given as a single value, every node will have the same service time.
        If given as a list, its length must match total number of nodes, including depot node.
        List index is a node, and the value within is that node's service time.

        :param vrp_maximum_route_time: Determines the time that each vehicle is allowed to spend
        on their routes. If this limit is exceeded, the solution the vehicles represent is invalid.
        If set to None, no limit is set.

        :param vrp_maximum_route_distance: Determines the total distance that each vehicle is allowed
        to move on their routes. If this limit is exceeded, the solution the vehicles represent is invalid.
        If set to None, no limit is set.

        :param vrp_distance_time_ratio: Conversion rate from distance to time. Multiply by -1 for reverse operation.
        Example values: Ratio 1 converts 1 distance unit to 1 time unit.
        Ratio 5 converts every 5 distance units to 1 time unit. Integer division by 5 is performed.
        Ratio -10 converts 1 distance unit into 10 time units. Integer multiplication by 10 is performed.
        Use integers only. If set to zero, distance units do not convert to time; in other words,
        any amount of distance converts to 0 time units.

        :param vrp_time_cost_ratio: Conversion rate from time to cost. Multiply by -1 for reverse operation.
        See vrp_distance_time_ratio for more details.

        :param vrp_distance_cost_ratio: Conversion rate from distance to cost. Multiply by -1 for reverse operation.
        See vrp_distance_time_ratio for more details.

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
        If given as a list, its length must match total number of nodes, including depot nodes.
        List index is a node, and the value within is that node's profit value.

        :param vrpp_optional_node: List of nodes that are considered optional, meaning that these nodes
        do not have to be visited.

        :param vrpp_exclude_travel_costs: Determines whether travel costs should be taken into account while
        assessing the fitness value. If set to True, they are ignored, making the problem a TOP. If set to False,
        they are considered, making the problem a PTP.

        :param mdvrp_depot_node: List of nodes that are to be treated like depot nodes.

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

        :param vrptw_hard_windows: Determines whether every single time window is a hard time window. If set to True,
        every time window is hard, and in so doing, those that violate the time window are cast aside. If set to False,
        the nature of the time windows is based on penalty coefficients. This variable is meant to boost algorithm
        efficiency for hard time window problems.
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
        self.vrp_node_service_time = vrp_node_service_time
        self.vrp_maximum_route_time = vrp_maximum_route_time
        self.vrp_maximum_route_distance = vrp_maximum_route_distance
        self.vrp_distance_time_ratio = vrp_distance_time_ratio
        self.vrp_time_cost_ratio = vrp_time_cost_ratio
        self.vrp_distance_cost_ratio = vrp_distance_cost_ratio

        self.cvrp_vehicle_capacity = cvrp_vehicle_capacity
        self.cvrp_node_demand = cvrp_node_demand

        self.ovrp_enabled = ovrp_enabled

        self.vrpp_node_profit = vrpp_node_profit
        self.vrpp_exclude_travel_costs = vrpp_exclude_travel_costs
        self.vrpp_optional_node = vrpp_optional_node

        if mdvrp_depot_node is None:
            self.mdvrp_depot_node = [0]
        else:
            self.mdvrp_depot_node = mdvrp_depot_node

        self.vrptw_node_time_window = vrptw_node_time_window
        self.vrptw_node_penalty = vrptw_node_penalty
        self.vrptw_hard_windows = vrptw_hard_windows

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
            nst_str = self.node_service_times_name + ": " + str(self.vrp_node_service_time).replace("\n", "")

        if self.cvrp_node_demand is None:
            nd_str = None
        else:
            nd_str = self.node_demands_name + ": " + str(self.cvrp_node_demand).replace("\n", "")

        if self.vrpp_node_profit is None:
            np_str = None
        else:
            np_str = self.node_profits_name + ": " + str(self.vrpp_node_profit).replace("\n", "")

        if self.vrptw_node_time_window is None:
            ntw_str = None
        else:
            ntw_str = self.node_time_windows_name + \
                      ": " + str(list(map(tuple, self.vrptw_node_time_window))).replace("\n", "")

        if self.vrptw_node_penalty is None:
            np2_str = None
        else:
            np2_str = self.node_penalties_name + ": " + str(self.vrptw_node_penalty) \
                .replace("\n", "")

        if self.vrp_distance_time_ratio > 0:
            conversion1_str = "{} to 1".format(str(self.vrp_distance_time_ratio))
        elif self.vrp_distance_time_ratio < 0:
            conversion1_str = "1 to {}".format(str(self.vrp_distance_time_ratio * (-1)))
        else:
            conversion1_str = "Does not convert to time"

        if self.vrp_time_cost_ratio > 0:
            conversion2_str = "{} to 1".format(str(self.vrp_time_cost_ratio))
        elif self.vrp_time_cost_ratio < 0:
            conversion2_str = "1 to {}".format(str(self.vrp_time_cost_ratio * (-1)))
        else:
            conversion2_str = "Does not convert to cost"

        if self.vrp_distance_cost_ratio > 0:
            conversion3_str = "{} to 1".format(str(self.vrp_distance_cost_ratio))
        elif self.vrp_distance_cost_ratio < 0:
            conversion3_str = "1 to {}".format(str(self.vrp_distance_cost_ratio * (-1)))
        else:
            conversion3_str = "Does not convert to cost"

        print("- Problem Parameters ----------------------------------------------------")
        print("VRP   - Node Count                | {}".format(len(self.vrp_path_table)))
        print("VRP   - Using XY-Coordinates      | {}".format(self.vrp_coordinates is not None))
        print("VRP   - Vehicle Count             | {}".format(self.vrp_vehicle_count))
        print("VRP   - Node Service Time         | {}".format(nst_str))
        print("VRP   - Maximum Route Time        | {}".format(self.vrp_maximum_route_time))
        print("VRP   - Maximum Route Distance    | {}".format(self.vrp_maximum_route_distance))
        print("VRP   - Distance-to-Time Ratio    | {}".format(conversion1_str))
        print("VRP   - Time-to-Cost Ratio        | {}".format(conversion2_str))
        print("VRP   - Distance-to-Cost Ratio    | {}".format(conversion3_str))
        print("CVRP  - Vehicle Supply Capacity   | {}".format(self.cvrp_vehicle_capacity))
        print("CVRP  - Node Supply Demand        | {}".format(nd_str))
        print("OVRP  - Enable Open Routes        | {}".format(self.ovrp_enabled))
        print("VRPP  - Node Profit               | {}".format(np_str))
        print("VRPP  - Exclude Travel Costs      | {}".format(str(self.vrpp_exclude_travel_costs)))
        print("VRPP  - Optional Nodes            | {}".format(str(self.vrpp_optional_node)))
        print("MDVRP - Depot Nodes               | {}".format(str(self.mdvrp_depot_node)))
        print("VRPTW - Node Time Window          | {}".format(ntw_str))
        print("VRPTW - Node Penalty Coefficient  | {}".format(np2_str))
        print("VRPTW - Hard Time Windows         | {}".format(str(self.vrptw_hard_windows)))


class ParamsGENALG:
    """
    Parameters for the genetic algorithm.
    """

    def __init__(self,
                 population_count=100,
                 population_initializer=0,
                 generation_count_min=100,
                 generation_count_max=1500,
                 cpu_individual_limit=5000,
                 cpu_total_limit=60000,
                 fitness_lower_bound=None,
                 fitness_upper_bound=None,
                 fitness_threshold=0,
                 parent_candidate_count=5,
                 parent_selection_function=0,
                 tournament_probability=0.75,
                 crossover_operator=0,
                 crossover_probability=0.90,
                 mutation_probability=0.10,
                 filtration_frequency=0,
                 sa_iteration_count=300,
                 sa_initial_temperature=300,
                 sa_p_coeff=1.15):
        """
        Constructor for GA parameters.
        :param population_count: Number of instances that contain the solution for the problem.

        :param population_initializer: Function that initializes population for the first generation.

        :param generation_count_min: Number of generations that must be created before termination.

        :param generation_count_max: Number of generations that cannot be exceeded.

        :param cpu_individual_limit: Time (in milliseconds) allotted for the creation of a valid individual, or
        modification into a valid individual.

        :param cpu_total_limit: Time (in milliseconds) allotted for the problem. Once time is up, the algorithm
        is stopped.

        :param fitness_lower_bound: Lower bound fitness value, set as target by the user. If the problem is
        to be minimized, the algorithm stops once a solution with a fitness value lower than this (or sufficiently
        close to it, determined by the fitness threshold) is found.

        :param fitness_upper_bound: Upper bound fitness value, set as target by the user. If the problem is
        to be maximized, the algorithm stops once a solution with a fitness value higher than this (or sufficiently
        close to it, determined by the fitness threshold) is found.

        :param fitness_threshold: Threshold value that determines whether a solution fitness value is sufficiently
        close to a bound fitness value. The higher this value is, the more easily solutions are accepted, thus
        termination of the algorithm is more likely to occur faster.

        :param parent_candidate_count: Determines how many individuals are selected from the population
        as candidates to becoming parents of the next generation.

        :param parent_selection_function: Function that decides how individuals are chosen to be
        parents of the next generation.

        :param tournament_probability: Coefficient p_t, assuming that tournament selection is used as
        the parent selection function.

        :param crossover_operator: Function that controls the crossover operation.

        :param crossover_probability: Probability of performing a crossover operation on the offspring
        of the selected parents. If crossover does not occur, offspring are exact replicas of the parents.

        :param mutation_probability: Probability of mutating an individual offspring upon its creation.
        The probability is for one node. If mutation does not occur, the node is skipped.
        Otherwise a followup check is performed.

        :param filtration_frequency: Determines how often, in terms of generations, the filtration procedure is
        performed. Filtration is the act of combining two most recent generations together, sorting them in
        descending order ana taking the first half of the result as the next generation. If set to 0 or less, the
        filtration procedure is ignored.

        :param sa_iteration_count: Number of iterations to be done during population initialization, if
        simulated annealing was selected as the population initializer.

        :param sa_initial_temperature: Temperature variable for simulated annealing.

        :param sa_p_coeff: Coefficient p for simulated annealing.
        """

        self.population_count = population_count
        self.population_initializer = population_initializer
        self.generation_count_min = generation_count_min
        self.generation_count_max = generation_count_max
        self.cpu_individual_limit = cpu_individual_limit
        self.cpu_total_limit = cpu_total_limit
        self.fitness_lower_bound = fitness_lower_bound
        self.fitness_upper_bound = fitness_upper_bound
        self.fitness_threshold = fitness_threshold
        self.parent_candidate_count = parent_candidate_count
        self.parent_selection_function = parent_selection_function
        self.tournament_probability = tournament_probability
        self.crossover_operator = crossover_operator
        self.crossover_probability = crossover_probability
        self.mutation_probability = mutation_probability
        self.filtration_frequency = filtration_frequency
        self.sa_iteration_count = sa_iteration_count
        self.sa_initial_temperature = sa_initial_temperature
        self.sa_p_coeff = sa_p_coeff

        self.str_population_initializer = [
            "Random",
            "Allele Mutation",
            "Gene Permutation",
            "Simulated Annealing"
        ]
        self.str_parent_selection_function = [
            "Best Fitness",
            "Roulette Selection",
            "Tournament Selection"
        ]
        self.str_crossover_operator = [
            "1-Point",
            "2-Point",
            "Order Crossover",
            "Vehicle Crossover"
        ]

    def print(self):
        """
        Convenience function for printing GA parameters.
        """

        pop_str = self.str_population_initializer[self.population_initializer]
        par_sel_str = self.str_parent_selection_function[self.parent_selection_function]
        cross_str = self.str_crossover_operator[self.crossover_operator]

        if self.filtration_frequency <= 0:
            filtration_fr_str = "Never"
        elif self.filtration_frequency == 1:
            filtration_fr_str = "Every Generation"
        else:
            filtration_fr_str = "Every {} Generations".format(self.filtration_frequency)

        print("- Genetic Algorithm Parameters ---------------------------------------------------")
        print("Population Count           | {}".format(self.population_count))
        print("Population Initializer     | {}".format(pop_str))
        print("Minimum Generation Count   | {}".format(self.generation_count_min))
        print("Maximum Generation Count   | {}".format(self.generation_count_max))
        print("Individual CPU Time Limit  | {} ms".format(self.cpu_individual_limit))
        print("Total CPU Time Limit       | {} ms".format(self.cpu_total_limit))
        print("Fitness Lower Bound        | {}".format(self.fitness_lower_bound))
        print("Fitness Upper Bound        | {}".format(self.fitness_upper_bound))
        print("Fitness Threshold          | {}".format(self.fitness_threshold))
        print("Parent Candidate Count     | {}".format(self.parent_candidate_count))
        print("Parent Selection Function  | {}".format(par_sel_str))
        print("Tournament Probability     | {:0.2f}".format(self.tournament_probability))
        print("Crossover Operator         | {}".format(cross_str))
        print("Crossover Probability      | {:0.2f}".format(self.crossover_probability))
        print("Mutation Probability       | {:0.2f}".format(self.mutation_probability))
        print("Filtration Frequency       | {}".format(filtration_fr_str))
        print("SA - Iteration Count       | {}".format(self.sa_iteration_count))
        print("SA - Initial Temperature   | {}".format(self.sa_initial_temperature))
        print("SA - Annealing Coefficient | {:0.2f}".format(self.sa_p_coeff))
