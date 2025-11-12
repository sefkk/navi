import heapq
import math 

def get_time_cost(edge, vehicle_type):
    """
    Calculates the time cost to traverse an edge, considering length, speed limit, and traffic.
    Time = (Length / Speed Limit) * Traffic Multiplier
    The result is in minutes.
    """
    # Check if the path is walkable for the chosen vehicle type
    if vehicle_type == 'walking' and not edge['is_walkable']:
        return float('inf')
    
    # Taxis and public transport can't use non-taxi/non-bus routes respectively
    if vehicle_type == 'taxi' and not edge['is_taxi_route']:
        return float('inf')
    
    if vehicle_type == 'public_transport' and not edge['is_bus_route']:
        return float('inf')
    
    length_km = edge['length']
    speed_kmh = edge['speed_limit']
    traffic_multiplier = edge['traffic']

    # For walking, a different speed should be used
    if vehicle_type == 'walking':
        walking_speed_kmh = 5 # 5 km/h is a standard walking speed
        # Calculate time in hours
        time_hours = length_km / walking_speed_kmh 
        time_minutes = time_hours * 60
    else:
        time_hours = length_km / speed_kmh
        time_minutes = time_hours * 60 * traffic_multiplier
    
    return time_minutes

def get_length_cost(edge):
    """
    Calculates the lenght cost to traverse en edge, in km. 
    """
    return edge['length']

def get_money_cost(edge, vehicle_type):
    """
    Calculates the monetary cost for a single edge based on vehicle type.
    """ 
    if vehicle_type == 'taxi':
        cost_per_km = 26.0 
        return edge['length'] * cost_per_km 
    elif vehicle_type == 'public-transport':
        # Public transport costs a flat fee per edge, assuming a simple model
        return 15 # The flat fee is added once per trip, not per edge
    elif vehicle_type == 'walking':
        return 0.0 
    else: # Default is 'car'
        cost_per_km = 5.0
        return edge['length'] * cost_per_km
    

def dijkstra(nodes, edges, start_id, end_id, priority, vehicle_type):
    print("Dijkstra's algorithm is working...")
    # 1. Build a graph from the nodes and edges
    graph = {node['id']: [] for node in nodes}
    for edge in edges:
        weight = 0 
        # Determine the weight based on the chosen priority
        if priority == 'distance':
            weight = get_length_cost(edge) 
        elif priority == 'time':
            weight = get_time_cost(edge, vehicle_type)
        elif priority == 'cost':
            weight = get_money_cost(edge, vehicle_type)

        graph[edge['from']].append((edge['to'], weight, edge))
        graph[edge['to']].append((edge['from'], weight, edge))

    # 2. Initialize distances and priority queue
    distances = {node['id']: float('inf') for node in nodes}
    distances[start_id] = 0
    priority_queue = [(0, start_id)]
    previous_nodes = {node['id']: None for node in nodes}
    
    # 3. Dijkstra's Algorithm
    while priority_queue:
        current_distance, current_node_id = heapq.heappop(priority_queue)

        if current_distance > distances[current_node_id]:
            continue

        if current_node_id == end_id:
            break

        for neighbor_id, weight, edge_info in graph[current_node_id]:
            distance = current_distance + weight
            if distance < distances[neighbor_id]:
                distances[neighbor_id] = distance
                previous_nodes[neighbor_id] = current_node_id
                heapq.heappush(priority_queue, (distance, neighbor_id))

    # 4. Check if a path was found (MOVED TO HERE)
    if previous_nodes.get(end_id) is None and start_id != end_id:
        return {"path": [], "error": "No path found"}
        
    # 5. Reconstruct Path and Calculate Totals
    path = []
    total_length = 0
    total_time = 0
    total_cost = 0
    current_node_id = end_id

    if vehicle_type == "public-transport": 
        total_cost += 150 # Flat fee for public transport
    if vehicle_type == "taxi":
        total_cost += 150 # Starting fee for taxi 

    while current_node_id is not None:
        path.insert(0, current_node_id)
        prev_node_id = previous_nodes[current_node_id]

        if prev_node_id is not None:
            edge = next((e for e in edges if (e['from'] == prev_node_id and e['to'] == current_node_id) or (e['from'] == current_node_id and e['to'] == prev_node_id)), None)
            if edge:
                total_length += get_length_cost(edge)
                total_time += get_time_cost(edge, vehicle_type)
                total_cost += get_money_cost(edge, vehicle_type)

        current_node_id = prev_node_id

    return {
        "path": path,
        "total_length": round(total_length, 2),
        "total_time": round(total_time, 2),
        "total_money_cost": round(total_cost, 2)
    }

