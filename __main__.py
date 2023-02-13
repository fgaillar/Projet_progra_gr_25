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
                board_info['map'] = {}
                current_key = 'map'
            elif "ghosts:" in line:
                current_key = "ghosts"
            elif "magic:" in line:
                current_key = "magic"
            elif current_key != "":
                split_line = line.strip().split()
                if current_key not in board_info:
                    board_info[current_key] = []
                if current_key == 'map':
                    size_x, size_y = int(split_line[0]), int(split_line[1])
                    board_info['size'] = size_x, size_y
                    for x in range(1, size_x + 1):
                        for y in range(1, size_y + 1):
                            board_info['map'][(x, y)] = 0
                elif current_key == 'ghosts':
                    team, x, y = int(split_line[0]), int(split_line[1]), int(split_line[2])
                    board_info['map'][(x, y)] = team
                    board_info[current_key].append(tuple(line.strip().split()))
                else:
                    if current_key == 'magic':
                        x, y, nb_magic = int(split_line[0]), int(split_line[1]), int(split_line[2])
                        board_info['map'][(x, y)] += nb_magic
                        board_info[current_key].append(tuple(line.strip().split()))
    else:
        print("This file is not in .ght please put an other one.")
    return board_info


def create_board(board_info):
    coord_y, coord_x = board_info['size']
    for y in range((coord_y*4)+1):
        for x in range((coord_x*8)+1):
            with term.location(x, y):
                if x % 8 == 0 and y % 4 == 0:
                    print('+')
                elif x % 8 == 0 and y % 4 != 0:
                    print('|')
                elif y % 4 == 0 and x % 8 != 0:
                    print('―')
                    # Print coord x
            if ((coord_y*4) == y and x % 4 == 0) and x % 8 != 0:
                with term.location(x, y+1):
                    print((x + 4)//8)
                    # Print coord y
            elif ((coord_x*8) == x and y % 2 == 0) and y % 4 != 0:
                with term.location(x+1, y):
                    print((y + 2)//4)



def main():
    create_board_info('bruh.ght')
    print(term.home + term.clear)
    print(create_board())



if __name__ == "__main__":
    main()
