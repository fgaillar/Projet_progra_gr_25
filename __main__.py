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
                    equipe, x, y = int(split_line[0]), int(split_line[1]), int(split_line[2])
                    board_info['map'][(x, y)] = equipe
                    board_info[current_key].append(tuple(line.strip().split()))
                else:
                    if current_key == 'magic':
                        x, y, nb_magic = int(split_line[0]), int(split_line[1]), int(split_line[2])
                        board_info['map'][(x, y)] += nb_magic
                        board_info[current_key].append(tuple(line.strip().split()))
    else:
        print("This file is not in .ght please put an other one.")
    return board_info


def create_board(rows, colmn):
    board = ['+' + '{}+'.format('-' * 7) * colmn]
    for i in range(rows):
        row = ['|' + '       |' * colmn]
        for j in range(3):
            board.append('\n'.join(row))
        board.append('+'+'{}+'.format('-' * 7) * colmn)
    return "\n".join(board)


def main():
    create_board_info('bruh.ght')
    board_info = create_board_info('bruh.ght')
    coord_x, coord_y = board_info['size']
    print(create_board(coord_y, coord_x))


if __name__ == "__main__":
    main()