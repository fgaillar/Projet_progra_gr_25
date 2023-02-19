import math, os, time, struct, socket
from blessed import Terminal
import module_connection as module
import IA as IA

term = Terminal()


def player_information(board_info):
    coord_y, coord_x = board_info['size']


def obtain_moves():
    spawn_ghost = False
    tab_heal = []
    tab_move = []
    tab_attack = []
    tab_get_magic = []
    next_move = input("Next move : ")
    next_move = next_move.split(" ")
    for i in range(len(next_move)):
        if "ghost" in next_move[i]:
           spawn_ghost = True
        elif "+" in next_move[i]:
            tab_heal.append(next_move[i])
        elif "$" in next_move[i]:
            tab_get_magic.append(next_move[i])
        elif "x" in next_move[i]:
            tab_attack.append(next_move[i])
        elif "@" in next_move[i]:
            tab_move.append(next_move[i])
    return [spawn_ghost, tab_heal, tab_get_magic, tab_attack, tab_move]


def play_game(map_path, group_1, type_1, group_2, type_2):
    """Play a game.

    Parameters
    ----------
    map_path: path of map file (str)
    group_1: group of player 1 (int)
    type_1: type of player 1 (str)
    group_2: group of player 2 (int)
    type_2: type of player 2 (str)

    Notes
    -----
    Player type is either 'human', 'AI' or 'remote'.

    If there is an external referee, set group id to 0 for remote player.

    """

    def create_board_info(map_path):
        if '.ght' in map_path:
            board_info = {}
            fh = open(map_path, 'r')
            lines = fh.readlines()
            fh.close()
            current_key = ""
            for line in lines:
                if "map:" in line:
                    current_key = 'map'
                elif "ghosts:" in line:
                    current_key = 'spawn'
                    board_info['spawn'] = {}
                elif "magic:" in line:
                    current_key = "magic"
                elif current_key != "":
                    split_line = line.strip().split()
                    if current_key == 'map':
                        size_x, size_y = int(split_line[0]), int(split_line[1])
                        board_info['size'] = size_x, size_y
                    elif current_key == 'spawn':
                        team, x, y = int(split_line[0]), int(split_line[1]), int(split_line[2])
                        if team == 1:
                            board_info['spawn']['team1'] = (x, y)
                            if not 'team1' in board_info:
                                board_info['team1'] = {}
                            board_info['team1'][(x,y)] = 100
                        if team == 2:
                            board_info['spawn']['team2'] = (x, y)
                            if not 'team2' in board_info:
                                board_info['team2'] = {}
                            board_info['team2'][(x,y)] = 100
                    else:
                        if current_key == 'magic':
                            if not 'magic' in board_info:
                                x, y, nb_magic = int(split_line[0]), int(split_line[1]), int(split_line[2])
                                board_info['magic'] = {}
                            board_info['magic'][(x, y)] = 100
        else:
            print("This file is not in .ght please put an other one.")
        return board_info

    def print_board(board_info):
        row = 2
        column = 4
        coord_y, coord_x = board_info['size']
        for y in range((coord_y * row) + 1):
            for x in range((coord_x * column) + 1):
                if x == 0 and y == 0:
                    print(term.move_xy(x, y) + '┌', end='')
                elif x % (column * coord_x) == 0 and y == 0:
                    print(term.move_xy(x, y) + '┐', end='')
                elif x == 0 and y % (coord_y * row) == 0:
                    print(term.move_xy(x, y) + '└', end='')
                elif y == 0 and x % column == 0:
                    print(term.move_xy(x, y) + '┬', end='')
                elif x % column == 0 and y % (coord_y * row) == 0:
                    print(term.move_xy(x, y) + '┴', end='')
                elif x % (column * coord_x) == 0 and y % (row * coord_x) == 0:
                    print(term.move_xy(x, y) + '┘', end='')
                elif x == 0 and y % row == 0:
                    print(term.move_xy(x, y) + '├', end='')
                elif x % (column * coord_x) == 0 and y % row == 0:
                    print(term.move_xy(x, y) + '┤', end='')
                elif x % column == 0 and y % row == 0:
                    print(term.move_xy(x, y) + '┼', end='')
                elif x % column == 0 and y % row != 0:
                    print(term.move_xy(x, y) + '│', end='')
                elif y % row == 0 and x % column != 0:
                    print(term.move_xy(x, y) + '─', end='')
                # Print coord Y
                if ((coord_y * row) == y and x % (column // 2) == 0) and x % column != 0:
                    print(term.move_xy(x, y + 1) + str((x + column // 2) // column), end='')
                # Print coord X
                elif ((coord_x * column) == x and y % (row // 2) == 0) and y % row != 0:
                    print(term.move_xy(x + 1, y) + str((y + row // 2) // row), end='')
                for ghost in board_info['team1']:
                    if ghost == (x, y):
                        print(term.move_xy(4 * x - 3, 2 * y - 1) + '\U0001F47B')
                for alien in board_info['team2']:
                    if alien == (x, y):
                        print(term.move_xy(4 * x - 3, 2 * y - 1) + '\U0001F47D')
                for magic in board_info['magic']:
                    if magic == (x, y):
                        print(term.move_xy(4 * x - 3, 2 * y - 1) + '\U0001F52E')

    ...

    # create connection, if necessary
    if type_1 == 'remote':
        connection = module.create_connection(group_2, group_1)
    elif type_2 == 'remote':
        connection = module.create_connection(group_1, group_2)

    nb_turn = 0
    game_over = False
    board_info = create_board_info('bruh.ght')
    print(term.enter_fullscreen)

    while not game_over:

        print(term.home + term.clear)
        coord_y, coord_x = board_info['size']
        # print(board_info)
        print_board(board_info)
        print(term.move_xy(0, coord_y * 8), end='')
        nb_turn += 1
        if input() == 'quit':
            game_over = True

        # get orders of player 1 and notify them to player 2, if necessary
        if type_1 == 'remote':
            orders = module.get_remote_orders(connection)
        else:
            orders = IA.get_AI_orders(..., 1)
            if type_2 == 'remote':
                module.notify_remote_orders(connection, orders)

        # get orders of player 2 and notify them to player 1, if necessary
        if type_2 == 'remote':
            orders = module.get_remote_orders(connection)
        else:
            orders = IA.get_AI_orders(..., 2)
            if type_1 == 'remote':
                module.notify_remote_orders(connection, orders)

        ...
        ...
        print(term.exit_fullscreen)

    # close connection, if necessary
    if type_1 == 'remote' or type_2 == 'remote':
        module.close_connection(connection)


if __name__ == "__main__":
    play_game('bruh.ght', 25, 'human', 16, 'human')
