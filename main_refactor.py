from explorer import Explorer
from tkinter import (
    Tk,
    Listbox,
    Scrollbar,
    END,
    Button,
    Entry,
    StringVar,
    Toplevel,
    Label,
    messagebox,
    PhotoImage,
)


class App:
    """Explorador de Archivos

    Esta clase contiene todos las funcionalidades y elementos que se utilizan para la simulación del
    explorador de archivos, basandose en un arbol binario el cual maeja la estructura con nodos y tambien
    se utiliza la clase Explorer que contiene los métodos de nuestro árbol.
    """

    def __init__(self) -> None:
        self._master_path = "./test"
        self._selected = ""
        self._exp = Explorer(self._master_path)
        self._nodes = []
        self._t = Tk()
        self.create_btn = PhotoImage(file="./assets/create.png").subsample(20, 20)
        self.rename_btn = PhotoImage(file="./assets/rename.png").subsample(20, 20)
        self.back_btn = PhotoImage(file="./assets/back.png").subsample(46, 46)
        self.delete_btn = PhotoImage(file="./assets/delete.png").subsample(20, 20)
        self._list_box = None
        self._rename_entry = None
        self._search_entry_text_variable = None
        self._search_entry = None
        self._create_entry = None
        self._create_win = None
        self._copy_path = ""
        self._cut_path = ""
        self._get_nodes(None)

    def _get_nodes(self, path):
        """Obtener archivos y carpetas.

        Este método obtiene los archivos y carpetas que hay en una ruta.

        Args:
            path (str): Ruta en la que se van a buscar los archivos y carpetas.
        """
        uri = None
        if path is not None:
            uri = path
        self._nodes = sorted(self._exp.list(uri), key=lambda x: x.name, reverse=True)

    def _create_list_box(self):
        """Crear contenedor de los archivos y carpetas.

        Este método inicializa el contenedor en el que se visualizan los archivos y carpetas
        y poder realizar las operaciones, de crear, eliminar y renombrarlas.
        """
        self._list_box = Listbox(
            self._t,
            font=("Times", 18),
            bd=0,
            fg="#464646",
            highlightthickness=0,
            selectbackground="#a6a6a6",
            activestyle="none",
        )
        self._list_box.place(y=40, relwidth=1, relheight=0.84)
        list_box_scrollbar = Scrollbar(self._t)
        self._list_box.config(yscrollcommand=list_box_scrollbar.set)
        list_box_scrollbar.config(command=self._list_box.yview)

    def _prev(self):
        """Navegar a la carpeta anterior.

        Este método cumple con la funcionalidad para navegar a la carpeta anterior,
        si no hay una carpeta anterior solo permanece en la que se encuentra actualmente.
        """
        if len(self._exp.history) >= 2:
            new_path = self._exp.history[-2]
            new_nodes = self._exp.list(new_path, True)
            new_nodes = sorted(new_nodes, key=lambda x: x.name, reverse=True)
            self._clean_list_box()
            self._nodes = new_nodes
            self._render_items()

    def _clean_list_box(self):
        """Limpiar carpeta

        Este método elimina todo el contenido de una carpeta dejandola totalmente vacía.
        """
        self._list_box.delete(0, END)

    def _delete_file(self):
        """Eliminar archivo.

        Este método elimina un archivo que este seleccionado, si no hay un
        archivo seleccionado no hace nada.
        """
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
        """Campos de textos para buscar y renombrar archivos y carpetas.

        Este método contiene las entradas y los estilos para buscar o renombrar un archivo o una carpeta.
        """
        # search entry
        search_entry_text_variable = StringVar()
        self._search_entry_text_variable = search_entry_text_variable
        search_entry = Entry(self._t, textvariable=search_entry_text_variable)
        search_entry.place(relx=0.65, y=4, relwidth=0.35, height=32)
        self._search_entry = search_entry

        # rename entry
        rename_entry = Entry(
            self._t,
        )
        rename_entry.place(relx=0.65, relwidth=0.35, height=32, rely=0.92)
        self._rename_entry = rename_entry

    def _create_buttons(self):
        """Crear botones

        Este método crea la interfaz de los botones que se van a utilizar para
        realizar las operaciones, dandole la ubicación a y los estilos.
        """
        prev_btn = Button(
            self._t,
            image=self.back_btn,
            command=self._prev,
        )
        prev_btn.place(relx=0, y=4)

        new_btn = Button(
            self._t,
            image=self.create_btn,
            command=self._new,
        )

        new_btn.place(
            relx=0.60,
            y=4,
        )

        rename_btn = Button(self._t, image=self.rename_btn, command=self._rename_file)
        rename_btn.place(relx=0.60, rely=0.92)

        delete_btn = Button(self._t, image=self.delete_btn, command=self._delete_file)
        delete_btn.place(y=4, relx=0.55)

    def _new(self):
        """Nuevo elemento

        Este método abre una nueva ventana en la cual se debe indicar el nombre del nuevo
        elemento para que este se cree y se añada a la ruta en la que se encuentra actualmente.
        """
        self._create_win = Toplevel(self._t)

        label = Label(
            self._create_win,
            text="Filename\nIf you want to create a folder add / before name",
        )
        label.grid(row=0)

        name_entry = Entry(self._create_win, width=30)
        name_entry.grid(row=1)
        self._create_entry = name_entry

        new_btn = Button(
            self._create_win,
            text="Create",
            width=4,
            height=1,
            command=self._create_file,
        )
        new_btn.grid(row=2)

    def _create_file(self):
        """Crear archivo

        Este método crea un nuevo archivo y lo añade a la ruta en la que se encuentra
        actualmente
        """
        try:
            self._exp.create(self._create_entry.get())
        except FileExistsError:
            messagebox.showerror(
                message="A file or folder already exist in this location",
                title="File already exists",
            )
        except:
            messagebox.showerror(
                message="Something went wrong", title="Unexpected error"
            )
        self._create_win.destroy()
        new_nodes = self._exp._list(self._exp.history[-1])
        self._nodes = sorted(new_nodes, key=lambda x: x.name, reverse=True)
        self._clean_list_box()
        self._render_items()

    def _rename_file(self):
        """Renombrar archivo

        Este método cambia el nombre del archivo que esta seleccionado.
        """
        new_name = self._rename_entry.get()

        if len(new_name) == 0:
            return

        self._exp.rename(self._selected, new_name)
        self._rename_entry.delete(0, END)
        new_nodes = self._exp._list(self._exp.history[-1])
        self._nodes = sorted(new_nodes, key=lambda x: x.name, reverse=True)
        self._clean_list_box()
        self._render_items()

    def _filter(self, *args):
        """Filtrar elementos

        Este método filtra los archivos y carpetas de acuerdo a los argumentos dados

        Args:
            *args: Los argumentos son dados por StringVar().trace
        """
        self.filter(self._exp.history[-1], self._search_entry_text_variable.get())

    def filter(self, path, name):
        """Filtrar archivos y/o carpetas.

        Este método busca archivos y/o carpetas que se encuentren en una ruta y que coincidan con el argumento.

        Args:
            path (str): Ruta en la que se va a buscar.
            name (str): Nombre por el que se va a hacer la busqueda.
        """
        if not name:
            self._nodes = sorted(
                self._exp._list(self._exp.history[-1]),
                key=lambda x: x.name,
                reverse=True,
            )
            self._clean_list_box()
            self._render_items()
        else:
            self._nodes = self._exp.search(path, name)
            if len(self._nodes) > 0:
                self._clean_list_box()
                self._render_items()

    def _render_items(self):
        """Mostrar elementos.

        Este método muestra los elementos que hay en la ruta actual.
        """

        for node in self._nodes:
            if node.is_file:
                self._list_box.insert(END, f"- {node.name}")
            else:
                self._list_box.insert(END, f"> {node.name}")

    def _open_folder(self, event):
        """Entrar a una carpeta

        Este método entra a una carpta y muestra los elementos que tiene
        """
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
        """Seleccionar elemento

        Este método selecciona un archivo permitiendo ejecutar sobre el las operaciones
        de eliminar, copiar, cortar y renombrar.
        """
        selection = event.widget.curselection()
        if len(selection) == 0:
            return
        data = str(event.widget.get(selection[0]))

        data = data.removeprefix("> ")
        data = data.removeprefix("- ")
        self._selected = data

        # clean entry
        self._rename_entry.delete(0, END)
        # set value to entry
        self._rename_entry.insert(0, self._selected)

    def _set_listeners(self):
        """Escucha de eventos

        Este método se encarga de escuchar los eventos que se ejecutan en la aplicación,
        estos eventos son: doble click, cambio en la barra de busqueda, control/command + c,
        control/command + v y control/command + x
        """
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
        """Cortar elemento

        Este método corta cualquier elemento
        """
        self._cut_path = f"{self._exp.history[-1]}/{self._selected}"
        pass

    def _copy(self, event):
        """Copiar elemento.

        Este método permite copiar un elemento y si es una carpeta copia lo que esta contiene.
        """
        self._cut_path = ""
        self._copy_path = f"{self._exp.history[-1]}/{self._selected}"

    def _paste(self, event):
        """Peger elemento

        Este método pega un elemento en la ruta en la que se encuentra,
        si es una carpeta pega lo que esta contiene.
        """
        paste_path = self._exp.history[-1]

        if len(self._cut_path) > 0:
            self._exp.copy(self._cut_path, paste_path, True)
            self._cut_path = ""
        else:
            self._exp.copy(self._copy_path, paste_path)

        self._rename_entry.delete(0, END)
        new_nodes = self._exp._list(self._exp.history[-1])
        self._nodes = sorted(new_nodes, key=lambda x: x.name, reverse=True)
        self._clean_list_box()
        self._render_items()

    def render(self):
        """Ejecución del programa

        Este método ejecuta la simulación del explorador de archivos
        """
        self._t.title("File Manager")
        self._t.minsize(width=650, height=650)

        self._create_buttons()
        self._create_entries()
        self._create_list_box()
        self._set_listeners()
        self._render_items()

        self._t.mainloop()


app = App()
app.render()
