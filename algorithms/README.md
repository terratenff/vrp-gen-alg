# vrp-gen-alg - Algorithms

Here are described the primary algorithms that the application uses.

## Table of Contents

- [GA](#ga)
- [Matrix Builder](#matrix-builder)
- [Parameter Builder](#parameter-builder)
- [Timer](#timer)

### GA

"genalg.py" file contains the core implementation of the GA. Briefly put, it does the following:
1. GA initialization (preparing instance variables, determining used extensions etc. See the code itself for specifics.)
2. Population initialization
3. Primary loop begins. One loop results in completion of one generation. Within the loop, the following is done:
  1. Perform the following subloop until new population is full (each subloop creates two offspring):
    1. Select two parents using the parent selection function.
    2. Perform crossover using selected crossover function..
    3. Perform mutation for the offspring.
    4. Add offspring to the new population.
  2. Validate individuals in the new population using selected evaluators.
  3. Replace invalid individuals with completely random individuals.
  4. Evaluate individuals using selected evaluator function.
  5. Sort new population in ascending/descending fitness order.
  6. Conduct the filtration strategy (or removal of duplicates) if it is time for it.
  7. Determine best overall individual.
4. Display best overall individual that has been discovered.
5. Plot figures from collected data.
6. Save collected data.
7. View plotted figures.
8. Terminate GA completely.

Primary loop is subject to termination via termination criteria. These are defined in instance object ParamsGENALG.

### Matrix Builder

"matrix_builder.py" file is in charge of the creation, (de)assignment and illustration of the matrix data that the application uses. These are cost matrices, coordinates, demands, service times, profits, time windows and penalties. The creation process includes a guided procedure, although the results are limited to randomly generated elements.

### Parameter Builder

"param_builder.py" file manages instance objects ParamsVRP and ParamsGENALG. Processes include guided initialization, saving and loading of both.

### Timer

This is simply a convenience implementation for CPU-time-based termination criteria.
