import copy

class Board:
    """Clase que representa el estado del tablero de NumberLink"""
    
    # Estados posibles de una celda
    EMPTY = 0
    VISITED = -1
    
    def __init__(self, board_data, number_positions):
        """
        Constructor del tablero
        
        Args:
            board_data: Matriz 2D con los números iniciales
            number_positions: Diccionario {numero: [(r1,c1), (r2,c2)]}
        """
        self.rows = len(board_data)
        self.cols = len(board_data[0]) if board_data else 0
        self.grid = copy.deepcopy(board_data)
        self.number_positions = copy.deepcopy(number_positions)
        self.original_grid = copy.deepcopy(board_data)  # Para referencia
        
    def copy(self):
        """Crea una copia profunda del tablero"""
        new_board = Board.__new__(Board)
        new_board.rows = self.rows
        new_board.cols = self.cols
        new_board.grid = copy.deepcopy(self.grid)
        new_board.number_positions = copy.deepcopy(self.number_positions)
        new_board.original_grid = copy.deepcopy(self.original_grid)
        return new_board
    
    def is_valid_move(self, r, c, number):
        """
        Verifica si es válido moverse a la celda (r,c) para el número dado
        
        Args:
            r: fila
            c: columna
            number: número que se está conectando
            
        Returns:
            bool: True si el movimiento es válido
        """
        # Verificar límites
        if r < 0 or r >= self.rows or c < 0 or c >= self.cols:
            return False
            
        cell_value = self.grid[r][c]
        
        # La celda está vacía
        if cell_value == self.EMPTY:
            return True
            
        # La celda ya fue visitada
        if cell_value == self.VISITED:
            return False
            
        # La celda contiene el mismo número que estamos conectando
        if cell_value == number:
            return True
            
        # La celda contiene un número diferente
        return False
    
    def mark_cell(self, r, c, state):
        """
        Marca una celda con un estado específico
        
        Args:
            r: fila
            c: columna
            state: nuevo estado de la celda
        """
        self.grid[r][c] = state
        
    def unmark_cell(self, r, c):
        """
        Desmarca una celda, restaurando su valor original
        
        Args:
            r: fila
            c: columna
        """
        self.grid[r][c] = self.original_grid[r][c]
        
    def get_neighbors(self, r, c):
        """
        Obtiene las celdas adyacentes (arriba, abajo, izquierda, derecha)
        
        Args:
            r: fila
            c: columna
            
        Returns:
            list: Lista de tuplas (r, c) de celdas adyacentes válidas
        """
        neighbors = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # arriba, abajo, izq, der
        
        for dr, dc in directions:
            new_r, new_c = r + dr, c + dc
            if 0 <= new_r < self.rows and 0 <= new_c < self.cols:
                neighbors.append((new_r, new_c))
                
        return neighbors
    
    def is_complete(self):
        """
        Verifica si el tablero está completamente resuelto
        
        Returns:
            bool: True si todas las celdas están ocupadas
        """
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r][c] == self.EMPTY:
                    return False
        return True
    
    def get_pairs(self):
        """
        Obtiene la lista de pares de posiciones a conectar
        
        Returns:
            list: Lista de tuplas ((r1,c1), (r2,c2), numero)
        """
        pairs = []
        for number, positions in self.number_positions.items():
            if len(positions) == 2:
                pairs.append((positions[0], positions[1], number))
        return pairs
    
    def __str__(self):
        """Representación en string del tablero para debugging"""
        result = []
        for r in range(self.rows):
            row = []
            for c in range(self.cols):
                val = self.grid[r][c]
                if val == self.EMPTY:
                    row.append('.')
                elif val == self.VISITED:
                    row.append('*')
                else:
                    row.append(str(val))
            result.append(' '.join(row))
        return '\n'.join(result)