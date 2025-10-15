import time
import re
from threading import Thread
import requests
import os

# === CONFIG ===
LOG_PATH = "/home/minipc/Desktop/Cubyz/logs/latest.log"  # Path to your log file - CHANGE ME
SERVER_ID = "ashframe"  # Server name - CHANGE ME
GAMEMODE = "survival"  # Set game mode manually: "survival", "creative", etc.
SCRIPT_VERSION = "1.1"  # Do not change
CENTRAL_URL = "https://semiacademic-loni-unseducibly.ngrok-free.dev/update"  # Do not change
SEND_INTERVAL = 10  # Seconds between updates
# ==============

connected_players = set()
death_count = 0

# Regex patterns
join_regex = re.compile(r'\[info\]: User (.+?) joined')
leave_regex = re.compile(r'\[info\]: Chat:\s+(.+?)\s+left')
death_regex = re.compile(r'\[info\]: Chat: .*? died of fall damage')

def clean_name(name):
    name = re.sub(r'§#(?:[0-9a-fA-F]{6})', '', name)
    name = re.sub(r'#(?:[0-9a-fA-F]{6})', '', name)
    name = re.sub(r'(\*\*|__|~~)', '', name)
    name = re.sub(r'[^\w\u0400-\u04FF]', '', name)
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
                    player_raw = join_regex.search(line).group(1)
                    player = clean_name(player_raw)
                    print(f"JOIN: Raw='{player_raw}' | Cleaned='{player}'")
                    if player not in connected_players:
                        connected_players.add(player)
                        print(f"✅ Player added: {player}")
                    else:
                        print(f"⚠️ Player already in connected list: {player}")

                elif leave_regex.search(line):
                    player_raw = leave_regex.search(line).group(1)
                    player = clean_name(player_raw)
                    print(f"LEAVE: Raw='{player_raw}' | Cleaned='{player}'")
                    if player in connected_players:
                        connected_players.discard(player)
                        print(f"✅ Player removed: {player}")
                    else:
                        print(f"⚠️ Player not found in connected list: {player}")

                elif death_regex.search(line):
                    death_count += 1
                    print(f"☠️ DEATH DETECTED | Total deaths: {death_count}")

    except FileNotFoundError:
        print(f"❌ Log file not found: {LOG_PATH}")
    except Exception as e:
        print(f"💥 Error following log: {e}")

def send_update():
    global death_count
    data = {
        "server_id": SERVER_ID,
        "player_count": len(connected_players),
        "players": list(connected_players),
        "new_deaths": death_count,
        "status": "online",
        "script_version": SCRIPT_VERSION,
        "gamemode": GAMEMODE  # ✅ New field added
    }

    try:
        print(f"📤 Sending update: {data}")
        requests.post(CENTRAL_URL, json=data)
        print("✅ Update sent successfully.")
        death_count = 0
    except Exception as e:
        print(f"❌ Failed to send update: {e}")

def periodic_send():
    while True:
        send_update()
        time.sleep(SEND_INTERVAL)

if __name__ == "__main__":
    print("Starting Cubyz Manager...")
    print("Gamemode:", GAMEMODE)
    print("Waiting for players to join...")

    Thread(target=follow_log, daemon=True).start()
    Thread(target=periodic_send, daemon=True).start()

    while True:
        time.sleep(1)
