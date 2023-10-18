import discord
from discord import app_commands
from discord.ext import commands
from keep_alive import keep_alive
from secret import TOKEN
import webscrape

# OUTDATED
# intents = discord.Intents().all()
# client = discord.Client(intents=intents)
bot = commands.Bot(command_prefix="?", intents=discord.Intents.all())
webscrape.update()


@bot.event
async def on_ready():
  print("We have logged in as {0.user}".format(bot))
  try:
    synced = await bot.tree.sync()
    print(f"Synced {len(synced)} commands.")
  except Exception as e:
    print(e)


@bot.event
async def on_message(message):
  if message.author == bot.user:
    return

  if message.content.startswith("?"):
    username = str(message.author.display_name).split('#')[0]
    # format message as ?(name) distance stroke
    user_message = str(message.content).lower().strip("? ")
    user_message = user_message.split()

    # if swimmer name is not stated, proceed to distance and stroke
    if user_message[0].startswith("1") or user_message[0].startswith(
        "2") or user_message[0].startswith("5"):
      swimmer = username.lower()
      distance = user_message[0]
      stroke = user_message[1].lower()
    # if swimmer name is stated, proceed to collect name, distance, stroke
    else:
      swimmer = user_message[0]
      distance = user_message[1]
      stroke = user_message[2]

    # find swimmer ID
    name, id = webscrape.name_match(webscrape.swimmer_ID, swimmer)

    # if ID DNE
    if id == None:
      await message.channel.send(
        f'I cannot find times for {name}. Please try again!')
      return

    # open file
    file = open(f"{id}.csv")
    found = False
    await message.channel.send(f"{name}'s best times:")

    # iterate through file of best times
    for line in file:
      event = line.split(",")
      if distance in event[0] and stroke in event[0].lower():
        found = True
        await message.channel.send(line.replace(",", " | "))

    if found is False:
      await message.channel.send(
        f"I cannot find a time for {name} swimming {distance} {stroke}. Sorry!"
      )


# slash command for best time
@bot.tree.command(name="besttime",
                  description="Get the best time for a swimmer")
async def besttime(interaction: discord.Interaction, swimmer: str,
                   distance: str, stroke: str):
  message = findbest(swimmer, distance, stroke)
  await interaction.response.send_message(message)


# function that finds the best times of a swimmer
def findbest(swimmer, distance, stroke):
  messages = []
  delimiter = ""

  # check if name exists:
  name, id = webscrape.name_match(webscrape.swimmer_ID, swimmer)
  if id == None:
    return (f'I cannot find times for {name}. Please try again!')

  # open file
  file = open(f"{id}.csv")
  found = False
  messages.append(f"{name}'s best times:\n")

  # iterate through file of best times
  for line in file:
    event = line.split(",")
    if distance in event[0] and stroke in event[0].lower():
      found = True
      messages.append(line.replace(",", " | "))

  if found is False:
    return (
      f"I cannot find a time for {name} swimming {distance} {stroke}. Sorry!")

  return delimiter.join(messages)


# keep discord bot online
# keep_alive()

bot.run(TOKEN)
