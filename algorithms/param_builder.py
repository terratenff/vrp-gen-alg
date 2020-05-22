#!/usr/bin/env python

"""
param_builder.py:

Setter for general parameters.
"""

from instances.params import InstanceParams


def set_general_parameters(vrp, alg_params):
    """
    Interactive function that requests the user to provide
    parameters when asked.
    :param vrp: Subject VRP.
    :param alg_params: Subject algorithm parameters.
    """

    print("(Input S to save given inputs, and skip to next section)")
    print("(Input Q to abort)")

    print("- Problem-specific general parameters ---------------")
    vrp_list = ["VRP - Vehicle Count (Default: 3)",
                "VRP - Depot Node (Default: 0)",
                "VRP - Vehicle Variance (Default: 0)"]
    vrp_values = []

    for i in range(3):
        vrp_value = _set_value(vrp_list[i])
        if vrp_value == "Q":
            return
        elif vrp_value == "S":
            break
        else:
            vrp_values.append(vrp_value)

    try:
        parameters = InstanceParams()
        parameters.vehicle_count = vrp_values[0]
        parameters.depot_node = vrp_values[1]
        parameters.vehicle_variance = vrp_values[2]
    except IndexError:
        pass
    finally:
        vrp.set_params(parameters)

    print("- Algorithm-specific parameters ---------------------")
    alg_list = ["GEN - Population Count (Default: 100)",
                "GEN - Mutation Probability (%) (Default: 10%)",
                "GEN - Offspring Count (Default: half of population)",
                "GEN - Crossover Function (select one from below)\n"
                "0 - Copy\n"
                "1 - Heavily Mutated Copy\n"
                "2 - Child of Two\n"
                "3 - Child of Three\n"
                "4 - Randomly Generated\n"
                "(Default: 0, will be selected if input is out of range)",
                "GEN - Population Retention Rate (%) (Default: 10%)",
                "ALG - Generation Count (Min) (Default: 100)",
                "ALG - Generation Count (Max) (Default: 1000)",
                "ALG - Acceptable Difference (Default: 10)"]
    alg_values = []

    for i in range(8):
        alg_value = _set_value(alg_list[i])
        if alg_value == "Q":
            return
        elif alg_value == "S":
            break
        else:
            alg_values.append(alg_value)

    try:
        alg_params.population_count = alg_values[0]
        alg_params.mutation_probability = alg_values[1]
        alg_params.offspring_count = alg_values[2]
        if alg_values[3] > 4 or alg_values[3] < 0:
            alg_params.crossover_function = 0
        else:
            alg_params.crossover_function = alg_values[3]
        
        alg_params.retention_rate = alg_values[4]
        alg_params.generation_count_min = alg_values[5]
        alg_params.generation_count_max = alg_values[6]
        alg_params.acceptable_difference = alg_values[7]
    except IndexError:
        pass


def _set_value(description):
    """
    Convenient, interactive function for requesting a value for
    specified parameter.
    :param description: Description of the requested parameter.
    :return: Appropriate user input.
    """

    value = None
    while value is None:
        try:
            value_raw = input(description + " > ")
            value = int(value_raw)
        except ValueError:
            value = None
            if value_raw == "Q":
                return "Q"
            elif value_raw == "S":
                return "S"
            else:
                print("Invalid input.")

    return value
