import random 
import math 
import numpy as np

# random.seed(31)
# np.random.seed(31) 

map_data = {
    "nodes": [],
    "edges": []
}

def generate_nodes(node_count, width, height, highway_ratio=0.24):
    """
    Generate a city-like node distribution with realistic highways.
    node_count: total number of nodes
    width, height: map dimensions
    highway_ratio: fraction of nodes belonging to highways
    """
    nodes = []
    city_center = (width / 2, height / 2) 
    city_center_1 = (200, 50)
    city_center_2 = (150, 600)
    city_center_3 = (700, 500)

    city_centers = [city_center_1, city_center_2, city_center_3]

    # a grid to represent allowed areas (1 = land, 0 = water) 
    allowed_grid = [
        [1, 1, 1, 0, 1],
        [1, 1, 0, 0, 1],
        [1, 1, 0, 0, 1],
        [1, 1, 0, 0, 1],
        [1, 1, 0, 0, 1]
    ]

    grid_rows = 5
    grid_cols = 5
    grid_cell_width = width / grid_cols
    grid_cell_height = height / grid_rows

    # a city center node 
    # nodes.append({"id": 1000, "x": int(city_center[0]), "y": int(city_center[1]), "is_highway": False})
    t = 0
    for node in city_centers:
        node_id = 1000 + t
        nodes.append({"id": node_id, "x": int(node[0]), "y": int(node[1]), "is_highway": True}) 
        t += 1
    
    # Step 3: Iterate through the grid and generate nodes in allowed cells
    for row in range(grid_rows):
        print(row)
        for col in range(grid_cols):
            if allowed_grid[row][col] == 1:
                # Calculate the bounds for the current grid cell
                cell_x_min = col * grid_cell_width
                cell_x_max = (col + 1) * grid_cell_width
                cell_y_min = row * grid_cell_height
                cell_y_max = (row + 1) * grid_cell_height

                # Determine number of nodes for this cell
                nodes_in_cell = int(node_count / (grid_rows * grid_cols)) + random.randint(-1, 3)

                # city nodes, non-highway
                for i in range(nodes_in_cell):
                    node_id = i + 1004 + len(nodes) + t
                    
                    # Try a limited number of times to prevent an infinite loop
                    for _ in range(100): 
                        is_too_close = False
                        
                        # Generate random coordinates within the specified area
                        if random.random() <= 1:
                            x = int(np.random.randint(cell_x_min, cell_x_max))
                            y = int(np.random.randint(cell_y_min, cell_y_max))

                        if not node_id in [node['id'] for node in nodes]:
                            new_node = {'id': node_id, 'x': x, 'y': y, 'is_highway': False}
                            print(node_id, "is implemented")
                        else:
                            node_id -= 100
                            new_node = {'id': node_id, 'x': x, 'y': y, 'is_highway': False}
                            print(node_id, "is implemented")

                        # Check the new node against all existing nodes
                        for existing_node in nodes:
                            if calculate_distance(new_node, existing_node) < 30: # minimum distance between nodes 
                                is_too_close = True
                                break # Exit this loop if a clash is found
                        
                        # If no clashes were found, add the new node and move on
                        if not is_too_close:
                            nodes.append(new_node)
                            t += 1
                            break  # Exit the retry loop if successful

    # highway nodes 
    highway_nodes = []

    # How many highway nodes to generate 
    highway_count = int(node_count * highway_ratio) + 1 # at least one highway node 
    
    # Step 3: Iterate through the grid and generate nodes in allowed cells
    for row in range(grid_rows):
        for col in range(grid_cols):
            if allowed_grid[row][col] == 1:
                # Calculate the bounds for the current grid cell
                cell_x_min = col * grid_cell_width
                cell_x_max = (col + 1) * grid_cell_width
                cell_y_min = row * grid_cell_height
                cell_y_max = (row + 1) * grid_cell_height

                # Determine number of nodes for this cell
                nodes_in_cell = int(node_count / (grid_rows * grid_cols)) + random.randint(0, 1) 

                for j in range(highway_count):
                    node_id = 1105 + node_count - highway_count + j 
                    
                    # Generate random coordinates within the specified area
                    if random.random() <= 1:
                        # Denser area
                        x = int(np.random.randint(cell_x_min, cell_x_max))
                        y = int(np.random.randint(cell_y_min, cell_y_max))
                    else:
                        # ring road around the city center 
                        angle = np.random.uniform(0, 2*np.pi)
                        radius = min(width, height) / 2.5
                        x = int(city_center[0] + radius * np.cos(angle) + np.random.normal(0, 15))
                        y = int(city_center[1] + radius * np.sin(angle) + np.random.normal(0, 15))
                    
                    x = max(20, min(width - 100, x))
                    y = max(20, min(height - 50, y))
                    
                    highway_nodes.append({"id": node_id, "x": x, "y": y, "is_highway": True})
                
                return nodes + highway_nodes

