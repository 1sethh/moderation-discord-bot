import discord, json, os, asyncio, time
from discord.ext import commands

start = time.time()

with open("config.json", "r") as config:
    c = json.load(config)

client = commands.Bot(command_prefix = "/", intents = discord.Intents.all(), help_command = None, case_insensitive = True, activity = discord.Activity(type = discord.ActivityType.listening, name = "/help"), allowed_mentions = discord.AllowedMentions(roles=True, users=True, everyone=False)) # command_prefix is not gonna be used, but is required sadly

@client.event
async def on_ready():
    print("Successfully loaded", __name__.replace("__", ""), f"in {round(time.time() - start)} seconds.")
    try:
        sync = await client.tree.sync()
        print(f"Synced {client.user.name} to {len(sync)} commands.")
    except Exception as SyncError:
        print(SyncError)
    
async def cogs():
    for folder in os.listdir("./cogs"):
        for file in os.listdir(f"./cogs/{folder}"):
            if file.endswith(".py"):
                await client.load_extension(f"cogs.{folder}.{file[:-3]}")

async def main():
    await cogs(), await client.start(c["token"])

asyncio.run(main())