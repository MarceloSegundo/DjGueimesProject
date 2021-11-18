import discord
from discord.ext import commands
from music import Player
import keep_alive
import os

TOKEN = os.environ['TOKEN']

#TODO: Add menu de interacao com o bot
#TODO: Sair da call quando ocioso apos um tempo
#Apresentacao commit
#apresentacao 2

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix = "?", intents = intents)

@bot.event
async def on_ready():
    print(f"Pai ta On {bot.user.name}")

async def setup():
  await bot.wait_until_ready()
  bot.add_cog(Player(bot))

#Start webservice
keep_alive.keep_alive()

bot.loop.create_task(setup())
bot.run(TOKEN)