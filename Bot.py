import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import os

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands.")
    except Exception as e:
        print(f"Sync error: {e}")

@bot.tree.command(name="serverlist", description="List the servers the bot is in and its permissions.")
async def serverlist(interaction: discord.Interaction):
    embed = discord.Embed(
        title="Server List",
        description="Here is a list of servers I am in along with my permissions:",
        color=discord.Color.from_rgb(255, 0, 0)
    )

    for guild in bot.guilds:
        permissions = guild.me.guild_permissions
        perms_list = [perm.replace("_", " ").title() for perm, value in permissions if value]
        perms_text = ", ".join(perms_list) if perms_list else "No Permissions"

        embed.add_field(
            name=guild.name,
            value=f"**Permissions:** {perms_text}",
            inline=False
        )

    await interaction.response.send_message(embed=embed, ephemeral=True)

# TOKEN desde Railway
token = os.getenv("TOKEN")

if not token:
    raise ValueError("No se encontró el TOKEN en las variables de entorno")

bot.run(token)
