import os
import discord
from discord.ext import commands
from discord import app_commands

from myserver import server_on

# Intents and bot setup
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.command()
async def sync(ctx):
    await bot.tree.sync()
    await ctx.send("Slash commands synced!")

# Command: /of - Calculates Overflow Time
@bot.tree.command(name="of", description="Calculate Overflow using HP and DMG.")
@app_commands.describe(hp="Enter HP value", dmg="Enter DMG value")
async def overflow(interaction: discord.Interaction, hp: float, dmg: float):
    if dmg == 0:
        await interaction.response.send_message("Error: DMG cannot be zero.", ephemeral=True)
        return
    
    # Calculate overflow time
    time = 110 - (90 * (hp / dmg))
    time = min(time, 90)  # Cap at 90 seconds

    # Convert to minutes and seconds
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

# Command: /ofm - Calculates Required DMG for Full Overflow
@bot.tree.command(name="ofm", description="Calculate required DMG for full overflow time.")
@app_commands.describe(hp="Enter HP value")
async def overflow_max(interaction: discord.Interaction, hp: float):
    dmg = hp / 0.2222  # Calculate required damage

    # Create embed
    embed = discord.Embed(title="FULL OVERFLOW DAMAGE REQUIREMENT", color=discord.Color.green())
    embed.add_field(name="Boss HP", value=f"{hp}", inline=True)
    embed.add_field(name="Equation", value=f"DMG = {hp} / 0.2222", inline=False)
    embed.add_field(name="You will need to deal:", value=f"**{dmg:.2f}** DMG\nin order to get full overflow time.", inline=False)

    await interaction.response.send_message(embed=embed)

# Sync commands on bot startup
@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user}")
    
server_on()

# Run the bot
bot.run(os.getenv('TOKEN'))
