from explorer import Explorer
from tkinter import Tk, Listbox, Scrollbar, END, Button, Entry, StringVar, Toplevel, Label, messagebox


class App:
    def __init__(self) -> None:
        self._master_path = './test'
        self._selected = ''
        self._exp = Explorer(self._master_path)
        self._nodes = []
        self._t = Tk()

        self._list_box = None
        self._rename_entry = None
        self._search_entry_text_variable = None
        self._search_entry = None
        self._create_entry = None
        self._create_win = None

        self._copy_path = ''

        self._get_nodes(None)

    def _get_nodes(self, path):
        uri = None
        if path is not None:
            uri = path
        self._nodes = sorted(
            self._exp.list(uri),
            key=lambda x: x.name,
            reverse=True
        )

    def _create_list_box(self):
        self._list_box = Listbox(
            self._t,
            font=('Times', 18),
            bd=0,
            width=55,
            height=20,
            fg='#464646',
            highlightthickness=0,
            selectbackground='#a6a6a6',
            activestyle="none",
        )
        self._list_box.grid(row=3, columnspan=120, pady=10)
        list_box_scrollbar = Scrollbar(self._t)
        self._list_box.config(yscrollcommand=list_box_scrollbar.set)
        list_box_scrollbar.config(command=self._list_box.yview)

    def _prev(self):
        if len(self._exp.history) >= 2:
            new_path = self._exp.history[-2]
            new_nodes = self._exp.list(new_path, True)
            new_nodes = sorted(new_nodes, key=lambda x: x.name, reverse=True)
            self._clean_list_box()
            self._nodes = new_nodes
            self._render_items()

    def _clean_list_box(self):
        self._list_box.delete(0, END)

    def _delete_file(self):
        if len(self._selected) == 0:
            return
        self._exp.delete(self._selected)
        self._rename_entry.delete(0, END)
        self._selected = ""
        new_nodes = self._exp._list(self._exp.history[-1])
        self._nodes = sorted(new_nodes, key=lambda x: x.name, reverse=True)
        self._clean_list_box()
        self._render_items()

    def _create_entries(self):
        # search entry
        search_entry_text_variable = StringVar()
        self._search_entry_text_variable = search_entry_text_variable
        search_entry = Entry(
            self._t, textvariable=search_entry_text_variable, width=30)
        search_entry.grid(row=0, column=10)
        self._search_entry = search_entry

        # rename entry
        rename_entry = Entry(self._t, width=30)
        rename_entry.grid(row=4, columnspan=150)
        self._rename_entry = rename_entry

    def _create_buttons(self):
        prev_btn = Button(self._t, text="<-", width=2,
                          height=1, command=self._prev)
        prev_btn.grid(row=0, column=0)

        new_btn = Button(self._t, text="New", width=10, height=1, command=self._new)
        new_btn.grid(row=0, column=20)

        rename_btn = Button(self._t, text="Rename", width=4,
                            height=1, command=self._rename_file)
        rename_btn.grid(row=4)

        delete_btn = Button(self._t, text="Delete", width=4,
                            height=1, command=self._delete_file)
        delete_btn.grid(row=4, column=20)


    def _new(self):
        self._create_win = Toplevel(self._t)
        
        # create name input in new window
        label = Label(self._create_win, text="Filename\nIf you want to create a folder add / before name")
        label.grid(row=0)

        name_entry = Entry(self._create_win, width=30)
        name_entry.grid(row=1)
        self._create_entry = name_entry

        new_btn = Button(self._create_win, text="Create", width=4,
                            height=1, command=self._create_file)
        new_btn.grid(row=2)

    def _create_file(self):
        try:
            self._exp.create(self._create_entry.get())
        except FileExistsError:
            messagebox.showerror(message="A file or folder already exist in this location", title="File already exists")
        except:
            messagebox.showerror(message="Something went wrong", title="Unexpected error")
        self._create_win.destroy()
        new_nodes = self._exp._list(self._exp.history[-1])
        self._nodes = sorted(new_nodes, key=lambda x: x.name, reverse=True)
        self._clean_list_box()
        self._render_items()

    def _rename_file(self):
        new_name = self._rename_entry.get()

        if len(new_name) == 0:
            return

        self._exp.rename(self._selected, new_name)
        self._rename_entry.delete(0, END)
        new_nodes = self._exp._list(self._exp.history[-1])
        self._nodes = sorted(new_nodes, key=lambda x: x.name, reverse=True)
        self._clean_list_box()
        self._render_items()

    # *args were given by StringVar().trace
    def _filter(self,*args):
        self.filter(self._exp.history[-1],self._search_entry_text_variable.get()) 

    def filter(self,path,name):
        if not name:
            self._nodes =sorted(self._exp._list(self._exp.history[-1]), key=lambda x: x.name, reverse=True)
            self._clean_list_box()
            self._render_items()
        else:
            self._nodes=self._exp.search(path,name)
            if len(self._nodes) > 0:
                self._clean_list_box()
                self._render_items()


    def _render_items(self):
        for node in self._nodes:
            if node.is_file:
                self._list_box.insert(END, f"- {node.name}")
            else:
                self._list_box.insert(END, f"> {node.name}")

    def _open_folder(self, event):
        selection = event.widget.curselection()
        data = event.widget.get(selection[0])
        data = data.replace("> ", "")
        data = data.replace("- ", "")
        if self._exp.is_folder(data):
            new_nodes = self._exp.list(data)
            self._clean_list_box()
            self._nodes = new_nodes
            self._render_items()

    def _select_item(self, event):
        selection = event.widget.curselection()
        if len(selection) == 0:
            return
        data = event.widget.get(selection[0])

        data = data.removeprefix("> ")
        data = data.removeprefix("- ")
        self._selected = data

        # clean entry
        self._rename_entry.delete(0, END)
        # set value to entry
        self._rename_entry.insert(0, self._selected)

    def _set_listeners(self):

        # on double click
        self._list_box.bind("<Double-1>", self._open_folder)

        # on select item
        self._list_box.bind("<<ListboxSelect>>", self._select_item)

        # search variable trace
        self._search_entry_text_variable.trace("w", self._filter)

        # on ctrl/command + c
        self._t.bind_all("<Control-c>", self._copy)
        self._t.bind_all("<Command-c>", self._copy)

        # on ctrl/command + x
        self._t.bind_all("<Control-x>", self._cut)
        self._t.bind_all("<Command-x>", self._cut)

        # on ctrl/command + v
        self._t.bind_all("<Control-v>", self._paste)
        self._t.bind_all("<Command-v>", self._paste)

    def _cut(self, event):
        self._cut_path = f"{self._exp.history[-1]}/{self._selected}"
        pass

    def _copy(self, event):
        self._copy_path = f"{self._exp.history[-1]}/{self._selected}"

    def _paste(self, event):
        paste_path = self._exp.history[-1]

        if len(self._cut_path) > 0:
            self._exp.copy(self._cut_path, paste_path, True)
        else:
            self._exp.copy(self._copy_path, paste_path)
            
        self._rename_entry.delete(0, END)
        new_nodes = self._exp._list(self._exp.history[-1])
        self._nodes = sorted(new_nodes, key=lambda x: x.name, reverse=True)
        self._clean_list_box()
        self._render_items()
        pass

    def render(self):
        self._t.geometry('500x530')
        self._t.title('File Manager')

        self._create_buttons()
        self._create_entries()
        self._create_list_box()
        self._set_listeners()
        self._render_items()

        self._t.mainloop()


app = App()
app.render()
