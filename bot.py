import os, discord
from dotenv import load_dotenv

load_dotenv()

client = discord.Client()

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

#@client.event


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

    if message.content.startswith('$rogSTX'):
        await message.channel.send('ROG STRIXX!')

    if message.content.startswith('$countI'):
        invite = await client.fetch_invite('f5v5FB9saE', with_counts=True)
        print('invites: ')
        print(invite)


client.run(os.getenv('TOKEN'))
