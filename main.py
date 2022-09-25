from code import interact
import discord
from discord import app_commands
from discord.ext import commands
import os
from dotenv import load_dotenv
import test
import globalVar

load_dotenv()

client = commands.Bot(command_prefix = "/", intents = discord.Intents.default())

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    try: 
        synced = await client.tree.sync()
        print("Bot is synced!")
        test.initialize()
    except Exception as e:
        print(e)

@client.tree.command(name = "list")
async def list(interaction: discord.Interaction):
    await interaction.response.send_message(test.showListSigned())

@client.tree.command(name = "joinlist")
@app_commands.describe(current_rank = "be honest, for fair play")
async def joinlist(interaction: discord.Interaction, current_rank: str):
    discord_id = str(interaction.user.id)
    discord_username = str(interaction.user._user)
    message = ''
    if (test.discordIdExist(discord_id)):
        #if joined
        if (not test.discordIdOnList(discord_username)):
            test.joinList(discord_id, current_rank, discord_username)
            # await interaction.response.send_message(f'You have joined the list! as #{globalVar.current_row_num_IGN + 3}')
            message = f'You have joined the list! as #{globalVar.current_row_num_DEF - 1}'
        else: 
            message = 'You have already joined the list, to amend your entry first use /unjoin'
    else:
        message = 'You have not registered your in-game ID, please use /setign'
    await interaction.response.send_message(message)
    # check if user has set ign if not, refer

@client.tree.command(name = "setign")
@app_commands.describe(in_game_tag = "FLOPPER#1234")
async def setign(interaction: discord.Interaction, in_game_tag: str):
    discord_id = str(interaction.user.id)
    saveResponse = test.saveIGN(discord_id, in_game_tag)
    msg = ''
    if (saveResponse):
        msg = 'You are set!'
    else:
        msg = 'Changed!'
    await interaction.response.send_message(f"{msg} ign: {in_game_tag} LINK TO id: {discord_id}")

# @client.tree.command(name = "unjoin")
# async def unjoin(interaction: discord.Interaction):
#     await interaction.response.send_message(test.showListSigned()) 
#unjoinlist

    #save to database

# @client.tree.command(name = "setrank")
# @app_commands.describe(rank = "Iron, Bronze, Silver, Gold, Platinum, Diamond, Ascendant, Immortal", tier = "1, 2, 3")
# async def say(interaction: discord.Interaction, rank: str, tier: int):
#     await interaction.response.send_message(f"user said: {rank} and {tier}")

discord_token = os.getenv('BOT_TOKEN')

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