import discord
from discord.ext import tasks
import requests

# ==== CONFIGURATION ====
BOT_TOKEN = 'long string of letters and numbers here'
CHANNEL_ID = 11111111  # Your voice/text channel ID
SERVER_ID = 'YOUR SERVER NAME'
API_URL = 'USE NGROK FOR URL'
UPDATE_INTERVAL = 300  # 5 minutes in seconds
# ========================

intents = discord.Intents.default()
client = discord.Client(intents=intents)

last_count = None

@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user}")
    update_channel_name.start()

@tasks.loop(seconds=UPDATE_INTERVAL)
async def update_channel_name():
    global last_count
    try:
        print(f"🔎 Fetching server data from: {API_URL}")
        response = requests.get(API_URL)
        if response.status_code != 200:
            print(f"❌ Failed to fetch data: HTTP {response.status_code}")
            return

        servers = response.json()


        server_data = servers.get(SERVER_ID)
        if not server_data:
            print(f"⚠️ Server ID '{SERVER_ID}' not found in API response.")
            return

        count = server_data.get("player_count", 0)

        if count != last_count:
            channel = await client.fetch_channel(CHANNEL_ID)
            new_name = f"🎮 Players Online: {count}"
            await channel.edit(name=new_name)
            print(f"📝 Renamed channel to: {new_name}")
            last_count = count
        else:
            print("⏳ No change in player count, skipping rename")

    except Exception as e:
        print(f"⚠️ Error during update: {e}")

client.run(BOT_TOKEN)
