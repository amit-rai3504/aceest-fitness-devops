# ACEest Fitness & Gym — DevOps Assignment

![CI](https://github.com/amit-rai3504/aceest-fitness-devops/actions/workflows/ci.yaml/badge.svg)

A Flask API for **ACEest Fitness & Gym**.  
This project demonstrates core DevOps practices: version control, automated testing, containerization, and CI/CD with GitHub Actions.

---

## 📂 Project Structure
```
aceest-fitness-devops/
├── aceest_fitness/        # Flask app (workout API)
│   └── __init__.py
├── run.py                 # Entrypoint script
├── tests/                 # Pytest unit tests
│   └── test_app.py
├── requirements.txt       # Python dependencies
├── Dockerfile             # Containerization
├── .dockerignore
├── .gitignore
├── .github/workflows/ci.yml  # GitHub Actions workflow
└── README.md
```

---

## 🚀 Running the Application Locally

### 1. Setup
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Run
```bash
python run.py
```
Visit [http://localhost:8080/health](http://localhost:8080/health) → should return `ok`.

---

## 📡 API Endpoints

- `GET /health` → Health check (`ok`)
- `GET /` → App info
- `POST /workouts` → Add a workout  
  Request body:
  ```json
  {"workout": "Pushups", "duration": 15}
  ```
- `GET /workouts` → List all workouts

---

## 🧪 Running Tests

```bash
pytest -q --cov=./ --cov-report=term
```

---

## 🐳 Docker Usage

### Build image
```bash
docker build -t aceest-fitness:local .
```

### Run container
```bash
docker run --rm -p 8080:8080 aceest-fitness:local
```

### Run tests inside container
```bash
docker run --rm aceest-fitness:local pytest -q
```

---

## ⚙️ CI/CD with GitHub Actions

Every push/PR triggers the pipeline:

1. **Build & Test**  
   - Install dependencies  
   - Run pytest with coverage  

2. **Docker Test**  
   - Build Docker image  
   - Run pytest inside the image  

Artifacts: `coverage.xml` uploaded on each run.  
The badge at the top shows build status for `main`.
