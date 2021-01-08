#!/usr/bin/env python

"""
validators.py:

Collection of functions that are used to validate individuals in the population.
"""


def validate_capacity(vrp, **kwargs):
    """
    Validates the vehicle capacity aspect of given individual's solution.
    :param vrp: An individual from the population.
    :param kwargs: Keyword arguments. The following are expected
    from it:

    - (int) 'capacity': Vehicle capacity.
    - (list<int>) 'demand': List of node demands.

    :return: True, if solution is capacity-wise valid. False if not.
    Second return value is a string that provides details about it.
    """

    vehicle_capacity = kwargs["capacity"]
    node_demands = kwargs["demand"]

    route_list = vrp.get_route_list()

    for active_route in route_list:
        current_capacity = 0
        if len(active_route) <= 1:
            continue

        recent_depot = active_route[0]
        for i in range(1, len(active_route)):
            destination_node = active_route[i]
            current_capacity += node_demands[destination_node]

            # Check if capacity constraint is violated.
            if current_capacity > vehicle_capacity:
                return False, "Capacity constraint violation (Route Node {} / {}, situated at {}): {} / {}" \
                    .format(i, len(active_route) + 1, destination_node, current_capacity, vehicle_capacity)

        # Traveling back to the depot node.
        current_capacity += node_demands[recent_depot]
        if current_capacity > vehicle_capacity:
            return False, "Capacity constraint violation (Return to Depot Node {}): {} / {}" \
                .format(recent_depot, current_capacity, vehicle_capacity)

        # Save route capacity for later inspections.
        vrp.route_capacities.append(current_capacity)

    return True, "Capacity constraint not violated"


def validate_maximum_time(vrp, **kwargs):
    """
    Validates the maximum travel time aspect of given individual's solution.
    :param vrp: An individual from the population.
    :param kwargs: Keyword arguments. The following are expected
    from it:

    - (int) 'maximum_time': Maximum travel time for every vehicle.
    - (numpy.ndarray) path_table: Square matrix that represents
      distances between nodes.
    - (function) 'distance_time_converter': Function that converts
      distance to time.
    - (list<tuple>) 'time_window': List of tuples that represent
      time windows of each node.
    - (list<int>) 'service_time': List of integers that represent
      node service times.

    :return: True, if solution is time-wise valid. False if not.
    Second return value is a string that provides details about it.
    """

    maximum_time = kwargs["maximum_time"]
    path_table = kwargs["path_table"]
    distance_time = kwargs["distance_time_converter"]
    time_windows = kwargs["time_window"]
    service_time = kwargs["service_time"]

    route_list = vrp.get_route_list()

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

            # Check if maximum time constraint is violated.
            if route_time > maximum_time:
                return False, "Maximum time constraint violation (Route Node {} / {}, situated at {}): {} / {}" \
                    .format(i, len(active_route) + 1, point_b, route_time, maximum_time)

            # Mark down most recent node for the return trip.
            recent_node = point_b

        # Traveling back to the depot node.
        distance_segment = path_table[recent_node][recent_depot]
        route_time += distance_time(distance_segment)
        start_window = time_windows[recent_depot][0]
        if route_time < start_window:
            route_time += start_window - route_time
        route_time += service_time[recent_depot]
        if route_time > maximum_time:
            return False, "Maximum time constraint violation (Return to Depot Node {}): {} / {}" \
                .format(recent_depot, route_time, maximum_time)

        # Save route time for later inspections.
        vrp.route_times.append(route_time)

    return True, "Maximum time constraint not violated"


def validate_maximum_distance(vrp, **kwargs):
    """
    Validates the maximum travel distance aspect of given individual's solution.
    :param vrp: An individual from the population.
    :param kwargs: Keyword arguments. The following are expected
    from it:

    - (int) 'maximum_distance': Maximum travel distance for every vehicle.
    - (numpy.ndarray) path_table: Square matrix that represents
      distances between nodes.

    :return: True, if solution is distance-wise valid. False if not.
    Second return value is a string that provides details about it.
    """

    maximum_distance = kwargs["maximum_distance"]
    path_table = kwargs["path_table"]

    route_list = vrp.get_route_list()

    for active_route in route_list:
        route_distance = 0
        if len(active_route) <= 1:
            continue
        recent_node = active_route[0]
        recent_depot = active_route[0]

        for i in range(1, len(active_route)):
            point_a = active_route[i - 1]
            point_b = active_route[i]
            route_distance += path_table[point_a][point_b]

            if route_distance > maximum_distance:
                return False, "Maximum distance constraint violation (Route Node {} / {}, situated at {}): {} / {}" \
                    .format(i, len(active_route) + 1, point_b, route_distance, maximum_distance)

            # Mark down most recent node for the return trip.
            recent_node = point_b

        # Traveling back to the depot node.
        route_distance += path_table[recent_node][recent_depot]
        if route_distance > maximum_distance:
            return False, "Maximum distance constraint violation (Return to Depot Node {}): {} / {}" \
                .format(recent_depot, route_distance, maximum_distance)

        # Save route time for later inspections.
        vrp.route_distances.append(route_distance)

    return True, "Maximum distance constraint not violated"


def validate_time_windows(vrp, **kwargs):
    """
    Validates the time window aspect of given individual's solution.
    This validator is to be used only if hard time windows are enabled.
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

    :return: True, if solution is valid in terms of time windows. False if not.
    Second return value is a string that provides details about it.
    """

    path_table = kwargs["path_table"]
    distance_time = kwargs["distance_time_converter"]
    time_windows = kwargs["time_window"]
    service_time = kwargs["service_time"]

    route_list = vrp.get_route_list()

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
            start_window = time_windows[point_b][0]
            end_window = time_windows[point_b][1]

            # If a vehicle arrives too late, the solution is invalid.
            # (If only some time windows are hard, soft time windows with high penalties should be used.)
            if route_time > end_window:
                return False, "Hard time window constraint violation (Route Node {} / {}, situated at {}): {} / {}" \
                    .format(i, len(active_route) + 1, point_b, route_time, end_window)

            # Check if arrival time is too early.
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
        start_window = time_windows[recent_depot][0]
        end_window = time_windows[recent_depot][1]
        if route_time > end_window:
            return False, "Hard time window constraint violation (Return to Depot Node {}): {} / {}" \
                .format(recent_depot, route_time, end_window)
        if route_time < start_window:
            route_time += start_window - route_time
        route_time += service_time[recent_depot]

    return True, "Hard time window constraint not violated"
