from code import interact
import discord
from discord import app_commands
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

client = commands.Bot(command_prefix = "/", intents = discord.Intents.default())

@client.event
async def on_ready():
    print("Bot is armed")
    try: 
        synced = await client.tree.sync()
        print("synced")
    except Exception as e:
        print(e)

@client.tree.command(name = "hello")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"hey")

@client.tree.command(name = "say")
@app_commands.describe(things_to_say = "this")
async def say(interaction: discord.Interaction, things_to_say: str):
    await interaction.response.send_message(f"user said: {things_to_say}")

discord_token = os.getenv('TOKEN')

client.run(discord_token)

# client = discord.Client(intents=discord.Intents.default())

# @client.event
# async def on_ready():
#     print('We have logged in as {0.user}'.format(client))

# @client.event
# async def on_message(message):
#     if message.author == client.user:
    #     return

    # if message.content.startswith('$hello'):
        # await message.channel.send('Hello!')

# @tree.command(name = "List Signer", description = "add your name to the list!", )
# @app_commands.command()
# async def ls(interaction: discord.Interaction, ls: str):
#     await interaction.response.send_message(f'test')

# @ls.autocomplete('ls')
# async def ls_autocomplete(
#     interaction: discord.Interaction,
#     current: str,
# ) -> List[app_commands.Choice[str]]:
#     rank = ['Gold', 'Plat', 'Dia', 'Watermelon', 'Melon', 'Cherry']
#     return [
#         app_commands.Choice(name=l, value=l)
#         for l in ls if current.lower() in l.lower()
#     ]