from os import walk, listdir, getenv
import discord
import asyncio
from bot_logger import error, info
from discord.ext import commands

class AudioPlayer(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    @commands.command()
    async def list(self, ctx):
        files = listdir(getenv('AUDIO_PATH'))
        info('sending list of files: {}'.format(len(files)))
        response = '\n'.join([file.split('.')[0] for file in files])
        await ctx.send(response)

    @commands.command()
    async def play(self, ctx, *, query):
        query = query + '.mp3'  # assume they type the name of the file correctly
        if query not in listdir(getenv('AUDIO_PATH')):
            await ctx.send('That audio does not exist you idiot')
            await commands.CommandError('File not found: {}'.format(query))
        else:
            query = getenv('AUDIO_PATH') + '/' + query
            source = discord.FFmpegPCMAudio(query)
            ctx.voice_client.play(source, after=lambda e: error('Player error: {}'.format(e) if e else None))



    @play.before_invoke
    async def ensure_connected(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send('Connect to a voice channel you dunce')
                await commands.CommandError('Author not connected to a voice channel')
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()
