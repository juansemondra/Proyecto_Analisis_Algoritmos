import tkinter as tk
from ui import NumberLinkUI

def main():
    root = tk.Tk()
    app = NumberLinkUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()