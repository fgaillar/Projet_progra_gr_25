from blessed import Terminal

term = Terminal()


def create_board_info(file):
    if '.ght' in file:
        board_info = {}
        fh = open(file, 'r')
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
                            board_info['team1'] = x, y
                        board_info['team1'] = x, y, 100
                    if team == 2:
                        board_info['spawn']['team2'] = (x, y)
                        if not 'team2' in board_info:
                            board_info['team2'] = {}
                        board_info['team2'] = x, y, 100
                else:
                    if current_key == 'magic':
                        if 'magic' in board_info:
                            x, y, nb_magic = int(split_line[0]), int(split_line[1]), int(split_line[2])
                            board_info['magic'] = (x, y), nb_magic
                        else:
                            board_info['magic'] = {}
    else:
        print("This file is not in .ght please put an other one.")
    return board_info


def create_board(board_info):
    row = 2
    column = 4
    coord_y, coord_x = board_info['size']
    for y in range((coord_y * row) + 1):
        for x in range((coord_x * column) + 1):
            if x == 0 and y == 0:
                print(term.move_xy(x, y) + '┌', end='')
            elif x % (column * coord_x) == 0 and y == 0:
                print(term.move_xy(x, y) + '┐', end='')
            elif y == 0 and x % column == 0:
                print(term.move_xy(x, y) + '┬', end='')
            elif x == 0 and y % (row * coord_x) == 0:
                print(term.move_xy(x, y) + '└', end='')
            elif x % (column * coord_x) == 0 and y % (row * coord_x) == 0:
                print(term.move_xy(x, y) + '┘', end='')
            elif x % column == 0 and y % (row * coord_x) == 0:
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
            elif ((coord_x * column) == x and y % (row // 2) == 0) and y % row != 0:
                print(term.move_xy(x + 1, y) + str((y + row // 2) // row), end='')
    print()



def player_information(board_info):
    coord_y, coord_x = board_info['size']


def main():
    game_over = False
    board_info = create_board_info('bruh.ght')
    term = Terminal()
    print(term.enter_fullscreen)
    while not game_over:
        print(term.home + term.clear)
        coord_y, coord_x = board_info['size']
        #print(board_info)
        create_board(board_info)
        print(term.move_xy(0, coord_y * 8), end='')
        if input():
            game_over = True
    print(term.exit_fullscreen)



if __name__ == "__main__":
    main()
