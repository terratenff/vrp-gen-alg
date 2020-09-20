#!/usr/bin/env python

"""
mediator.py:

Primarily takes user input to direct the application in the
proper direction.
"""

from algorithms import param_builder, matrix_builder, genalg


def inspect(code, vrp_params, alg_params):
    """
    Interprets given user input and proceeds to execute an
    appropriate function.
    :param code: User input.
    :param vrp_params: VRP parameters being used.
    :param alg_params: General algorithmic parameters being used.
    :return: User input and updated parameters.
    """

    if code == 1:
        matrix_builder.generate_random_distance_matrix(vrp_params)
    elif code == 2:
        matrix_builder.select_distance_matrix(vrp_params)
    elif code == 3:
        print(vrp_params.vrp_path_table)
    elif code == 4:
        param_builder.set_vrp_parameters(vrp_params)
    elif code == 5:
        param_builder.set_algorithm_parameters(alg_params)
    elif code == 6:
        vrp_params.print()
        print()
        alg_params.print()
        print()
    elif code == 7:
        genalg.run_gen_alg(vrp_params, alg_params)
    return code, vrp_params, alg_params
