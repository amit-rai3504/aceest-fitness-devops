from flask import Flask, jsonify, request, render_template, redirect, url_for

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

# ----- Minimal HTML GUI (new) -----

@app.get("/ui")
def ui_home():
    # optional message via query string (?msg=... or ?err=...)
    msg = request.args.get("msg") or ""
    err = request.args.get("err") or ""
    return render_template("ui.html", workouts=DB["workouts"], msg=msg, err=err)

@app.post("/ui/submit")
def ui_submit():
    # Handle standard form submission (no JS required)
    name = (request.form.get("workout") or "").strip()
    duration_raw = request.form.get("duration", "").strip()

    errors = []
    if not name or not duration_raw:
        errors.append("Please enter both workout and duration.")
    else:
        try:
            duration = int(duration_raw)
            if duration <= 0:
                errors.append("Duration must be a positive integer (minutes).")
        except ValueError:
            errors.append("Duration must be a number.")

    if errors:
        return redirect(url_for("ui_home", err="; ".join(errors)))

    DB["workouts"].append({"workout": name, "duration": int(duration_raw)})
    return redirect(url_for("ui_home", msg=f"'{name}' added successfully!"))
