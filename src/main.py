import time
import requests
import disnake,json,os,random
from disnake.ext import commands

with open("token.json") as file:
    config = json.load(file)
    token = config["token"]
    
clientIntents = disnake.Intents.default()
clientIntents.voice_states = True
clientIntents.dm_messages = True

client = commands.Bot(command_prefix="?" , intents=clientIntents, help_command=None, reload=True)
client.start_time = time.time()

for folder in os.listdir('./cogs'):
    if folder.endswith('.py'):
        client.load_extension(f'cogs.{folder[:-3]}')
    elif os.path.isdir(f'./cogs/{folder}'):
        for file in os.listdir(f'./cogs/{folder}'):
            if file.endswith('.py'):
                client.load_extension(f'cogs.{folder}.{file[:-3]}')
                
client.run(token)