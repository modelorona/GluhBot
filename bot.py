import discord

class GluhClient(discord.Client):
    async def on_read(self):
        print('logged on as {0}'.format(self.user))
    
    async def on_message(self, message):
        print('message from {0.author}: {0.content}'.format(message))

