# purpose: this file runs a discord bot which will send me new comments so I can verify them

import discord
import os
import threading
import asyncio

MY_ID = 760189518934048778
STARTED = False
db = None

intents = discord.Intents.default()
intents.reactions = True
intents.members = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    global STARTED
    STARTED = True
    
    print(f"{client.user} is up!")
    
    user = await client.fetch_user(MY_ID)
    await user.send("I'm running! (list, delete, undelete)")

@client.event
async def on_message(message):
    if client.user == message.author:
        return

    if message.content.lower() == "ping":
        await message.channel.send("pong")

    msg = message.content.split(" ")
    command = msg[0].lower();

    if command == "delete":
        id = int(msg[1])
        db.db_cursor.execute("UPDATE comments SET public=0 WHERE comment_id=?", (id, ))
        db.db.commit()

        await message.channel.send(f"Set {id} visability off")
        
    if command == "undelete":
        id = int(msg[1])
        db.db_cursor.execute("UPDATE comments SET public=1 WHERE comment_id=?", (id, ))
        db.db.commit()

        await message.channel.send(f"Set {id} visability on")

    # send all emssages in blocks of 20 messages
    if command == "list":
        block = ""

        for c in db.get_all_comments():
            public = "✅" if c["public"] else "❌"

            comment = f"""\n`{c["comment_id"]}` {public}: [{c["user_name"]}] {c["content"]}"""

            # discord limits messages to 2000 charecters
            if len(comment + block) > 2000:
                await message.channel.send(block)
                await asyncio.sleep(1/40) # rate limit 50/sec
                block = ""

            # idek how this would happen but just in case
            if len(comment) > 2000:
                while len(comment) > 2000:
                    await message.channel.send(comment[:2000])
                    await asyncio.sleep(1/40) # rate limit 50/sec
                    comment = comment[2000:]

            block += comment

        await message.channel.send(block)

@client.event
async def on_reaction_add(reaction, user):
    if client.user == user: # if its reacting to its own messages
        return

    if reaction.emoji == u"❌":
        public = 0
    elif reaction.emoji == u"✅":
        public = 1
    else:
        return

    id = reaction.message.content.split("`")[1]

    db.db_cursor.execute("UPDATE comments SET public=? WHERE comment_id=?", (public, id))
    db.db.commit()

    me = await client.fetch_user(MY_ID)
    await me.send(f"Set comment `{id}`'s visibility to {public}")

def validate_comment(id):
    comment = db.get_comment(id)
    
    async def inner():
        async def inner_inner():
            me = await client.fetch_user(MY_ID)
        
            message = await me.send(f"""**--------Comment `{comment["comment_id"]}`--------**
> __{comment["user_name"]} on {comment["posted_on"]} under {comment["post_id"]}__
> """ + "\n> ".join(comment["content"].split("\n")))
        
            await message.add_reaction(u"❌")
            await message.add_reaction(u"✅")

        print(await asyncio.gather(inner_inner(), return_exceptions=True))


    asyncio.run_coroutine_threadsafe(inner(), client.loop)

def validate_all_comments():
    for comment in db.get_all_comments():
        validate_comment(comment["comment_id"])

def start_up(db_):
    global db
    db = db_
    
    # start client in background
    thread = threading.Thread(target=lambda : client.run(os.environ["DISCORD_KEY"]))
    thread.daemon = True
    thread.start()
    print("Starting moderation bot...")
