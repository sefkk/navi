# NaviSim - Navigation Simulator

A web-based pathfinding visualization tool that allows you to explore different pathfinding algorithms (Dijkstra, A*) with various travel modes (Car, Taxi, Public Transport, Walking) and priorities (Distance, Time, Cost).

## Features

- 🗺️ Random map generation with highways and regular roads
- 🚗 Multiple travel modes: Car, Taxi, Public Transport, Walking
- 🧮 Pathfinding algorithms: Dijkstra, A*
- ⚡ Multiple priorities: Distance, Time, Cost
- 🎨 Interactive canvas with smooth animations
- 📊 Real-time path calculation with distance, time, and cost metrics

## Local Development

### Prerequisites

- Python 3.12+
- pip

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd navi
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate 
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the application:
```bash
python app.py
```

5. Open your browser and navigate to `http://127.0.0.1:5000`

## Deployment

This project is configured for easy deployment on Railway, Render, or other platforms. The app uses relative URLs and is production-ready.
