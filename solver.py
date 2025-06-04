from board import Board
import time
from collections import deque

class NumberLinkSolver:
    """Solucionador EXHAUSTIVO para NumberLink con instrumentación de heurísticas"""
    
    def __init__(self, time_limit=600, debug=False, require_all_cells=False):
        # Métricas generales
        self.solutions_found = 0
        self.nodes_explored = 0

        # Configuración
        self.time_limit = time_limit
        self.debug = debug
        self.require_all_cells = require_all_cells

        # Temporizador
        self.start_time = None

        # Instrumentación de heurísticas
        self.order_names = [
            "distancia",            # 0
            "borde",                # 1
            "flexibilidad",         # 2
            "distancia_inversa"     # 3
        ]
        self.order_used = None     # Índice de la heurística que resolvió

    # ------------------------------------------------------------------------- #
    # UTILIDADES DE DEBUG
    # ------------------------------------------------------------------------- #
    def _debug_print(self, message, level=0):
        if self.debug:
            indent = "  " * level
            print(f"{indent}{message}")

    # ------------------------------------------------------------------------- #
    # FUNCIÓN PRINCIPAL
    # ------------------------------------------------------------------------- #
    def resolver_tablero(self, board):
        """Intenta resolver el tablero probando varias órdenes heurísticas"""
        self.start_time = time.time()
        self.nodes_explored = 0
        self.solutions_found = 0
        self.order_used = None            # reset

        pairs = board.get_pairs()
        paths = []

        self._debug_print("=== BÚSQUEDA EXHAUSTIVA ===")
        self._debug_print(f"Tablero: {board.rows}x{board.cols}")
        self._debug_print(f"Pares: {len(pairs)}")
        self._debug_print(f"Tiempo límite: {self.time_limit}s")

        # Lista de funciones / listas de ordenación
        orderings = [
            self._order_by_distance,
            self._order_by_border_preference,
            self._order_by_flexibility,
            list(reversed(self._order_by_distance(pairs, board)))
        ]

        # Probar cada heurística hasta éxito o tiempo agotado
        for order_idx, ordering_func in enumerate(orderings):
            if time.time() - self.start_time > self.time_limit:
                break

            self._debug_print(f"\n--- Probando orden {order_idx + 1} ({self.order_names[order_idx]}) ---")

            sorted_pairs = (
                ordering_func(pairs, board) if callable(ordering_func) else ordering_func
            )

            self._debug_print("Orden de pares:")
            for i, (start, end, num) in enumerate(sorted_pairs):
                dist = abs(start[0] - end[0]) + abs(start[1] - end[1])
                self._debug_print(f"  {i+1}. Número {num}: {start} -> {end} (dist: {dist})")

            # Copia fresca del tablero
            working_board = board.copy()
            paths_copy = []

            if self._resolver_exhaustivo(0, working_board, sorted_pairs, paths_copy):
                self.order_used = order_idx          # << registro de heurística ganadora
                self._debug_print(f"\n¡SOLUCIÓN ENCONTRADA con orden {order_idx + 1} ({self.order_names[order_idx]})!")
                return True, paths_copy

        self._debug_print("\n=== NO SE ENCONTRÓ SOLUCIÓN ===")
        self._debug_print(f"Nodos explorados: {self.nodes_explored}")
        return False, []

    # ------------------------------------------------------------------------- #
    # HEURÍSTICAS DE ORDEN DE PARES
    # ------------------------------------------------------------------------- #
    def _order_by_distance(self, pairs, board):
        return sorted(pairs, key=lambda p: abs(p[0][0] - p[1][0]) + abs(p[0][1] - p[1][1]))

    def _order_by_border_preference(self, pairs, board):
        def score(pair):
            start, end, _ = pair
            dist = abs(start[0] - end[0]) + abs(start[1] - end[1])

            start_border = (
                start[0] in (0, board.rows - 1) or start[1] in (0, board.cols - 1)
            )
            end_border = (
                end[0] in (0, board.rows - 1) or end[1] in (0, board.cols - 1)
            )

            if start_border and end_border and dist > 5:
                return 1
            elif dist <= 3:
                return 3
            return 2
        return sorted(pairs, key=score)

    def _order_by_flexibility(self, pairs, board):
        def flex(pair):
            start, end, _ = pair
            start_deg = len(
                [n for n in board.get_neighbors(*start) if board.grid[n[0]][n[1]] == Board.EMPTY]
            )
            end_deg = len(
                [n for n in board.get_neighbors(*end) if board.grid[n[0]][n[1]] == Board.EMPTY]
            )
            return min(start_deg, end_deg)
        return sorted(pairs, key=flex)

    # ------------------------------------------------------------------------- #
    # BACKTRACKING EXHAUSTIVO
    # ------------------------------------------------------------------------- #
    def _resolver_exhaustivo(self, idx, board, pairs, paths):
        if time.time() - self.start_time > self.time_limit:
            self._debug_print("Tiempo límite alcanzado", idx)
            return False

        self.nodes_explored += 1
        if self.nodes_explored % 5000 == 0:
            self._debug_print(f"Progreso: {self.nodes_explored} nodos", idx)

        # Caso base
        if idx == len(pairs):
            if self.require_all_cells and not board.is_complete():
                return False
            return True

        start, end, number = pairs[idx]
        if self.debug and (idx < 2 or self.nodes_explored % 1000 == 1):
            self._debug_print(f"Nodo {self.nodes_explored}: Par {idx+1}/{len(pairs)} Nº{number}", idx)

        caminos = self._buscar_caminos_exhaustivo(start, end, board, number)
        if not caminos:
            return False

        for path in caminos:
            self._marcar_camino(path, board)
            paths.append(path)

            # Poda rápida de conectividad para 1-2 pares siguientes
            ok = True
            for nxt in pairs[idx+1:idx+3]:
                if not self._conectividad_basica(nxt[0], nxt[1], board, nxt[2]):
                    ok = False
                    break

            if ok and self._resolver_exhaustivo(idx + 1, board, pairs, paths):
                return True

            self._desmarcar_camino(path, board)
            paths.pop()

        return False

    # ------------------------------------------------------------------------- #
    # GENERACIÓN DE CAMINOS (BFS AMPLIO)
    # ------------------------------------------------------------------------- #
    def _buscar_caminos_exhaustivo(self, start, end, board, number):
        if start == end:
            return [[start]]

        max_paths = 200
        manhattan = abs(start[0] - end[0]) + abs(start[1] - end[1])
        max_len = manhattan * 8 + 15

        res = []
        queue = [(start, [start], {start})]

        while queue and len(res) < max_paths:
            cur, path, visited = queue.pop(0)
            if len(path) > max_len:
                continue
            if cur == end:
                res.append(path)
                continue
            for nbr in board.get_neighbors(*cur):
                if nbr not in visited and board.is_valid_move(nbr[0], nbr[1], number):
                    queue.append((nbr, path + [nbr], visited | {nbr}))

        res.sort(key=len)
        return res

    # ------------------------------------------------------------------------- #
    # PODA DE CONECTIVIDAD
    # ------------------------------------------------------------------------- #
    def _conectividad_basica(self, start, end, board, number):
        if start == end:
            return True

        visited = {start}
        q = deque([start])
        checks = 0
        max_checks = board.rows * board.cols * 3

        while q and checks < max_checks:
            cur = q.popleft()
            checks += 1
            for nbr in board.get_neighbors(*cur):
                if nbr == end:
                    return True
                if nbr not in visited and board.is_valid_move(nbr[0], nbr[1], number):
                    visited.add(nbr)
                    q.append(nbr)
        return False

    # ------------------------------------------------------------------------- #
    # UTILIDADES DE MARCADO / DESMARCADO
    # ------------------------------------------------------------------------- #
    def _marcar_camino(self, path, board):
        for r, c in path:
            if board.original_grid[r][c] == Board.EMPTY:
                board.mark_cell(r, c, Board.VISITED)

    def _desmarcar_camino(self, path, board):
        for r, c in path:
            if board.original_grid[r][c] == Board.EMPTY:
                board.unmark_cell(r, c)

    # ------------------------------------------------------------------------- #
    # ESTADÍSTICAS
    # ------------------------------------------------------------------------- #
    def get_statistics(self):
        elapsed = time.time() - self.start_time if self.start_time else 0
        return {
            "nodes_explored": self.nodes_explored,
            "solutions_found": self.solutions_found,
            "time_elapsed": elapsed,
            "order_used": self.order_used,
            "order_name": (
                None if self.order_used is None else self.order_names[self.order_used]
            )
        }