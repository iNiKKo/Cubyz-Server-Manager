from flask_cors import CORS
import time
import re
from flask import Flask, jsonify
from threading import Thread

app = Flask(__name__)
CORS(app)
# Add your full path for the latest.log
log_path = "YOUR/FULL/PATH/latest.log"

connected_players = set()

# Regex to detect joins and leaves from your log format
join_regex = re.compile(r'\[info\]: User (.+?) joined')
leave_regex = re.compile(r'\[info\]: Chat: (.+?) left')


def clean_name(name):
    # Remove § color codes (if any)
    cleaned = re.sub(r'§[^ ]*', '', name)
    # Remove hex color codes like #ff7700
    cleaned = re.sub(r'#([0-9a-fA-F]{6})', '', cleaned)
    # Remove extra whitespace and non-alphanumeric (except spaces)
    cleaned = re.sub(r'[^\w\s]', '', cleaned)
    return cleaned.strip()


def build_initial_player_list():
    players = set()
    try:
        with open(log_path, "r", encoding="utf-8") as f:
            for line in f:
                join_match = join_regex.search(line)
                if join_match:
                    name = clean_name(join_match.group(1))
                    players.add(name)
                leave_match = leave_regex.search(line)
                if leave_match:
                    name = clean_name(leave_match.group(1))
                    players.discard(name)
    except FileNotFoundError:
        print(f"Log file not found: {log_path}")
    except Exception as e:
        print(f"Error building initial player list: {e}")
    return players

def follow_log():
    global connected_players
    try:
        with open(log_path, "r", encoding="utf-8") as f:
            f.seek(0, 2)  # Go to the end of file
            while True:
                line = f.readline()
                if not line:
                    time.sleep(0.1)
                    continue

                print(f"LOG LINE: {line.strip()}")

                join_match = join_regex.search(line)
                if join_match:
                    player = clean_name(join_match.group(1))
                    if player not in connected_players:
                        connected_players.add(player)
                        print(f"JOIN: {player}")

                leave_match = leave_regex.search(line)
                if leave_match:
                    player = clean_name(leave_match.group(1))
                    if player in connected_players:
                        connected_players.discard(player)
                        print(f"LEAVE: {player}")

    except FileNotFoundError:
        print(f"Log file not found: {log_path}")
    except Exception as e:
        print(f"Error reading log: {e}")

@app.route("/")
def index():
    return "<h1>Cubyz Player Count API</h1><p>Try /playercount or /playerlist</p>"

@app.route("/playercount")
def player_count():
    return jsonify(players=len(connected_players))

@app.route("/playerlist")
def player_list():
    return jsonify(players=list(connected_players))

def run_flask():
    app.run(host="0.0.0.0", port=5000)

if __name__ == "__main__":
    connected_players = build_initial_player_list()
    print(f"Initial players loaded: {connected_players}")
    Thread(target=follow_log, daemon=True).start()
    run_flask()

