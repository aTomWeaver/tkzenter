from tkinter import Tk
from tkinter import ttk
from tkinter import StringVar
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import filedialog

SKIP = "skip"
RSPAN = "rspan"

class Tkzenter(Tk):
    def __init__(self, app_title: str = "Tkzenter"):
        super().__init__()
        self.app_title = app_title
        self.title(app_title)
