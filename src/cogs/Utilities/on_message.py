import datetime
import json
import disnake
from disnake.ext import commands


class OnMessageCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        # Make sure the bot doesn't respond to its own messages
        if message.author == self.bot.user:
            return

        try:
            with open("data/dollars.json", "r") as file:
                data = json.load(file)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            data = {}

        user_id = str(message.author.id)
        if user_id in data:
            data[user_id] += 0.25
        else:
            data[user_id] = 0.25

        with open("data/dollars.json", "w") as file:
            json.dump(data, file)

        # Ensure that the bot processes commands in messages
        await self.bot.process_commands(message)

def setup(bot):
    bot.add_cog(OnMessageCog(bot))
