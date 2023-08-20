import sys
from typing import Any, Coroutine, Literal
import discord
from discord import app_commands
import random
from discord.flags import Intents
from typing import Optional
import pytz
import datetime

from util.ConfigHandler import ConfigHandler
from util.TimezoneHandler import AsyncTimezoneHandler

description = "A bot for PnD"

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

configHandler = ConfigHandler()
timezoneHandler = AsyncTimezoneHandler()

token = configHandler.get_token()
guild_id = configHandler.get_guild_id()
if isinstance(token, Exception) or isinstance(guild_id, Exception):
    sys.exit(1)

MY_GUILD = discord.Object(guild_id)    

class BotClient(discord.Client):
    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        self.tree = app_commands.CommandTree(self)
    
    async def setup_hook(self) -> Coroutine[Any, Any, None]:
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)

client = BotClient(intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user} (ID: {client.user.id})")
    print("-------")


@client.tree.command()
@app_commands.describe(
    dice="What dice you want to use (1d20, 1d6, 2d4 etc)",
    modifier="Optional: roll modifier"
)
async def roll(interaction: discord.Interaction, dice: str, modifier: int = 0):
    """Rolls a dice in NdN format where N is a number"""
    dice.replace("D", "d")
    try:
        rolls, d = map(int, dice.split('d'))
    except Exception:
        await interaction.response.send_message("Format must be in NdN e.g., 1d20")
        return
    
    if rolls < 1:
        await interaction.response.send_message(f"Minimum 1 roll is required you silly sausage :)")
        return

    if d not in [4, 6, 8, 10, 12, 20]:
        await interaction.response.send_message(f"The die you provided ({rolls}d{d}) does not match any DnD standard die")
        return

    roll_results = [random.randint(1, d) for _ in range(rolls)]
    total = sum(roll_results)
    total += modifier
    rolls_string = ", ".join(map(str, roll_results))
    result = f"[{rolls_string}]"
    
    if modifier > 0:
        result += f" +{modifier}"
    elif modifier < 0:
        result += f" {modifier}"
    
    result += f" = {total}"

    await interaction.response.send_message(f"```{interaction.user.display_name} rolled {dice}: {result}```")
    print(f"{interaction.user} rolled {result}")


@client.tree.command()
@app_commands.describe(
    continent="Which continent you're in.",
    city="The city associated with your time-zone (Use underscore for spaces, e.g., New_York)"
)
async def add_user(interaction: discord.Interaction, continent: Literal['America', 'Europe'], city: str):
    """Add user for time-zone commands"""
    timezone = f"{continent}/{city.capitalize()}"

    print(f"Trying to add user: {interaction.user} with timezone: {timezone}")

    if timezone not in pytz.all_timezones:
        await interaction.response.send_message("Provided timezone does not exist!")
        return
    
    try:
        await timezoneHandler.add_user(str(interaction.user), timezone)
    except Exception as e:
        await interaction.response.send_message("Shit's fucked, yo. Please try again without murdering me. It hurts :'(")
        return

    await interaction.response.send_message("User succesfully updated!")

@client.tree.command()
@app_commands.describe(
    date_time="Date and time in this format only: 2023-08-23 16:00:00"
)
async def suggest_time(interaction: discord.Interaction, date_time: str):
    """Suggest a datetime and see what time it is for everyone else"""
    print(f"User {interaction.user} has suggested time: {date_time}")
    
    timezone = await timezoneHandler.read_user(str(interaction.user))
    if isinstance(timezone, Exception):
        print("Timezone is fucked")
        await interaction.response.send_message("Pleaaseee provide a proper datetime")
        return
    print("Timezone:", timezone)
    dt = timezoneHandler.date_from_string(timezone, date_time)
    print("dt", dt)
    if isinstance(dt, Exception):
        print("Dt is fucked")
        await interaction.response.send_message("Pleaaseee provide a proper datetime")
        return
    
    users = await timezoneHandler.get_local_datetime_all(dt)
    if isinstance(users, Exception):
        await interaction.response.send_message("I'm sorry, but something fucky happened")
        return

    retval = ""
    for user in users:
        for key, val in user.items():
            retval += f"{key} - {val}\n"

    await interaction.response.send_message(retval)

client.run(token)

