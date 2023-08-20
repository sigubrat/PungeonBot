import sys
from typing import Any, Coroutine
import discord
from discord import app_commands
import random
from discord.flags import Intents
from util.ConfigHandler import ConfigHandler
from typing import Optional


description = "A bot for PnD"

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

configHandler = ConfigHandler()
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

    if d not in [4, 6, 8, 10, 12, 20]:
        await interaction.response.send_message(f"The die you provided ({rolls}d{d}) does not match any DnD standard die")

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

    await interaction.response.send_message(f"```{interaction.user.display_name} rolled: {result}```")
    print(f"{interaction.user} rolled {result}")


client.run(token)

