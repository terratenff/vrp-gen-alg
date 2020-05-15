#!/usr/bin/env python

"""
main.py:

TODO
"""

from algorithms.matrix_builder import load_variable
from instances.params import InstanceParams, AlgorithmParams
from instances.vrp import VRP
from input_options.menu import loop


def main():
    print("--- Vehicle Routing Problem with Genetic Algorithm ---")
    matrix_file = "sample"
    matrix_data = load_variable(matrix_file, force_load=True)

    vrp_params = InstanceParams()
    alg_params = AlgorithmParams()

    vrp = VRP(matrix_data, vrp_params)

    code = 0

    while code != -1:
        code, vrp = loop(vrp, alg_params)
    print("Closing program...")


if __name__ == "__main__":
    main()
