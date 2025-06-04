"""
Módulo de estadísticas para el solver de NumberLink
"""

import time
try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("Advertencia: matplotlib no está instalado. Los gráficos no estarán disponibles.")

from board import Board
from solver import NumberLinkSolver

class SolverStatistics:
    """Clase para recopilar y analizar estadísticas del solver"""
    
    def __init__(self):
        self.results = []
    
    def analyze_board(self, board, name=""):
        """Analiza un tablero y guarda estadísticas"""
        solver = NumberLinkSolver()
        
        start_time = time.time()
        success, paths = solver.resolver_tablero(board)
        end_time = time.time()
        
        stats = {
            'name': name,
            'size': f"{board.rows}x{board.cols}",
            'pairs': len(board.get_pairs()),
            'success': success,
            'time': end_time - start_time,
            'nodes_explored': solver.nodes_explored,
            'paths_found': len(paths) if success else 0
        }
        
        self.results.append(stats)
        return stats
    
    def print_summary(self):
        """Imprime un resumen de todas las estadísticas"""
        print("\nRESUMEN DE ESTADÍSTICAS")
        print("=" * 60)
        print(f"{'Tablero':<20} {'Tamaño':<10} {'Pares':<8} {'Éxito':<8} {'Tiempo(s)':<10} {'Nodos':<10}")
        print("-" * 60)
        
        for stat in self.results:
            print(f"{stat['name']:<20} {stat['size']:<10} {stat['pairs']:<8} "
                  f"{'Sí' if stat['success'] else 'No':<8} {stat['time']:<10.3f} {stat['nodes_explored']:<10}")
    
    def plot_performance(self):
        """Genera gráficos de rendimiento"""
        if not MATPLOTLIB_AVAILABLE:
            print("matplotlib no está instalado. No se pueden generar gráficos.")
            return
            
        if not self.results:
            print("No hay datos para graficar")
            return
        
        # Filtrar solo resultados exitosos
        successful = [r for r in self.results if r['success']]
        
        if not successful:
            print("No hay soluciones exitosas para graficar")
            return
        
        # Preparar datos
        names = [r['name'] for r in successful]
        times = [r['time'] for r in successful]
        nodes = [r['nodes_explored'] for r in successful]
        
        # Crear figura con subplots
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Gráfico de tiempos
        ax1.bar(names, times)
        ax1.set_xlabel('Tablero')
        ax1.set_ylabel('Tiempo (segundos)')
        ax1.set_title('Tiempo de Resolución por Tablero')
        ax1.tick_params(axis='x', rotation=45)
        
        # Gráfico de nodos explorados
        ax2.bar(names, nodes)
        ax2.set_xlabel('Tablero')
        ax2.set_ylabel('Nodos Explorados')
        ax2.set_title('Nodos Explorados por Tablero')
        ax2.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.savefig('performance_stats.png')
        plt.show()

def benchmark_solver():
    """Ejecuta un benchmark completo del solver"""
    stats = SolverStatistics()
    
    # Benchmark 1: Tableros de tamaño creciente
    print("Ejecutando benchmark de tableros de tamaño creciente...")
    
    sizes = [3, 4, 5, 6, 7]
    for size in sizes:
        # Crear tablero simple con 2 pares
        board_data = [[0 for _ in range(size)] for _ in range(size)]
        board_data[0][0] = 1
        board_data[size-1][size-1] = 1
        board_data[0][size-1] = 2
        board_data[size-1][0] = 2
        
        number_positions = {
            1: [(0, 0), (size-1, size-1)],
            2: [(0, size-1), (size-1, 0)]
        }
        
        board = Board(board_data, number_positions)
        stats.analyze_board(board, f"Simple_{size}x{size}")
    
    # Mostrar resultados
    stats.print_summary()
    
    # Generar gráficos si matplotlib está disponible
    stats.plot_performance()

if __name__ == "__main__":
    benchmark_solver()