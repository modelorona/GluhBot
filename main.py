# for non windows sytem, load the opus audio manually
from os import name
if name != 'nt':
    import load_opus

from dotenv import load_dotenv
load_dotenv()
from os import getenv
from discord.ext import commands
import bot_logger
import download_audio
import download_blog_tts
from audio_cog import AudioPlayer


# todo: fix this to set up audio folder before the downloaders
drive_downloader = download_audio.GoogleDriveFolderDownloader()
drive_downloader.download_audio()

blog_downloader = download_blog_tts.BlogDownloader()
blog_downloader.download_blog()

bot = commands.Bot(command_prefix=commands.when_mentioned_or('!g '))

@bot.event
async def on_ready():
    bot_logger.info('bot ready')
    
bot_logger.info('attaching AudioPlayer cog')
bot.add_cog(AudioPlayer(bot))

bot_logger.info('running bot')
bot.run(getenv('DISC_KEY'))


