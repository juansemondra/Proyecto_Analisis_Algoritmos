"""
Casos de prueba para el solver de NumberLink
"""

import os
from board import Board
from solver import NumberLinkSolver
from loader import load_board_from_file

def test_example_7x7():
    """Prueba con el ejemplo proporcionado de 7x7"""
    print("=== Test: Ejemplo 7x7 ===")
    board_data, number_positions = load_board_from_file("example.txt")
    board = Board(board_data, number_positions)
    
    print("Tablero inicial:")
    print(board)
    print()
    
    # Primero probar sin debug
    solver = NumberLinkSolver()
    success, paths = solver.resolver_tablero(board)
    
    if success:
        print("¡Solución encontrada!")
        print(f"Estadísticas: {solver.get_statistics()}")
        print("\nCaminos encontrados:")
        for i, path in enumerate(paths):
            pairs = board.get_pairs()
            if i < len(pairs):
                number = pairs[i][2]
                print(f"Número {number}: {path}")
    else:
        print("No se encontró solución")
        print(f"Estadísticas: {solver.get_statistics()}")
        
        # Si no encuentra solución, probar con debug para ver qué pasa
        print("\n--- Ejecutando con debug para diagnosticar ---")
        debug_solver = NumberLinkSolver(debug=True, time_limit=10)
        debug_solver.resolver_tablero(board.copy())
    
    return success

def test_simple_3x3():
    """Prueba con un tablero simple 3x3"""
    print("\n=== Test: Tablero 3x3 simple ===")
    
    # Crear tablero manualmente
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
    
    solver = NumberLinkSolver()
    success, paths = solver.resolver_tablero(board)
    
    if success:
        print("¡Solución encontrada!")
        print(f"Estadísticas: {solver.get_statistics()}")
    else:
        print("No se encontró solución")
        print(f"Estadísticas: {solver.get_statistics()}")
        
        # Debug si falla
        print("\n--- Debug ---")
        debug_solver = NumberLinkSolver(debug=True, time_limit=5)
        debug_solver.resolver_tablero(board.copy())
    
    return success

def test_no_solution():
    """Prueba con un tablero sin solución"""
    print("\n=== Test: Tablero sin solución ===")
    
    # Tablero imposible: los números 2 bloquean completamente el paso
    board_data = [
        [1, 2, 1],
        [2, 2, 2],
        [3, 2, 3]
    ]
    
    number_positions = {
        1: [(0, 0), (0, 2)],
        2: [(0, 1), (1, 0)],  # Solo ponemos 2 posiciones aunque hay más 2s
        3: [(2, 0), (2, 2)]
    }
    
    board = Board(board_data, number_positions)
    print("Tablero inicial:")
    print(board)
    print()
    
    solver = NumberLinkSolver(time_limit=5)  # Límite más corto para este caso
    success, paths = solver.resolver_tablero(board)
    
    if success:
        print("¡Solución encontrada! (inesperado)")
    else:
        print("No se encontró solución (esperado)")
        print(f"Estadísticas: {solver.get_statistics()}")
    
    return not success  # Éxito si NO encuentra solución

def test_very_simple_2x2():
    """Prueba con un tablero 2x2 muy simple"""
    print("\n=== Test: Tablero 2x2 muy simple ===")
    
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
    
    solver = NumberLinkSolver(debug=False)
    success, paths = solver.resolver_tablero(board)
    
    if success:
        print("¡Solución encontrada!")
        print(f"Estadísticas: {solver.get_statistics()}")
        print(f"Camino: {paths[0]}")
    else:
        print("No se encontró solución")
        print(f"Estadísticas: {solver.get_statistics()}")
        
        # Debug si falla un caso tan simple
        print("\n--- Debug del caso 2x2 ---")
        debug_solver = NumberLinkSolver(debug=True)
        debug_solver.resolver_tablero(board.copy())
    
    return success

def test_complex_5x5():
    """Prueba con un tablero más complejo 5x5"""
    print("\n=== Test: Tablero 5x5 complejo ===")
    
    board_data = [
        [1, 0, 0, 0, 2],
        [0, 0, 3, 0, 0],
        [0, 4, 0, 4, 0],
        [0, 0, 3, 0, 0],
        [1, 0, 0, 0, 2]
    ]
    
    number_positions = {
        1: [(0, 0), (4, 0)],
        2: [(0, 4), (4, 4)],
        3: [(1, 2), (3, 2)],
        4: [(2, 1), (2, 3)]
    }
    
    board = Board(board_data, number_positions)
    print("Tablero inicial:")
    print(board)
    print()
    
    solver = NumberLinkSolver()
    success, paths = solver.resolver_tablero(board)
    
    if success:
        print("¡Solución encontrada!")
        print(f"Estadísticas: {solver.get_statistics()}")
        
        # Verificar que se usaron todas las celdas
        total_cells = sum(len(path) for path in paths)
        expected_cells = 5 * 5
        print(f"Celdas utilizadas: {total_cells}/{expected_cells}")
    else:
        print("No se encontró solución")
        print(f"Estadísticas: {solver.get_statistics()}")
    
    return success

def create_test_file(filename, content):
    """Crea un archivo de prueba temporal"""
    with open(filename, 'w') as f:
        f.write(content)

def run_all_tests():
    """Ejecuta todos los casos de prueba"""
    print("Ejecutando todos los casos de prueba...\n")
    
    results = []
    
    # Test 0: Caso muy simple primero
    results.append(("Tablero 2x2 simple", test_very_simple_2x2()))
    
    # Test 1: Ejemplo original
    results.append(("Ejemplo 7x7", test_example_7x7()))
    
    # Test 2: Tablero simple
    results.append(("Tablero 3x3 simple", test_simple_3x3()))
    
    # Test 3: Sin solución
    results.append(("Tablero sin solución", test_no_solution()))
    
    # Test 4: Tablero complejo
    results.append(("Tablero 5x5 complejo", test_complex_5x5()))
    
    # Test 5: Tablero adicional desde archivo
    print("\n=== Test: Tablero adicional 4x4 ===")
    test_content = """4,4
1,1,1
1,4,2
2,2,3
3,1,3
3,3,2
4,4,1"""
    
    create_test_file("test_4x4.txt", test_content)
    
    try:
        board_data, number_positions = load_board_from_file("test_4x4.txt")
        board = Board(board_data, number_positions)
        solver = NumberLinkSolver()
        success, _ = solver.resolver_tablero(board)
        results.append(("Tablero 4x4 desde archivo", success))
        print(f"Resultado: {'Éxito' if success else 'Fallo'}")
    except Exception as e:
        print(f"Error en test 4x4: {e}")
        results.append(("Tablero 4x4 desde archivo", False))
    finally:
        if os.path.exists("test_4x4.txt"):
            os.remove("test_4x4.txt")
    
    # Resumen
    print("\n" + "="*50)
    print("RESUMEN DE PRUEBAS:")
    print("="*50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASÓ" if result else "✗ FALLÓ"
        print(f"{test_name}: {status}")
    
    print(f"\nTotal: {passed}/{total} pruebas pasadas")
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)