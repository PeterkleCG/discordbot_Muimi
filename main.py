import os
import discord
from discord.ext import commands
from discord import app_commands

from myserver import server_on

# Intents and bot setup
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# Create slash command
@bot.tree.command(name="of", description="Calculate Overflow using HP and DMG.")
@app_commands.describe(hp="Enter HP value", dmg="Enter DMG value")
async def overflow(interaction: discord.Interaction, hp: float, dmg: float):
    if dmg == 0:
        await interaction.response.send_message("Error: DMG cannot be zero.", ephemeral=True)
        return
    
    time = 110 - (90 * (hp / dmg))
    time = min(time, 90)  # Ensure time does not exceed 90
    
    await interaction.response.send_message(f"Calculated Overflow Time: `{time:.2f}`")

# Sync commands on bot startup
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user}")

server_on()

# Run the bot
bot.run(os.getenv('TOKEN'))