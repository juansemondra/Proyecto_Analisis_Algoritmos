import tkinter as tk
from tkinter import filedialog, messagebox
from loader import load_board_from_file

CELL_SIZE = 60

class NumberLinkUI:
    def __init__(self, root):
        self.root = root # Asignar root primero
        self.root.title("NumberLink - Entrega 1")
        self.canvas = tk.Canvas(root, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # Variables del estado del tablero
        self.board_data = []
        self.number_positions = {}
        self.rows = self.cols = 0

        # Variables del estado del dibujo actual
        self.path = []
        self.drawing_number = None
        self.completed_paths = {}  # {numero: [(r, c), ...]}

        # Vinculación de eventos del ratón al canvas
        self.canvas.bind("<Button-1>", self.on_click_start)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_release)

        # Vinculación del evento de redimensionar la ventana
        self.root.bind("<Configure>", self.redraw)

        # Cargar el tablero inicial
        self.load_board()

    def load_board(self):
        path = filedialog.askopenfilename(title="Selecciona archivo del tablero")
        if not path:
            self.root.destroy() # Salir si no se selecciona archivo
            return
        try:
            self.board_data, self.number_positions = load_board_from_file(path)
            self.rows = len(self.board_data)
            self.cols = len(self.board_data[0])
            self.completed_paths = {} # Reiniciar caminos al cargar nuevo tablero
            self.path = [] # Reiniciar camino en progreso
            self.drawing_number = None # Reiniciar número en dibujo
            self.draw_board()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo cargar el archivo del tablero:\n{e}")
            self.root.destroy()


    def draw_board(self):
        self.canvas.delete("all")
        # Ajustar tamaño canvas si es necesario (puede ser redundante con redraw, pero asegura estado inicial)
        self.canvas.config(width=self.cols * CELL_SIZE, height=self.rows * CELL_SIZE)

        for r in range(self.rows):
            for c in range(self.cols):
                x1 = c * CELL_SIZE
                y1 = r * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black")

                value = self.board_data[r][c]
                if value != 0:
                    # Determinar si es un punto de inicio/fin
                    is_endpoint = False
                    if value in self.number_positions:
                        if (r,c) in self.number_positions[value]:
                            is_endpoint = True

                    fill_color = "blue" # Color por defecto para números
                    # Podríamos añadir lógica para colorear diferente si es endpoint, si se desea

                    self.canvas.create_text(
                        x1 + CELL_SIZE / 2,
                        y1 + CELL_SIZE / 2,
                        text=str(value),
                        font=("Arial", 20, "bold" if is_endpoint else "normal"),
                        fill=fill_color
                    )

        # Dibuja caminos completos guardados
        for number, path_coords in self.completed_paths.items():
            self.draw_path(path_coords, number) # Usar el número para posible color futuro

    def redraw(self, event=None): # Añadir event=None para poder llamarlo sin evento
        # Event puede ser None si se llama desde draw_board o load_board
        if not self.board_data: # No hacer nada si no hay tablero cargado
             return
        # Ajustar tamaño del canvas al contenedor (ventana) si es necesario
        # O simplemente usar las dimensiones fijas calculadas
        new_width = self.cols * CELL_SIZE
        new_height = self.rows * CELL_SIZE
        self.canvas.config(width=new_width, height=new_height)
        # Volver a dibujar todo
        self.draw_board()
        # Redibujar el camino en progreso si existe
        if self.path:
            self.draw_path(self.path, self.drawing_number)

    def get_cell_from_xy(self, x, y):
        col = x // CELL_SIZE
        row = y // CELL_SIZE
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return row, col
        return None

    def are_adjacent(self, a, b):
        # Verifica si dos celdas (tuplas (r,c)) son adyacentes horizontal o verticalmente
        return abs(a[0] - b[0]) + abs(a[1] - b[1]) == 1

    def on_click_start(self, event):
        cell = self.get_cell_from_xy(event.x, event.y)
        if not cell:
            return
        r, c = cell
        number = self.board_data[r][c]

        # Si se hace clic en un número
        if number != 0:
            # Si ya existe un camino para este número, borrarlo para redibujar
            if number in self.completed_paths:
                del self.completed_paths[number]
                print(f"Ruta eliminada para número {number}. Puedes volver a dibujarla.")
                self.draw_board() # Actualizar tablero visualmente
            # Solo iniciar un nuevo camino si no se está dibujando otro
            elif self.drawing_number is None:
                 # Asegurarse que es uno de los puntos de inicio/fin originales
                 if number in self.number_positions and cell in self.number_positions[number]:
                    self.path = [cell]
                    self.drawing_number = number
                    print(f"Iniciando dibujo para número {number} desde {cell}")
                 else:
                     print(f"La celda {cell} con número {number} no es un punto de inicio/fin válido.")
            else:
                print(f"Ya estás dibujando el camino para el número {self.drawing_number}.")
        # Si se hace clic en una celda vacía, no hacer nada
        else:
             print("Clic en celda vacía.")


    def on_mouse_drag(self, event):
        # Solo actuar si se está en modo dibujo (se ha hecho clic en un número válido)
        if self.drawing_number is None:
            return

        cell = self.get_cell_from_xy(event.x, event.y)
        # Ignorar si el cursor está fuera del tablero o sobre la misma celda
        if not cell or cell == self.path[-1]:
            return

        last_cell = self.path[-1]
        # Permitir movimiento solo a celdas adyacentes
        if self.are_adjacent(last_cell, cell):
            r, c = cell
            current_val_in_cell = self.board_data[r][c]

            # Condiciones para añadir la celda al camino:
            # 1. La celda está vacía (0).
            # 2. La celda contiene el número final del par que estamos dibujando
            #    Y esta celda es una de las posiciones originales de ese número
            #    Y no es la celda inicial del camino actual.
            is_target_endpoint = (current_val_in_cell == self.drawing_number and
                                  cell in self.number_positions.get(self.drawing_number, []) and
                                  cell != self.path[0])

            # No permitir pasar sobre un número que no sea el destino
            if current_val_in_cell != 0 and not is_target_endpoint:
                print(f"No se puede pasar sobre el número {current_val_in_cell} en {cell}")
                return

            # Evitar añadir la misma celda dos veces seguidas (aunque get_cell_from_xy ya lo previene un poco)
            if cell not in self.path:
                 # Verificar si esta celda ya pertenece a otro camino completado
                 is_occupied_by_other_path = False
                 for num, completed_path in self.completed_paths.items():
                     if cell in completed_path:
                         is_occupied_by_other_path = True
                         print(f"La celda {cell} ya está ocupada por el camino del número {num}")
                         break

                 if not is_occupied_by_other_path:
                    self.path.append(cell)
                    # Redibujar el tablero base y encima el camino en progreso
                    self.draw_board()
                    self.draw_path(self.path, self.drawing_number)
            # Permitir volver atrás borrando el último segmento si se arrastra a la penúltima celda
            elif len(self.path) > 1 and cell == self.path[-2]:
                 self.path.pop()
                 self.draw_board()
                 self.draw_path(self.path, self.drawing_number)


    def on_mouse_release(self, event):
        # Solo finalizar si estábamos dibujando
        if not self.path or self.drawing_number is None:
            self.path = [] # Asegurar que el camino se limpia si fue inválido desde el inicio
            self.drawing_number = None
            return

        end_cell = self.path[-1]
        r, c = end_cell
        start_cell = self.path[0]

        # Condición de éxito: La última celda contiene el número que estábamos dibujando,
        # es una de las posiciones originales de ese número, y no es la misma que la celda inicial.
        is_valid_endpoint = (self.board_data[r][c] == self.drawing_number and
                             end_cell in self.number_positions.get(self.drawing_number, []) and
                             end_cell != start_cell)

        if is_valid_endpoint:
            # Verificar que el otro extremo del par original no esté en medio de este camino
            other_endpoint = None
            endpoints = self.number_positions.get(self.drawing_number, [])
            if len(endpoints) == 2:
                 other_endpoint = endpoints[0] if endpoints[1] == start_cell else endpoints[1]

            path_valid = True
            if other_endpoint and other_endpoint in self.path[1:-1]:
                 print(f"Ruta inválida: El otro extremo {other_endpoint} está en medio del camino.")
                 path_valid = False

            if path_valid:
                print(f"Ruta completa para número {self.drawing_number}: {self.path}")
                self.completed_paths[self.drawing_number] = self.path.copy()
                # Chequear condición de victoria solo si el camino fue válido
                if self.check_win_condition():
                    self.draw_board() # Redibujar para mostrar el último camino
                    messagebox.showinfo("¡Felicidades!", "¡Has completado el tablero!")
                    # Opcional: deshabilitar más interacciones o cerrar
                    # self.canvas.unbind("<Button-1>")
                    # self.canvas.unbind("<B1-Motion>")
                    # self.canvas.unbind("<ButtonRelease-1>")
            else:
                 print("Ruta inválida, se descarta.")
        else:
            print(f"Ruta inválida: Finalizó en {end_cell} (valor={self.board_data[r][c]}) que no es el par correcto para {self.drawing_number} iniciado en {start_cell}.")

        # Resetear estado de dibujo independientemente de si fue válido o no
        self.path = []
        self.drawing_number = None
        # Redibujar siempre al final para limpiar camino temporal si fue inválido
        # o mostrar el estado actualizado con el camino guardado.
        self.draw_board()

    def draw_path(self, path_coords, number):
        # Podríamos tener un mapa de colores si quisiéramos diferenciar números
        # colors = {1: "red", 2: "green", 3: "blue", 4: "orange", ...}
        # color = colors.get(number, "grey") # Usar gris por defecto
        color = "red" # Por ahora, todos rojos

        if len(path_coords) < 2: return # No se puede dibujar línea con menos de 2 puntos

        for i in range(len(path_coords) - 1):
            r1, c1 = path_coords[i]
            r2, c2 = path_coords[i+1]

            # Calcular coordenadas centrales de las celdas
            x1 = c1 * CELL_SIZE + CELL_SIZE / 2
            y1 = r1 * CELL_SIZE + CELL_SIZE / 2
            x2 = c2 * CELL_SIZE + CELL_SIZE / 2
            y2 = r2 * CELL_SIZE + CELL_SIZE / 2

            # Dibujar línea
            self.canvas.create_line(x1, y1, x2, y2, width=8, fill=color, capstyle=tk.ROUND, smooth=tk.TRUE)

        # Opcional: dibujar círculos en los extremos para mejor visualización
        for r, c in [path_coords[0], path_coords[-1]]:
             if self.board_data[r][c] != 0: # Solo dibujar si es un número (no vacío)
                 x_center = c * CELL_SIZE + CELL_SIZE / 2
                 y_center = r * CELL_SIZE + CELL_SIZE / 2
                 radius = CELL_SIZE / 4
                 self.canvas.create_oval(x_center - radius, y_center - radius,
                                         x_center + radius, y_center + radius,
                                         fill=color, outline="")


    def check_win_condition(self):
        # 1. Verificar si todos los pares de números definidos originalmente tienen un camino completo
        if len(self.completed_paths) != len(self.number_positions):
            #print(f"Win check fail: Caminos completados ({len(self.completed_paths)}) != Pares de números ({len(self.number_positions)})")
            return False

        # 2. Verificar si todas las celdas del tablero están cubiertas por algún camino
        covered_cells = set()
        for path in self.completed_paths.values():
            for cell in path:
                covered_cells.add(cell)

        total_cells = self.rows * self.cols
        if len(covered_cells) != total_cells:
            #print(f"Win check fail: Celdas cubiertas ({len(covered_cells)}) != Celdas totales ({total_cells})")
            # Verifiquemos si alguna celda *no numérica* quedó sin cubrir
            for r in range(self.rows):
                for c in range(self.cols):
                     # No necesitamos chequear las celdas con números iniciales, esas deben estar cubiertas por definición
                     # if self.board_data[r][c] == 0 and (r, c) not in covered_cells:
                     if (r, c) not in covered_cells: # Más simple: si alguna celda no está cubierta, falló.
                         #print(f"Win check fail: Celda no cubierta: {(r, c)}")
                         return False
            # Si llegamos aquí, significa que len(covered_cells) != total_cells, pero no encontramos celdas sin cubrir,
            # lo cual indica una posible inconsistencia lógica. Mejor retornar False.
            return False

        print("¡Condición de victoria cumplida!")
        return True

# Esto permite ejecutar ui.py directamente para pruebas rápidas, aunque no es necesario para la ejecución normal.
# if __name__ == '__main__':
#     root = tk.Tk()
#     app = NumberLinkUI(root)
#     root.mainloop()