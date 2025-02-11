from table2ascii import table2ascii as t2a, PresetStyle
import regex

# Helper function to retrieve the full name of a swimmer
def fullname(first_name, swimmer_data):
    for full_name in swimmer_data.keys():
        if full_name.split()[0].lower() == first_name.lower():
            return full_name
    return None


# Function to find the best times for a swimmer
def findBest(swimmer, distance, stroke, swimmer_data):
    if swimmer not in swimmer_data:
        return None  # Indicate no data found

    best_times = swimmer_data[swimmer]
    rows = []
    for event in best_times[1:]:  # Skip the header row
        event_name = event[0]
        course = event[1]
        time = event[2]
        points = event[3]
        date = regex.sub(r'\d{1,2}\s', '', event[4])  # Remove the day
        if distance in event_name and stroke in event_name.lower():
            rows.append([course, time, points, date])

    return rows if rows else None


# Main command setup function
async def setup(bot, swimmer_data):
    @bot.tree.command(name="get_times", description="Retrieve swimmer times.")
    async def get_times(interaction, name: str, distance: str, stroke: str):
        # Resolve the swimmer's name
        swimmer = fullname(name if name.lower() != "me" else interaction.user.display_name, swimmer_data)

        if not swimmer:
            await interaction.response.send_message(
                f"I cannot find a swimmer matching the name '{name}'. Please try again.", ephemeral=True
            )
            return

        results = findBest(swimmer, distance, stroke, swimmer_data)
        if not results:
            await interaction.response.send_message(
                f"I cannot find times for {swimmer} swimming {distance} {stroke}. Sorry!", ephemeral=True
            )
            return

        output = t2a(
            header=["Course", "Time", "Pts", "Date"],
            body=results,
            style=PresetStyle.thin_compact
        )
        print(f"\nREQUEST BY: {interaction.user.display_name}: find best {swimmer} {distance} {stroke}\n {output}", flush=True)
        await interaction.response.send_message(f"```\n{swimmer}'s {distance} {stroke} times:\n{output}\n```", ephemeral=True)
