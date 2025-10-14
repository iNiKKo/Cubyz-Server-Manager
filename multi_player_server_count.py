import time
import re
from threading import Thread
import requests
import os

# === CONFIG ===
LOG_PATH = "/home/minipc/Desktop/Cubyz/logs/latest.log"  # Path to your log file
SERVER_ID = "ashframe"  # server name
SCRIPT_VERSION = "1.0"  # Do not change
CENTRAL_URL = "https://semiacademic-loni-unseducibly.ngrok-free.dev/update"
SEND_INTERVAL = 10  # Seconds between updates
# ==============

connected_players = set()
death_count = 0


join_regex = re.compile(r'\[info\]: User (.+?) joined')
leave_regex = re.compile(r'\[info\]: Chat: (.+?) left')
death_regex = re.compile(r'\[info\]: Chat: .*? died of fall damage')

def clean_name(name):
    name = re.sub(r'§.', '', name)
    name = re.sub(r'#([0-9a-fA-F]{6})', '', name)
    name = re.sub(r'[^\w\s]', '', name)
    return name.strip()

def follow_log():
    global connected_players, death_count
    print("Watching log for new activity...")

    try:
        with open(LOG_PATH, "r", encoding="utf-8") as f:
            f.seek(0, os.SEEK_END)  
            while True:
                line = f.readline()
                if not line:
                    time.sleep(0.1)
                    continue

                if join_regex.search(line):
                    player = clean_name(join_regex.search(line).group(1))
                    if player not in connected_players:
                        connected_players.add(player)
                        print(f"JOIN: {player}")

                elif leave_regex.search(line):
                    player = clean_name(leave_regex.search(line).group(1))
                    if player in connected_players:
                        connected_players.discard(player)
                        print(f"LEAVE: {player}")

                elif death_regex.search(line):
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
        print(f"✅ Sent update: {data}")
        death_count = 0
    except Exception as e:
        print(f"❌ Failed to send update: {e}")

def periodic_send():
    while True:
        send_update()
        time.sleep(SEND_INTERVAL)

if __name__ == "__main__":
    print("Starting Cubyz Tracker...")
    print("Waiting for players to join...")

    Thread(target=follow_log, daemon=True).start()
    Thread(target=periodic_send, daemon=True).start()

    while True:
        time.sleep(1)

