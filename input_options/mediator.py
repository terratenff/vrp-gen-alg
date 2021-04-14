#!/usr/bin/env python

"""
mediator.py:

Primarily takes user input to direct the application in the
proper direction.
"""

from algorithms import param_builder, matrix_builder, genalg
from input_options.utility import get_input


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
        sub_code = data_interaction("What kind of data is to be generated?")
        matrix_builder.data_selector(vrp_params, code, sub_code)
    elif code == 2:
        sub_code = data_interaction("What kind of data should be selected for use?")
        matrix_builder.data_selector(vrp_params, code, sub_code)
    elif code == 3:
        sub_code = data_interaction("What kind of data should be deselected?")
        matrix_builder.data_selector(vrp_params, code, sub_code)
    elif code == 4:
        sub_code = data_interaction("What kind of data should be viewed?")
        matrix_builder.data_selector(vrp_params, code, sub_code)
    elif code == 5:
        param_builder.set_vrp_parameters(vrp_params)
    elif code == 6:
        param_builder.set_algorithm_parameters(alg_params)
    elif code == 7:
        param_name = input("Save current parameter settings as?\n(Empty input to abort) > ")
        if len(param_name) > 0:
            print("Attempting to save parameters...")
            param_builder.save_params(param_name, vrp_params, alg_params)
    elif code == 8:
        param_name = input("Specify the name of the parameter settings to load.\n(Empty input to abort) > ")
        if len(param_name) > 0:
            print("Attempting to load parameters...")
            param_builder.load_params(param_name, vrp_params, alg_params)
    elif code == 9:
        vrp_params.print()
        print()
        alg_params.print()
        print()
    elif code == 0:
        genalg.run_gen_alg(vrp_params, alg_params)
    return code, vrp_params, alg_params


def data_interaction(purpose_str):
    """
    Instructs user to select a specific data type to interact with.
    :param purpose_str: Description of what is to be done with the data.
    :return: User input that specifies data in question.
    """

    print("----------------------------------------------------------------------")
    print(purpose_str)
    print("----------------------------------------------------------------------")
    print("1 - Node Cost Matrix")
    print("2 - Node XY-Coordinates")
    print("3 - Node Demands")
    print("4 - Node Penalty Coefficients")
    print("5 - Node Profits")
    print("6 - Node Service Times")
    print("7 - Node Time Windows")
    print("----------------------------------------------------------------------")
    print("(Exit with 0)")

    return get_input(0, 7)
