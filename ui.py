import tkinter as tk
from tkinter import filedialog
from loader import load_board_from_file

CELL_SIZE = 60

class NumberLinkUI:
    def __init__(self, root):
        self.root = root
        self.root.title("NumberLink - Entrega 1")
        self.canvas = tk.Canvas(root, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.board_data = []
        self.number_positions = {}
        self.rows = self.cols = 0

        self.path = []
        self.drawing_number = None
        self.completed_paths = {}  # número: ruta [(r, c), ...]

        self.canvas.bind("<Button-1>", self.on_click_start)
        self.canvas.bind("<B1-Motion>", self.on_mouse_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_mouse_release)

        self.root.bind("<Configure>", self.redraw)
        self.load_board()

    def load_board(self):
        path = filedialog.askopenfilename(title="Selecciona archivo del tablero")
        if not path:
            return
        self.board_data, self.number_positions = load_board_from_file(path)
        self.rows = len(self.board_data)
        self.cols = len(self.board_data[0])
        self.draw_board()

    def draw_board(self):
        self.canvas.delete("all")
        for r in range(self.rows):
            for c in range(self.cols):
                x1 = c * CELL_SIZE
                y1 = r * CELL_SIZE
                x2 = x1 + CELL_SIZE
                y2 = y1 + CELL_SIZE
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black")

                value = self.board_data[r][c]
                if value != 0:
                    self.canvas.create_text(
                        x1 + CELL_SIZE / 2,
                        y1 + CELL_SIZE / 2,
                        text=str(value),
                        font=("Arial", 20),
                        fill="blue"
                    )

        # Dibuja caminos completos
        for number, path in self.completed_paths.items():
            self.draw_path(path, number)

    def redraw(self, event):
        self.canvas.config(width=self.cols * CELL_SIZE, height=self.rows * CELL_SIZE)
        self.draw_board()
        if self.path:
            self.draw_path(self.path, self.drawing_number)

    def get_cell_from_xy(self, x, y):
        col = x // CELL_SIZE
        row = y // CELL_SIZE
        if 0 <= row < self.rows and 0 <= col < self.cols:
            return row, col
        return None

    def are_adjacent(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1]) == 1

    def on_click_start(self, event):
        cell = self.get_cell_from_xy(event.x, event.y)
        if not cell:
            return
        r, c = cell
        number = self.board_data[r][c]
        if number != 0:
            # ¿Ya tiene una ruta guardada?
            if number in self.completed_paths:
                del self.completed_paths[number]
                print(f"Ruta eliminada para número {number}")
                self.draw_board()
            else:
                self.path = [cell]
                self.drawing_number = number

    def on_mouse_drag(self, event):
        if self.drawing_number is None:
            return

        cell = self.get_cell_from_xy(event.x, event.y)
        if not cell or cell in self.path:
            return

        last = self.path[-1]
        if self.are_adjacent(last, cell):
            r, c = cell
            # Solo pasar por celdas vacías o la meta con el mismo número
            if self.board_data[r][c] == 0 or self.board_data[r][c] == self.drawing_number:
                self.path.append(cell)
                self.draw_board()
                self.draw_path(self.path, self.drawing_number)

    def on_mouse_release(self, event):
        if not self.path:
            return

        end_cell = self.path[-1]
        r, c = end_cell
        if self.board_data[r][c] == self.drawing_number and end_cell != self.path[0]:
            print(f"Ruta completa para número {self.drawing_number}: {self.path}")
            self.completed_paths[self.drawing_number] = self.path.copy()
        else:
            print("Ruta inválida, se descarta")

        self.path = []
        self.drawing_number = None
        self.draw_board()

    def draw_path(self, path, number):
        for i in range(len(path) - 1):
            r1, c1 = path[i]
            r2, c2 = path[i + 1]
            x1 = c1 * CELL_SIZE + CELL_SIZE // 2
            y1 = r1 * CELL_SIZE + CELL_SIZE // 2
            x2 = c2 * CELL_SIZE + CELL_SIZE // 2
            y2 = r2 * CELL_SIZE + CELL_SIZE // 2
            self.canvas.create_line(x1, y1, x2, y2, width=6, fill="red", capstyle=tk.ROUND)