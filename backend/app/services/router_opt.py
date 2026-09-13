"""
Pickup route optimization for a volunteer visiting multiple donor/recipient stops.
Uses OR-Tools for a proper TSP solve; falls back to a simple nearest-neighbor
order if OR-Tools isn't installed (keeps the endpoint usable either way).
"""
from app.services.matcher import haversine_km


def optimize_route(start: tuple[float, float], stops: list[tuple[float, float]]) -> list[int]:
    """
    start: (lat, lng) of the volunteer's current location
    stops: list of (lat, lng) points to visit
    Returns the visiting order as indices into `stops`.
    """
    points = [start] + stops
    n = len(points)
    if n <= 2:
        return list(range(len(stops)))

    try:
        from ortools.constraint_solver import routing_enums_pb2, pywrapcp

        def dist(i, j):
            return int(haversine_km(points[i][0], points[i][1], points[j][0], points[j][1]) * 1000)

        manager = pywrapcp.RoutingIndexManager(n, 1, 0)
        routing = pywrapcp.RoutingModel(manager)

        def distance_callback(from_index, to_index):
            return dist(manager.IndexToNode(from_index), manager.IndexToNode(to_index))

        transit_idx = routing.RegisterTransitCallback(distance_callback)
        routing.SetArcCostEvaluatorOfAllVehicles(transit_idx)

        params = pywrapcp.DefaultRoutingSearchParameters()
        params.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC

        solution = routing.SolveWithParameters(params)
        if not solution:
            raise RuntimeError("no solution")

        order = []
        index = routing.Start(0)
        while not routing.IsEnd(index):
            node = manager.IndexToNode(index)
            if node != 0:
                order.append(node - 1)  # shift back to `stops` indexing
            index = solution.Value(routing.NextVar(index))
        return order

    except Exception:
        # Fallback: greedy nearest-neighbor from start
        remaining = list(range(len(stops)))
        order = []
        current = start
        while remaining:
            nxt = min(remaining, key=lambda i: haversine_km(current[0], current[1], stops[i][0], stops[i][1]))
            order.append(nxt)
            current = stops[nxt]
            remaining.remove(nxt)
        return order