def calculate_distance(node1, node2):
    """
    Calculates Euclidean distance between two nodes.
    """
    return math.sqrt(((node1['x'] - node2['x']) ** 2) + ((node1['y'] - node2['y']) ** 2))

def generate_edges(nodes):
    """
    Generates edges between nodes based on distance and assigns attributes.
    """
    edges = []
    # Step 1: Initialize a dictionary to count edges for each node
    edge_counts = {node['id']: 0 for node in nodes}

    # --- PHASE 1: Initial Random Edge Generation --- 
    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):

            # not to create too many edges, and keep the app somewhat realistic 
            if calculate_distance(nodes[i], nodes[j]) < 450 and (np.random.random() <= 1):
                
                # Step 2: Check if both nodes have less than 4 edges
                if edge_counts[nodes[i]['id']] < 4 and edge_counts[nodes[j]['id']] < 4:

                    length = calculate_distance(nodes[i], nodes[j]) / 10

                    # if the road is a highway
                    if nodes[i]['is_highway'] and nodes[j]['is_highway']:
                        highway = True
                        speed_limit = random.choice([90, 110, 130]) # higher speed limit 
                        traffic = random.uniform(1.0, 2.05) # less traffic
                        is_bus_route = random.random() < 0.8 # 80% chance of being a bus route  
                        is_taxi_route = True 
                        is_walkable = False # highways are not walkable
                        
                    else:
                        highway = False
                        speed_limit = random.choice([50, 70, 90]) # lower speed limit 
                        traffic = random.uniform(1.0, 2.75) # more traffic 
                        is_bus_route = random.random() < 0.8 # 80% chance of being a bus route 
                        is_taxi_route = True 
                        is_walkable = random.random() < 0.8 # 80% chance of being walkable 
                        
                    new_edge = {'from': nodes[i]['id'],
                            'to': nodes[j]['id'],
                            'length': round(length, 2),
                            "highway": highway,
                            'speed_limit': speed_limit,
                            'traffic': round(traffic, 2),
                            'is_bus_route': is_bus_route,
                            'is_taxi_route': is_taxi_route,
                            "is_walkable": is_walkable}
                    
                    if not edge_overlaps(new_edge, edges, nodes):
                        edges.append(new_edge)
                        edge_counts[nodes[i]['id']] += 1
                        edge_counts[nodes[j]['id']] += 1

    # --- PHASE 2: Connect Isolated Nodes ---
    all_node_ids = [node['id'] for node in nodes]
    for node_id in all_node_ids:
        if edge_counts[node_id] == 0:
            # Find the nearest neighbor to the isolated node
            isolated_node = next(n for n in nodes if n['id'] == node_id)
            min_dist = float('inf')
            nearest_neighbor = None

            for other_node in nodes:
                if other_node['id'] != node_id and edge_counts[other_node['id']] < 3:
                    dist = calculate_distance(isolated_node, other_node)
                    if dist < min_dist:
                        min_dist = dist
                        nearest_neighbor = other_node

            if nearest_neighbor:
                # Add a new edge to the nearest neighbor
                new_edge = {
                    'from': isolated_node['id'],
                    'to': nearest_neighbor['id'],
                    'length': round(min_dist / 10, 2),
                    'highway': False,
                    'speed_limit': random.choice([50, 70, 90]),
                    'traffic': random.uniform(1.0, 2.0),
                    'is_bus_route': random.choice([True, False]),
                    'is_taxi_route': True,
                    "is_walkable": True,
                }

                edges.append(new_edge)
                edge_counts[nodes[i]['id']] += 1
                edge_counts[nodes[j]['id']] += 1

    # return edges

    # --- PHASE 3: Ensure all nodes are connected to the city center ---
    city_center_id = 1001
    
    # Create a set to keep track of nodes already connected to the city center
    connected_nodes = {city_center_id}

    # Use a breadth-first search (BFS) or depth-first search (DFS) to find all connected nodes
    queue = [city_center_id]
    while queue:
        current_node_id = queue.pop(0)
        # Find all neighbors of the current node
        for edge in edges:
            if edge['from'] == current_node_id and edge['to'] not in connected_nodes:
                connected_nodes.add(edge['to'])
                queue.append(edge['to'])
            elif edge['to'] == current_node_id and edge['from'] not in connected_nodes:
                connected_nodes.add(edge['from'])
                queue.append(edge['from'])

    # Connect any remaining disconnected nodes to the city center
    all_node_ids = [node['id'] for node in nodes]
    city_center_node = next(n for n in nodes if n['id'] == city_center_id)

    for node_id in all_node_ids:
        if node_id not in connected_nodes:
            # Find the disconnected node
            disconnected_node = next(n for n in nodes if n['id'] == node_id)
            
            # Create a new edge connecting it to the city center
            length = calculate_distance(disconnected_node, city_center_node) / 10
            
            new_edge = {
                'from': node_id,
                'to': city_center_id,
                'length': round(length, 2),
                'highway': False,
                'speed_limit': random.choice([50, 70, 90]),
                'traffic': random.uniform(1.0, 2.0),
                'is_bus_route': random.choice([True, False]),
                'is_taxi_route': True,
                "is_walkable": True,
            }
            
            if not edge_overlaps(new_edge, edges, nodes):
                edges.append(new_edge)
                edge_counts[node_id] += 1
                edge_counts[city_center_id] += 1
            
    return edges

