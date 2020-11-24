#!/usr/bin/env python

"""
menu.py:

Maintains a general console menu for the user.
"""

from input_options import mediator
from input_options.utility import get_input


def loop(vrp_params, alg_params):
    """
    Loop function for user input and interaction.
    :param vrp_params: VRP parameters.
    :param alg_params: Genetic Algorithm parameters.
    :return: User input and current state of problem instance.
    """

    print("------- Selected Data List --------")
    print("Distance Matrix: | " + str(vrp_params.cost_matrices_name))
    print("Coordinates:     | " + str(vrp_params.coordinates_name))
    print("Demands:         | " + str(vrp_params.node_demands_name))
    print("Penalties:       | " + str(vrp_params.node_penalties_name))
    print("Profits:         | " + str(vrp_params.node_profits_name))
    print("Service Times:   | " + str(vrp_params.node_service_times_name))
    print("Time Windows:    | " + str(vrp_params.node_time_windows_name))
    print("-----------------------------------")
    print("0 - RUN | 1 - Generate Data | 2 - Select Data | 3 - Deselect Data | 4 - View Data | 5 - Set Params (VRP) |"
          " 6 - Set Params (GENALG) | 7 - Save Params | 8 - Load Params | 9 - View Params | -1 - Exit")

    code = get_input(-1, 9)
    output, vrp_params, alg_params = mediator.inspect(code, vrp_params, alg_params)

    return output, vrp_params, alg_params
