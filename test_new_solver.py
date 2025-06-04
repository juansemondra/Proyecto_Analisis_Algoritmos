"""
Pruebas específicas para el solver mejorado
"""

from board import Board
from solver import NumberLinkSolver
from loader import load_board_from_file
import time

def test_example_7x7_mejorado():
    """Prueba el ejemplo 7x7 con el solver mejorado"""
    print("=== Test: Ejemplo 7x7 con Solver Mejorado ===")
    
    try:
        board_data, number_positions = load_board_from_file("example.txt")
        board = Board(board_data, number_positions)
        
        print("Tablero inicial:")
        print(board)
        print("\nPares a conectar:")
        for i, (start, end, num) in enumerate(board.get_pairs()):
            print(f"  {i+1}. Número {num}: {start} -> {end}")
        
        # Probar con el solver mejorado
        solver = NumberLinkSolver(time_limit=30, debug=True, require_all_cells=True)
        
        print("\n--- Iniciando resolución ---")
        start_time = time.time()
        success, paths = solver.resolver_tablero(board)
        end_time = time.time()
        
        print(f"\nResultado: {'ÉXITO' if success else 'FALLO'}")
        print(f"Tiempo total: {end_time - start_time:.3f}s")
        print(f"Estadísticas: {solver.get_statistics()}")
        
        if success:
            print("\nCaminos encontrados:")
            pairs = board.get_pairs()
            for i, path in enumerate(paths):
                if i < len(pairs):
                    number = pairs[i][2]
                    print(f"  Número {number}: {len(path)} celdas - {path[:3]}...{path[-3:]}")
            
            # Verificar cobertura
            covered = set()
            for path in paths:
                covered.update(path)
            print(f"\nCobertura total: {len(covered)}/{board.rows * board.cols} celdas")
        
        return success
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_performance_comparison():
    """Compara el rendimiento en varios tableros"""
    print("\n=== Comparación de Rendimiento ===")
    
    test_files = ["example.txt"]  # Añadir más archivos si están disponibles
    
    for filename in test_files:
        try:
            board_data, number_positions = load_board_from_file(filename)
            board = Board(board_data, number_positions)
            
            print(f"\nTablero {filename} ({board.rows}x{board.cols}):")
            
            # Sin debug para medir rendimiento real
            solver = NumberLinkSolver(time_limit=30, require_all_cells=True)
            
            start_time = time.time()
            success, paths = solver.resolver_tablero(board)
            end_time = time.time()
            
            stats = solver.get_statistics()
            print(f"  Resultado: {'ÉXITO' if success else 'FALLO'}")
            print(f"  Tiempo: {end_time - start_time:.3f}s")
            print(f"  Nodos explorados: {stats['nodes_explored']}")
            
        except Exception as e:
            print(f"  Error: {e}")

def test_impossible_board():
    """Prueba con un tablero imposible para verificar que no se cuelga"""
    print("\n=== Test: Tablero Imposible ===")
    
    # Tablero diseñado para ser imposible
    board_data = [
        [1, 2, 3, 4],
        [2, 0, 0, 3],
        [1, 0, 0, 4],
        [5, 6, 6, 5]
    ]
    
    number_positions = {
        1: [(0, 0), (2, 0)],
        2: [(0, 1), (1, 0)],
        3: [(0, 2), (1, 3)],
        4: [(0, 3), (2, 3)],
        5: [(3, 0), (3, 3)],
        6: [(3, 1), (3, 2)]
    }
    
    board = Board(board_data, number_positions)
    print("Tablero:")
    print(board)
    
    solver = NumberLinkSolver(time_limit=5, debug=False)
    
    start_time = time.time()
    success, paths = solver.resolver_tablero(board)
    end_time = time.time()
    
    print(f"\nResultado: {'ÉXITO' if success else 'FALLO'} (esperado: FALLO)")
    print(f"Tiempo: {end_time - start_time:.3f}s")
    print(f"Nodos explorados: {solver.get_statistics()['nodes_explored']}")
    
    return not success  # Éxito si no encuentra solución

def run_all_tests():
    """Ejecuta todas las pruebas del solver mejorado"""
    print("="*60)
    print("PRUEBAS DEL SOLVER MEJORADO")
    print("="*60)
    
    results = []
    
    # Test principal: el ejemplo 7x7
    results.append(("Ejemplo 7x7", test_example_7x7_mejorado()))
    
    # Test de rendimiento
    test_performance_comparison()
    
    # Test de tablero imposible
    results.append(("Tablero imposible", test_impossible_board()))
    
    # Resumen
    print("\n" + "="*60)
    print("RESUMEN DE PRUEBAS:")
    print("="*60)
    
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