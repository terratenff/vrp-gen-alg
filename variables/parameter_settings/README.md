# vrp-gen-alg - Parameter settings

This folder contains a collection of parameter settings that the application uses. They are split into two different categories: VRP-related settings and GA-related settings.

## Table of Contents

- [Parameter settings structure](#parameter-settings-structure)
- [VRP-settings](#vrp-settings)
  - [vrp_contents](#vrp_contents)
  - [vrp_path_table_override](#vrp_path_table_override)
  - [vrp_path_table_mapping](#vrp_path_table_mapping)
  - [vrp_vehicle_count](#vrp_vehicle_count)
  - [vrp_node_service_time](#vrp_node_service_time)
  - [vrp_maximum_route_time](#vrp_maximum_route_time)
  - [vrp_maximum_route_distance](#vrp_maximum_route_distance)
  - [vrp_distance_time_ratio](#vrp_distance_time_ratio)
  - [vrp_time_cost_ratio](#vrp_time_cost_ratio)
  - [vrp_distance_cost_ratio](#vrp_distance_cost_ratio)
  - [cvrp_vehicle_capacity](#cvrp_vehicle_capacity)
  - [cvrp_node_demand](#cvrp_node_demand)
  - [ovrp_enabled](#ovrp_enabled)
  - [vrpp_node_profit](#vrpp_node_profit)
  - [vrpp_exclude_travel_costs](#vrpp_exclude_travel_costs)
  - [vrpp_optional_node](#vrpp_optional_node)
  - [mdvrp_depot_node](#mdvrp_depot_node)
  - [mdvrp_optimize_depot_nodes](#mdvrp_optimize_depot_nodes)
  - [vrptw_node_time_window](#vrptw_node_time_window)
  - [vrptw_node_penalty](#vrptw_node_penalty)
  - [vrptw_hard_windows](#vrptw_hard_windows)
- [GA-settings](#ga-settings)
  - [population_count](#population_count)
  - [population_initializer](#population_initializer)
  - [generation_count_min](#generation_count_min)
  - [generation_count_max](#generation_count_max)
  - [cpu_individual_limit](#cpu_individual_limit)
  - [cpu_total_limit](#cpu_total_limit)
  - [fitness_lower_bound](#fitness_lower_bound)
  - [fitness_upper_bound](#fitness_upper_bound)
  - [fitness_threshold](#fitness_threshold)
  - [parent_candidate_count](#parent_candidate_count)
  - [parent_selection_function](#parent_selection_function)
  - [tournament_probability](#tournament_probability)
  - [crossover_operator](#crossover_operator)
  - [crossover_probability](#crossover_probability)
  - [mutation_probability](#mutation_probability)
  - [invalidity_correction](#invalidity_correction)
  - [filtration_frequency](#filtration_frequency)
  - [replace_valid_individuals](#replace_valid_individuals)
  - [sa_iteration_count](#sa_iteration_count)
  - [sa_initial_temperature](#sa_initial_temperature)
  - [sa_p_coeff](#sa_p_coeff)

### Parameter settings structure

The general structure of the parameter settings are that of key-value-pairs without quotation marks, separated by the equals-sign. Some parameters accept multiple values. These are given by separating them with whitespace. "sample.txt" can be found from both subfolders "vrp" and "genalg". They can be used as reference.

### VRP-settings

VRP-related settings are located in the subfolder "vrp". Here are the details of each. Note that cost matrix, path table, distance matrix and time matrix are used interchangeably.

#### vrp_contents

This is an exception to the rule, structured with two equals-signs. It consists of two different values that in conjunction with one another define the primary contents of the problem.
- The first value is either "matrix" or "coordinates". It determines the nature of the primary contents. Setting it "matrix" specifically aims to use a cost matrix only, while setting it "coordinates" aims to use a list of coordinates, from which a cost matrix can be created. If coordinates are used, additional plots are available for drawing.
- The second value defines the name of the text file that is to be used. If the first value is set to "matrix", the subfolder "cost_matrices" is searched. With "coordinates", the subfolder "coordinates" is searched instead.

The values of this parameter should not be set to none.

#### vrp_path_table_override

This parameter is relevant only if coordinates are used. There are two different behaviours based on provided input:
- If set to None, a cost matrix is generated from the coordinates that are being used.
- If set to the name of a cost matrix, that will be used as the cost matrix for selected coordinates.

Path table override allows one to use coordinates and asymmetric matrices simultaneously. In addition, some paths could be disabled this way while also making the plotting of maps possible (see README.md on plotting for more information about plotting maps).

#### vrp_path_table_mapping

Path table mapping overrides the number of nodes that are being used: the indices of the path table mapping represent the overridden nodes. It is a list that contains integers lower than the size of a path table. Said integers redirect to the indices of the path table. This parameter could be useful in cases where the entire cost matrix is not needed, or there is a need for vehicles to visit various nodes more than once due to having multiple requests with different demands, service times and time windows.

For example, take a cost matrix that accommodates 10 nodes. There are a total of 15 requests, some of which involve visiting the same node multiple times. A path table mapping of this could be "0 1 1 2 3 4 5 5 5 6 7 8 9 9 10". This means that overridden nodes 1 and 2 (indexing starting from 0) are located in the same place as old node 1, and overridden nodes 7, 8 and 9 are situated at old node 5, and overridden nodes 13 and 14 are at node 9.

If this is set to None, one-to-one mapping is used: in the aforementioned example that would be "0 1 2 3 4 5 6 7 8 9". If coordinates are used, this parameter has to be set to None if the plotting of maps is desired (see README.md on plotting for more information about plotting maps).

#### vrp_vehicle_count

Vehicle count represents the number of vehicles that are reserved for the problem instance. Setting this parameter low ensures that limited number of vehicles are being used, but doing so impacts the algorithm's ability to find a valid solution quickly, resulting in the algorithm either taking too long or being unable to find a solution to begin with. Setting the number of vehicles high ensures faster discovery of a valid solution (albeit worse than usual), thus improving algorithm efficiency; however, while the algorithm has the quirk of using less vehicles than what was reserved, the algorithm is not specialized in minimizing the number of vehicles used.

#### vrp_node_service_time

Node service time is the time that is needed to perform a service upon arrival. Once a vehicle arrives at a node, servicing begins. Once servicing has been completed, the vehicle proceeds towards another node. Each node has a service time of their own Depots are expected to have their service times at zero. Expected parameter value is the name of a text file situated in the variable subfolder "node_service_times". If set to None, nodes will have their service times set to zero. Service times on depot nodes are ignored.

#### vrp_maximum_route_time

Maximum route time is a constraint that enforces how long a vehicle can be on its assigned route. If a vehicle spends too long a time on its route, the solution that it's a part of becomes invalid. Setting this parameter to None sets maximum route time to infinity, effectively removing maximum route time constraint.

This parameter effectively creates hard time windows for depot nodes: if they are broken, the individual in question becomes invalid. This can hinder the application's ability to find a solution that respects these time windows. A way to combat this is to replace them with soft time windows, aimed at depot nodes, and then give depots extremely high penalty coefficients to simulate hard time windows.

#### vrp_maximum_route_distance

Maximum route distance functions in a similar manner when compared to maximum route time. The distance that a vehicle travels is collected from the cost matrix. If a vehicle's route is too long in terms of distance, then the solution that it's part of becomes invalid. Setting this parameter to None removes the constraint by making maximum distance infinity.

#### vrp_distance_time_ratio

Distance-to-time ratio is a coefficient that is used to convert distance units to time units. For example, if the coefficient is 2, 10 distance units convert to 20 time units, while 0.50 converts 10 distance units to 5 time units. Setting this parameter to 0 means that distance does not translate to time at all: any number of distance units convert to 0 time units. This parameter cannot be set to a negative value.

#### vrp_time_cost_ratio

Time-to-cost ratio is a coefficient that is used to convert time units to cost units. Cost units make the eventual fitness value. This parameter works similarly to that of distance-to-time ratio.

#### vrp_distance_cost_ratio

Distance-to-cost ratio is a coefficient that is used to convert distance units to cost units. Cost units make the eventual fitness value. This parameter works similarly to that of time-to-cost ratio.

#### cvrp_vehicle_capacity

Vehicle capacity is a constraint that determines the amount of things that vehicles can carry. Every vehicle is assumed to be the same, so they have the same capacity. If a vehicle goes over capacity during its route, the solution it's part of becomes invalid. Multiple capacity types can be defined by placing whitespace between different values. Different capacities are assumed to be unique: Items of type A use storage A, and items of type B use storage B, but items of type A cannot use storage B, and items of type B cannot use storage A. If multiple capacity types are used, node demands must be modified accordingly.

#### cvrp_node_demand

Node demands represent capacities that nodes request. Depots do not have any demands. Demands are assumed to be positive, although setting them negative is possible, but discouraged, since the act of both picking up and delivering goods in a route is not supported. Expected parameter value is the name of a text file situated in the variable subfolder "node_demands". If set to None, nodes will have their demands set to zero.

#### ovrp_enabled

This is a flag parameter that determines whether the problem instance is an open variant. Setting the parameter to True will transform the current VRP instance into its open variant at the beginning of the algorithm by modifying the cost matrix such that any trip to a depot is free. Technically the vehicles still do return to the depots where from which they started. If set to False, this procedure is skipped.

#### vrpp_node_profit

Node profits represent the profits that can be made by visiting nodes. Depots do not have profits. Each node can have different profits: the higher it is, the more of interest it is. Profits have merit to them only if the nodes that have them are considered optional. Profits are assumed to be positive, although it is possible to have them be negative. Expected parameter value is the name of a text file situated in the variable subfolder "node_profits". If set to None, nodes will have their profits set to zero.

#### vrpp_exclude_travel_costs

This is a flag that determines whether travel-related costs should be deducted from the profits. It is effectively a toggle between (C)TOP and (C)PTP. Setting the parameter True converts the problem instance into a (C)TOP. Setting the parameter False converts the problem instance into a (C)PTP. This parameter is utilized only if there are optional nodes selected.

#### vrpp_optional_node

Optional nodes mark the nodes that do not have to be visited. If any nodes are defined here, problem instance becomes a VRPP, the nature of which can be controlled with the previous parameter ([vrpp_exclude_travel_costs](#vrpp_exclude_travel_costs)). Depot nodes cannot be selected as optional. Multiple optional nodes can be defined by separating them with whitespace. Setting this parameter to None makes every node mandatory for visits.

#### mdvrp_depot_node

Depot nodes mark the locations where vehicles start and conclude their routes. Multiple depot nodes can be defined by separating them with whitespace, but at least one depot node must be defined. The application assumes that if a vehicle starts its route from depot A, it also concludes its route on depot A, not on depot B.

#### mdvrp_optimize_depot_nodes

This flag determines whether depot nodes for each vehicle should be optimized. The optimization consists of selecting a depot node for a vehicle such that the sum of the costs of the first and last trips are as low as possible. If this parameter is set to True, that procedure is performed every time an offspring is created. If set to False, that procedure is skipped and, in order to ensure that every depot sees use, a mutation operator is introduced. The mutation involves changing a vehicle's currently used depot node.

#### vrptw_node_time_window

Node time windows determine when a node can be serviced. If a vehicle arrives too early, it has to wait before servicing. If a vehicle arrives too late, either a penalty is incurred based on how late the vehicle is, or the solution becomes invalid. Depot nodes are allowed to have time windows separately. Expected parameter value is the name of a text file situated in the variable subfolder "node_time_windows". If set to None, nodes won't have time windows at all (technically they'll be between zero and infinity).

#### vrptw_node_penalty

Penalties are incurred if vehicles arrive at their destinations too late. The application applies a linear penalty function using coefficients. The later a vehicle is, the higher the penalty. The higher the penalty coefficient, the more important the node is. Expected parameter value is the name of a text file situated in the variable subfolder "node_penalties". If set to None, nodes have their penalty coefficients set to zero.

#### vrptw_hard_windows

This flag determines whether hard time windows should be explicitly enforced. Soft time windows utilize penalties, while hard time windows invalidate solutions. Soft time windows can simulate hard time windows by having extremely high penalty coefficients. Setting this parameter to True makes every time window hard, thus always excluding solutions that violate time windows by being late. If set to False, every time window is considered soft.

### GA-settings

GA-related settings are located in the subfolder "genalg". Here are the details of each.

#### population_count

As a population-based algorithm, GA maintains a population of individuals that represent solutions to the problem instance. This parameter defines the size of said population. The higher it is, the more opportunities GA has to find optimal solutions; however, computation times become longer. The lower it is, the faster GA operates, at the expense of its precision. Population count is usually set somewhere between 25 and 100.

#### population_initializer

Population initializer is a function that determines how generation 0 population is created. An integer code that represents a function is provided here. The following population initializers are available:
- 0: Random
  - Every individual is created randomly.
- 1: Allele Permutation
  - A random individual is created. Then it is mutated (using allele swap) and copied to the population every time.
- 2: Gene Permutation
  - A random individual is created. Then its chromosome is split into random genes. Using them, permutations of them are created and added to the population. If permutations run out, another random individual is created and the process is repeated until the population is completed.
- 3: Simulated Annealing (SA)
  - A heuristic algorithm that can also be used to solve VRP instances. Individuals that are accepted by SA are added to the population. If resulting population is greater than population count, it is sorted in ascending (or descending if maximizing) order and the first subset of individuals are taken. If resulting population is less than population count, the rest of the individuals are created randomly.
- 4: Nearest Neighbor
  - Simple heuristic algorithm that is commonly used to solve TSP instances. It selects a random node at the beginning, and from that it always moves to the node nearest to its current location. 1 or more of these kinds of results are made from randomly selected subsets of nodes. These are then split to smaller routes by distributing depot nodes randomly. If resulting solution to VRP is valid, it is added to the population.


 If SA is used as the population initializer, additional parameters are to be configured.

#### generation_count_min

Minimum generation count is one of few termination criteria that the application uses. If this number of generations pass by while discovered optimal solution remains unchanged, the algorithm is terminated. If a new optimal solution is discovered, this counter is reset.

#### generation_count_max

Maximum generation count is one of few termination criteria that the application uses. If this number of generations pass by, the algorithm is terminated.

#### cpu_individual_limit

Individual CPU time limit is one of few termination criteria that the application uses. It is given in milliseconds. If the creation of an individual takes longer than this, the algorithm is terminated **without yielding results**.

#### cpu_total_limit

Total CPU time limit is one of few termination criteria that the application uses. It is given in milliseconds. If algorithm execution - excluding population initialization - takes longer than this, the algorithm is terminated.

#### fitness_lower_bound

Fitness lower bound is one of few termination criteria that the application uses. If the fitness value of a discovered optimal solution is less than this, the algorithm is terminated. This is only used when the objective is to minimize the fitness value. If this is set to None, this termination criterion is not used.

#### fitness_upper_bound

Fitness upper bound is one of few termination criteria that the application uses. If the fitness value of a discovered optimal solution is more than this, the algorithm is terminated. This is only used when the objective is to maximize the fitness value. If this is set to None, this termination criterion is not used.

#### fitness_threshold

Fitness threshold is the acceptable difference between the fitness value of a discovered optimal solution and either fitness upper or lower bound. For example, if the lower bound is 1000, while the threshold is 50, then an individual with 1050 fitness is considered acceptable, thus terminating the algorithm. Likewise, if the upper bound is set to 1000, an individual with 950 fitness is also acceptable.

#### parent_candidate_count

Parent candidate count determines how many individuals are selected at random to compete to become a parent for the crossover operation. This is expected to be at least 2 and at most the population count.

#### parent_selection_function

Parent selection function determines how a parent is selected from a collection of candidate individuals. An integer code that represents a function is provided here. The following parent selection functions are available:
- 0: Best Fitness
 - From the collection of candidates the one with the lowest (or highest if maximizing) fitness is chosen.
- 1: Roulette Wheel Selection
 - The probability of an individual being chosen is relative to its own fitness value: its fitness value is divided by candidate group's total fitness. This is the case if maximizing: if minimizing, the complement rule is applied as well.
- 2: Tournament Selection
 - Candidate individuals are sorted in ascending (or descending if maximizing) order. Then they are assigned probabilities of being chosen based on their positions. Individual in first place is given a set probability (see next parameter), while others are given lower probabilities that are based on given probability.

#### tournament_probability

This is the probability that a candidate individual is chosen from a group of candidates in tournament selection if it has placed first in the tournament. Marking the probability as p, candidate individuals have the following probabilities of being selected:
- 1st: p
- 2nd: p*(1 - p)
- 3rd: p*(1 - p)^2
- 4th: p*(1 - p)^3
- nth: p*(1 - p)^n
- last place: 1 - (sum of probabilities of every other position)

#### crossover_operator

Crossover operator is a function that conducts the crossover procedure of the GA. Two parents are used to create two offspring. An integer code that represents a function is provided here. The following crossover operators are available:
- 0: 1-Point
  - A cutoff point is selected for both chromosomes. Contents of one side of the point are flipped, and the rest are rearranged so that there are no duplicates.
- 1: 2-Point
  - This is similar to 1-Point, except that two cutoff points are selected, and the contents between them are flipped.
- 2: Order Crossover (OX)
  - For each chromosome a random, unique gene is selected for preservation. Offspring A has the preserved gene of parent A, and the rest of the chromosome comes from parent B. Vice versa for offspring B.
- 3: Vehicle Crossover (VX)
  - This is the same as OX, except that genes subject to preservation are full routes.

#### crossover_probability

The probability of the crossover operation taking place. If crossover does not take place, offspring will be exact replicas of their parents.

#### mutation_probability

The probability of the mutation operation taking place after crossover.

#### invalidity_correction

Invalidity correction function takes an individual that has been found invalid and makes it valid again. An integer code represents a function that is used to repair invalid individuals. The following invalidity correction functions are available:
- 0: Random Valid Individual
  - A completely random individual is created from scratch. It is then validated. This process is repeated until a valid individual is created.
- 1: Best Individual
  - Invalid individual is replaced with the best individual that has been discovered during the current execution of the genetic algorithm.
- 2: Neighbor of the Best Individual
  - The best individual is taken and then mutated. If resulting individual is invalid, the process is repeated.
- 3: Indefinite Mutation
  - Invalid individual is mutated and validated. Whenever the individual is invalid it is mutated again. Once the individual is valid, the mutation stops.
- 4: Best Individual + Mutation
  - Invalidity correction functions 1 and 3 combined. The best individual is taken and then continuously mutated until it is valid.
- 5: Retry Individual Creation
  - Instead of attempting to fix an invalid individual, it is instead discarded, and the algorithm proceeds as normal.

#### filtration_frequency

Filtration frequency defines how often the filtration strategy is applied. This is given in terms of generations. Setting this to 0 means that the filtration strategy is not used at all. Setting this to x means that it is used once every x generations.

In the filtration strategy, populations of the two most recent generations are combined into one. Then it is sorted in ascending/descending order. From this combined and sorted population, the first half is taken. Any duplicates within this new population are replaced with completely random individuals.

#### replace_valid_individuals

This operation is the same as the filtration strategy, except that it is aimed at the most recent population. Setting this to 0 means that this strategy is not used at all. Setting this to x means that it is used once every x generations.

#### sa_iteration_count

This parameter is used in the population initializer SA. The parameter determines how many iterations SA is allowed to have. The more iterations, the more optimal solution SA will likely find, but with increasing computation times. The lower the iteration count, the faster SA will finish, at the expense of individual fitness.

#### sa_initial_temperature

This parameter is used in the population initializer SA. The parameter determines the volatility of SA. The higher it is, the more likely SA is to accept worse individuals into the population. The lower the initial temperature, the less likely SA is to accept worse individuals. By accepting worse individuals, it is possible to avoid early convergence into a local maximum.

#### sa_p_coeff

Annealing coefficient is used to control the temperature for each iteration. This is expected to be at least 1.00. The greater it is, the faster the temperature drops with each iteration.
