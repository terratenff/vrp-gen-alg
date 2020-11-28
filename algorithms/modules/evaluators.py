#!/usr/bin/env python

"""
evaluators.py:

Collection of functions that are used to evaluate individuals in the population.
"""


def _get_route_list(vrp):
    """
    Converts individual's solution into a list of routes that it consists of.
    :param vrp: An individual within the population.
    :return: List of vehicle routes, in which the first element represents the depot node being used.
    """

    vehicle_count = vrp.vehicle_count
    solution = vrp.solution
    depot_nodes = vrp.depot_node_list
    depot_indices = [i for i, x in enumerate(solution) if x in depot_nodes]

    route_list = []
    for i in range(1, vehicle_count):
        route_start = depot_indices[i - 1]
        route_end = depot_indices[i]
        route = solution[route_start:route_end]
        route_list.append(route)

    route_list.append(solution[depot_indices[vehicle_count - 1]:])
    return route_list


def evaluate_travel_distance(vrp, **kwargs):
    """
    Evaluates total travel distance of an individual's solution
    using a path table.
    :param vrp: An individual from the population.
    :param kwargs: Keyword arguments. The following are expected
    from it:

    - (numpy.ndarray) path_table: Square matrix that represents
      distances between nodes.

    :return: Total travel distance that comes from the solution
    presented by given individual.
    """

    path_table = kwargs["path_table"]

    route_list = _get_route_list(vrp)

    distance = 0
    for active_route in route_list:
        if len(active_route) <= 1:
            continue
        recent_node = active_route[0]
        recent_depot = active_route[0]

        for i in range(1, len(active_route)):
            point_a = active_route[i - 1]
            point_b = active_route[i]
            distance += path_table[point_a][point_b]

            # Mark down most recent node for the return trip.
            recent_node = point_b

        # Traveling back to the depot node.
        distance += path_table[recent_node][recent_depot]

    return distance


def evaluate_travel_time(vrp, **kwargs):
    """
    Evaluates total travel time of an individual's solution
    using time windows, service times and a path table.
    :param vrp: An individual from the population.
    :param kwargs: Keyword arguments. The following are expected
    from it:

    - (numpy.ndarray) path_table: Square matrix that represents
      distances between nodes.
    - (function) 'distance_time_converter': Function that converts
      distance to time.
    - (list<tuple>) 'time_window': List of tuples that represent
      time windows of each node.
    - (list<int>) 'service_time': List of integers that represent
      node service times.

    :return: Total travel distance that comes from the solution
    presented by given individual. Also returns total times
    for each route. (int/float, list<int/float>)
    """

    path_table = kwargs["path_table"]
    distance_time = kwargs["distance_time_converter"]
    time_windows = kwargs["time_window"]
    service_time = kwargs["service_time"]

    route_list = _get_route_list(vrp)

    route_times = []
    for active_route in route_list:
        route_time = 0
        if len(active_route) <= 1:
            continue
        recent_node = active_route[0]
        recent_depot = active_route[0]

        for i in range(1, len(active_route)):
            point_a = active_route[i - 1]
            point_b = active_route[i]
            distance_segment = path_table[point_a][point_b]
            route_time += distance_time(distance_segment)

            # Check if arrival time is too early.
            start_window = time_windows[point_b][0]
            if route_time < start_window:
                # Vehicle has to wait until the beginning of the time window.
                route_time += start_window - route_time

            # Upon arrival the servicing begins. This takes time to complete.
            route_time += service_time[point_b]

            # Mark down most recent node for the return trip.
            recent_node = point_b

        # Traveling back to the depot node.
        route_time = 0
        distance_segment = path_table[recent_node][recent_depot]
        route_time += distance_time(distance_segment)
        start_window = time_windows[recent_depot][0]
        if route_time < start_window:
            route_time += start_window - route_time
        route_time += service_time[recent_depot]

        # Add route time to a list of vehicle times.
        route_times.append(route_time)

    return sum(route_times), route_times


def evaluate_travel_cost(vrp, **kwargs):
    """
    Evaluates total travel costs of an individual's solution
    using time windows, service times, penalties and a path table.
    :param vrp: An individual from the population.
    :param kwargs: Keyword arguments. The following are expected
    from it:

    - (numpy.ndarray) path_table: Square matrix that represents
      distances between nodes.
    - (function) 'distance_time_converter': Function that converts
      distance to time.
    - (function) 'distance_cost_converter': Function that converts
      distance to cost.
    - (function) 'time_cost_converter': Function that converts
      time to cost.
    - (list<tuple>) 'time_window': List of tuples that represent
      time windows of each node.
    - (list<int>) 'service_time': List of integers that represent
      node service times.
    - (list<float>) 'penalty': List of penalty coefficients that represent
      the importance of the nodes.

    :return: Total travel costs that come from the solution
    presented by given individual.
    """

    path_table = kwargs["path_table"]
    distance_time = kwargs["distance_time_converter"]
    distance_cost = kwargs["distance_cost_converter"]
    time_cost = kwargs["time_cost_converter"]
    time_windows = kwargs["time_window"]
    service_time = kwargs["service_time"]
    penalty = kwargs["penalty"]

    route_list = _get_route_list(vrp)

    time = 0
    cost = 0
    for active_route in route_list:
        route_time = 0
        if len(active_route) <= 1:
            continue
        recent_node = active_route[0]
        recent_depot = active_route[0]

        for i in range(1, len(active_route)):
            point_a = active_route[i - 1]
            point_b = active_route[i]
            distance_segment = path_table[point_a][point_b]
            route_time += distance_time(distance_segment)
            cost += distance_cost(distance_segment)

            # Check if arrival time is too late.
            end_window = time_windows[point_b][1]
            if route_time > end_window:
                # Vehicle has arrived too late. A penalty is calculated.
                cost += penalty[point_b] * (route_time - end_window)

            # Check if arrival time is too early.
            start_window = time_windows[point_b][0]
            if route_time < start_window:
                # Vehicle has to wait until the beginning of the time window.
                route_time += start_window - route_time

            # Upon arrival the servicing begins. This takes time to complete.
            route_time += service_time[point_b]

            # Mark down most recent node for the return trip.
            recent_node = point_b

        # Traveling back to the depot node.
        distance_segment = path_table[recent_node][recent_depot]
        route_time += distance_time(distance_segment)
        cost += distance_cost(distance_segment)
        end_window = time_windows[recent_depot][1]
        if route_time > end_window:
            cost += penalty[recent_depot] * (route_time - end_window)
        start_window = time_windows[recent_depot][0]
        if route_time < start_window:
            route_time += start_window - time

        # Add route time to total time taken.
        time += route_time

    # Convert total time taken into costs.
    cost += time_cost(time)

    return cost


def evaluate_profits(vrp, **kwargs):
    """
    Evaluates total profits acquired from visiting various nodes.
    :param vrp: An individual of the population.
    :param kwargs: Keyword arguments. The following are expected
    from it:
    - (list<int>) 'node_profit': List of profits that one could get
      from visiting respective nodes.

    :return: Total profits that come from visiting nodes specified
    by given individual.
    """

    node_profit_list = kwargs["node_profit"]
    solution = vrp.solution
    node_count = vrp.node_count
    unvisited_optional_nodes = vrp.unvisited_optional_nodes
    profit = 0
    for i in range(node_count):
        node = solution[i]
        if node not in unvisited_optional_nodes:
            profit += node_profit_list[node]

    return profit
