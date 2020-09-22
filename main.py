#!/usr/bin/env python

"""
main.py:

Entry point for the console application.
"""

from algorithms.matrix_builder import initialize
from instances.params import ParamsVRP, ParamsGENALG
from input_options.menu import loop


def main():
    print("--- Vehicle Routing Problem with Genetic Algorithm ---")
    matrix_file = "sample"
    matrix_data = initialize(matrix_file)

    vrp_params = ParamsVRP(matrix_data)
    alg_params = ParamsGENALG()

    vrp_params.content_name = matrix_file

    code = -2

    while code != -1:
        code, vrp_params, alg_params = loop(vrp_params, alg_params)

    print("Closing program...")


if __name__ == "__main__":
    main()
