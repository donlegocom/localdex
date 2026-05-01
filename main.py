import tkinter as tk
from app.window import LocalDexWindow

if __name__ == "__main__":
    root = tk.Tk()
    app = LocalDexWindow(root)
    root.mainloop()