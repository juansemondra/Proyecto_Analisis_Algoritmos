"""
Generador de tableros aleatorios para NumberLink
"""

import random
from board import Board
from solver import NumberLinkSolver

class BoardGenerator:
    """Genera tableros aleatorios válidos para NumberLink"""
    
    def __init__(self, size, num_pairs):
        self.size = size
        self.num_pairs = num_pairs
    
    def generate_random_board(self, max_attempts=100):
        """
        Genera un tablero aleatorio con solución garantizada
        
        Returns:
            Board: Tablero generado o None si no se pudo generar
        """
        for attempt in range(max_attempts):
            board = self._create_random_placement()
            if board and self._verify_solvable(board):
                return board
        
        return None
    
    def _create_random_placement(self):
        """Crea una colocación aleatoria de números"""
        # Inicializar tablero vacío
        board_data = [[0 for _ in range(self.size)] for _ in range(self.size)]
        number_positions = {}
        
        # Colocar pares de números
        available_cells = [(r, c) for r in range(self.size) for c in range(self.size)]
        random.shuffle(available_cells)
        
        for num in range(1, self.num_pairs + 1):
            if len(available_cells) < 2:
                return None
            
            # Seleccionar dos posiciones aleatorias
            pos1 = available_cells.pop()
            pos2 = available_cells.pop()
            
            board_data[pos1[0]][pos1[1]] = num
            board_data[pos2[0]][pos2[1]] = num
            
            number_positions[num] = [pos1, pos2]
        
        return Board(board_data, number_positions)
    
    def _verify_solvable(self, board):
        """Verifica si el tablero tiene solución"""
        solver = NumberLinkSolver(time_limit=5)  # Límite corto para verificación
        success, _ = solver.resolver_tablero(board)
        return success
    
    def generate_with_difficulty(self, difficulty='medium'):
        """
        Genera un tablero con dificultad específica
        
        Args:
            difficulty: 'easy', 'medium', 'hard'
            
        Returns:
            Board: Tablero generado
        """
        # Ajustar parámetros según dificultad
        if difficulty == 'easy':
            # Menos pares, más espacio
            actual_pairs = max(2, self.num_pairs - 1)
        elif difficulty == 'hard':
            # Más pares, menos espacio
            actual_pairs = min(self.num_pairs + 1, (self.size * self.size) // 4)
        else:
            actual_pairs = self.num_pairs
        
        temp_generator = BoardGenerator(self.size, actual_pairs)
        return temp_generator.generate_random_board()
    
    def save_to_file(self, board, filename):
        """Guarda el tablero en un archivo"""
        with open(filename, 'w') as f:
            f.write(f"{board.rows},{board.cols}\n")
            
            for number, positions in board.number_positions.items():
                for r, c in positions:
                    f.write(f"{r+1},{c+1},{number}\n")

def generate_test_boards():
    """Genera varios tableros de prueba"""
    print("Generando tableros de prueba...")
    
    # Generar tableros de diferentes tamaños
    configs = [
        (4, 2, 'easy'),
        (5, 3, 'medium'),
        (6, 4, 'hard'),
        (7, 5, 'hard')
    ]
    
    for size, pairs, difficulty in configs:
        print(f"\nGenerando tablero {size}x{size} con {pairs} pares (dificultad: {difficulty})...")
        
        generator = BoardGenerator(size, pairs)
        board = generator.generate_with_difficulty(difficulty)
        
        if board:
            filename = f"generated_{size}x{size}_{difficulty}.txt"
            generator.save_to_file(board, filename)
            print(f"Tablero guardado en: {filename}")
            print("Vista previa:")
            print(board)
        else:
            print(f"No se pudo generar un tablero válido")

if __name__ == "__main__":
    generate_test_boards()