# bot.py
from email.policy import default
import os

import nextcord
from nextcord.ext import commands
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='')

@bot.event
async def on_ready():
    await bot.change_presence(activity=nextcord.Activity(type=nextcord.ActivityType.watching, name=':D'))

guilds=[641076884838547480, 844732033442906142]
bot.streak = 0
bot.record = 0

@bot.slash_command(name="update_record", description="Updates the smile record", guild_ids=guilds, default_permission=False)
async def update_record(interaction: nextcord.Interaction, record: int):
    bot.record = record
    await interaction.send(f"The record was updated to {record}")\

@bot.slash_command(name="update_streak", description="Updates the streak", guild_ids=guilds, default_permission=False)
async def update_streak(interaction: nextcord.Interaction, streak: int):
    bot.streak = streak
    await interaction.send(f"The streak was updated to {streak}")

@bot.slash_command(name="smile", description="Check the :D stats", guild_ids=guilds)
async def smile(interaction: nextcord.Interaction):
    embed = nextcord.Embed(title="Smile Stats", description=f"Current streak: {bot.streak}\nCurrent record: {bot.record}", color=nextcord.Color.blue())
    await interaction.send(embed=embed)

@bot.event
async def on_message(message):
    smileemoji = 0
    for emoji in message.guild.emojis:
                if emoji.name == 'colonD':
                    smileemoji = emoji
    if message.author == bot.user:
        return
    if message.channel.name == 'smile':
        if message.content == ':D':
            if smileemoji != 0:
                await message.add_reaction(smileemoji)
            bot.streak += 1
        else:
            if bot.streak != 0:
                await message.channel.send(f"Oh no! <@{message.author.id}> broke a streak of {bot.streak} D:\nStreak reset!")
                if bot.streak > bot.record:
                    bot.record = bot.streak
                    await message.channel.send(f"That streak was a new record of {bot.record}!")
            bot.streak = 0
    else:
        if message.content == ':D':
            if smileemoji != 0:
                await message.add_reaction(smileemoji)

bot.run(TOKEN)
