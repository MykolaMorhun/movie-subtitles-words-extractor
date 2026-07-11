import tkinter as tk

from app.models.main_window_model import MainWindowModel
from app.views.main_window_view import MainWindowView
from app.controllers.main_window_controller import MainWindowController

def main():
    root = tk.Tk()

    model = MainWindowModel()
    view = MainWindowView(root)
    controller = MainWindowController(model, view)

    try:
        root.mainloop()
    except KeyboardInterrupt:
        root.destroy()


if __name__ == "__main__":
    main()
