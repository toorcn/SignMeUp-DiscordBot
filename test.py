import googleAuth
import spreadsheetread
import spreadsheetwrite
import globalVar

def getLatestRow(sheet_id):
    sheet_list = spreadsheetread.run(sheet_id, f'A2:D300')
    return len(sheet_list) + 2

def showListSigned():
    sheet_list = spreadsheetread.run(globalVar.DEF_id, f'A2:D{globalVar.current_row_num_DEF}')
    counter = 0
    output = ''
    for row in sheet_list:
        message = ''
        counter += 1
        for items in row:
            message += f'{items} '
        output += f'{counter}. {message}\n'
    print(output)
    return output

def getRow(discord_id):
    sheet_list = spreadsheetread.run(globalVar.IGN_id, f'A2:D{globalVar.current_row_num_IGN}')
    currentRow = 2
    for sl in sheet_list:
        if (str(discord_id) == sl[0]):
            return currentRow
        currentRow += 1
    return -1

def getIGN(discord_id):
    sheet_list = spreadsheetread.run(globalVar.IGN_id, f'A2:D{globalVar.current_row_num_IGN}')   
    for sl in sheet_list:
        if (str(discord_id) == sl[0]):
            return sl[1]

def saveIGN(discord_id, in_game_tag):
    if (getRow(discord_id) == -1):
        spreadsheetwrite.run(globalVar.IGN_id, [discord_id, in_game_tag])
        return True
    else:
        spreadsheetwrite.setRow(globalVar.IGN_id, [discord_id, in_game_tag], getRow(discord_id))
        return False

def joinList(discord_id, rank, discord_username):
    get_IGN = getIGN(discord_id)
    spreadsheetwrite.run(globalVar.DEF_id, [discord_username, get_IGN, rank, ''])

def discordIdExist(discord_id):
    temp = getRow(discord_id)
    if (temp == -1):
        print("NOT")
        return False
    else:
        print("TRUE")
        return True

def discordIdOnList(discord_username):
    sheet_list = spreadsheetread.run(globalVar.DEF_id, f'A2:D{globalVar.current_row_num_DEF - 1}') 
    for sl in sheet_list:
        try:
            if (str(discord_username) == sl[0]):
                return True
        except:
            continue
    return False

def initialize():
    googleAuth.authenticate()
    print('Loading sheet lines...')
    globalVar.current_row_num_DEF = getLatestRow(globalVar.DEF_id)
    print(f'Default sheet available line: {globalVar.current_row_num_DEF}')
    globalVar.current_row_num_IGN = getLatestRow(globalVar.IGN_id)
    print(f'IGN sheet available line: {globalVar.current_row_num_IGN}')
    print("Line load complete! Bot is ready!")


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