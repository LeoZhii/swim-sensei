import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import json
from messageController import load_commands

load_dotenv()
COMMAND_PREFIX = "?"
SWIMMER_DATA_FILE = "data/best-times.json"

bot = commands.Bot(command_prefix=COMMAND_PREFIX, intents=discord.Intents.all())
discord_token = os.getenv("DISCORD_TOKEN")

# Load swimmer data
def load_swimmer_data(filename):
    with open(filename, 'r') as file:
        return json.load(file)

swimmer_data = load_swimmer_data(SWIMMER_DATA_FILE)


@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")
    print("Syncing Commands...")
    await load_commands(bot, swimmer_data)
    print("Commands Successfully Synced.")

bot.run(discord_token)