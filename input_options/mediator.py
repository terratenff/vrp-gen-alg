#!/usr/bin/env python

"""
mediator.py:

Primarily takes user input to direct the application in the
proper direction.
"""

from algorithms import param_builder, matrix_builder, genalg


def inspect(code, vrp, alg_params):
    """
    Interprets given user input and proceeds to execute an
    appropriate function.
    :param code: User input.
    :param vrp: Subject VRP type subject to interactions.
    :param alg_params: General algorithmic parameters being used.
    :return: User input and subject VRP.
    """

    if code == 1:
        matrix_builder.generate_random_distance_matrix(vrp)
    elif code == 2:
        matrix_builder.select_distance_matrix(vrp)
    elif code == 3:
        print(vrp.path_table)
    elif code == 4:
        param_builder.set_general_parameters(vrp, alg_params)
    elif code == 5:
        # vrp = vrp_handler.vrp_menu(vrp)
        pass
    elif code == 6:
        vrp.print()
        print()
        vrp.params.print()
        print()
        alg_params.print()
        print()
    elif code == 7:
        genalg.run_gen_alg(vrp, alg_params)
    return code, vrp
