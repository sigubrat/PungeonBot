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
client.run(token)

@client.event
async def on_ready():
    print(f"Logged in as {client.user} (ID: {client.user.id})")
    print("-------")

@client.tree.command()
@app_commands.describe(
    dice="What dice you want to use (1d20, 1d6, 2d4 etc)"
)
async def roll(interaction: discord.Interaction, dice: str):
    """Rolls a dice in NdN format where N is a number"""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await interaction.response.send_message("Format must be in NdN e.g., 1d20")
        return
    
    roll = [random.randint(1, limit) for r in range(rolls)]
    total = sum(roll)
    result = ', '.join(str(roll))
    result += f' = {total}'
    await interaction.response.send_message(result)




