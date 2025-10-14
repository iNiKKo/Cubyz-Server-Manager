import time
import re
from threading import Thread
import requests

# === CONFIG ===
LOG_PATH = "/home/minipc/Desktop/Cubyz/logs/latest.log"  # YOUR LOG PATH
SERVER_ID = "ashframe"  # YOUR SERVER NAME
SCRIPT_VERSION = "1.0" # DONT TOUCH ME
CENTRAL_URL = "https://semiacademic-loni-unseducibly.ngrok-free.dev/update" # DONT TOUCH ME
SEND_INTERVAL = 10  # seconds
# ==============

connected_players = set()
death_count = 0

# Regex to detect join, leave, death lines
join_regex = re.compile(r'\[info\]: User (.+?) joined')
leave_regex = re.compile(r'\[info\]: Chat: (.+?) left')
death_regex = re.compile(r'\[info\]: Chat: .*? died of fall damage')

def clean_name(name):
    # Clean player names (remove colors and symbols)
    name = re.sub(r'§.', '', name)
    name = re.sub(r'#([0-9a-fA-F]{6})', '', name)
    name = re.sub(r'[^\w\s]', '', name)
    return name.strip()

def build_initial_player_list():
    players = set()
    try:
        with open(LOG_PATH, "r", encoding="utf-8") as f:
            for line in f:
                join_match = join_regex.search(line)
                if join_match:
                    players.add(clean_name(join_match.group(1)))
                leave_match = leave_regex.search(line)
                if leave_match:
                    players.discard(clean_name(leave_match.group(1)))
    except FileNotFoundError:
        print(f"Log file not found: {LOG_PATH}")
    except Exception as e:
        print(f"Error reading log for initial player list: {e}")
    return players

def follow_log():
    global connected_players, death_count
    try:
        with open(LOG_PATH, "r", encoding="utf-8") as f:
            f.seek(0, 2)  # Go to end of file for live tailing
            while True:
                line = f.readline()
                if not line:
                    time.sleep(0.1)
                    continue

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

                if death_regex.search(line):
                    death_count += 1
                    print(f"DEATH DETECTED | Total deaths: {death_count}")

    except FileNotFoundError:
        print(f"Log file not found: {LOG_PATH}")
    except Exception as e:
        print(f"Error following log: {e}")

def send_update():
    global death_count
    data = {
        "server_id": SERVER_ID,
        "player_count": len(connected_players),
        "players": list(connected_players),
        "new_deaths": death_count,
        "status": "online",
        "script_version": SCRIPT_VERSION
    }
    try:
        requests.post(CENTRAL_URL, json=data)
        print(f"Sent update: {data}")
        death_count = 0  # Reset deaths after sending
    except Exception as e:
        print(f"Failed to send update: {e}")

def periodic_send():
    while True:
        send_update()
        time.sleep(SEND_INTERVAL)

if __name__ == "__main__":
    connected_players = set()
    print(f"Initial players loaded: {connected_players}")

    Thread(target=follow_log, daemon=True).start()
    Thread(target=periodic_send, daemon=True).start()

    while True:
        time.sleep(1)

