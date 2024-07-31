from tkinter import *
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
        self.menubar = Menu(self)

        self.menu_cascades = {}
        self.rows = {}
        self.frames = {}
        self.tkvars = {}
        self.buttons = {}
        self.entries = {}
        self.labels = {}

    def cascades_create(self, list_of_names: list[str]):
        '''Accepts a list of cascade names and adds them to the menubar.'''
        for name in list_of_names:
            cascade = Menu(self.menubar, tearoff=0)
            self.menubar.add_cascade(label=name, menu=cascade)
            self.menu_cascades[name] = cascade

    def menubar_add(self, cascade_name: str, list_of_labels_and_fns: list[list]):
        '''Creates a cascade of cascade_name and adds given labels and
        functions.

        Each element in list_of_labels_and_fns is a list consisting of a
        label for the menu option and the function it should run.

        Ex) self.menubar_add("Edit", [["Preferences", edit_prefs],
                                      ["Presets", edit_presets]])
        '''
        if cascade_name not in self.menu_cascades:
            self.cascades_create([cascade_name])
        for label, fn in list_of_labels_and_fns:
            self.menu_cascades[cascade_name].add_command(label=label,
                                                         command=fn)

    def frame_create(self, root, name: str):
        self.frames[name] = ttk.Frame(root)

    def tkvar_create(self, kind: str, name: str, initial: str = ""):
        kinds = {
                "string": StringVar
                }
        self.tkvars[name] = kinds[kind]()
        if initial:
            self.tkvars[name].set(initial)

    def tkvars_create(self, list_of_tkvars: list[list]):
        for tkvar in list_of_tkvars:
            kind, name, *initial = tkvar
            if initial:
                self.tkvar_create(kind, name, initial=initial)
            else:
                self.tkvar_create(kind, name)

    def label_create(self, root, name, text="", textvar=""):
        if text and textvar:
            # TODO: proper exception here
            print("A label cannot have both text and a textvariable.")
            return
        if text:
            self.labels[name] = ttk.Label(root, text=text)
        elif textvar:
            self.labels[name] = ttk.Label(root, textvariable=textvar)

    def button_create(self, root, name: str, text: str,
                      command: callable = None):
        self.buttons[name] = ttk.Button(root, text=text)
        if command:
            self.buttons[name].configure(command=command)

    def buttons_create(self, list_of_btn_lists: list[list]):
        for btn_list in list_of_btn_lists:
            root, name, text, *command = btn_list
            if command:
                self.button_create(root, name, text, command=command[0])
            else:
                self.button_create(root, name, text)

    def entry_create(self, root, name: str, label: str = ""):
        self.entries[name] = ttk.Entry(root)
        if label:
            self.label_create(root, name, text=label)

    def entries_create(self, list_of_entry_lists: list[list]):
        for entry_list in list_of_entry_lists:
            root, name, *label = entry_list
            if label:
                self.entry_create(root, name, label=label[0])
            else:
                self.entry_create(root, name)

    def grid_group(self, list_of_rows: list[list]):
        for i, widget_list in enumerate(list_of_rows):
            col_span = 1
            last_widget = None
            for j, widget in enumerate(widget_list):
                if widget == SKIP:
                    continue
                elif widget == RSPAN:
                    col_span += 1
                    if widget == widget_list[-1]:
                        last_widget.grid(columnspan=col_span)
                    continue
                else:
                    if col_span > 1:
                        last_widget.grid(columnspan=col_span)
                    widget.grid(row=i, column=j)
                last_widget = widget


if __name__ == "__main__":
    gui = Tkzenter("Test Gui")
    gui.menubar_add("Edit", [
        ["Preferences", lambda: print("editing...")]
        ])
    gui.label_create(gui, 'test', text="Testing")
    gui.button_create(gui, 'button', text="Hi", command=lambda: print("heyo"))
    gui.buttons_create([
        [gui, 'btn1', 'hi', lambda: print("hello")],
        [gui, 'btn2', 'bye', lambda: print("goodbye")],
        [gui, 'btn3', 'hi again', lambda: print("hi again")],
        ])
    gui.entry_create(gui, 'entry1', label="yo")
    gui.entries_create([
        [gui, 'entry2', "this is entry 2"],
        [gui, 'entry3', "this is entry 3"],
        ])
    l, b, e = gui.labels, gui.buttons, gui.entries
    gui.grid_group([[l["test"], b['button']],
                    [l["entry1"], e["entry1"]],
                    [b["btn1"], b["btn2"], b["btn3"]],
                    [e["entry2"], e["entry3"]],
                    [l["entry2"], l["entry3"]],
                    ])
    gui.mainloop()
