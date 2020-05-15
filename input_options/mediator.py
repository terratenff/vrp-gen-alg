#!/usr/bin/env python

"""
mediator.py:

TODO
"""

from algorithms import param_builder, matrix_builder, genalg
from input_options import vrp_handler


def inspect(code, vrp, alg_params):
    if code == 1:
        matrix_builder.generate_random_distance_matrix(vrp)
    elif code == 2:
        matrix_builder.select_distance_matrix(vrp)
    elif code == 3:
        print(vrp.path_table)
    elif code == 4:
        param_builder.set_general_parameters(vrp, alg_params)
    elif code == 5:
        vrp = vrp_handler.vrp_menu(vrp)
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
