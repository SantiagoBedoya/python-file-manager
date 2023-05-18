from explorer import Explorer
from tkinter import Tk, Listbox, Scrollbar, END, Button, Entry


class App:
    def __init__(self) -> None:
        self._master_path = './test'
        self._selected = ''
        self._exp = Explorer(self._master_path)
        self._nodes = []
        self._t = Tk()

        self._list_box = None
        
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
        self._exp.delete(self._selected)
        new_nodes = self._exp._list(self._exp.history[-1])
        self._nodes = sorted(new_nodes, key=lambda x: x.name, reverse=True)
        self._clean_list_box()
        self._render_items()

    def _create_entries(self):
        # search entry
        search_entry = Entry(self._t, width=40)
        search_entry.grid(row=0, column=100)

    def _create_buttons(self):
        prev_btn = Button(self._t, text="<-", width=2,
                          height=1, command=self._prev)
        prev_btn.grid(row=0, column=0)

        search_btn = Button(self._t, text="Search", width=4, height=1)
        search_btn.grid(row=0, column=101)

        delete_btn = Button(self._t, text="Delete", width=4,
                            height=1, command=self._delete_file)
        delete_btn.grid(row=4, columnspan=150)

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
        data = event.widget.get(selection[0])
        data = data.replace("> ", "")
        data = data.replace("- ", "")
        self._selected = data

    def _set_listeners(self):

        # on double click
        self._list_box.bind("<Double-1>", self._open_folder)

        # on select item
        self._list_box.bind("<<ListboxSelect>>", self._select_item)

    def render(self):
        self._t.geometry('500x520')
        self._t.title('File Manager')

        self._create_buttons()
        self._create_entries()
        self._create_list_box()
        self._set_listeners()
        self._render_items()

        self._t.mainloop()


app = App()
app.render()
