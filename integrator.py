import googleAuth
import spreadsheetread
import spreadsheetwrite
import globalVar
import re
import discord

def getLatestRow(sheet_id):
    sheet_list = spreadsheetread.run(sheet_id, f'A2:D300')
    return len(sheet_list) + 2

def showListSigned(interaction):
    if (globalVar.current_row_num_DEF == 2):
        return '`No one signed up yet.`'
    sheet_list = spreadsheetread.run(globalVar.DEF_id, f'A2:D{globalVar.current_row_num_DEF}')
    index_embed_string, game_embed_string, rank_embed_string = '', '', ''
    valid_counter = 0
    for entry in sheet_list:
        if (entry == []):
            continue
        spacer_nextln = ''
        index = valid_counter + 1
        if (valid_counter % 5 == 0):
            spacer_nextln = '\n'
        game_tag = entry[1]
        try:
            RVI = int(entry[3])
        except:
            RVI = 0
        game_rank = ''
        if (RVI >= 1 and RVI <= 3):
            game_rank = 'Iron'
        if (RVI >= 4 and RVI <= 6):
            game_rank = 'Bronze'
        if (RVI >= 7 and RVI <= 9):
            game_rank = 'Silver'
        if (RVI >= 10 and RVI <= 12):
            game_rank = 'Gold'
        if (RVI >= 13 and RVI <= 15):
            game_rank = 'Platinum'
        if (RVI >= 16 and RVI <= 18):
            game_rank = 'Diamond'
        if (RVI >= 19 and RVI <= 21):
            game_rank = 'Ascendant'
        if (RVI >= 22 and RVI <= 24):
            game_rank = 'Immortal'
        if ((RVI+2) % 3 == 0):
            game_rank += ' I'
        if ((RVI+1) % 3 == 0):
            game_rank += ' II'
        if (RVI % 3 == 0):
            game_rank += ' III'
        if (RVI == 25):
            game_rank = 'Lord Radiant'    
        if (RVI == 0):
            game_rank = 'Unranked'
        # game_rank = entry[2]

        index_embed_string += f'{spacer_nextln}{index})\n'
        game_embed_string += f'{spacer_nextln}{game_tag}\n'
        rank_embed_string += f'{spacer_nextln}{game_rank}\n'
        # rank_embed_string += f'{spacer_nextln}{game_rank}\n'
        valid_counter += 1

    embed = discord.Embed(title="__*Valorant Game Night List  (Wednesday, 9PM)*__", color=0xff4655, timestamp=interaction.created_at)
    embed.add_field(name='**Num**', value=index_embed_string, inline=True)
    embed.add_field(name='**Game Tag**', value=game_embed_string, inline=True)
    embed.add_field(name='**Rank**', value=rank_embed_string, inline=True)
    return embed
    # discord_embed_string = ''
    # discord_tag = entry[0]
    # discord_embed_string += f'{discord_tag}\n'
    # embed.add_field(name=f'**Discord Tag**', value=discord_embed_string, inline=True)

def getRow(sheet_id, discord_id):
    end_var = 0
    if sheet_id == globalVar.DEF_id:
        end_var = globalVar.current_row_num_DEF
    elif sheet_id == globalVar.IGN_id:
        end_var = globalVar.current_row_num_IGN
    sheet_list = spreadsheetread.run(sheet_id, f'A2:D{end_var}')
    currentRow = 2
    for sl in sheet_list:
        try:
            if (str(discord_id) == sl[0]):
                return currentRow
        except:
            currentRow += 1
            continue
        currentRow += 1
    return -1

def getIGN(discord_id):
    sheet_list = spreadsheetread.run(globalVar.IGN_id, f'A2:D{globalVar.current_row_num_IGN}')   
    for sl in sheet_list:
        if (str(discord_id) == sl[0]):
            return sl[1]

def saveIGN(discord_id, in_game_tag):
    if (getRow(globalVar.IGN_id, discord_id) == -1):
        spreadsheetwrite.run(globalVar.IGN_id, [discord_id, in_game_tag])
        return True
    else:
        spreadsheetwrite.setRow(globalVar.IGN_id, [discord_id, in_game_tag], getRow(globalVar.IGN_id, discord_id))
        return False

