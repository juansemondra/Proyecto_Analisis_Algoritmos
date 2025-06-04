from board import Board
import time

class NumberLinkSolver:
    """Solucionador automático para el juego NumberLink usando backtracking optimizado"""
    
    def __init__(self, time_limit=30, debug=False, require_all_cells=True):
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
        Función principal para resolver el tablero
        
        Args:
            board: Instancia de Board con el tablero a resolver
            
        Returns:
            tuple: (éxito, caminos) donde caminos es una lista de listas de coordenadas
        """
        self.start_time = time.time()
        self.nodes_explored = 0
        self.solutions_found = 0
        
        pairs = board.get_pairs()
        paths = []
        
        self._debug_print(f"=== INICIANDO RESOLUCIÓN ===")
        self._debug_print(f"Tablero: {board.rows}x{board.cols}")
        self._debug_print(f"Pares: {len(pairs)}")
        self._debug_print(f"Requiere todas las celdas: {self.require_all_cells}")
        
        # Crear copia del tablero
        working_board = board.copy()
        
        # Intentar diferentes ordenamientos
        orderings = [
            self._ordenar_por_distancia,      # Más cortos primero
            self._ordenar_por_restriccion,    # Más restrictivos primero
            lambda p, b: list(reversed(self._ordenar_por_distancia(p, b))),  # Más largos primero
        ]
        
        for idx, ordering_func in enumerate(orderings):
            if time.time() - self.start_time > self.time_limit:
                break
                
            self._debug_print(f"\nProbando ordenamiento {idx + 1}: {ordering_func.__name__}")
            
            sorted_pairs = ordering_func(pairs, working_board)
            board_copy = working_board.copy()
            paths_copy = []
            
            if self._resolver_recursivo(0, board_copy, sorted_pairs, paths_copy):
                self._debug_print(f"¡Solución encontrada con {ordering_func.__name__}!")
                return True, paths_copy
        
        self._debug_print(f"\n=== No se encontró solución ===")
        self._debug_print(f"Nodos explorados: {self.nodes_explored}")
        
        return False, []
    
    def _ordenar_por_distancia(self, pairs, board):
        """Ordena por distancia Manhattan (más cortos primero)"""
        return sorted(pairs, key=lambda p: abs(p[0][0] - p[1][0]) + abs(p[0][1] - p[1][1]))
    
    def _ordenar_por_restriccion(self, pairs, board):
        """Ordena por nivel de restricción (más restrictivos primero)"""
        def restriccion_score(pair):
            start, end, _ = pair
            # Contar vecinos libres
            free = 0
            for pos in [start, end]:
                for n in board.get_neighbors(pos[0], pos[1]):
                    if board.grid[n[0]][n[1]] == Board.EMPTY:
                        free += 1
            # Penalizar esquinas y bordes
            corners = sum(1 for pos in [start, end]
                         if (pos[0] in [0, board.rows-1]) + (pos[1] in [0, board.cols-1]) >= 2)
            edges = sum(1 for pos in [start, end]
                       if pos[0] in [0, board.rows-1] or pos[1] in [0, board.cols-1])
            return -free + corners * 3 + edges
        
        return sorted(pairs, key=restriccion_score)
    
    def _resolver_recursivo(self, index, board, pairs, paths):
        """Función recursiva principal del backtracking"""
        # Verificar tiempo
        if time.time() - self.start_time > self.time_limit:
            return False
            
        self.nodes_explored += 1
        
        # Caso base: todos los pares conectados
        if index == len(pairs):
            # Verificar si se cumple la condición de victoria
            if self.require_all_cells:
                complete = board.is_complete()
                if complete:
                    self.solutions_found += 1
                self._debug_print(f"Todos los pares conectados. Completo: {complete}", index)
                return complete
            else:
                self.solutions_found += 1
                self._debug_print(f"Todos los pares conectados (sin requerir completitud)", index)
                return True
        
        start, end, number = pairs[index]
        
        # Debug para los primeros niveles
        if self.debug and (index < 3 or self.nodes_explored % 50 == 1):
            self._debug_print(f"Nodo {self.nodes_explored}: Conectando {number} de {start} a {end}", index)
        
        # Buscar todos los caminos posibles
        possible_paths = self._buscar_caminos(start, end, board, number)
        
        if not possible_paths:
            self._debug_print(f"No se encontraron caminos para {number}", index)
            return False
        
        self._debug_print(f"Encontrados {len(possible_paths)} caminos posibles para {number}", index)
        
        # Probar cada camino
        for path_idx, path in enumerate(possible_paths):
            # Marcar camino
            self._marcar_camino(path, board)
            paths.append(path)
            
            self._debug_print(f"Probando camino {path_idx + 1}/{len(possible_paths)}: {path}", index + 1)
            
            # Verificación básica de viabilidad solo para casos más complejos
            viable = True
            if len(pairs) > 3 and index < len(pairs) - 1:
                viable = self._es_estado_viable_basico(board, pairs[index + 1:])
                self._debug_print(f"Estado viable: {viable}", index + 1)
            
            if viable:
                # Continuar recursión
                if self._resolver_recursivo(index + 1, board, pairs, paths):
                    return True
            
            # Backtrack
            self._desmarcar_camino(path, board)
            paths.pop()
            self._debug_print(f"Backtracking del camino {path_idx + 1}", index + 1)
        
        return False
    
    def _buscar_caminos(self, start, end, board, number):
        """Busca todos los caminos posibles entre start y end"""
        if start == end:
            return [[start]]
        
        # Límites más generosos
        max_length = board.rows * board.cols  # Longitud máxima = todas las celdas
        max_paths = 20  # Más caminos para explorar
        
        # Para tableros pequeños, no limitar tanto
        if board.rows * board.cols <= 16:  # 4x4 o menor
            max_paths = 50
            
        paths = []
        
        def dfs(current, path, visited):
            if len(paths) >= max_paths:
                return
            
            if current == end:
                paths.append(path[:])
                return
            
            if len(path) > max_length:
                return
            
            # Explorar vecinos
            neighbors = board.get_neighbors(current[0], current[1])
            
            # Para tableros pequeños, no optimizar el orden de vecinos
            if board.rows * board.cols > 16:
                neighbors.sort(key=lambda n: abs(n[0] - end[0]) + abs(n[1] - end[1]))
            
            for neighbor in neighbors:
                if neighbor not in visited and board.is_valid_move(neighbor[0], neighbor[1], number):
                    new_path = path + [neighbor]
                    new_visited = visited | {neighbor}
                    dfs(neighbor, new_path, new_visited)
        
        # Iniciar búsqueda
        dfs(start, [start], {start})
        
        # Ordenar por longitud (más cortos primero)
        paths.sort(key=len)
        
        self._debug_print(f"Búsqueda de caminos para {number}: {len(paths)} caminos encontrados")
        
        return paths[:max_paths]
    
    def _es_estado_viable_basico(self, board, remaining_pairs):
        """Verificación básica de viabilidad (solo para casos complejos)"""
        # Verificar solo el siguiente par
        if not remaining_pairs:
            return True
            
        next_start, next_end, next_number = remaining_pairs[0]
        
        # Verificación simple: ¿hay al menos un camino directo posible?
        return self._hay_camino_simple(next_start, next_end, board, next_number)
    
    def _hay_camino_simple(self, start, end, board, number):
        """BFS simple para verificar conectividad básica"""
        if start == end:
            return True
        
        visited = {start}
        queue = [start]
        max_iterations = board.rows * board.cols  # Evitar bucles infinitos
        iterations = 0
        
        while queue and iterations < max_iterations:
            iterations += 1
            current = queue.pop(0)
            
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
        
        if self.debug:
            self._debug_print(f"Camino marcado: {path}")
            self._debug_print(f"Tablero después de marcar:\n{board}")
    
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