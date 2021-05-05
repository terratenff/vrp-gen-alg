# vrp-gen-alg - Algorithm Modules

Here are described a collection of modules that have been implemented specifically for the GA.

## Table of Contents

- [Population Initializers](#population-initializers)
  - [Random](#random)
  - [Allele Permutation](#allele-permutation)
  - [Gene Permutation](#gene-permutation)
  - [Simulated Annealing](#simulated-annealing)
  - [Nearest Neighbor](#nearest-neighbor)
- [Parent Selectors](#parent-selectors)
  - [Best Fitness](#best-fitness)
  - [Roulette Wheel Selection](#roulette-wheel-selection)
  - [Tournament Selection](#tournament-selection)
- [Crossover Operators](#crossover-operators)
  - [1-Point](#1-point)
  - [2-Point](#2-point)
  - [Order Crossover](#order-crossover)
  - [Vehicle Crossover](#vehicle-crossover)
- [Mutation Operators](#mutation-operators)
  - [Allele Swap](#allele-swap)
  - [Sequence Inversion](#sequence-inversion)
  - [Sequence Shuffle](#sequence-shuffle)
  - [Sequence Relocation](#sequence-relocation)
  - [Vehicle Diversification](#vehicle-diversification)
  - [Add Optional Node](#add-optional-node)
  - [Remove Optional Node](#remove-optional-node)
  - [Change Depot](#change-depot)
- [Validators](#validators)
- [Invalidity Correction Functions](#invalidity-correction-functions)
  - [Random Valid Individual](#random-valid-individual)
  - [Best Individual](#best-individual)
  - [Neighbor of the Best Individual](#neighbor-of-the-best-individual)
  - [Indefinite Mutation](#indefinite-mutation)
  - [Best Individual and Mutation](#best-individual-and-mutation)
  - [Retry Individual Creation](#retry-individual-creation)
- [Evaluators](#evaluators)

### Population Initializers

Population initializers create generation 0 population, since there are no individuals to choose for crossover operations as parents.

#### Random

(Integer code 0) Each individual in the population is created randomly. Also, for each proposed solution for the individual, there is 10% chance that [vehicle diversification](#vehicle-diversification) is applied.

#### Allele Permutation

(Integer code 1) A random individual is first created. Then, for each mutation operation performed, a copy of the individual is added to the population. Of all the mutation operators, only [allele swap](#allele-swap) is used every time.

#### Gene Permutation

(Integer code 2) A random individual is first created. Then its chromosome (solution) is split into randomly-sized genes. These are then moved around to create permutations that are given to individuals for the population. If resulting population is insufficient, another random individual is created, and the aforementioned procedure is repeated.

#### Simulated Annealing

(Integer code 3) Heuristic algorithm that can also be used to solve VRP instances. It is based on the annealing technique in metallurgy where imperfections of metal are fixed, starting at high temperatures, and concluding at low temperatures. As a population initializer, individuals that are accepted by SA are added to the population. If resulting population is too large, the most recent individuals are selected for the population. If resulting population is too small, the rest of the individuals are created randomly.

#### Nearest Neighbor

(Integer code 4) Simple heuristic algorithm that is commonly used to solve TSP instances. It selects a random node at the beginning, and from that it always moves to the node nearest to its current location. 1 or more of these kinds of results are made from randomly selected subsets of nodes. These are then split to smaller routes by distributing depot nodes randomly. If resulting solution to VRP is valid, it is added to the population.

### Parent Selectors

Parent selectors nominate individuals as parents for the crossover operation. In this application, for every parent selector function, a pool of candidates is of specific size, and individuals are placed there randomly.

#### Best Fitness

(Integer code 0) From the pool of candidates, the individual with the best fitness value is selected as a parent.

#### Roulette Wheel Selection

(Integer code 1) The probability of candidate in the pool being selected is linearly dependent of its fitness value. Its fitness value is divided by total fitness value of the pool. This is the case for highest fitness value: for lowest fitness value, complement rule is applied.

#### Tournament Selection

(Integer code 2) Pool of candidates is sorted in ascending/descending order. The probability of being selected is determined by its placement in the pool.

### Crossover Operators

In the crossover operation, two parents create two offspring by sharing their genes with one another so that their offspring inherit them.

#### 1-Point

(Integer code 0) A cutoff point is selected randomly for both chromosomes. Contents beyond that point are flipped. The rest of the chromosome is adjusted to ensure that both everything necessary is there and that no duplicates exist.

#### 2-Point

(Integer code 1) This is similar to 1-Point crossover operator, except two cutoff points are selected for both chromosomes. The contents between the points are flipped, and everything else is adjusted similarly to 1-Point.

#### Order Crossover

(Integer code 2) (OX) A random, unique gene is selected for each parent. Their locations in the chromosomes are also maintained. Offspring A inherits parent A's gene and gets the rest of the chromosome from parent B. Vice versa for offspring B.

#### Vehicle Crossover

(Integer code 3) (VX) This is similar to OX. The difference is in the selection of the random, unique gene; it is limited to full vehicle routes.

### Mutation Operators

In the mutation operation, the offspring from the crossover are modified slightly (or not at all) to maintain population diversity. This combats premature convergence to a local optimum.

#### Allele Swap

Two alleles are selected at random and are swapped.

#### Sequence Inversion

A random gene is selected from the chromosome. Its contents are then reversed.

#### Sequence Shuffle

A random gene is selected from the chromosome. Its contents are then shuffled.

#### Sequence Relocation

A random gene is selected from the chromosome. Its position is then changed.

#### Vehicle Diversification

Every depot node in the chromosome is redistributed such that each vehicle has a nearly equal-sized route to follow.

#### Add Optional Node

An unused optional node is added to the chromosome. If none of these exist, a used optional node is removed instead. This is relevant only in VRPP instances.

#### Remove Optional Node

A used optional node is removed from the chromosome. If none of these exist, an unused node is added instead. This is relevant only in VRPP instances.

#### Change Depot

Selects a depot node at random and changes it to some other depot node. This is relevant only in MDVRP instances if depot nodes are not optimized.

### Validators

Validators ensure that solutions proposed by individuals do not violate any constraints that are in place. Constraints that are enforced for every vehicle include:
- Maximum travel time
- Maximum travel distance
- Maximum capacity
- Time windows

If a solution of an individual violates one or more of these constraints, the individual is deemed invalid. In such a case, it is repaired using an invalidity correction function.

### Invalidity Correction Functions

Invalidity Correction functions are used to convert invalid individuals to valid ones.

#### Random Valid Individual

A completely random individual is created from scratch. It is then validated. This process is repeated until a valid individual is created.

#### Best Individual

Invalid individual is replaced with the best individual that has been discovered during the current execution of the genetic algorithm.

#### Neighbor of the Best Individual

The best individual is taken and then mutated. If resulting individual is invalid, the process is repeated.

#### Indefinite Mutation

Invalid individual is mutated and validated. Whenever the individual is invalid it is mutated again. Once the individual is valid, the mutation stops.

#### Best Individual and Mutation

Combination of [best individual](#best-individual) and [indefinite mutation](#indefinite-mutation). The best individual is taken and then continuously mutated until it is valid.

#### Retry Individual Creation

Instead of attempting to fix an invalid individual, it is instead discarded, and the algorithm proceeds as normal.

### Evaluators

Once individuals have been validated, they are evaluated. Using the primary evaluation function and unit conversion factors (distance-to-time, time-to-cost and distance-to-cost) validated individuals are assigned a fitness value. For non-VRPP instances the fitness value represents total travel costs. For VRPP-instances, the fitness value represents either total profits ((C)TOP) or difference between total profits and travel costs ((C)PTP).
