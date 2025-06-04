from board import Board
import time
from collections import deque

class NumberLinkSolver:
    """Solucionador EXHAUSTIVO para NumberLink - prioriza encontrar solución sobre velocidad"""
    
    def __init__(self, time_limit=300, debug=False, require_all_cells=False):  # 5 minutos por defecto
        self.solutions_found = 0
        self.nodes_explored = 0
        self.time_limit = time_limit
        self.start_time = None
        self.debug = debug
        self.require_all_cells = require_all_cells
        
    def _debug_print(self, message, level=0):
        """Imprime mensaje de debug con indentación"""
        if self.debug:
            indent = "  " * level
            print(f"{indent}{message}")
        
    def resolver_tablero(self, board):
        """
        Función principal - busca exhaustivamente hasta encontrar solución
        """
        self.start_time = time.time()
        self.nodes_explored = 0
        self.solutions_found = 0
        
        pairs = board.get_pairs()
        paths = []
        
        self._debug_print(f"=== BÚSQUEDA EXHAUSTIVA ===")
        self._debug_print(f"Tablero: {board.rows}x{board.cols}")
        self._debug_print(f"Pares: {len(pairs)}")
        self._debug_print(f"Tiempo límite: {self.time_limit}s")
        
        # Probar MÚLTIPLES órdenes de pares
        orderings = [
            self._order_by_distance,
            self._order_by_border_preference,
            self._order_by_flexibility,
            list(reversed(self._order_by_distance(pairs, board)))
        ]
        
        for order_idx, ordering_func in enumerate(orderings):
            if time.time() - self.start_time > self.time_limit:
                break
                
            self._debug_print(f"\n--- Probando orden {order_idx + 1} ---")
            
            if callable(ordering_func):
                sorted_pairs = ordering_func(pairs, board)
            else:
                sorted_pairs = ordering_func
            
            self._debug_print("Orden de pares:")
            for i, (start, end, num) in enumerate(sorted_pairs):
                dist = abs(start[0] - end[0]) + abs(start[1] - end[1])
                self._debug_print(f"  {i+1}. Número {num}: {start} -> {end} (dist: {dist})")
            
            # Crear copia fresca del tablero
            working_board = board.copy()
            paths_copy = []
            
            if self._resolver_exhaustivo(0, working_board, sorted_pairs, paths_copy):
                self._debug_print(f"\n¡SOLUCIÓN ENCONTRADA con orden {order_idx + 1}!")
                return True, paths_copy
        
        self._debug_print(f"\n=== NO SE ENCONTRÓ SOLUCIÓN ===")
        self._debug_print(f"Nodos explorados: {self.nodes_explored}")
        
        return False, []
    
    def _order_by_distance(self, pairs, board):
        """Orden por distancia - más cortos primero"""
        return sorted(pairs, key=lambda p: abs(p[0][0] - p[1][0]) + abs(p[0][1] - p[1][1]))
    
    def _order_by_border_preference(self, pairs, board):
        """Orden por preferencia de borde - bordes largos primero"""
        def score(pair):
            start, end, num = pair
            dist = abs(start[0] - end[0]) + abs(start[1] - end[1])
            
            start_border = (start[0] == 0 or start[0] == board.rows-1 or
                           start[1] == 0 or start[1] == board.cols-1)
            end_border = (end[0] == 0 or end[0] == board.rows-1 or
                         end[1] == 0 or end[1] == board.cols-1)
            
            if start_border and end_border and dist > 5:
                return 1  # Prioridad alta
            elif dist <= 3:
                return 3  # Prioridad baja (flexibles al final)
            else:
                return 2  # Prioridad media
            
        return sorted(pairs, key=score)
    
    def _order_by_flexibility(self, pairs, board):
        """Orden por flexibilidad - menos flexibles primero"""
        def flexibility_score(pair):
            start, end, num = pair
            
            # Contar opciones de movimiento
            start_neighbors = len([n for n in board.get_neighbors(start[0], start[1])
                                 if board.grid[n[0]][n[1]] == Board.EMPTY])
            end_neighbors = len([n for n in board.get_neighbors(end[0], end[1])
                               if board.grid[n[0]][n[1]] == Board.EMPTY])
            
            return min(start_neighbors, end_neighbors)  # Menos opciones = menos flexible
        
        return sorted(pairs, key=flexibility_score)
    
    def _resolver_exhaustivo(self, index, board, pairs, paths):
        """Backtracking exhaustivo - explora TODO hasta encontrar solución"""
        
        # Check time limit
        if time.time() - self.start_time > self.time_limit:
            self._debug_print(f"Tiempo límite alcanzado", index)
            return False
            
        self.nodes_explored += 1
        
        # Progreso cada 1000 nodos
        if self.nodes_explored % 1000 == 0:
            elapsed = time.time() - self.start_time
            self._debug_print(f"Progreso: {self.nodes_explored} nodos, {elapsed:.1f}s")
        
        # Caso base: todos los pares conectados
        if index == len(pairs):
            if self.require_all_cells:
                complete = board.is_complete()
                if complete:
                    self._debug_print(f"¡SOLUCIÓN COMPLETA ENCONTRADA!", index)
                return complete
            else:
                self._debug_print(f"¡SOLUCIÓN ENCONTRADA!", index)
                return True
        
        start, end, number = pairs[index]
        
        if self.debug and (index < 2 or self.nodes_explored % 100 == 1):
            self._debug_print(f"Nodo {self.nodes_explored}: Par {index+1}/{len(pairs)} - Número {number} de {start} a {end}", index)
        
        # Buscar caminos con límites MUY generosos
        caminos_posibles = self._buscar_caminos_exhaustivo(start, end, board, number)
        
        if self.debug and (index < 2 or self.nodes_explored % 100 == 1):
            self._debug_print(f"Caminos encontrados: {len(caminos_posibles)}", index + 1)
        
        if not caminos_posibles:
            return False
        
        # Probar TODOS los caminos encontrados
        for i, camino in enumerate(caminos_posibles):
            if self.debug and index < 2 and i < 5:
                self._debug_print(f"Probando camino {i+1}/{len(caminos_posibles)}: longitud {len(camino)}", index + 1)
            
            # Marcar camino
            self._marcar_camino(camino, board)
            paths.append(camino)
            
            # Validación MUY básica - solo verificar que no se rompió todo
            validation_ok = True
            
            # Solo verificar los próximos 2 pares para no ser demasiado estricto
            if index < len(pairs) - 1:
                next_pairs_to_check = pairs[index+1:index+3]  # Solo los próximos 2
                for check_start, check_end, check_num in next_pairs_to_check:
                    if not self._conectividad_basica(check_start, check_end, board, check_num):
                        validation_ok = False
                        break
            
            if validation_ok:
                # Continuar recursión
                if self._resolver_exhaustivo(index + 1, board, pairs, paths):
                    return True
            
            # Backtrack
            self._desmarcar_camino(camino, board)
            paths.pop()
        
        return False
    
    def _buscar_caminos_exhaustivo(self, start, end, board, number):
        """Búsqueda exhaustiva de caminos - límites MUY generosos"""
        if start == end:
            return [[start]]
        
        # Límites ENORMES para no cortar soluciones válidas
        max_paths = 50  # Muchos más caminos
        manhattan_dist = abs(start[0] - end[0]) + abs(start[1] - end[1])
        max_length = manhattan_dist * 5 + 10  # MUCHO más generoso
        
        paths = []
        
        # BFS exhaustivo
        queue = [(start, [start], {start})]
        
        while queue and len(paths) < max_paths:
            current, path, visited = queue.pop(0)
            
            # Solo cortar si realmente es demasiado largo
            if len(path) > max_length:
                continue
            
            if current == end:
                paths.append(path)
                continue
            
            # Explorar TODAS las direcciones posibles
            neighbors = board.get_neighbors(current[0], current[1])
            for neighbor in neighbors:
                if neighbor not in visited and board.is_valid_move(neighbor[0], neighbor[1], number):
                    new_path = path + [neighbor]
                    new_visited = visited | {neighbor}
                    queue.append((neighbor, new_path, new_visited))
        
        # Ordenar por longitud (más cortos primero, pero probar todos)
        paths.sort(key=len)
        
        return paths
    
    def _conectividad_basica(self, start, end, board, number):
        """Verificación MUY básica de conectividad - solo lo esencial"""
        if start == end:
            return True
        
        # BFS simple con límite generoso
        visited = {start}
        queue = deque([start])
        max_checks = board.rows * board.cols  # Límite muy generoso
        checks = 0
        
        while queue and checks < max_checks:
            current = queue.popleft()
            checks += 1
            
            for neighbor in board.get_neighbors(current[0], current[1]):
                if neighbor == end:
                    return True
                
                if neighbor not in visited and board.is_valid_move(neighbor[0], neighbor[1], number):
                    visited.add(neighbor)
                    queue.append(neighbor)
        
        return False
    
    def _marcar_camino(self, path, board):
        """Marca un camino en el tablero"""
        for r, c in path:
            if board.original_grid[r][c] == Board.EMPTY:
                board.mark_cell(r, c, Board.VISITED)
    
    def _desmarcar_camino(self, path, board):
        """Desmarca un camino del tablero"""
        for r, c in path:
            if board.original_grid[r][c] == Board.EMPTY:
                board.unmark_cell(r, c)
    
    def get_statistics(self):
        """Obtiene estadísticas de la resolución"""
        elapsed_time = time.time() - self.start_time if self.start_time else 0
        return {
            'nodes_explored': self.nodes_explored,
            'solutions_found': self.solutions_found,
            'time_elapsed': elapsed_time
        }