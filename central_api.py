from flask import Flask, request, jsonify
import json
import time
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DATA_FILE = "servers.json"


try:
    with open(DATA_FILE, "r") as f:
        server_data = json.load(f)
except:
    server_data = {}

@app.route("/update", methods=["POST"])
def update():
    data = request.json
    server_id = data.get("server_id")
    if not server_id:
        return {"error": "Missing server_id"}, 400


    previous = server_data.get(server_id, {})
    previous_deaths = previous.get("death_count", 0)


    new_deaths = data.get("new_deaths", 0)
    total_deaths = previous_deaths + new_deaths

    server_data[server_id] = {
        "player_count": data.get("player_count", 0),
        "players": data.get("players", []),
        "death_count": total_deaths,
        "status": data.get("status", "online"),
        "script_version": data.get("script_version", "unknown"),
        "timestamp": time.time()
    }

    with open(DATA_FILE, "w") as f:
        json.dump(server_data, f, indent=2)

    return {"status": "ok"}

@app.route("/servers.json")
def servers():
    return jsonify(server_data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

