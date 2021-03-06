#!/usr/bin/env python

"""
validators.py:

Collection of functions that are used to validate individuals.
"""


def validate_capacity(vrp, **kwargs):
    """
    Validates vehicle capacities of given individual's solution.
    :param vrp: An individual subject to validation.
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

    for demand_type in range(node_demands.shape[1]):
        capacity_type_list = []
        for active_route in route_list:
            if len(active_route) <= 1:
                continue

            current_capacity = 0
            recent_depot = active_route[0]
            for i in range(1, len(active_route)):
                destination_node = active_route[i]
                current_capacity += node_demands[:, demand_type][destination_node]

                # Check if capacity constraint is violated.
                if current_capacity > vehicle_capacity[demand_type]:
                    return False, "Capacity constraint violation (Route Node {} / {}, situated at {}): {} / {}" \
                        .format(
                            i,
                            len(active_route) + 1,
                            destination_node,
                            current_capacity,
                            vehicle_capacity[demand_type]
                        )

            # Traveling back to the depot node.
            current_capacity += node_demands[:, demand_type][recent_depot]
            if current_capacity > vehicle_capacity[demand_type]:
                return False, "Capacity constraint violation (Return to Depot Node {}): {} / {}" \
                    .format(recent_depot, current_capacity, vehicle_capacity[demand_type])

            # Save route capacity for later inspections.
            capacity_type_list.append(current_capacity)
        vrp.route_capacities.append(capacity_type_list)

    return True, "Capacity constraint not violated"


def validate_maximum_time(vrp, **kwargs):
    """
    Validates the maximum travel time of given individual's solution.
    :param vrp: An individual subject to validation.
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
    - (bool) 'ovrp': Flag that determines whether problem instance
      is an OVRP.

    :return: True, if solution is time-wise valid. False if not.
    Second return value is a string that provides details about it.
    """

    maximum_time = kwargs["maximum_time"]
    path_table = kwargs["path_table"]
    distance_time = kwargs["distance_time_converter"]
    time_windows = kwargs["time_window"]
    service_time = kwargs["service_time"]
    is_open = kwargs["ovrp"]

    route_list = vrp.get_route_list()

    for active_route in route_list:
        route_time = 0
        if len(active_route) <= 1:
            continue
        recent_node = active_route[0]
        recent_depot = active_route[0]

        # In case the first destination of the route involves waiting. That waiting time is instead
        # converted into a time at which the vehicle starts its route.
        route_start_time = max(
            0,
            time_windows[active_route[1]][0] - distance_time(path_table[active_route[0]][active_route[1]])
        )

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
            if route_time - route_start_time > maximum_time:
                return False, "Maximum time constraint violation (Route Node {} / {}, situated at {}): {} / {}" \
                    .format(i, len(active_route) + 1, point_b, route_time, maximum_time)

            # Mark down most recent node for the return trip.
            recent_node = point_b

        # Traveling back to the depot node.
        if not is_open:
            distance_segment = path_table[recent_node][recent_depot]
            route_time += distance_time(distance_segment)
            start_window = time_windows[recent_depot][0]
            if route_time < start_window:
                route_time += start_window - route_time
            route_time += service_time[recent_depot]
            if route_time - route_start_time > maximum_time:
                return False, "Maximum time constraint violation (Return to Depot Node {}): {} / {}" \
                    .format(recent_depot, route_time, maximum_time)

        # Save route time for later inspections.
        vrp.route_times.append(route_time)

    return True, "Maximum time constraint not violated"


def validate_maximum_distance(vrp, **kwargs):
    """
    Validates the maximum travel distance of given individual's solution.
    :param vrp: An individual subject to validation.
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
    Validates the time windows of given individual's solution.
    This validator is to be used only if hard time windows are enabled.
    :param vrp: An individual subject to validation.
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
    - (bool) 'ovrp': Flag that determines whether problem instance
      is an OVRP.

    :return: True, if solution is valid in terms of time windows. False if not.
    Second return value is a string that provides details about it.
    """

    path_table = kwargs["path_table"]
    distance_time = kwargs["distance_time_converter"]
    time_windows = kwargs["time_window"]
    service_time = kwargs["service_time"]
    is_open = kwargs["ovrp"]

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
        if not is_open:
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
