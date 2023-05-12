# purpose: this file runs a discord bot which will send me new comments so I can verify them

import discord
import os
import threading
import asyncio

MY_ID = 760189518934048778
STARTED = False

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    global STARTED
    STARTED = True
    
    print(f"{client.user} is up!")
    
    user = await client.fetch_user(MY_ID)
    await user.send("I'm running!")

def validate_comment(comment):    
    async def inner():
        async def inner_inner():
            user = await client.fetch_user(MY_ID)
        
            message = await user.send(f"""Comment `{comment["comment_id"]}`:
    > __{comment["user_name"]} on {comment["posted_on"]} under {comment["post_id"]}__
    > """ + "\n> ".join(comment["content"].split("\n")))
        
            await message.add_reaction(u"❌")
            await message.add_reaction(u"✅")

        print(await asyncio.gather(inner_inner(), return_exceptions=True))


    asyncio.run_coroutine_threadsafe(inner(), client.loop)



# start client in background
threading.Thread(target=lambda : client.run(os.environ["DISCORD_KEY"])).start()
print("Starting moderation bot...")
while not STARTED:
    pass