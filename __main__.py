import math, os, time, struct, socket
from blessed import Terminal
import module_connection as module
import IA as IA

term = Terminal()


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
        """Create a dictionary which contain all information

        parameter:
        -------------
        map_path:

        return:
        -------------
        board_info : a dyco which contain all information of the board and spawn
        """
        if '.ght' in map_path:
            board_info = {}
            fh = open(map_path, 'r')
            lines = fh.readlines()
            fh.close()
            current_key = ""
            board_info['nb_magic'] = 500
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
                            board_info['team1'][(x, y)] = 100
                        if team == 2:
                            board_info['spawn']['team2'] = (x, y)
                            if not 'team2' in board_info:
                                board_info['team2'] = {}
                            board_info['team2'][(x, y)] = 100
                    else:
                        if current_key == 'magic':
                            if not 'magic' in board_info:
                                x, y, nb_magic = int(split_line[0]), int(split_line[1]), int(split_line[2])
                                board_info['magic'] = {}
                            board_info['magic'][(x, y)] = 100
        else:
            print("This file is not in .ght please put an other one.")
        return board_info

    def print_board():
        """Print the board on the screen

        parameter:
        -------------
        board_info:

        """
        row = 3
        column = 6
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
                elif x == (column * coord_x) and y == (row * coord_y):
                    print(term.move_xy(x, y) + '┘', end='')
                elif x % column == 0 and y == (coord_y * row):
                    print(term.move_xy(x, y) + '┴', end='')
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
                elif ((coord_x * column) == x and y % (row // 2) == 0) and y % row != 0 and y % row != 1:
                    print(term.move_xy(x + 1, y - 1) + str((y + row // 2) // row), end='')
                # Print ghost and magic
                if ((x + 2) / column, (y + 1) / row) in board_info['team1'] and (
                (x + 2) / column, (y + 1) / row) in board_info['magic']:
                    print(term.move_xy(x - 3, y) + "\U0001F47B", end='')
                    print(term.move_xy(x, y) + "\U0001F52E")
                    print(term.move_xy(x - 3, y - 1) + str(board_info['team1'][((x + 2) / column, (y + 1) / row)]))
                    print(term.move_xy(x, y - 1) + str(board_info['magic'][((x + 2) / column, (y + 1) / row)]))
                    print(term.move_xy(x - 1, y + 1) + " ")
                elif ((x + 2) / column, (y + 1) / row) in board_info['magic']:
                    print(term.move_xy(x - 1, y) + "\U0001F52E")
                    print(term.move_xy(x - 1, y - 1) + str(board_info['magic'][((x + 2) / column, (y + 1) / row)]))
                elif ((x + 2) / column, (y + 1) / row) in board_info['team1']:
                    print(term.move_xy(x - 1, y) + "\U0001F47B")
                    print(term.move_xy(x - 1, y - 1) + str(board_info['team1'][((x + 2) / column, (y + 1) / row)]))
                if ((x + 2) / column, (y + 1) / row) in board_info['team2'] and (
                (x + 2) / column, (y + 1) / row) in board_info['magic']:
                    print(term.move_xy(x - 3, y) + "\U0001F47D", end='')
                    print(term.move_xy(x, y) + "\U0001F52E")
                    print(term.move_xy(x - 3, y - 1) + str(board_info['team2'][((x + 2) / column, (y + 1) / row)]))
                    print(term.move_xy(x, y - 1) + str(board_info['magic'][((x + 2) / column, (y + 1) / row)]))
                    print(term.move_xy(x - 1, y + 1) + " ")
                elif ((x + 2) / column, (y + 1) / row) in board_info['team2']:
                    print(term.move_xy(x - 1, y) + "\U0001F47D")
                    print(term.move_xy(x - 1, y - 1) + str(board_info['team2'][((x + 2) / column, (y + 1) / row)]))

    def new_ghost(team, ghost):
        """Add a ghost and and remove magic to the current player.

        Parameters
        ----------
        team: ghosts of the current player (dictionnary)
        ghost: starting data of the current player (starting point, magic point and emoji) (list)

        Returns
        -------
        board_info : dictionary with all the information of the game (dict)

        """
        if ghost[0] not in board_info[team] and board_info['nb_magic'] >= 300:
            board_info[team][ghost[0]] = 100
            board_info['nb_magic'] -= 300
        return board_info

    def heal_ghost(team, player_actions, i):
        """Heal a ghost and and remove magic to the current player.

        Parameters
        ----------
        team: ghosts of the current player (dictionnary)
        player_actions: All the moves of the current players (list)
        i: Random variable for iterating (int)
        board_info : dictionary with all the information of the game (dict)

        Returns
        -------
        team: ghosts of the current player (dictionnary)

        """
        y = int(player_actions[1][i].split("-")[0])
        x = int((player_actions[1][i].split("-")[1]).split(":")[0])
        heal_amount = int(player_actions[1][i].split("+")[1])
        size_x, size_y = board_info['size']
        if (x, y) in board_info[team]:
            hp_ghost = board_info[team][(x, y)]
            if 0 < x <= size_x and 0 < y <= size_y and hp_ghost + heal_amount <= 100 and \
                    board_info['nb_magic'] >= heal_amount * 2:
                team[x, y] += heal_amount
                board_info['nb_magic'] -= heal_amount * 2
        return team

    def obtain_moves(current_player):
        """Get the move from the current player and return it.

        Parameters
        ----------
        current_player: Tell if the player is a human or an AI (str)
        board_info : dictionary with all the information of the game (dict)

        Returns
        -------
        spawn_ghost: Move if the current player spawn a new ghost (boolean)
        tab_heal: List of moves when the current player heal a ghost (list)
        tab_get_magic: List of moves when the current player get the magic (list)
        tab_attack: List of moves when the current player attack the other player (list)
        tab_move: List of moves when the current player move a ghost (list)

        """
        spawn_ghost = False
        tab_heal = []
        tab_move = []
        tab_attack = []
        tab_get_magic = []
        if current_player == "human":
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
        #if current_player == "IA":
         #   spawn_ghost, tab_heal, tab_get_magic, tab_attack, tab_move = IA(spawn_ghost, tab_heal, tab_move, tab_attack,
                                                                            #tab_get_magic, team1, team2, ghost1, ghost2,
                                                                            #magic_dictionnary, size_map)

        return [spawn_ghost, tab_heal, tab_get_magic, tab_attack, tab_move]

    def take_magic_cell(magic_dictionnary, i, player_actions, size_map, already_played, ghost, team):
        """Take the magic points and add it to the current player.

        Parameters
        ----------
        magic_dictionnary: list of magic cells (coo, number of magic) (dictionnary)
        i: Random variable for iterating (int)
        player_actions: All the moves of the current players (list)
        size_map: size of the board (list)
        already_played: Tell if a ghost has already played (boolean)
        team: ghosts of the current player (dictionnary)

        Returns
        -------
        team: ghosts of the current player (dictionnary)

        """
        y = int(player_actions[2][i].split("-")[0])
        x = int((player_actions[2][i].split("-")[1]).split(":")[0])
        size_x, size_y = board_info['size']
        if (x, y) not in already_played:
            if x > 0 and x <= size_x and y > 0 and y <= size_y and (x, y) in board_info['magic'] and (
            x, y) in board_info[team]:
                board_info['nb_magic'] += board_info['magic'][(x, y)]
                del board_info['magic'][(x, y)]
                already_played.append((x, y))
        return already_played

    def ghost_attack(i, touched, player_actions, already_played):
        """Remove hp from the attacked ghost and add magic points to the current player.

        Parameters
        ----------
        i: Random variable for iterating (int)
        touched: Tell if the a ghost has attacked (int)
        player_actions: All the moves of the current players (list)
        already_played: Tell if a ghost has already played (boolean)

        Returns
        -------
        touched: Tell if the a ghost has attacked (int)
        already_played: Tell if a ghost has already played (boolean)

        """
        y1 = int(player_actions[3][i].split("-")[0])
        x1 = int((player_actions[3][i].split("-")[1]).split(":")[0])
        y2 = int((player_actions[3][i].split("x")[1]).split("-")[0])
        x2 = int((player_actions[3][i].split("x")[1]).split("-")[1])
        size_x, size_y = board_info['size']
        if (x1, y1) not in already_played:
            if 0 < x1 <= size_x and y1 > 0 <= size_y \
                    and 0 < x2 <= size_x and 0 < y2 <= size_y \
                    and (x1, y1) in board_info['team1'] and (x2, y2) in board_info['team2'] \
                    and -1 <= (x1 - x2) <= 1 and -1 <= (y1 - y2) <= 1:
                if board_info['team2'][(x2, y2)] > 0:
                    board_info['team2'][(x2, y2)] -= 10
                    board_info['nb_magic'] += 10
                    touched += 1
                    already_played.append((x1, y1))
        return touched, already_played

    def move(i, player_actions, already_played):
        """Move a ghost of the current player.

        Parameters
        ----------
        team1: ghost of player 1 (dictionnary)
        team2: ghost of player 2 (dictionnary)
        i: Random variable for iterating (int)
        player_actions: All the moves of the current players (list)
        size_map: size of the board (list)
        already_played: Tell if a ghost has already played (boolean)
        ghost1: starting data of player 1 (starting point, magic point and emoji) (list)
        ghost2: starting data of player 2 (starting point, magic point and emoji) (list)

        Returns
        -------
        team1: ghost of player 1 (dictionnary)
        already_played: Tell if a ghost has already played (boolean)

        """
        y1 = int(player_actions[4][i].split("-")[0])
        x1 = int((player_actions[4][i].split("-")[1]).split(":")[0])
        y2 = int((player_actions[4][i].split("@")[1]).split("-")[0])
        x2 = int((player_actions[4][i].split("@")[1]).split("-")[1])
        size_x, size_y = board_info['size']
        if (x1, y1) not in already_played:
            if x1 > 0 and x1 <= size_x and y1 > 0 and y1 <= size_y \
                    and x2 > 0 and x2 <= size_x and y2 > 0 and y2 <= size_y \
                    and (x1 - x2) >= -1 and (x1 - x2) <= 1 and (y1 - y2) >= -1 and (y1 - y2) <= 1 \
                    and (x1, y1) in board_info['team1'] and (x2, y2) not in board_info['team1'] and (x2, y2) not in board_info['team2'] \
                    and (x2, y2) != ghost1[0] and (x2, y2) != ghost2[0]:
                board_info['team1'][(x2, y2)] = board_info['team1'][x1, y1]
                del board_info['team1'][x1, y1]
                already_played.append((x2, y2))
        return already_played


    def print_player_information(board_info):
        """

        parameter:
        ---------------
        board_info:

        return:
        ---------------

        """
        longueur_board = term.height
        ...

    # create connection, if necessary
    if type_1 == 'remote':
        connection = module.create_connection(group_2, group_1)
    elif type_2 == 'remote':
        connection = module.create_connection(group_1, group_2)

    nb_turn = 0
    game_over = False
    board_info = create_board_info('bruh.ght')
    print_player_information(board_info)
    coord_y, coord_x = board_info['size']
    print(term.enter_fullscreen)

    while not game_over:

        print(term.home + term.clear)
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
    play_game('bruh.ght', 25, 'human', 2, 'IA')
