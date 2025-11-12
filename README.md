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
git clone <your-repo-url>
cd navi
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
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

## Deployment Options

### Option 1: Railway (Recommended - No Sleep Issues) ⭐

Railway offers a free tier with $5/month credit and services stay awake longer.

1. Push your code to GitHub
2. Go to [Railway](https://railway.app)
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Railway will auto-detect Python and deploy
6. The `Procfile` and `railway.json` are already configured

**Advantages:**
- ✅ Services stay awake longer (no immediate sleep)
- ✅ $5/month free credit
- ✅ Fast deployments
- ✅ Easy to use

### Option 2: Render (Free but Sleeps)

Render's free tier spins down after 15 minutes of inactivity.

1. Push your code to GitHub
2. Go to [Render Dashboard](https://dashboard.render.com)
3. Click "New" → "Blueprint" (or "Web Service")
4. Connect your GitHub repository
5. Render will auto-detect `render.yaml` or configure manually:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`

**Note:** Free tier services sleep after inactivity and take ~30 seconds to wake up.

### Option 3: Fly.io (Always-On Free Tier)

Fly.io offers a free tier that stays awake.

1. Install Fly CLI: `curl -L https://fly.io/install.sh | sh`
2. Login: `fly auth login`
3. Launch: `fly launch` (in project directory)
4. Deploy: `fly deploy`

### Option 4: PythonAnywhere (Free Tier)

1. Sign up at [PythonAnywhere](https://www.pythonanywhere.com)
2. Upload your files
3. Configure web app
4. Free tier has some limitations but stays awake

### Environment Variables

No environment variables are required for basic deployment. The app will automatically use the PORT environment variable provided by the hosting service.

## Project Structure

```
navi/
├── app.py              # Flask application
├── generator.py        # Map generation logic
├── path_maker.py       # Pathfinding algorithms
├── requirements.txt    # Python dependencies
├── render.yaml         # Render deployment configuration
├── static/
│   ├── script.js       # Frontend JavaScript
│   ├── styles.css      # Styling
│   └── img/            # Image assets
└── templates/
    └── index.html      # Main HTML template
```

## Technologies Used

- **Backend**: Flask, Python
- **Frontend**: Vanilla JavaScript, HTML5 Canvas
- **Algorithms**: Dijkstra, A* (planned)
- **Deployment**: Render, Gunicorn

## License

This project is open source and available for personal and educational use.

