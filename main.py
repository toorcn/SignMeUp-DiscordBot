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
version = '1.3.1'

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    try: 
        synced = await client.tree.sync()
        print("Bot is synced!")
        integrator.initialize()
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Sushi code!"))
        channel = client.get_channel(int(os.getenv('Start_channel_id')))        
        await channel.send(f'SignMeUp Alpha {version} (VALORANT) is ready!\nHow to join Valorant Game Night:\n> First time? /settag cat poop#0102\n> (once or when tag change)\n> To join: /join XXXX/X\n> (first 4 letters of your rank/tier)\n> - Example: /join SILV/2\n> To unjoin: /unjoin\n> To see list: /list\n> For more information: /help')   
    except Exception as e:
        print(e)

@client.tree.command(name = "help")
async def help(interaction: discord.Interaction):
    if (interaction.channel.name == os.getenv('Channel_name_1')):
        await interaction.response.send_message(f'\n> First time? /settag <GAME TAG>\n> To join: /join <XXXX/X>\n> - Example: /join DIAM/2\n> To unjoin: /unjoin\n> To view a list: /list', ephemeral=True)
        print("COMMAND help used")

@client.tree.command(name = "list")
async def list(interaction: discord.Interaction):
    if (interaction.channel.name == os.getenv('Channel_name_1')):
        await interaction.response.send_message(f'```{integrator.showListSigned()}```')
        print("COMMAND list used")

@client.tree.command(name = "refreshlist")
async def refreshlist(interaction: discord.Interaction):
    if (interaction.channel.name == os.getenv('Channel_name_1')):
        integrator.initialize()
        await interaction.response.send_message('> Fresh success!')
        print("COMMAND refresh used")

@client.tree.command(name = "join")
@app_commands.describe(current_rank = "be honest, for fair play")
async def join(interaction: discord.Interaction, current_rank: str):
    if (interaction.channel.name == os.getenv('Channel_name_1')):
        await interaction.response.defer(ephemeral=True)
        discord_id = str(interaction.user.id)
        discord_username = str(interaction.user._user)
        # message = ''
        if (await integrator.discordIdExist(discord_id)):
            #if joined
            if (not (await integrator.discordIdOnList(discord_username))):
                # message = f'> You have joined the list! as #{globalVar.current_row_num_DEF - 1}'
                await interaction.followup.send(f'> You have joined the list! as #{globalVar.current_row_num_DEF - 1}')
                await integrator.joinList(discord_id, current_rank, discord_username)
                await client.get_channel(int(os.getenv('Start_channel_id'))).send(f'> ({integrator.getIGN(discord_id)} JOIN) Player count -> #{integrator.getPlayerCount()}')
                # test if rank is valud
            else: 
                # message = '> You have already joined the list, to amend your entry first use /unjoin'
                await interaction.followup.send('> You have already joined the list, to amend your entry first use /unjoin')
        else:
            # message = '> You have not registered your in-game ID, please use /settag <GAME TAG>'
            await interaction.followup.send('> You have not registered your in-game ID, please use /settag <GAME TAG>')
        # await interaction.response.send_message(message, ephemeral=True)
        # check if user has set ign if not, refer
        print(f"COMMAND join used - {discord_username}")

@client.tree.command(name = "settag")
@app_commands.describe(in_game_tag = "FLOPPER#1234")
async def settag(interaction: discord.Interaction, in_game_tag: str):
    if (interaction.channel.name == os.getenv('Channel_name_1')):
        await interaction.response.defer(ephemeral=True)
        discord_id = str(interaction.user.id)
        saveResponse = integrator.saveIGN(discord_id, in_game_tag)
        msg = ''
        if (saveResponse):
            msg = 'You are set!'
        else:
            msg = 'Changed! if you have joined a list, please unjoin and join again.'
        await interaction.followup.send(f"> {msg}\n> ign: {in_game_tag} -LINK TO- id: {discord_id}")
        print(f"COMMAND settag used - {in_game_tag}")

@client.tree.command(name = "unjoin")
async def unjoin(interaction: discord.Interaction):
    if (interaction.channel.name == os.getenv('Channel_name_1')):
        await interaction.response.defer(ephemeral=True)
        discord_id = str(interaction.user.id)    
        discord_username = str(interaction.user._user)
        message = ''
        if (not (await integrator.unjoinFromList(discord_username))):
            # await interaction.response.send_message(f'> You have yet to join a list, use /join', ephemeral=True) 
            message = 'You have yet to join a list, use /join'
        else:
            # await interaction.response.send_message(f'> You have unjoined!', ephemeral=True) 
            message = 'You have unjoined!'
        # await interaction.response.send_message(f'> {message}', ephemeral=True) 
        await interaction.followup.send(f'> {message}');
        if (message == 'You have unjoined!'):
            await client.get_channel(int(os.getenv('Start_channel_id'))).send(f'> ({integrator.getIGN(discord_id)} UNJOINED) Player count -> #{integrator.getPlayerCount()}')
        print(f"COMMAND unjoin used - {discord_username}")

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