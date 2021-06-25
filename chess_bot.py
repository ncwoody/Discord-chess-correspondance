import discord
import chess
from random import *

client = discord.Client()
board = chess.Board()

@client.event
async def on_ready():
    try:
        print('Logged in as {0.user}'.format(client))
    except:
        print("Could not login")

@client.event
async def on_message(message):
    if message.author == client.user:  # so we don't respond to our own messages- we shouldn't but just in case
        return
    elif message.content.startswith('!help'):  # if someone wants to list our functions
        await message.channel.send('!board to print the current board')
        await message.channel.send('!move to send a move, must be in uci format and typed like: !move a2a3, for example')
        await message.channel.send('To elaborate, this is broken down into two spaces, the first being the space where the piece came from, and the second being the space the piece is moving to')
        await message.channel.send('In the example I gave above, this would move a piece (such as a pawn) from space a2 to space a3')
        await message.channel.send('!end to check for the end of the game, and to reset the board if game is over')
        await message.channel.sent('!ai to let the bot make a move itself (currently will choose a move randomly)')
    elif message.content.startswith('!board'):  # if someone wants to print the board
        test_str = str(board) # gets the board in a string for printing
        n = 16  # I really wish we could use the board.unicode() function, but discord likes to print the black pawn pieces as an emoji, which screws that idea up
        x = [test_str[i:i+n] for i in range(0, len(test_str), n)]   # breaking each line of the board into different printing lines
        z = '```'  # begins a code block
        z += '    A B C D E F G H\n'
        z += '    _ _ _ _ _ _ _ _\n'
        v = 0
        for y in x:  # looping through each line
            if v == 0:
                z += '8 | '
            elif v == 1:
                z += '7 | '
            elif v == 2:
                z += '6 | '
            elif v == 3:
                z += '5 | '
            elif v == 4:
                z += '4 | '
            elif v == 5:
                z += '3 | '
            elif v == 6:
                z += '2 | '
            elif v == 7:
                z += '1 | '
            z += y  # adds the line to the code block
            v = v+1
        z += '\n    _ _ _ _ _ _ _ _'
        z += '\n    A B C D E F G H'
        z += '```'  # ends a code block
        await message.channel.send(z)
    elif message.content.startswith('!move'):  # if someone wants to make a move
        movestr = message.content
        movestr = movestr.replace("!move", "")
        movestr = movestr.strip()
        move = chess.Move.from_uci(movestr)
        board.push(move)
        
        # we print the move for convienence
        test_str = str(board)
        n = 16
        x = [test_str[i:i+n] for i in range(0, len(test_str), n)]
        z = '```'  # begins a code block
        z += '    A B C D E F G H\n'
        z += '    _ _ _ _ _ _ _ _\n'
        v = 0
        for y in x:  # looping through each line
            if v == 0:
                z += '8 | '
            elif v == 1:
                z += '7 | '
            elif v == 2:
                z += '6 | '
            elif v == 3:
                z += '5 | '
            elif v == 4:
                z += '4 | '
            elif v == 5:
                z += '3 | '
            elif v == 6:
                z += '2 | '
            elif v == 7:
                z += '1 | '
            z += y  # adds the line to the code block
            v = v+1
        z += '\n    _ _ _ _ _ _ _ _'
        z += '\n    A B C D E F G H'
        z += '```'  # ends a code block
        await message.channel.send(z)

        # checking the various states of the game
        x = board.is_check()
        if x == True:
            await message.channel.send('Check!')
        x = board.is_checkmate()
        if x == True:
            await message.channel.send('Checkmate!')
        x = board.is_stalemate()
        if x == True:
            await message.channel.send('Stalemate!')
    elif message.content.startswith('!end'):  # if someone wants to check if the game is over
        x = board.is_checkmate()
        if x == True:
            await message.channel.send("Game Over due to checkmate!!")
            board.reset_board()
        y = board.is_stalemate()
        if y == True:
            await message.channel.send("Game Over due to stalemate...")
            await message.channel.send("Nobody wins...")
            board.reset_board()
        if x == False and y == False:
            await message.channel.send("Game is not over, keep playing!")
    elif message.content.startswith('!ai'):  # if someone wants a move to be chosen randomly
        check = False  # looping variable
        while check == False:  # while a legal move is not chosen
            # getting the first space
            x = randint(0, 7)  # we get a letter with the following lines
            y = ""
            if x == 0:
                y = "a"
            elif x == 1:
                y = "b"
            elif x == 2:
                y = "c"
            elif x == 3:
                y = "d"
            elif x == 4:
                y = "e"
            elif x == 5:
                y = "f"
            elif x == 6:
                y = "g"
            elif x == 7:
                y = "h"
            x = randint(1,8)  # getting a number
            # getting the second space - do that agin
            a = randint(0, 7)  # we get a letter with the following lines
            b = ""
            if a == 0:
                b = "a"
            elif a == 1:
                b = "b"
            elif a == 2:
                b = "c"
            elif a == 3:
                b = "d"
            elif a == 4:
                b = "e"
            elif a == 5:
                b = "f"
            elif a == 6:
                b = "g"
            elif a == 7:
                b = "h"
            a = randint(1,8)  # getting a number
            z = y + str(x) + b + str(a)  # converting the randoms into a string
            move = chess.Move.from_uci(z)  # converting it into the correct format
            check = move in board.legal_moves  # we check to see if it is a legal move
            if check == True:  # if this is a legal move
                board.push(move)
                # we print the move for convienence
                await message.channel.send("The move is " + z)
                test_str = str(board)
                n = 16
                x = [test_str[i:i+n] for i in range(0, len(test_str), n)]
                z = '```'  # begins a code block
                z += '    A B C D E F G H\n'
                z += '    _ _ _ _ _ _ _ _\n'
                v = 0
                for y in x:  # looping through each line
                    if v == 0:
                        z += '8 | '
                    elif v == 1:
                        z += '7 | '
                    elif v == 2:
                        z += '6 | '
                    elif v == 3:
                        z += '5 | '
                    elif v == 4:
                        z += '4 | '
                    elif v == 5:
                        z += '3 | '
                    elif v == 6:
                        z += '2 | '
                    elif v == 7:
                        z += '1 | '
                    z += y  # adds the line to the code block
                    v = v+1
                z += '\n    _ _ _ _ _ _ _ _'
                z += '\n    A B C D E F G H'
                z += '```'  # ends a code block
                await message.channel.send(z)

token = <insert your token here>                
client.run(token)
