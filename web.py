from flask import Flask, render_template, request, redirect
import json
import os
from dotenv import load_dotenv

load_dotenv()

STATS_FILE = "stats.json"
PASSWORD = os.getenv("WEB_PASSWORD", "")

app = Flask(__name__)

def load_stats():
    try:
        with open(STATS_FILE) as f:
            return json.load(f)
    except FileNotFoundError:
        return {"kills": 0, "deaths": 0}

def save_stats(stats):
    with open(STATS_FILE, "w") as f:
        json.dump(stats, f)

@app.route("/", methods=["GET", "POST"])
def dashboard():
    stats = load_stats()

    if request.method == "POST":
        if PASSWORD and request.form.get("password") != PASSWORD:
            return "Nieprawidłowe hasło", 403

        action = request.form.get("action")

        if action == "kill":
            stats["kills"] += 1
        elif action == "death":
            stats["deaths"] += 1
        elif action == "reset":
            stats = {"kills": 0, "deaths": 0}
        elif action == "resmonth":
            stats = {"kills": 0, "deaths": 0}

        save_stats(stats)
        return redirect("/")

    kd = stats["kills"] / stats["deaths"] if stats["deaths"] > 0 else stats["kills"]
    return render_template("dashboard.html", stats=stats, kd=kd, password_required=bool(PASSWORD))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)