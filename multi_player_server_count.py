from flask_cors import CORS
import time
import re
from flask import Flask, jsonify
from threading import Thread
import requests

#  CHANGE THIS CHHANGE THIS CHANGE THIS
log_path = "/home/minipc/Desktop/Cubyz/logs/latest.log"
#  CHANGE THIS CHHANGE THIS CHANGE THIS
connected_players = set()

join_regex = re.compile(r'\[info\]: User (.+?) joined')
leave_regex = re.compile(r'\[info\]: Chat: (.+?) left')

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
    global connected_players
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
    except FileNotFoundError:
        print(f"Log file not found: {log_path}")
    except Exception as e:
        print(f"Error reading log: {e}")

SERVER_ID = "ashframe"  # CHANGE THIS TO YOUR SERVER NAME
CENTRAL_URL = "https://semiacademic-loni-unseducibly.ngrok-free.dev/update"

def send_update():
    data = {
        "server_id": SERVER_ID,
        "player_count": len(connected_players),
        "players": list(connected_players)
    }
    try:
        requests.post(CENTRAL_URL, json=data)
        print(f"Sent update: {data}")
    except Exception as e:
        print(f"Failed to send update: {e}")

def periodic_send():
    while True:
        send_update()
        time.sleep(10)  # send every x seconds

if __name__ == "__main__":
    connected_players = build_initial_player_list()
    print(f"Initial players loaded: {connected_players}")
    Thread(target=follow_log, daemon=True).start()
    Thread(target=periodic_send, daemon=True).start()


    while True:
        time.sleep(1)
