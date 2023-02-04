
def create_board_info(file):
    if '.ght' in file:
        board_info = {}
        fh = open(file, 'r')
        lines = fh.readlines()
        fh.close()
        current_key = ""
        for line in lines:
            if "map:" in line:
                current_key = "map"
            elif "ghosts:" in line:
                current_key = "ghosts"
            elif "magic:" in line:
                current_key = "magic"
            elif current_key != "":
                if current_key not in board_info:
                    board_info[current_key] = []
                board_info[current_key].append(tuple(line.strip().split()))

    board_info["ghosts"] = tuple(magic_data for magic_data in board_info["ghosts"])
    board_info["magic"] = tuple(magic_data for magic_data in board_info["magic"])

    return board_info


def create_board(info):
    board = []

