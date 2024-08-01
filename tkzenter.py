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

    def stay_on_top(self, boolean: bool = True):
        self.attributes("-topmost", boolean)

    def pad_row(self, row: int, direction: str, qty: int):
        if direction not in 'xy':
            # TODO: proper exception here
            print("Invalid direction. Options are 'x', 'y', or 'xy'.")
            return
        for elm in self.grid_slaves(row=row):
            if 'x' in direction:
                elm.grid(padx=qty)
            if 'y' in direction:
                elm.grid(pady=qty)

    def pad_buttons(self, list_of_buttons_and_padstrings: list[list]):
        for button, padstring in list_of_buttons_and_padstrings:
            button.configure(padding=padstring)

    def make_sticky(self, direction: str, widgets: list):
        for letter in direction:
            if letter not in 'nsew':
                # TODO proper exception here
                print(f"Invalid letter: {letter}")
                return
        for w in widgets:
            w.grid(sticky=direction)

    def dialog(self, kind: str, msg: str = "", title: str = "") -> str | bool | None:
        if not title:
            title = self.app_title
        m = messagebox
        mboxes = {
                'info': m.showinfo,
                'alert': m.showwarning,
                'error': m.showerror,
                'askyesno': m.askyesno,
                'askyesnocancel': m.askyesnocancel,
                'askokcancel': m.askokcancel,
                'askretrycancel': m.askretrycancel
                }
        d = simpledialog
        dlgs = {
                'askstring': d.askstring,
                'askinteger': d.askinteger,
                'askfloat': d.askfloat
                }
        f = filedialog
        f_dlgs = {
                'askopenfilename': f.askopenfilename,
                'askdirectory': f.askdirectory
                }
        if kind in mboxes:
            result = mboxes[kind](title=title, message=msg)
        elif kind in dlgs:
            result = dlgs[kind](title=title, prompt=msg)
        elif kind in f_dlgs:
            result = f_dlgs[kind]()
        else:
            # TODO proper exception here
            print("Invalid dialog option.")
            return
        return result


if __name__ == "__main__":
    gui = Tkzenter("Test Gui")
    gui.menubar_add("Edit", [
        ["Preferences", lambda: print("editing...")]
        ])
    gui.label_create(gui, 'test', text="Testing")
    gui.button_create(gui, 'button', text="Hi", command=lambda: print("heyo"))
    gui.buttons_create([
        [gui, 'btn1', 'hi', lambda: gui.dialog("alert", "Testing the alert!")],
        [gui, 'btn2', 'bye', lambda: print(gui.dialog("askopenfilename"))],
        [gui, 'btn3', 'hi again', lambda: print("hi again")],
        ])
    gui.entry_create(gui, 'entry1', label="yo")
    gui.entries_create([
        [gui, 'entry2', "this is entry 2"],
        [gui, 'entry3', "this is entry 3"],
        ])
    l, b, e = gui.labels, gui.buttons, gui.entries
    gui.pad_buttons([
        [b["btn1"], '20 10 1 10'],
        [b["btn2"], '1 10 1 10'],
        [b["btn3"], '1 10 1 10'],
        ])
    gui.grid_group([[l["test"], b['button']],
                    [l["entry1"], e["entry1"]],
                    [b["btn1"], b["btn2"], b["btn3"]],
                    [e["entry2"], e["entry3"], RSPAN],
                    [l["entry2"], l["entry3"]],
                    ])
    gui.make_sticky('e', [l["entry2"], l["entry3"]])
    gui.pad_row(1, 'y', 30)
    gui.pad_row(3, 'y', 30)
    gui.stay_on_top()
    gui.mainloop()
