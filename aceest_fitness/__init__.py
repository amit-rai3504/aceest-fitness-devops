# aceest_fitness/__init__.py
from flask import Flask, jsonify, request

app = Flask(__name__)
DB = {"workouts": []}

@app.get("/")
def index():
    return jsonify({"app": "ACEest Fitness & Gym", "message": "Welcome to ACEest API"}), 200

@app.get("/health")
def health():
    return "ok", 200

@app.get("/workouts")
def get_workouts():
    return jsonify(DB["workouts"]), 200

@app.post("/workouts")
def add_workout():
    data = request.get_json(silent=True) or {}
    name = (data.get("workout") or "").strip()
    try:
        duration = int(data.get("duration", 0))
    except (TypeError, ValueError):
        duration = 0
    errors = []
    if not name:
        errors.append("workout is required")
    if duration <= 0:
        errors.append("duration must be a positive integer (minutes)")
    if errors:
        return jsonify({"errors": errors}), 400
    entry = {"workout": name, "duration": duration}
    DB["workouts"].append(entry)
    return jsonify(entry), 201
