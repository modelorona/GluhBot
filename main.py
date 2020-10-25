from os import getenv
import settings
import set_up_logging
import download_audio
import bot

drive_downloader = download_audio.GoogleDriveFolderDownloader()
drive_downloader.download_audio()
# client = bot.GluhClient()
# client.run(getenv('DISC_KEY'))

