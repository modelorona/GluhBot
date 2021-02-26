from os import listdir, getenv
from discord import FFmpegPCMAudio
from bot_logger import error, info
from discord.ext import commands
import asyncio

class AudioPlayer(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot


    @commands.command()
    async def list(self, ctx):
        files = listdir(getenv('AUDIO_PATH'))
        info('sending list of files: {}'.format(len(files)))
        response = '\n'.join(sorted([file.split('.')[0] for file in files]))
        await ctx.send(response)


    @commands.command()
    async def options(self, ctx):
        response = '\n'.join([
            '*!g list* -> get all song names',
            '*!g play _<song name>_* -> play a specific song',
            # '*!g loop _<song name>_* -> will attempt to loop the given sound forever, use with caution',
            # '*!g loop _<song name>_ _<X>_* -> will attempt to loop the given sound _X_ amount of times',
            '*!g stop* -> stop playing the current song',
            '*!g options* -> print available bot options'
        ])
        await ctx.send(response)


    @commands.command()
    async def play(self, ctx, *, query: str):
        query = query + '.mp3'  # assume they type the name of the file correctly
        if query not in listdir(getenv('AUDIO_PATH')):
            await ctx.send('That audio does not exist you idiot')
            await commands.CommandError('File not found: {}'.format(query))
        else:
            query = getenv('AUDIO_PATH') + '/' + query
            source = FFmpegPCMAudio(query)
            ctx.voice_client.play(source, after=lambda e: error('Player error: {}'.format(e) if e else None))


    # @commands.command()
    # async def loop(self, ctx, name: str, times: int=None):
    #     # todo: this below can def be made into a function or decorator check, as it's used in multiple places
    #     name = name + '.mp3'
    #     if name not in listdir(getenv('AUDIO_PATH')):
    #         await ctx.send('That audio does not exist you idiot')
    #         await commands.CommandError('File not found: {}'.format(name))
    #     else:
    #         name = getenv('AUDIO_PATH') + '/' + name
    #         source = FFmpegPCMAudio(name)

    #         # bad implementation, but should work for now
    #         def repeat(ctx, audio):
    #             ctx.voice_client.play(audio, after=lambda e: repeat(ctx, audio))

    #         if times is None:
    #             # loop time, simple while until death lol
    #             while(True):
    #                 ctx.voice_client.play(source, after=lambda e: repeat(ctx, source))
    #         # else:
    #             # for x in range(times):


    @commands.command()
    async def stop(self, ctx):
        if ctx.voice_client is not None:
            if ctx.voice_client.is_playing():
                ctx.voice_client.stop()


    @play.before_invoke
    @stop.before_invoke
    async def ensure_connected(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send('Connect to a voice channel you dunce')
                await commands.CommandError('Author not connected to a voice channel')
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()

