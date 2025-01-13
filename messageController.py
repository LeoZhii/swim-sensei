import os
from importlib import import_module


async def load_commands(bot, swimmer_data):
    for filename in os.listdir('./commands'):
        if filename.endswith('.py') and not filename.startswith('__'):
            module = import_module(f"commands.{filename[:-3]}") # remove ".py"
            await module.setup(bot, swimmer_data)
