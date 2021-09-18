import discord
from discord.ext import commands
from music import Player
import keep_alive

#TODO: Add menu de interacao com o bot
#TODO: Add error handle

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
bot.run("ODg4MTA4MDI2MjAzMTExNDM1.YUN5DQ.wsWy4gZ4R-0CYla6Nr4WSqnvG9M")