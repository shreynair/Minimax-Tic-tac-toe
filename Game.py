from pickle import FALSE
from Board import Board
from Board import copy
from functools import reduce
from sys import exit

def play():
    print("Enter a board size: ")
    n = int(input())
    board = Board(n)
    print("Press 1 for X or -1 for O")
    human = int(input())
    ai = (-1) * human
    
    print("Enter moves while space seperated ex: 1,1")
    print("Player 1 uses X")
    print("Player -1 uses O")
    victory = False
    turn = 0

    functions = {}
    functions[human] = makePlayerMove
    functions[ai] = makeAImove

    while(not victory):
        print(f"Turn: {turn}")
        print(board)
        victory = functions[1](1, board)
        print(board)
        if(victory):
            break
        victory = functions[-1](-1, board)
        print(board)
        turn += 1

    match(board.get_Winner()):
        case 1:
            print("Player X Wins!")
        case -1:
            print("Player O Wins!")
        case _:
            print("Nobody wins!")

    exit()


def makePlayerMove(player, board):
    valid = False
    row = 0
    col = 0
    print(f"Player {player} move: ")

    while(not valid):
        try:
            line = input()
            linearr = str.split(line, ",")

            row = int(linearr[0])
            col = int(linearr[1])
            if(board.is_Empty(row, col)):
                board.set_Value(row, col, player)
                valid = True
            else:
                print("Invalid move! Enter moves comma seperated, ex: 0,0")
        except:
            print("Invalid Move!")
            print("Enter moves coma seperated, ex: 0,0")
    return board.check_Win()

def makeAImove(player, board):
    import numpy as np

    print(f"Player {player} move: ")
    possible_moves = board.moves()
    move_rewards = [None for _ in range(len(possible_moves))]

    for i, move in enumerate(possible_moves):
        move_rewards[i] = minimax((-1) * player, copy(board).set_Value(move[0], move[1], player))

    if player == 1:
        best_idx = np.argmax(move_rewards)
    else:
        best_idx = np.argmin(move_rewards)

    best_move = possible_moves[best_idx]
    board.set_Value(best_move[0], best_move[1], player)

    return board.check_Win()

def minimax(player, board):
    moves = board.moves()
    if(board.check_Win()):
        return board.get_Winner()

    states = list(map(lambda move: copy(board).set_Value(move[0], move[1], player), board.moves()))
    for i in states:
        i.winner = minimax((-1) * player, i)
    
    if(player == 1):
        return max(states, key = lambda x: x.get_Winner()).get_Winner()
    else:
        return min(states, key = lambda x: x.get_Winner()).get_Winner()

play()