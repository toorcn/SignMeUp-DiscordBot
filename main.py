from code import interact
from multiprocessing.connection import Client
import discord
from discord import app_commands
from discord.ext import commands
import os
from dotenv import load_dotenv
import integrator
import globalVar

load_dotenv()

client = commands.Bot(command_prefix = "/", intents = discord.Intents.default())

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    try: 
        synced = await client.tree.sync()
        print("Bot is synced!")
        integrator.initialize()
        channel = client.get_channel(int(os.getenv('Start_channel_id')))
        await channel.send('SignMeUp Alpha (VALORANT) is ready!\n> To join: /join <XXXX/X>\n> - Example: /join DIAM/2\n> To unjoin: /unjoin\n> For more help: /help')
    except Exception as e:
        print(e)

@client.tree.command(name = "help")
async def help(interaction: discord.Interaction):
    if (interaction.channel.name != os.getenv('Channel_name_1')):
        return 
    await interaction.response.send_message(f'\n> First time? /setign <GAME TAG>\n> To join: /join <XXXX/X>\n> - Example: /join DIAM/2\n> To unjoin: /unjoin\n> To view a list: /list\n> If a manual edit has been made: /refreshlist', ephemeral=True)

@client.tree.command(name = "list")
async def list(interaction: discord.Interaction):
    if (interaction.channel.name != os.getenv('Channel_name_1')):
        return 
    await interaction.response.send_message(f'```{integrator.showListSigned()}```')

@client.tree.command(name = "refreshlist")
async def refreshlist(interaction: discord.Interaction):
    if (interaction.channel.name != os.getenv('Channel_name_1')):
        return 
    integrator.initialize()
    await interaction.response.send_message('> Fresh success!')

@client.tree.command(name = "join")
@app_commands.describe(current_rank = "be honest, for fair play")
async def join(interaction: discord.Interaction, current_rank: str):
    if (interaction.channel.name != os.getenv('Channel_name_1')):
        return 
    discord_id = str(interaction.user.id)
    discord_username = str(interaction.user._user)
    message = ''
    if (integrator.discordIdExist(discord_id)):
        #if joined
        if (not integrator.discordIdOnList(discord_username)):
            await interaction.response.send_message(f'> You have joined the list! as #{globalVar.current_row_num_DEF - 1}', ephemeral=True)
            await client.get_channel(int(os.getenv('Start_channel_id'))).send(f'> Player count: #{globalVar.current_row_num_DEF - 1}')

            integrator.joinList(discord_id, current_rank, discord_username)
            # test if rank is valud
        else: 
            await interaction.response.send_message('> You have already joined the list, to amend your entry first use /unjoin', ephemeral=True)
    else:
        await interaction.response.send_message('> You have not registered your in-game ID, please use /setign <GAME TAG>', ephemeral=True)
    # await interaction.response.send_message(message)
    # check if user has set ign if not, refer

@client.tree.command(name = "setign")
@app_commands.describe(in_game_tag = "FLOPPER#1234")
async def setign(interaction: discord.Interaction, in_game_tag: str):
    if (interaction.channel.name != os.getenv('Channel_name_1')):
        return 
    discord_id = str(interaction.user.id)
    saveResponse = integrator.saveIGN(discord_id, in_game_tag)
    msg = ''
    if (saveResponse):
        msg = 'You are set!'
    else:
        msg = 'Changed! if you have joined a list, please unjoin and join again.'
    await interaction.response.send_message(f"> {msg}\n> ign: {in_game_tag} -LINK TO- id: {discord_id}", ephemeral=True)

@client.tree.command(name = "unjoin")
async def unjoin(interaction: discord.Interaction):
    if (interaction.channel.name != os.getenv('Channel_name_1')):
        return 
    discord_id = str(interaction.user.id)
    discord_username = str(interaction.user._user)
    message = ''
    if (not integrator.unjoinFromList(discord_username)):
        message = 'You have yet to join a list, use /join'
    else:
        message = 'You have unjoined!'
    await interaction.response.send_message(f'> {message}', ephemeral=True) 

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