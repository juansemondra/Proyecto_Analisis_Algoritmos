def load_board_from_file(path):
    with open(path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    
    rows, cols = map(int, lines[0].split(","))
    board_data = [[0 for _ in range(cols)] for _ in range(rows)]
    number_positions = {}

    for line in lines[1:]:
        r, c, number = map(int, line.split(","))
        board_data[r - 1][c - 1] = number
        if number not in number_positions:
            number_positions[number] = []
        number_positions[number].append((r - 1, c - 1))
    
    return board_data, number_positions