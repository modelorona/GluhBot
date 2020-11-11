import ctypes
import ctypes.util
import discord

discord.opus.load_opus(ctypes.util.find_library('opus'))
discord.opus.is_loaded()