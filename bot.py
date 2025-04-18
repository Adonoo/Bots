import discord
from openai import OpenAI
from dotenv import load_dotenv
import os
import asyncio
from random import randint

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

FRIEND_ID_LIST = [344563884490752011, 335496196594466837, 373406852597284865, 1125518726805069834, 423962402476785664, 330969657840500738]

openai_client = OpenAI(
    api_key=OPENAI_API_KEY, 
    base_url="https://api.deepseek.com/v1"
)

client = discord.Client(self_bot=True)

@client.event
async def on_connect():
    print(f'Logged in as {client.user}')

@client.event
async def on_message(message):

    if message.author == client.user:
        return

    if isinstance(message.channel, discord.DMChannel):

        if message.author.id in FRIEND_ID_LIST:
            
            print(f"DM from {message.author.name}: {message.content}")

            response = openai_client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "Du schreibst mit einem guten Freund, beleidige ihn passend zu seiner Nachricht. Benutze keine Emojis und antworte in einem Satz"},
                    {"role": "user", "content": message.content}
                ],
                temperature=1
            )

            reply = response.choices[0].message.content

            if len(reply) > 100:
                answertime = 6 + randint(0, 3)
            elif len(reply) > 50:
                answertime = 4 + randint(0, 3)
            else:
                answertime = 2 + randint(0, 3)

            async with message.channel.typing():
                await asyncio.sleep(answertime)
                await message.channel.send(reply)
            print(response.choices[0].message.content)

client.run(DISCORD_TOKEN)