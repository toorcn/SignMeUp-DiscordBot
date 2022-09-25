import googleAuth
import spreadsheetread
import spreadsheetwrite
import globalVar

def getLatestRow(sheet_id):
    sheet_list = spreadsheetread.run(sheet_id, f'A2:D300')
    return len(sheet_list) + 2

def showListSigned():
    if (globalVar.current_row_num_DEF == 2):
        return 'No one signed up yet.'
    sheet_list = spreadsheetread.run(globalVar.DEF_id, f'A2:D{globalVar.current_row_num_DEF}')
    counter = 0
    spacer_counter = 0
    # RVI = rank value
    output = 'IND.  DISCORD  GAME  RANK  RVI\n'
    for row in sheet_list:
        message = ''
        counter += 1
        for items in row:
            message += f'{items} '
        output += f'{counter}. {message}\n'
        if (counter == spacer_counter + 10):
            spacer_counter += 10
            output += '\n'
    return output

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

def joinList(discord_id, rank, discord_username):
    get_IGN = getIGN(discord_id)
    rank_data = str(rank).split('/')
    rank_division = str(rank_data[0].upper())[:4]
    rank_entry = 0
    rank_tier = 0
    try:
        rank_tier = str(rank_data[1]) 
    except:
        rank_tier
    if (rank_division == 'IRON'):
        rank_entry += 0
    if (rank_division == 'BRON'):
        rank_entry += 3
    if (rank_division == 'SILV'):
        rank_entry += 6
    if (rank_division == 'GOLD'):
        rank_entry += 9
    if (rank_division == 'PLAT'):
        rank_entry += 12
    if (rank_division == 'DIAM'):
        rank_entry += 15
    if (rank_division == 'ASCD'):
        rank_entry += 18
    if (rank_division == 'IMMO'):
        rank_entry += 21

    if (rank_tier == '1'):
        rank_entry += 1
    if (rank_tier == '2'):
        rank_entry += 2
    if (rank_tier == '3'):
        rank_entry += 3
    
    if (rank_division == 'RADI'):
        rank_entry = 25
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
        entry = ['UNJOINED', row_data[0][1], row_data[0][2], row_data[0][3]]
    except: 
        entry = ['UNJOINED', row_data[0][1], row_data[0][2]]
    spreadsheetwrite.setRow(globalVar.DEF_id, entry, row)
    return True

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