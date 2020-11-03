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

