import asyncio
import discord
import pafy
import youtube_dl
from discord.ext import commands


class Player(commands.Cog):
    def __init__(self, bot):
        print("Initializing...")
        self.bot = bot
        self.song_queue = {}

        self.setup()

    def setup(self):
        print(f"Guilds: {self.bot.guilds}")
        for guild in self.bot.guilds:
            self.song_queue[guild.id] = []
        print(f"Voice Clients: {self.bot.voice_clients}")

    async def check_queue(self, ctx):
        print("----------------check_queue---------------")
        print(f"songQueueInit: {self.song_queue[ctx.guild.id]}")
        
        if len(self.song_queue[ctx.guild.id]) > 0:
            self.vaiTocar = True
            print("Tem elemento na queue")
            ctx.voice_client.stop()
            print(f" songQueueFirst: {self.song_queue[ctx.guild.id][0]}")
            await self.play_song(ctx, self.song_queue[ctx.guild.id][0])
            self.song_queue[ctx.guild.id].pop(0)
            return None

        ctx.voice_client.stop()   

        print(f" songQueueFinal: {self.song_queue[ctx.guild.id]}")
        print("------------------------------------")

    async def search_song(self, amount, song, get_url=False):
        info = await self.bot.loop.run_in_executor(
            None, lambda: youtube_dl.YoutubeDL({
                "format": "bestaudio",
                "quiet": True
            }).extract_info(f"ytsearch{amount}:{song}",
                            download=False,
                            ie_key="YoutubeSearch"))
        if len(info["entries"]) == 0: return None

        return [entry["webpage_url"]
                for entry in info["entries"]] if get_url else info

    async def play_song(self, ctx, song):
        url = pafy.new(song).getbestaudio().url
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(url))
        ctx.voice_client.play(source,
                              after=lambda error: self.bot.loop.create_task(
                                  self.check_queue(ctx)))
        #Volume padrao
        ctx.voice_client.source.volume = 0.5
        await ctx.send(f"Lançando a braba: {song}")

    #faz o bot entrar no channel
    @commands.command()
    async def chama(self, ctx):

        #for debug
        print("----------------Chama---------------")
        print(f" Content_MSG: {ctx.message.content} \n Quem_escreveu: {ctx.author} \n QualCanal: {ctx.message.channel}")
        print("------------------------------------")

        if ctx.author.voice is None:
            return await ctx.send("Não tá no canal, otário")

        if ctx.voice_client is not None:
            await ctx.voice_client.disconnect()

        await ctx.author.voice.channel.connect()

    #faz o bot sair do channel
    @commands.command()
    async def vaza(self, ctx):

        #for debug
        print("----------------Vaza---------------")
        print(f" Content_MSG: {ctx.message.content} \n Quem_escreveu: {ctx.author} \n QualCanal: {ctx.message.channel}")
        print("------------------------------------")

        if ctx.voice_client is not None:
            return await ctx.voice_client.disconnect()

        await ctx.send("Vazei, trouxa!")

    #busca no yt a musica ou toca a url
    @commands.command()
    async def toca(self, ctx, *, song=None):

        #for debug
        print("----------------Toca---------------")
        print(f" Content_MSG: {ctx.message.content} \n Quem_escreveu: {ctx.author} \n QualCanal: {ctx.message.channel}")
        print(f" Song: {song}")
        

        if song is None:
            return await ctx.send("Lança a braba")

        if ctx.voice_client is None:
            return await ctx.send(
                "Tem que conectar no canal pra tocar, jumento")

        #handle song nao eh url
        if not ("youtube.com/watch?" in song or "https://youtu.be/" in song):
            await ctx.send("To procurando, pera ae, vai demorar")

            result = await self.search_song(1, song, get_url=True)
            print(f" resultSongNotLink: {result}")

            if result is None:
                return await ctx.send("Achei não, cabeça de pica")

            song = result[0]
            print(f" songWithResult: {song}")

        if ctx.voice_client.source is not None:
            print(f" voice_client.source: {ctx.voice_client.source}")
            print(f" voice_client.isPlaying: {ctx.voice_client.is_playing()}")

            queue_len = len(self.song_queue[ctx.guild.id])
            print(f" queueLen: {queue_len}")

            #Tamanho maximo da queue
            queue_len_max = 50

            if queue_len < queue_len_max:
                self.song_queue[ctx.guild.id].append(song)
                print("------------------------------------")
                return await ctx.send(
                    f"Já tem uma tocando, essa aqui vai na posição {queue_len+1} da fila"
                )
            else:
                print("------------------------------------")
                return await ctx.send(
                    f"Mano, mais que {queue_len_max} tá de sacanagem né")

        print("------------------------------------")
        await self.play_song(ctx, song)

    #busca no yt a musica ou toca a url
    @commands.command()
    async def tocar(self, ctx, *, song=None):

        #for debug
        print("----------------Tocar---------------")
        print(f" Content_MSG: {ctx.message.content} \n Quem_escreveu: {ctx.author} \n QualCanal: {ctx.message.channel}")

        if song is None:
            print("------------------------------------")
            return await ctx.send("Lança a braba")

        if ctx.voice_client is None:
            print("------------------------------------")
            return await ctx.send(
                "Tem que conectar no canal pra tocar, jumento")

        #handle song nao eh url
        if not ("youtube.com/watch?" in song or "https://youtu.be/" in song):
            await ctx.send("To procurando, pera ae, vai demorar")

            result = await self.search_song(1, song, get_url=True)
            print(f" resultSongNotLink: {result}")

            if result is None:
                print("------------------------------------")
                return await ctx.send("Achei não, cabeça de pica")

            song = result[0]
            print(f" songWithResult: {song}")

        if ctx.voice_client.source is not None:
            print(f" voice_client.source: {ctx.voice_client.source}")
            print(f" voice_client.isPlaying: {ctx.voice_client.is_playing}")
            
            queue_len = len(self.song_queue[ctx.guild.id])
            print(f" queueLen: {queue_len}")

            #Tamanho maximo da queue
            queue_len_max = 50

            if queue_len < queue_len_max:
                self.song_queue[ctx.guild.id].append(song)
                print("------------------------------------")
                return await ctx.send(
                    f"Já tem uma tocando, essa aqui vai na posição {queue_len+1} da fila"
                )
            else:
                print("------------------------------------")
                return await ctx.send(
                    f"Mano, mais que {queue_len_max} tá de sacanagem né")

        print("------------------------------------")
        await self.play_song(ctx, song)

    #faz uma busca e traz os cinco primeiros resultados pra copiar a url
    @commands.command()
    async def buscar(self, ctx, *, song=None):

        #for debug
        print("----------------buscar---------------")
        print(f" Content_MSG: {ctx.message.content} \n Quem_escreveu: {ctx.author} \n QualCanal: {ctx.message.channel}")
        print("------------------------------------")

        if song is None:
            return await ctx.send(
                "Tem que colocar a música pra pesquisar, burrão")

        await ctx.send("To procurando, pera ae, vai demorar")

        info = await self.search_song(5, song)

        embed = discord.Embed(
            title=f"Resultados de '{song}':",
            description="*Pode copiar a URL se não foi o primeiro resultado*\n",
            colour=discord.Colour.red())

        amount = 0
        for entry in info["entries"]:
            embed.description += f"[{entry['title']}]({entry['webpage_url']})\n"
            amount += 1

        embed.set_footer(text=f"Mostrando os primeiros {amount} resultados")
        await ctx.send(embed=embed)

    #mostra a queue atual
    @commands.command()
    async def fila(self, ctx):  #mostra a fila da guild

        #for debug
        print("----------------Fila---------------")
        print(f" Content_MSG: {ctx.message.content} \n Quem_escreveu: {ctx.author} \n QualCanal: {ctx.message.channel}")
        print("------------------------------------")

        if len(self.song_queue[ctx.guild.id]) == 0:
            return await ctx.send("NÃO TEM NADA AQUI!!!!! C A V A L O")

        #TODO: colocar o titulo do video na description
        embed = discord.Embed(title="Fila de Músicas",
                              description="",
                              colour=discord.Colour.dark_gold())

        i = 1
        for url in self.song_queue[ctx.guild.id]:
            embed.description += f"{i}) {url}\n"
            i += 1

        embed.set_footer(text="Se leu é gay")
        await ctx.send(embed=embed)

    @commands.command()
    async def lista(self, ctx):  #mostra a fila da guild

        #for debug
        print("----------------Lista---------------")
        print(f" Content_MSG: {ctx.message.content} \n Quem_escreveu: {ctx.author} \n QualCanal: {ctx.message.channel}")
        print("------------------------------------")

        if len(self.song_queue[ctx.guild.id]) == 0:
            return await ctx.send("NÃO TEM NADA AQUI!!!!! C A V A L O")

        #TODO: colocar o titulo do video na description
        embed = discord.Embed(title="Fila de Músicas",
                              description="",
                              colour=discord.Colour.dark_gold())

        i = 1
        for url in self.song_queue[ctx.guild.id]:
            embed.description += f"{i}) {url}\n"
            i += 1

        embed.set_footer(text="Se leu é gay")
        await ctx.send(embed=embed)

    #inicia a votacao pra skipar
    @commands.command()
    async def skip(self, ctx):

        #for debug
        print("----------------Skip---------------")
        print(f" Content_MSG: {ctx.message.content} \n Quem_escreveu: {ctx.author} \n QualCanal: {ctx.message.channel}")
        print("------------------------------------")

        if ctx.voice_client is None:
            return await ctx.send("Não to tocando nada, tu é surdo?")

        if ctx.author.voice is None:
            return await ctx.send("Tem que estar em um canal, burrão")

        if ctx.author.voice.channel.id != ctx.voice_client.channel.id:
            return await ctx.send("Não to tocando no teu canal, bolsominion")

        poll = discord.Embed(
            title=
            f"Vote pra skipar a musica que o {ctx.author.name}#{ctx.author.discriminator} colocou",
            description="**80% do canal tem que votar pra skipar**",
            colour=discord.Colour.blue())
        poll.add_field(name="Skipar", value=":white_check_mark:")
        poll.add_field(name="Continuar", value=":no_entry_sign:")
        poll.set_footer(text="A votação terminar em 15 segundos")

        #So manda uma msg temporaria, precisa armazenar a msg pra obter as reacoes
        poll_msg = await ctx.send(embed=poll)
        poll_id = poll_msg.id

        await poll_msg.add_reaction(u"\u2705")  #Sim
        await poll_msg.add_reaction(u"\U0001F6AB")  #Nao

        #await asyncio.sleep(4)
        await asyncio.sleep(8)  # 8 Segundos pra votar

        poll_msg = await ctx.channel.fetch_message(poll_id)

        votes = {u"\u2705": 0, u"\U0001F6AB": 0}
        reacted = []

        for reaction in poll_msg.reactions:
            if reaction.emoji in [u"\u2705", u"\U0001F6AB"]:
                async for user in reaction.users():
                    if user.voice.channel.id == ctx.voice_client.channel.id and user.id not in reacted and not user.bot:
                        votes[reaction.emoji] += 1
                        reacted.append(user.id)

        skip = False

        if votes[u"\u2705"] > 0:
            if votes[u"\U0001F6AB"] == 0 or votes[u"\u2705"] / (
                    votes[u"\u2705"] + votes[u"\U0001F6AB"]
            ) > 0.60:  # votacao passa se maior que 50
                skip = True
                embed = discord.Embed(
                    title="Skipada",
                    description=
                    "***A votação passou, a música vai de base agora***",
                    colour=discord.Colour.green())

        if not skip:
            embed = discord.Embed(
                title="Não skipou :c",
                description=
                "***A votação falhou, vai continuar a tocar essa merda***",
                colour=discord.Colour.red())

        embed.set_footer(text="A votação terminou")

        await poll_msg.clear_reactions()
        await poll_msg.edit(embed=embed)

        if skip:
            ctx.voice_client.stop()
            await self.check_queue(ctx)

    #pausa o que ta tocando
    @commands.command()
    async def pause(self, ctx):

        #for debug
        print("----------------Pause---------------")
        print(f" Content_MSG: {ctx.message.content} \n Quem_escreveu: {ctx.author} \n QualCanal: {ctx.message.channel}")
        print("------------------------------------")

        if ctx.voice_client.is_playing():
            ctx.voice_client.pause()
        else:
            await ctx.send("Nem ta tocando nada, doidão")

    #retoma o que ta pausado
    @commands.command()
    async def play(self, ctx):

        #for debug
        print("----------------Play---------------")
        print(f" Content_MSG: {ctx.message.content} \n Quem_escreveu: {ctx.author} \n QualCanal: {ctx.message.channel}")
        print("------------------------------------")

        if ctx.voice_client.is_paused():
            ctx.voice_client.resume()
        else:
            await ctx.send("Nem tem nada pausado, tá na noia?")

    #forca o skip sem nenhuma votacao
    #TODO: add um filtro pra quem pode skipar
    @commands.command()
    async def fs(self, ctx):

        #for debug
        print("----------------Fs---------------")
        print(f" Content_MSG: {ctx.message.content} \n Quem_escreveu: {ctx.author} \n QualCanal: {ctx.message.channel}")
        print("------------------------------------")

        if ctx.voice_client is None:
            return await ctx.send("Não to tocando nada, tu é surdo?")

        if ctx.author.voice is None:
            return await ctx.send("Tem que estar em um canal, burrão")

        if ctx.author.voice.channel.id != ctx.voice_client.channel.id:
            return await ctx.send("Não to tocando no teu canal, bolsominion")

        ctx.voice_client.stop()
        await self.check_queue(ctx)

    @commands.command()
    async def comandos(self, ctx):

        #for debug
        print("----------------Comandos---------------")
        print(f" Content_MSG: {ctx.message.content} \n Quem_escreveu: {ctx.author} \n QualCanal: {ctx.message.channel}")
        print("------------------------------------")

        embed = discord.Embed(
            title="Lista de Comandos",
            description=
            "?chama - Chama o Bot pro canal\n ?vaza - Faz o bot vazar da call :c\n ?toca ou ?tocar - Toca a musica, é obvio\n ?lista ou ?fila - Exibe a playlist atual\n ?buscar - Ele procura as musicas e da só o link pra tu copiar\n ?skip - Abre uma votacao pra skipar a musica\n ?play e ?pause - Eles fazem isso ai mesmo",
            colour=discord.Colour.dark_gold())
        embed.set_footer(text="Se leu é gay")
        await ctx.send(embed=embed)
