def load_board_from_file(path):
    with open(path, "r") as f:
        lines = [line.strip() for line in f if line.strip()]
    
    # Limpiar espacios extra y dividir por comas
    first_line = lines[0].replace(" ", "").split(",")
    rows, cols = map(int, first_line)
    
    board_data = [[0 for _ in range(cols)] for _ in range(rows)]
    number_positions = {}

    for line in lines[1:]:
        # Limpiar espacios extra antes de dividir
        clean_line = line.replace(" ", "").split(",")
        r, c, number = map(int, clean_line)
        
        # Convertir a índices base 0
        board_data[r - 1][c - 1] = number
        if number not in number_positions:
            number_positions[number] = []
        number_positions[number].append((r - 1, c - 1))
    
    return board_data, number_positions