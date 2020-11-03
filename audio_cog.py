from os import walk, listdir, getenv
import discord
import asyncio
from bot_logger import info
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
        print(query)


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
