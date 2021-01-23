# vrp-gen-alg

vrp-gen-alg is an application that attempts to solve the Vehicle Routing Problem and some of its extensions using the metaheuristic algorithm called the Genetic Algorithm. It is implemented using Python as the programming language along with the scientific libraries NumPy, SciPy and Matplotlib. tkinter is used to implement the GUI that shows figures created by the application.

## Table of Contents

- [Vehicle Routing Problem](#vehicle-routing-problem)
- [Supported VRP extensions](#supported-vrp-extensions)
- [Genetic Algorithm](#genetic-algorithm)
- [More details](#more-details)

### Vehicle Routing Problem

The Vehicle Routing Problem (VRP) is an NP-hard combinatorial optimization problem where a variable number of vehicles must be given routes to visit a collection of customers such that the following conditions apply:
- Every vehicle starts and ends its route at a depot.
- Every customer is serviced exactly once by exactly one vehicle.

Adhering to aforementioned conditions, the objective is to minimize (travel) costs associated with the vehicles. Under some circumstances the number of vehicles have to be minimized as well. Some additional constraints that are involved in this include a maximum travel time and/or distance that the vehicles are given. Setting the number of vehicles to one transforms the problem into the Traveling Salesman's Problem (TSP).

Various extensions of the VRP have been studied in many researches, the most common one of them being the Capacitated Vehicle Routing Problem (CVRP). In CVRP, vehicles are given a uniform capacity that represents the amount of goods a vehicle can carry. Additionally, each customer is given a demand that acts as the amount of goods that the customer has requested. Vehicles must now be given routes that ensure that their capacities are not exceeded by customer demands.

### Supported VRP extensions

In addition to VRP and CVRP, vrp-gen-alg supports the following extensions (and its combinations):
- Open Vehicle Routing Problem (OVRP): Upon the end of their routes, the vehicles do not return to the depot nodes that they started from. In doing so, the routes are left "open".
- Vehicle Routing Problem with Profits (VRPP): Customers are split into mandatory and optional customers. Mandatory customers must be serviced, while optional customers do not have to be serviced. Each customer is also assigned a profit value that determines the worth of the customer. The objective becomes maximization, but varies slightly based on the nature of the VRPP. The following extensions of VRPP are supported by the application:
  - (Capacitated) Team Orienteering Problem ((C)TOP): The objective is to maximize profits only. Constraints associated with this problem tend to be strict. Additionally, there are points A and B where vehicles start and end their routes; however, in vrp-gen-alg, this detail is ignored (i.e. points A and B are the same).
  - (Capacitated) Profitable Tour Problem ((C)PTP): This is similar to (C)TOP, with the exception being the objective that is to maximize the difference between profits and travel costs.
- Multi-Depot Vehicle Routing Problem (MDVRP): Usually there is only one depot where vehicles start their routes. In this extension, there are more than one of them. In vrp-gen-alg it is assumed that a vehicle starts and ends its route at the same depot.
- Vehicle Routing Problem with Time Windows (VRPTW): Each customer is given a time window during which the customer can be serviced. If a vehicle arrives too early, it has to wait until the lower bound of the time window has passed. If a vehicle arrives too late, two different things can happen, depending on which types of time windows are being used - both of which are supported by vrp-gen-alg:
  - Soft time windows: Each customer is assigned a penalty function that calculates a cost based on how late a vehicle is. The longer a vehicle was late, the higher penalty, and the higher the penalty in general, the more important the customer is.
  - Hard time windows: Being late is not allowed at all; therefore, if a vehicle is late, the solution is no longer valid. Hard time windows can be simulated with soft time windows by using extremely high penalties.

### Genetic Algorithm

The Genetic Algorithm (GA) is a stochastic, population-based metaheuristic algorithm that simulates natural selection described by Darwin. A population is initialized at the beginning. Then, for each generation, a new population is generated by selecting individuals with good genes from the current population for breeding: the offspring that are created by said individuals create the new population. The idea behind this is that good genes are kept while bad genes are removed. With good genes, the individuals are expected to get closer towards the optimal solution with each generation.

### More details

Each folder contains a README.md that provides more documentation on what each part of the application does. Check them for the specifics of the application. For information on how to use the application, see INSTRUCTIONS.md.
