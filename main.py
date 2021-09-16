import discord
from discord.ext import commands
import music

print('Start')

#TODO: Add menu de interacao com o bot
#TODO: Add error handle

cogs = [music]

client = commands.Bot(command_prefix = "?")

for i in range(len(cogs)):
  cogs[i].setup(client)

client.run("ODg4MTA4MDI2MjAzMTExNDM1.YUN5DQ.wsWy4gZ4R-0CYla6Nr4WSqnvG9M")