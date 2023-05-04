import discord
from keep_alive import keep_alive
from secret import TOKEN

intents = discord.Intents().all()
client = discord.Client(intents=intents)


@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))


@client.event
async def on_message(message):
  if message.author == client.user:
    return

  if message.content.startswith("$hello"):
    await message.channel.send("Hello!")

  if message.content.startswith("?"):
    username = str(message.author.display_name).split('#')[0]
    # format message as ?(name) distance stroke
    user_message = str(message.content).lower().strip("? ")
    user_message = user_message.split()
    if user_message[0].startswith("1") or user_message[0].startswith(
        "2") or user_message[0].startswith("5"):
      swimmer = username.lower()
      distance = user_message[0]
      stroke = user_message[1]
      course = user_message[2]
    else:
      swimmer = user_message[0]
      distance = user_message[1]
      stroke = user_message[2]
      course = user_message[3]

    if "short" in course:
      course = "25"
    elif "long" in course:
      course = "50"

    # open file
    file = open("SwimDataTest1.csv")
    file.readline()
    for line in file:
      event = line.split(",")

      if swimmer in event[0].lower() and distance in event[1].lower(
      ) and stroke in event[1].lower() and course in event[2].lower():
        await message.channel.send(
          "The best time for {}'s {} in a {} pool is {}, achieved at {} {}".
          format(event[0], event[1], event[2], event[3], event[4], event[5],
                 event[6]))
        return
    await message.channel.send(
      "I cannot find a time for {} swimming {} {}. Sorry!".format(
        swimmer, distance, stroke))


keep_alive()
client.run(TOKEN)