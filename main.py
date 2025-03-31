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
    
     # Calculate overflow time
    time = 110 - (90 * (hp / dmg))
    time = min(time, 90)  # Cap time at 90
    
    # Convert to minutes and seconds format
    minutes = int(time // 60)
    seconds = int(time % 60)
    formatted_time = f"{minutes}:{seconds:02d}"

    # Create embed
    embed = discord.Embed(title="OVERFLOW TIME GIVEN WITH DAMAGE", color=discord.Color.blue())
    embed.add_field(name="Boss HP", value=f"{hp}", inline=True)
    embed.add_field(name="Damage Dealt", value=f"{dmg}", inline=True)
    embed.add_field(name="Equation", value=f"overflow (seconds) = 110 - (90 * ({hp} / {dmg}))", inline=False)
    embed.add_field(name="Result", value=f"overflow (seconds) = `{time:.2f}` ({formatted_time})", inline=False)

    await interaction.response.send_message(embed=embed)

# Sync commands on bot startup
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user}")

server_on()

# Run the bot
bot.run(os.getenv('TOKEN'))
