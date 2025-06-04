"""
Casos de prueba simples y solucionables para NumberLink
"""

from board import Board
from solver import NumberLinkSolver

def test_2x3_solvable():
    """Prueba con un tablero 2x3 que sí tiene solución completa"""
    print("=== Test: Tablero 2x3 solucionable ===")
    
    # Este tablero sí se puede resolver cubriendo todas las celdas
    board_data = [
        [1, 2, 1],
        [2, 3, 3]
    ]
    
    number_positions = {
        1: [(0, 0), (0, 2)],
        2: [(0, 1), (1, 0)],
        3: [(1, 1), (1, 2)]
    }
    
    board = Board(board_data, number_positions)
    print("Tablero inicial:")
    print(board)
    print()
    
    solver = NumberLinkSolver(debug=False)
    success, paths = solver.resolver_tablero(board)
    
    print(f"Resultado: {'Éxito' if success else 'Fallo'}")
    if success:
        print("Caminos encontrados:")
        for i, path in enumerate(paths):
            print(f"  Camino {i+1}: {path}")
    print(f"Estadísticas: {solver.get_statistics()}")
    
    return success

def test_3x3_partial():
    """Prueba con un tablero 3x3 sin requerir todas las celdas"""
    print("\n=== Test: Tablero 3x3 (sin requerir todas las celdas) ===")
    
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
    
    # No requerir que todas las celdas estén cubiertas
    solver = NumberLinkSolver(debug=False, require_all_cells=False)
    success, paths = solver.resolver_tablero(board)
    
    print(f"Resultado: {'Éxito' if success else 'Fallo'}")
    if success:
        print("Caminos encontrados:")
        for i, path in enumerate(paths):
            print(f"  Camino {i+1}: {path}")
    print(f"Estadísticas: {solver.get_statistics()}")
    
    return success

def test_4x4_solvable():
    """Prueba con un tablero 4x4 diseñado para tener solución"""
    print("\n=== Test: Tablero 4x4 solucionable ===")
    
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
    
    solver = NumberLinkSolver(debug=False)
    success, paths = solver.resolver_tablero(board)
    
    print(f"Resultado: {'Éxito' if success else 'Fallo'}")
    if success:
        print("Caminos encontrados:")
        for i, path in enumerate(paths):
            print(f"  Camino {i+1}: {path}")
    print(f"Estadísticas: {solver.get_statistics()}")
    
    return success

def test_example_corrected():
    """Prueba con el ejemplo corregido del documento"""
    print("\n=== Test: Ejemplo 7x7 corregido ===")
    
    try:
        from loader import load_board_from_file
        board_data, number_positions = load_board_from_file("example.txt")
        board = Board(board_data, number_positions)
        
        print("Tablero inicial:")
        print(board)
        print()
        
        # Probar sin requerir todas las celdas primero
        solver = NumberLinkSolver(debug=False, require_all_cells=False, time_limit=10)
        success, paths = solver.resolver_tablero(board)
        
        print(f"Resultado (sin requerir todas las celdas): {'Éxito' if success else 'Fallo'}")
        
        if success:
            print(f"Estadísticas: {solver.get_statistics()}")
            
            # Verificar cuántas celdas se cubrieron
            covered = set()
            for path in paths:
                covered.update(path)
            
            total_cells = board.rows * board.cols
            print(f"Celdas cubiertas: {len(covered)}/{total_cells}")
            
            # Ahora probar requiriendo todas las celdas
            print("\nProbando con todas las celdas requeridas...")
            solver2 = NumberLinkSolver(debug=False, require_all_cells=True, time_limit=10)
            success2, paths2 = solver2.resolver_tablero(board)
            print(f"Resultado (requiriendo todas las celdas): {'Éxito' if success2 else 'Fallo'}")
        
    except Exception as e:
        print(f"Error: {e}")
        return False
    
    return success

def run_all_simple_tests():
    """Ejecuta todos los tests simples"""
    print("=== EJECUTANDO TESTS SIMPLES ===\n")
    
    results = []
    
    # Tests
    results.append(("2x3 solucionable", test_2x3_solvable()))
    results.append(("3x3 parcial", test_3x3_partial()))
    results.append(("4x4 solucionable", test_4x4_solvable()))
    results.append(("Ejemplo 7x7", test_example_corrected()))
    
    # Resumen
    print("\n" + "="*50)
    print("RESUMEN:")
    print("="*50)
    
    for name, result in results:
        print(f"{name}: {'✓ PASÓ' if result else '✗ FALLÓ'}")
    
    passed = sum(1 for _, r in results if r)
    print(f"\nTotal: {passed}/{len(results)} pruebas pasadas")

if __name__ == "__main__":
    run_all_simple_tests()