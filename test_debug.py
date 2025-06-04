"""
Casos de prueba simples para debugging del solver
"""

from board import Board
from solver import NumberLinkSolver
from loader import load_board_from_file

def test_minimal_2x2():
    """Prueba con el tablero más simple posible 2x2"""
    print("=== Test: Tablero 2x2 minimal ===")
    
    # Tablero 2x2 con un solo par
    board_data = [
        [1, 0],
        [0, 1]
    ]
    
    number_positions = {
        1: [(0, 0), (1, 1)]
    }
    
    board = Board(board_data, number_positions)
    print("Tablero inicial:")
    print(board)
    print()
    
    # Probar con debug activado
    solver = NumberLinkSolver(debug=True, time_limit=10)
    success, paths = solver.resolver_tablero(board)
    
    print(f"Resultado: {'Éxito' if success else 'Fallo'}")
    if success:
        print(f"Camino encontrado: {paths[0]}")
    
    return success

def test_simple_3x3_debug():
    """Prueba el tablero 3x3 con debug activado"""
    print("\n=== Test: Tablero 3x3 con debug ===")
    
    board_data = [
        [1, 0, 2],
        [0, 0, 0],
        [1, 0, 2]
    ]
    
    number_positions = {
        1: [(0, 0), (2, 0)],
        2: [(0, 2), (2, 2)]
    }
    
    board = Board(board_data, number_positions)
    print("Tablero inicial:")
    print(board)
    print()
    
    # Probar con debug activado
    solver = NumberLinkSolver(debug=True, time_limit=10)
    success, paths = solver.resolver_tablero(board)
    
    print(f"Resultado: {'Éxito' if success else 'Fallo'}")
    if success:
        print(f"Caminos encontrados: {paths}")
    
    return success

def test_board_validation():
    """Prueba las funciones de validación del tablero"""
    print("\n=== Test: Validación del tablero ===")
    
    board_data = [
        [1, 0, 2],
        [0, 0, 0],
        [1, 0, 2]
    ]
    
    number_positions = {
        1: [(0, 0), (2, 0)],
        2: [(0, 2), (2, 2)]
    }
    
    board = Board(board_data, number_positions)
    
    # Probar is_valid_move
    print("Probando is_valid_move:")
    test_cases = [
        ((0, 1), 1, "celda vacía para número 1"),
        ((1, 0), 1, "celda vacía para número 1"),
        ((0, 2), 1, "celda con número 2 para número 1"),
        ((2, 0), 1, "celda con número 1 para número 1"),
        ((1, 1), 2, "celda vacía para número 2"),
    ]
    
    for (r, c), number, description in test_cases:
        result = board.is_valid_move(r, c, number)
        print(f"  {description}: {result}")
    
    # Probar get_neighbors
    print("\nProbando get_neighbors:")
    for r in range(board.rows):
        for c in range(board.cols):
            neighbors = board.get_neighbors(r, c)
            print(f"  Vecinos de ({r},{c}): {neighbors}")
    
    # Probar get_pairs
    print(f"\nPares encontrados: {board.get_pairs()}")

def test_example_debug():
    """Prueba el ejemplo 7x7 con debug mejorado"""
    print("\n=== Test: Ejemplo 7x7 con debug ===")
    
    try:
        board_data, number_positions = load_board_from_file("example.txt")
        board = Board(board_data, number_positions)
        
        print("Tablero inicial:")
        print(board)
        print(f"Pares a conectar: {board.get_pairs()}")
        print()
        
        # Probar con tiempo más largo y debug activado
        solver = NumberLinkSolver(debug=True, time_limit=30, require_all_cells=False)
        success, paths = solver.resolver_tablero(board)
        
        print(f"Resultado: {'Éxito' if success else 'Fallo'}")
        print(f"Estadísticas: {solver.get_statistics()}")
        
        if success:
            print("Caminos encontrados:")
            for i, path in enumerate(paths):
                pairs = board.get_pairs()
                if i < len(pairs):
                    number = pairs[i][2]
                    print(f"  Número {number}: {path}")
        
        return success
        
    except FileNotFoundError:
        print("Archivo example.txt no encontrado")
        return False
    except Exception as e:
        print(f"Error: {e}")
        return False

def test_known_solvable():
    """Prueba con un tablero que sabemos que tiene solución"""
    print("\n=== Test: Tablero 4x4 solucionable conocido ===")
    
    board_data = [
        [1, 2, 3, 4],
        [0, 0, 0, 0],
        [0, 0, 0, 0],
        [1, 2, 3, 4]
    ]
    
    number_positions = {
        1: [(0, 0), (3, 0)],
        2: [(0, 1), (3, 1)],
        3: [(0, 2), (3, 2)],
        4: [(0, 3), (3, 3)]
    }
    
    board = Board(board_data, number_positions)
    print("Tablero inicial:")
    print(board)
    print()
    
    solver = NumberLinkSolver(debug=True, time_limit=10)
    success, paths = solver.resolver_tablero(board)
    
    print(f"Resultado: {'Éxito' if success else 'Fallo'}")
    if success:
        print("Caminos encontrados:")
        for i, path in enumerate(paths):
            pairs = board.get_pairs()
            if i < len(pairs):
                number = pairs[i][2]
                print(f"  Número {number}: {path}")
    
    return success

def run_debug_tests():
    """Ejecuta todos los tests de debugging"""
    print("=== EJECUTANDO TESTS DE DEBUGGING ===\n")
    
    results = []
    
    # Test 1: Tablero minimal
    results.append(("Tablero 2x2 minimal", test_minimal_2x2()))
    
    # Test 2: Validaciones
    test_board_validation()
    
    # Test 3: Tablero 3x3 con debug
    results.append(("Tablero 3x3 debug", test_simple_3x3_debug()))
    
    # Test 4: Tablero 4x4 conocido
    results.append(("Tablero 4x4 solucionable", test_known_solvable()))
    
    # Test 5: Ejemplo con debug (debe funcionar ahora)
    results.append(("Ejemplo 7x7", test_example_debug()))
    
    print("\n" + "="*50)
    print("RESUMEN DE TESTS DE DEBUG:")
    print("="*50)
    
    for test_name, result in results:
        status = "✓ PASÓ" if result else "✗ FALLÓ"
        print(f"{test_name}: {status}")

if __name__ == "__main__":
    run_debug_tests()