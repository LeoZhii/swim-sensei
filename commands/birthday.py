import datetime
from data import webscrape

birthdays = webscrape.swimmer_bday


# Helper function to calculate age
def get_age(swimmer_name):
    today = datetime.date.today()  # Current date
    name, bday = webscrape.name_match(birthdays, swimmer_name)

    if bday is None:
        return None  # Swimmer not found

    bday = datetime.datetime.strptime(bday, "%Y-%m-%d").date()
    age = today.year - bday.year - ((today.month, today.day) < (bday.month, bday.day))
    return age


# Command setup
async def setup(bot, swimmer_data):
    @bot.tree.command(name="get_age", description="Retrieve a swimmer's age.")
    async def get_age_command(interaction, swimmer: str):
        age = get_age(swimmer)
        if age is None:
            await interaction.response.send_message(
                f"Could not find the swimmer '{swimmer}' in the database.", ephemeral=True
            )
        else:
            await interaction.response.send_message(
                f"{swimmer} is {age} years old.", ephemeral=True
            )
