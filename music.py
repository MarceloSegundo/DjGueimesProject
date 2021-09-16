import discord
from discord.ext import commands
import youtube_dl

class music(commands.Cog):
  def __init__(self, client):
    self.client = client

  #Entrar no canal de voz somente se _author estiver em um canal. Comando: ?chama
  @commands.command()
  async def chama(self, ctx):
      if ctx.author.voice is None:
        await ctx.send("Você não está em um canal de voz, otário")
      voice_channel = ctx.author.voice.channel
      if ctx.voice_client is None:
        await voice_channel.connect()
        print('Entrou no canal')
      else:
        await ctx.voice_channel.move_to(voice_channel)

  #Sair do canal de voz. Comando: ?vaza
  @commands.command()
  async def vaza(self, ctx):
      await ctx.voice_client.disconnect()
      print('vazouuu')

  #Busca a musica da url passada. (Somente url). Comando: ?toca URL
  #TODO: fazer a busca no yt quando nao for url
  @commands.command()
  async def toca(self, ctx, url):
    ctx.voice_client.stop()
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
    YDL_OPTIONS = {'format': "bestaudio"}
    vc = ctx.voice_client

    #TODO: add msg de erro quando nao encontrar
    with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
        print('Baixando....')
        info = ydl.extract_info(url, download = False)
        print('info: ' + info)
        url2 = info['formats'][0]['url']
        print('url2: ' + url2)
        source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
        vc.play(source)    
        print('Tocando...')

  #Pausa a musica atual. Comando: ?pause
  #TODO: add nome de comando criativo
  @commands.command()
  async def pause(self, ctx):
      await ctx.voice_client.pause()
      await ctx.send("Pausadão")

  #Resume a musica atual. Comando: ?resume
  #TODO: add nome do comando criativo
  @commands.command()
  async def resume(self, ctx):
      await ctx.voice_client.resume()
      await ctx.send("Deu play foi?")

#TODO: Add queue e comandos da queue
#TODO: Add interacao com spotfy
#TODO: Testar se funciona com podcasts longos

def setup(client):
  client.add_cog(music(client))