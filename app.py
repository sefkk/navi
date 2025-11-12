import os
from flask import Flask, jsonify, request, render_template
from flask_cors import CORS

# Import the map generation functions
from generator import generate_nodes, generate_edges

# Import your pathfinding algorithms
from path_maker import dijkstra # a_star can be added here once implemented

# --- Flask App Setup ---
app = Flask(__name__)

# This is a crucial step that allows your JavaScript frontend
# to make requests to this backend.
CORS(app)

# This global variable will store the generated map data in memory.
# This ensures that pathfinding requests use the same map
# that was sent to the frontend.
map_data = {}

@app.route('/')
def index():
    """
    Renders the main HTML page for the frontend.
    This serves your index.html file to the browser.
    """
    return render_template('index.html')

@app.route('/generate_map', methods=['GET'])
def generate_map():
    """
    Generates a random map (nodes and edges) and stores it in
    the 'map_data' global variable. It then returns the data
    as a JSON response to the frontend.
    """
    global map_data
    
    # Get canvas dimensions from request or use defaults
    # Frontend will send these via query params if available
    canvas_width = request.args.get('width', default=950, type=int)
    canvas_height = request.args.get('height', default=800, type=int)
    
    node_count = 24
    width = canvas_width
    height = canvas_height

    nodes = generate_nodes(node_count, width, height)
    edges = generate_edges(nodes)
    
    map_data = {
        "nodes": nodes,
        "edges": edges
    }
    
    return jsonify(map_data)

@app.route('/find_path', methods=['POST'])
def find_path():
    """
    Finds the shortest path between two nodes using a selected algorithm.
    This endpoint receives the start and end node IDs from the frontend,
    calls the appropriate pathfinding function, and returns the result
    as a JSON response.
    """
    data = request.get_json()
    start_id = data.get('start_node_id')
    end_id = data.get('end_node_id')
    algorithm = data.get('algorithm').lower()
    priority = data.get('priority').lower()
    vehicle_type = data.get('travel_mode') # New parameter from frontend 

    # Check if a map has been generated
    if not map_data:
        return jsonify({"error": "Map not generated. Please generate the map first."}), 400

    # Ensure the node IDs are valid integers
    try:
        start_id = int(start_id)
        end_id = int(end_id)
    except (ValueError, TypeError):
        return jsonify({"error": "Invalid node IDs."}), 400
    
    path_result = {}
    if algorithm == 'dijkstra':
        # Call your Dijkstra function with the map data and vehicle type
        path_result = dijkstra(map_data['nodes'], map_data['edges'], start_id, end_id, priority, vehicle_type)
    elif algorithm == 'a_star':
        # You would call your a_star function here
        # path_result = a_star(...)
        return jsonify({"error": "A* algorithm is not yet implemented."}), 501
    else:
        return jsonify({"error": "Invalid algorithm selected."}), 400

    return jsonify(path_result)


if __name__ == '__main__':
    # This block runs the Flask development server.
    # For production, Railway/Render will use gunicorn via Procfile
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)