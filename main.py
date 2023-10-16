import discord
from keep_alive import keep_alive
from secret import TOKEN
import webscrape

intents = discord.Intents().all()
client = discord.Client(intents=intents)
webscrape.update()


@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))


@client.event
async def on_message(message):
  if message.author == client.user:
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


# keep discord bot online
keep_alive()

client.run(TOKEN)
