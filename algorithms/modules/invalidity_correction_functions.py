#!/usr/bin/env python

"""
invalidity_correction_functions.py:

Collection of functions that are used to repair individuals that have been declared invalid.
"""

from algorithms.modules.population_initializers import random_valid_individual as rvi
from instances.vrp import VRP

from copy import deepcopy

import numpy as np


def random_valid_individual(violator, **kwargs):
    """
    Repairs an invalid individual by replacing it with a completely random
    individual that has been validated.
    
    @param violator: Subject individual that was deemed invalid.
    @param **kwargs: Collection of keyword arguments that are needed for
    fixing the violator:
    - (dict) 'individual_args': Collection of parameters that are needed for
      creating a new, random and valid individual.
    
    @return: Repaired individual.
    """
    
    individual_args = kwargs["individual_args"]
    return rvi(**individual_args)


def best_individual(violator, **kwargs):
    """
    Repairs an invalid individual by replacing it with the best individual that
    GA has come across so far.
    
    @param violator: Subject individual that was deemed invalid.
    @param **kwargs: Collection of keyword arguments that are needed for
    fixing the violator:
    - (VRP) 'best_individual': The best individual that GA has discovered
      so far.
    
    @return: Repaired individual.
    """
    
    violator_id = violator.individual_id
    best_individual_instance = deepcopy(kwargs["best_individual"])
    best_individual_instance.individual_id = violator_id
    return best_individual_instance, "Best Individual Used"


def neighbor_of_best_individual(violator, **kwargs):
    """
    Repairs an invalid individual by replacing it with a neighbor of the best
    individual that GA has come across so far.
    
    @param violator: Subject individual that was deemed invalid.
    @param **kwargs: Collection of keyword arguments that are needed for
    fixing the violator:
    - (VRP) 'best_individual': The best individual that GA has discovered
      so far.
    - (dict) 'individual_args': Collection of parameters that contain
      validation parameters for validating mutations.
    
    @return: Repaired individual.
    """
    
    best_individual_base = deepcopy(kwargs["best_individual"])
    individual_timer = kwargs["individual_args"]["individual_timer"]
    validation_args = kwargs["individual_args"]["validation_args"]
    violator_id = violator.individual_id
    
    validated = False
    
    while validated is False:
        validated = True
        best_individual_instance = deepcopy(best_individual_base)
        mutation_selector = np.random.randint(0, len(VRP.mutation_operator))
        VRP.mutation_operator[mutation_selector](best_individual_instance)
        for validator in VRP.validator:
            best_individual_instance.valid, msg = \
                validator(best_individual_instance, **validation_args)
            if best_individual_instance.valid is False:
                validated = False
                break
        if individual_timer.past_goal():
            return None, "(Neighbor of the Best Individual) Invalidity correction is taking too long."
    
    best_individual_instance.individual_id = violator_id
    return best_individual_instance, "(Neighbor of the Best Individual) Invalidity correction OK"


def indefinite_mutation(violator, **kwargs):
    """
    Repairs an invalid individual by mutating it indefinitely. Once a valid
    individual is found, the mutating stops.
    
    @param violator: Subject individual that was deemed invalid.
    @param **kwargs: Collection of keyword arguments that are needed for
    fixing the violator:
    - (VRP) 'best_individual': The best individual that GA has discovered
      so far.
    - (dict) 'individual_args': Collection of parameters that contain
      validation parameters for validating mutations.
    
    @return: Repaired individual.
    """
    
    individual_timer = kwargs["individual_args"]["individual_timer"]
    validation_args = kwargs["individual_args"]["validation_args"]
    
    violator_copy = deepcopy(violator)
    validated = False
    
    while validated is False:
        validated = True
        mutation_selector = np.random.randint(0, len(VRP.mutation_operator))
        VRP.mutation_operator[mutation_selector](violator_copy)
        for validator in VRP.validator:
            violator_copy.valid, msg = \
                validator(violator_copy, **validation_args)
            if violator_copy.valid is False:
                validated = False
                break
        if individual_timer.past_goal():
            return None, "(Indefinite Mutation) Invalidity correction is taking too long."
    
    return violator_copy, "(Indefinite Mutation) Invalidity correction OK"


def best_individual_and_mutation(violator, **kwargs):
    """
    Repairs an invalid individual by replacing it with the best individual that
    GA has come across so far and then indefinitely mutating it. Once a valid
    individual is discovered, the mutating stops.
    
    @param violator: Subject individual that was deemed invalid.
    @param **kwargs: Collection of keyword arguments that are needed for
    fixing the violator:
    - (VRP) 'best_individual': The best individual that GA has discovered
      so far.
    - (dict) 'individual_args': Collection of parameters that contain
      validation parameters for validating mutations.
    
    @return: Repaired individual.
    """
    
    best_individual_instance = deepcopy(kwargs["best_individual"])
    best_individual_instance.individual_id = violator.individual_id
    individual_timer = kwargs["individual_args"]["individual_timer"]
    validation_args = kwargs["individual_args"]["validation_args"]
    validated = False
    
    while validated is False:
        validated = True
        mutation_selector = np.random.randint(0, len(VRP.mutation_operator))
        VRP.mutation_operator[mutation_selector](best_individual_instance)
        for validator in VRP.validator:
            best_individual_instance.valid, msg = \
                validator(best_individual_instance, **validation_args)
            if best_individual_instance.valid is False:
                validated = False
                break
        if individual_timer.past_goal():
            return None, "(Best Individual + Mutation) Invalidity correction is taking too long."
    
    return best_individual_instance, "(Best Individual + Mutation) Invalidity correction OK"