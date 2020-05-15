#!/usr/bin/env python

"""
params.py:

TODO
"""


class InstanceParams:
    """
    General parameters for every VRP type.
    """

    def __init__(self, vrp_vehicle_count=3,
                 vrp_depot_node=0,
                 vrp_vehicle_variance=0):
        """
        Constructor for general VRP parameters.
        :param vrp_vehicle_count: Number of initial vehicles available for the problem.
        :param vrp_depot_node: Index of the depot.
        :param vrp_vehicle_variance: Variance of available vehicles for mutations.
        """

        # On the subject of vehicle variance:
        # Example: If vehicle count is 4 and vehicle variance is 2, then
        # the vehicle count can vary (via mutations) between 4-2 and 4+2.

        self.vehicle_count = vrp_vehicle_count
        self.depot_node = vrp_depot_node
        self.vehicle_variance = vrp_vehicle_variance

    def print(self):
        """
        Convenience function for printing general instance parameters.
        """

        print("- Instance Parameters ----------------------------------------------------")
        print("VRP - Vehicle Count             | " + str(self.vehicle_count))
        print("VRP - Depot Node                | " + str(self.depot_node))
        print("VRP - Vehicle Variance          | " + str(self.vehicle_variance))
        print("--------------------------------------------------------------------------")


class AlgorithmParams:
    """
    General parameters for the genetic algorithm.
    """

    def __init__(self, gen_population_count=100,
                 gen_mutation_probability=10,
                 gen_offspring_count=50,
                 gen_crossover_function=0,
                 gen_retention_rate=10,
                 alg_generation_count_min=100,
                 alg_generation_count_max=1000,
                 alg_acceptable_difference=10):
        """
        Constructor for GA parameters.
        :param gen_population_count: Number of instances that contain the solution for the problem.
        :param gen_mutation_probability: Probability of mutating an instance more than once.
        :param gen_offspring_count: Number of instances subject to crossover.
        :param gen_crossover_function: Integer code representing a specific crossover function.
        :param gen_retention_rate: Probability of keeping low-fitness instances.
        :param alg_generation_count_min: Minimum number of generations for unchanging fitness value.
        :param alg_generation_count_max: Number of generations allotted for the computations.
        :param alg_acceptable_difference: Fitness threshold for iteration purposes.
        """

        # On the subject of minimum number of generations:
        # If the instance of best fitness value remains unchanged, then the generations
        # will be repeated this many times before giving up on finding a better solution.

        # On the subject of acceptable difference:
        # Prior to computing a solution for the VRP, a lower bound is estimated for the problem.
        # If the difference between computed solution and lower bound is lower than the threshold,
        # then the algorithm will stop looking for better solutions.

        self.population_count = gen_population_count
        self.mutation_probability = gen_mutation_probability
        self.offspring_count = gen_offspring_count
        self.crossover_function = gen_crossover_function
        self.crossover_functions = ["Copy",
                                    "Heavily Mutated Copy",
                                    "Child of Two",
                                    "Child of Three",
                                    "Randomly Generated"]
        self.retention_rate = gen_retention_rate
        self.generation_count_min = alg_generation_count_min
        self.generation_count_max = alg_generation_count_max
        self.acceptable_difference = alg_acceptable_difference

    def print(self):
        """
        Convenience function for printing GA parameters.
        """

        print("- Algorithm Parameters ---------------------------------------------------")
        print("GEN - Population Count          | " + str(self.population_count))
        print("GEN - Mutation Probability      | " + str(self.mutation_probability) + "%")
        print("GEN - Offspring Count           | " + str(self.offspring_count))
        print("GEN - Crossover Function        | " + str(self.crossover_functions[self.crossover_function]))
        print("GEN - Population Retention Rate | " + str(self.retention_rate) + "%")
        print("--------------------------------------------------------------------------")
        print("ALG - Generation Count (Min)    | " + str(self.generation_count_min))
        print("ALG - Generation Count (Max)    | " + str(self.generation_count_max))
        print("ALG - Acceptable Difference     | " + str(self.acceptable_difference))
        print("--------------------------------------------------------------------------")