def do_intersect(p1, q1, p2, q2):
    """
    Check if line segment 'p1q1' and 'p2q2' intersect.
    """
    def orientation(a, b, c):
        val = (b[1] - a[1]) * (c[0] - b[0]) - (b[0] - a[0]) * (c[1] - b[1])
        if abs(val) < 1e-9:
            return 0  # collinear
        return 1 if val > 0 else 2

    def on_segment(a, b, c):
        return (min(a[0], c[0]) <= b[0] <= max(a[0], c[0]) and
                min(a[1], c[1]) <= b[1] <= max(a[1], c[1]))

    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)

    # General case
    if o1 != o2 and o3 != o4:
        return True

    # Special cases
    if o1 == 0 and on_segment(p1, p2, q1): return True
    if o2 == 0 and on_segment(p1, q2, q1): return True
    if o3 == 0 and on_segment(p2, p1, q2): return True
    if o4 == 0 and on_segment(p2, q1, q2): return True

    return False

def edge_overlaps(new_edge, edges, nodes):
    """
    Check if new_edge overlaps with any existing edge.
    """
    from_node = next(n for n in nodes if n['id'] == new_edge['from'])
    to_node = next(n for n in nodes if n['id'] == new_edge['to'])
    p1, q1 = (from_node['x'], from_node['y']), (to_node['x'], to_node['y'])

    for e in edges:
        e_from = next(n for n in nodes if n['id'] == e['from'])
        e_to = next(n for n in nodes if n['id'] == e['to'])
        p2, q2 = (e_from['x'], e_from['y']), (e_to['x'], e_to['y'])

        # skip if they share a node (adjacent edges can touch at endpoints)
        if new_edge['from'] in [e['from'], e['to']] or new_edge['to'] in [e['from'], e['to']]:
            continue

        if do_intersect(p1, q1, p2, q2):
            return True

    return False
