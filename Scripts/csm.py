import time
import re
from threading import Thread
import socket
import json
import os

# Configurable variables
LOG_PATH = "/home/minipc/Desktop/cubyz_auth_server/logs/latest.log"  # PATH TO YOUR LOGS
SERVER_ID = "Ashframe"  # SERVER NAME KEEP IT UNDER 2 WORDS
SERVER_IP = "cb.ashframe.net"  # YOUR SERVER IP
ICON_URL = "https://i.postimg.cc/7PzpSzKm/Snail.png"  # BANNER / ICON FOR YOUR CARD (on the website)
GAMEMODE = "survival"  # YOUR GAMEMODE
SCRIPT_VERSION = "1.3"
SEND_INTERVAL = 60
SPAWN_CLEAN_NAME = "SPAWN"  # Special user name that triggers "online" status currently doesnt work.


CENTRAL_API_IP = "api.ashframe.net" #new api that uses tcp not http
CENTRAL_API_PORT = 5001


connected_players = set()
death_count = 0
server_status = "online"


join_chat_regex = re.compile(r'\[info\]: Chat:\s+(.*?)\s+joined', re.IGNORECASE)
join_user_regex = re.compile(r'\[info\]: User\s+(.*?)\s+joined using version', re.IGNORECASE)
leave_regex = re.compile(r'\[info\]: Chat:\s+(.+?)\s+left', re.IGNORECASE)
death_regex = re.compile(r'\[info\]: Chat: .*? died', re.IGNORECASE)


info_port_regex = re.compile(r'^\[info\]:\s+.*?:(\d{1,5})$', re.IGNORECASE)

def clean_name(name):

    name = re.sub(r'§#(?:[0-9a-fA-F]{6})', '', name)
    name = re.sub(r'#(?:[0-9a-fA-F]{6})', '', name)
    name = re.sub(r'(\*\*|__|~~)', '', name)
    name = re.sub(r'[^\w\u0400-\u04FF]', '', name)
    return name.strip()

def update_status():

    global server_status
    spawn_present = SPAWN_CLEAN_NAME in connected_players
    new_status = "online" if spawn_present else "offline"

    if new_status != server_status:
        server_status = new_status
        print(f"Server status changed to: {server_status.upper()}")
        send_update()

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


                if join_chat_regex.search(line):
                    player_raw = join_chat_regex.search(line).group(1)
                    player = clean_name(player_raw)
                    print(f"JOIN (chat): Raw='{player_raw}' | Cleaned='{player}'")
                    if player not in connected_players:
                        connected_players.add(player)
                        print(f"Player added: {player}")
                        update_status()
                    else:
                        print(f"Player already in connected list: {player}")

                elif join_user_regex.search(line):
                    player_raw = join_user_regex.search(line).group(1)
                    player = clean_name(player_raw)
                    print(f"JOIN (user): Raw='{player_raw}' | Cleaned='{player}'")
                    if player not in connected_players:
                        connected_players.add(player)
                        print(f"Player added: {player}")
                        update_status()
                    else:
                        print(f"Player already in connected list: {player}")


                elif leave_regex.search(line):
                    player_raw = leave_regex.search(line).group(1)
                    player = clean_name(player_raw)
                    print(f"LEAVE: Raw='{player_raw}' | Cleaned='{player}'")
                    if player in connected_players:
                        connected_players.discard(player)
                        print(f"Player removed: {player}")
                        update_status()
                    else:
                        print(f"Player not found in connected list: {player}")


                elif death_regex.search(line):
                    death_count += 1
                    print(f"DEATH DETECTED | Total deaths: {death_count}")


                elif info_port_regex.search(line):

                    port = info_port_regex.search(line).group(1)
                    print(f"Server started with port: {port}")

                    server_status = "online"
                    send_update()

    except FileNotFoundError:
        print(f"Log file not found: {LOG_PATH}")
    except Exception as e:
        print(f"Error following log: {e}")

def send_update():

    global death_count, server_status
    data = {
        "server_id": SERVER_ID,
        "players": list(connected_players),
        "player_count": len(connected_players),
        "new_deaths": death_count,
        "status": server_status,
        "script_version": SCRIPT_VERSION,
        "gamemode": GAMEMODE,
        "ip": SERVER_IP,
        "icon": ICON_URL,
        "timestamp": int(time.time())
    }


    data_string = json.dumps(data)

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((CENTRAL_API_IP, CENTRAL_API_PORT))
            s.sendall(data_string.encode('utf-8'))

        print(f"Sent update: {data}")
        death_count = 0

    except Exception as e:
        print(f"Failed to send update: {e}")

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
