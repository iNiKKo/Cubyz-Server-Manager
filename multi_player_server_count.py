from flask_cors import CORS
import time
import re
from flask import Flask, jsonify
from threading import Thread
import requests

# === CHANGE THESE ===
log_path = "/home/minipc/Desktop/Cubyz/logs/latest.log" # YOUR LOG PATH
SERVER_ID = "ashframe"  # YOUR SERVER NAME
SCRIPT_VERSION = "1.0" # DON'T TOUCH
CENTRAL_URL = "https://semiacademic-loni-unseducibly.ngrok-free.dev/update" # DON'T TOUCH
# ====================

connected_players = set()
death_count = 0  # Count fall deaths

# Regex patterns
join_regex = re.compile(r'\[info\]: User (.+?) joined')
leave_regex = re.compile(r'\[info\]: Chat: (.+?) left')
death_regex = re.compile(r'\[info\]: Chat: .*? died of fall damage')

def clean_name(name):
    cleaned = re.sub(r'§[^ ]*', '', name)
    cleaned = re.sub(r'#([0-9a-fA-F]{6})', '', cleaned)
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
    global connected_players, death_count
    try:
        with open(log_path, "r", encoding="utf-8") as f:
            f.seek(0, 2)
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
        print(f"Log file not found: {log_path}")
    except Exception as e:
        print(f"Error reading log: {e}")

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
        death_count = 0
    except Exception as e:
        print(f"Failed to send update: {e}")

def periodic_send():
    while True:
        send_update()
        time.sleep(10)

if __name__ == "__main__":
    connected_players = build_initial_player_list()
    print(f"Initial players loaded: {connected_players}")
    Thread(target=follow_log, daemon=True).start()
    Thread(target=periodic_send, daemon=True).start()
    
    while True:
        time.sleep(1)

