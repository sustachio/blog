# purpose: this file runs a discord bot which will send me new comments so I can verify them

import discord
import os

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"{client.user} is up!")
    
    user = await client.fetch_user("760189518934048778")
    await user.send("Hello there!")

client.run(os.environ["DISCORD_KEY"])