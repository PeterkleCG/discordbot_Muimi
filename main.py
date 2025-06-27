import os
import discord
from discord.ext import commands
from discord import app_commands

from myserver import server_on

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)


# Shared View for "Share to Public" button
class ShareView(discord.ui.View):
    def __init__(self, embed_to_share: discord.Embed):
        super().__init__(timeout=120)
        self.embed_to_share = embed_to_share

    @discord.ui.button(label="📢 แชร์ให้ทุกคนเห็น", style=discord.ButtonStyle.blurple)
    async def share(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.channel.send(embed=self.embed_to_share)
        await interaction.response.edit_message(content="✅ แชร์เรียบร้อยแล้ว", view=None)


@bot.command()
async def sync(ctx):
    await bot.tree.sync()
    await ctx.send("Slash commands synced!")


# /of command
@bot.tree.command(name="of", description="Calculate Overflow using HP and DMG.")
@app_commands.describe(hp="Enter HP value", dmg="Enter DMG value")
async def overflow(interaction: discord.Interaction, hp: float, dmg: float):
    if dmg == 0:
        await interaction.response.send_message("Error: DMG cannot be zero.", ephemeral=True)
        return

    time = 110 - (90 * (hp / dmg))
    time = min(time, 90)

    minutes = int(time // 60)
    seconds = int(time % 60)
    formatted_time = f"{minutes}:{seconds:02d}"

    embed = discord.Embed(title="OVERFLOW TIME GIVEN WITH DAMAGE", color=discord.Color.blue())
    embed.add_field(name="Boss HP", value=f"{hp}", inline=True)
    embed.add_field(name="Damage Dealt", value=f"{dmg}", inline=True)
    embed.add_field(name="Equation", value=f"overflow (seconds) = 110 - (90 * ({hp} / {dmg}))", inline=False)
    embed.add_field(name="Result", value=f"overflow (seconds) = `{time:.2f}` ({formatted_time})", inline=False)

    view = ShareView(embed)
    await interaction.response.send_message(embed=embed, view=view, ephemeral=True)


# /ofm command
@bot.tree.command(name="ofm", description="Calculate required DMG for full overflow time.")
@app_commands.describe(hp="Enter HP value")
async def overflow_max(interaction: discord.Interaction, hp: float):
    dmg = hp / 0.2222

    embed = discord.Embed(title="FULL OVERFLOW DAMAGE REQUIREMENT", color=discord.Color.green())
    embed.add_field(name="Boss HP", value=f"{hp}", inline=True)
    embed.add_field(name="Equation", value=f"DMG = {hp} / 0.2222", inline=False)
    embed.add_field(name="You will need to deal:", value=f"**{dmg:.2f}** DMG\nin order to get full overflow time.", inline=False)

    view = ShareView(embed)
    await interaction.response.send_message(embed=embed, view=view, ephemeral=True)


# /of2 command
@bot.tree.command(name="of2", description="Calculate Overflow Time with 2 damages.")
@app_commands.describe(hp="Boss HP", dmg1="First Damage dealt", dmg2="Second Damage dealt")
async def of2(interaction: discord.Interaction, hp: float, dmg1: float, dmg2: float):
    if dmg1 == 0 or dmg2 == 0:
        await interaction.response.send_message("Error: DMG values cannot be zero.", ephemeral=True)
        return

    score1 = hp - dmg2
    score2 = hp - dmg1

    time1 = 110 - (90 * (score1 / dmg1))
    time2 = 110 - (90 * (score2 / dmg2))
    time1 = min(time1, 90)
    time2 = min(time2, 90)

    m1, s1 = divmod(int(time1), 60)
    m2, s2 = divmod(int(time2), 60)
    fmt1 = f"{m1}:{s1:02d}"
    fmt2 = f"{m2}:{s2:02d}"

    embed = discord.Embed(title="OVERFLOW TIME GIVEN WITH DAMAGE", color=discord.Color.purple())
    embed.add_field(name="Boss HP", value=f"**{hp}**", inline=False)

    embed.add_field(name="🔹 Damage Dealt 1", value=f"**{dmg1}**", inline=False)
    embed.add_field(name="Score 1", value=f"**HP - DMG2 = {hp} - {dmg2} = {score1}**", inline=False)
    embed.add_field(name="Equation 1", value=f"overflow (seconds) = 110 - [90 × ({score1} ÷ {dmg1})]", inline=False)
    embed.add_field(name="Result 1", value=f"overflow (seconds) = **{time1:.2f}** (`{fmt1}`)", inline=False)

    embed.add_field(name="\u200b", value="━━━━━━━━━━━━━━━━━━━━━━", inline=False)

    embed.add_field(name="🔹 Damage Dealt 2", value=f"**{dmg2}**", inline=False)
    embed.add_field(name="Score 2", value=f"**HP - DMG1 = {hp} - {dmg1} = {score2}**", inline=False)
    embed.add_field(name="Equation 2", value=f"overflow (seconds) = 110 - [90 × ({score2} ÷ {dmg2})]", inline=False)
    embed.add_field(name="Result 2", value=f"overflow (seconds) = **{time2:.2f}** (`{fmt2}`)", inline=False)

    view = ShareView(embed)
    await interaction.response.send_message(embed=embed, view=view, ephemeral=True)


@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"✅ Logged in as {bot.user}")


server_on()
bot.run(os.getenv('TOKEN'))