async def joinList(discord_id, rank, discord_username):
    get_IGN = getIGN(discord_id)
    # rank_data = str(rank).split('/')
    rank_data = re.split('/| ', str(rank))
    rank_division = str(rank_data[0].upper())[:2]
    rank_entry = -1
    rank_tier = 0
    skip_add = False
    try:
        rank_tier = str(rank_data[1])[:1]
    except:
        rank_tier
    if (rank_division == 'IR'):
        rank_entry += 1
    if (rank_division == 'BR'):
        rank_entry += 4
    if (rank_division == 'SI'):
        rank_entry += 7
    if (rank_division == 'GO'):
        rank_entry += 10
    if (rank_division == 'PL'):
        rank_entry += 13
    if (rank_division == 'DI'):
        rank_entry += 16
    if (rank_division == 'AS'):
        rank_entry += 19
    if (rank_division == 'IM'):
        rank_entry += 22
    if (rank_division == 'RA'):
        rank_entry = 26
        skip_add = True
    if (rank_entry < 0):
        rank_entry += 1
        skip_add = True

    if (rank_tier == '1' and skip_add == False):
        rank_entry += 1
    if (rank_tier == '2' and skip_add == False):
        rank_entry += 2
    if (rank_tier == '3' and skip_add == False):
        rank_entry += 3

    spreadsheetwrite.run(globalVar.DEF_id, [discord_username, get_IGN, rank, rank_entry])

async def discordIdExist(discord_id):
    temp = getRow(globalVar.IGN_id, discord_id)
    if (temp == -1):
        return False
    else:
        return True

async def discordIdOnList(discord_username):
    sheet_list = spreadsheetread.run(globalVar.DEF_id, f'A2:D{globalVar.current_row_num_DEF - 1}') 
    for sl in sheet_list:
        try:
            if (str(discord_username) == sl[0]):
                return True
        except:
            continue
    return False

async def unjoinFromList(discord_username):
    row = getRow(globalVar.DEF_id, discord_username)
    if (row == -1):
        return False
    row_data = spreadsheetread.run(globalVar.DEF_id, f'A{row}:D{row}') 
    # print(f'get list row {getRow(globalVar.DEF_id, discord_username)}')
    entry = []
    try:
        # entry = ['UNJOINED', row_data[0][1], row_data[0][2], row_data[0][3]]
        entry = ['', '', '', '']
    except: 
        # entry = ['UNJOINED', row_data[0][1], row_data[0][2]]
        entry = ['', '', '']
    spreadsheetwrite.setRow(globalVar.DEF_id, entry, row)
    return True

def getPlayerCount():
    sheet_list = spreadsheetread.run(globalVar.DEF_id, f'A2:D{globalVar.current_row_num_DEF + 1}')
    counter = 0
    for sl in sheet_list:
        try:
            if (not ('UNJOINED' == str(sl[0]) or '' == str(sl[0]))):
                counter += 1
        except:
            print('continue')
            continue
    return counter

def initialize():
    googleAuth.authenticate()
    print('Loading sheet lines...')
    globalVar.current_row_num_DEF = getLatestRow(globalVar.DEF_id)
    print(f'Default sheet available line: {globalVar.current_row_num_DEF}')
    globalVar.current_row_num_IGN = getLatestRow(globalVar.IGN_id)
    print(f'IGN sheet available line: {globalVar.current_row_num_IGN}')
    print("Line load complete! \nBot is ready!")


# testing
# if __name__ == '__main__':
#     initialize()
#     # print(f'creds TEST: {globalVar.creds}') entry
#     spreadsheetwrite.run(globalVar.DEF_id, ['hyyy#morb', 'tg#192', 'im', ''])
#     # getLatestRow()
#     print('list')
#     spreadsheetwrite.run(globalVar.IGN_id, ["364782648", "hg#4"])
#     # print(type(globalVar.row_data))
#     # showListSigned()
#     print(f"not filled row at {globalVar.current_row_num_DEF}")
#     print(f"not filled row at {globalVar.current_row_num_IGN}")
#     print("cycle complete")