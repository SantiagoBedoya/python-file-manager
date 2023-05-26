import os
import shutil


class Node:
    """Esta clase es la unidad en la que se trabajará en el arbol.

    Esta clase contiene atributos que son necesarios para inicializarla.

    Attributes:
        name (str): Nombre del nodo.
        is_file (bool): Se utiliza para saber si es un archivo o una carpeta.
        path (str): Ruta en la que se encuentra el nodo.
        children (str[]): Nodos hijos que tiene el nodo si es una carpeta.
    """

    def __init__(self, name, path, is_file) -> None:
        self.name = name
        self.is_file = is_file
        self.path = path
        self.children = []


class Explorer:
    """Esta clase es el árbol que contiene las operciones que se necesitan para la construcción de la simulación del explorador.

    Esta clase contiene métodos tanto públicos como privados que realizan las operacione para obtener, buscar, crear, actualizar y eliminar nodos.

    Attributes:
        path (str): Ruta en la que inicia el explorador.
        history (str[]): Historial de rutas que se han recorrido.
        root_node (str): Ruta en la que se encuentra el nodo.
    """

    def __init__(self, path) -> None:
        self.path = path
        self.history = [path]
        self.root_node = None
        self.get_nodes()

    def get_nodes(self):
        """Obtener nodos

        Este metodo hace llama al método privado _get_nodes para obtener todos los nodos y organizarlos en el árbol
        """
        self.root_node = Node("root", self.path, False)
        self._get_nodes(self.path, self.root_node)

    def _get_nodes(self, path, node):
        """Obtiene todos los nodos

        Este método va recolectando todos los nodos y los organiza en el árbol del explorador.

        Args:
            path (str): Ruta en la que empieza a buscar los nodos.
            node (Node): Nodo padre en el que se empieza a construir el árbol.
        """
        entries = os.listdir(path)
        for entry in entries:
            uri = os.path.join(path, entry)
            if os.path.isfile(uri):
                node.children.append(Node(entry, uri, True))
            else:
                # it's a folder
                child_node = Node(entry, uri, False)
                node.children.append(child_node)
                self._get_nodes(uri, child_node)

    def delete(self, path):
        """Eliminar un nodo

        Este método elimina un nodo basandose en la ruta que se le dé.

        Args:
            path (str): Ruta en la que está ubicado el nodo para eliminarlo
        """
        uri = os.path.join(self.history[-1], path)
        if os.path.isdir(uri):
            shutil.rmtree(uri)
        else:
            os.remove(uri)

    def create(self, path=""):
        """Crear un nodo

        Este método crea un nodo y lo inserta en la ruta que se le dá.

        Args:
            path (str): Ruta en la que se inserta el nodo, por defecto inserta el nodo en la raiz.--
        """
        if path.startswith("/"):
            path = path.removeprefix("/")
            uri = os.path.join(self.history[-1], path)
            os.makedirs(uri)
        else:
            uri = os.path.join(self.history[-1], path)
            f = open(uri, "w+")
            f.close()

    def rename(self, path, new_name):
        """Cambiar el nombre de un nodo

        Este método encuentra el nodo según la ruta que se le dé y le cambia el nombre al nodo.

        Args:
            path (str): Ruta en la que se encuentra el nodo.
            new_name (str): Nombre que va a reemplazar el nombre del nodo.
        """
        uri = os.path.join(self.history[-1], path)
        new_uri = os.path.join(self.history[-1], new_name)
        os.rename(uri, new_uri)

    def search(self, path, name):
        """Buscar un nodo.

        Este método busca un nodo basandose en la ruta que se le da y el nombre del nodo.

        Args:
            path (str): Ruta en la que se busca el nodo.
            name (str): Nombre del nodo.
        """
        directorio = os.listdir(path)
        items = []
        for item in directorio:
            uri = os.path.join(path, item)
            if name in item:
                items.append(Node(item, uri, os.path.isfile(uri)))
            if os.path.isdir(uri):
                self.search(uri, name)
        return items

    def _list(self, path):
        """Listar nodos

        Este método privado lista los nodos hijos según el path que se le pase.

        Args:
            path (str)= Ruta de la carpeta que se va a listar.

        Returns:
            Devuelve la lista de los nodos que se van a listar.
        """
        nodes = []
        entries = os.listdir(path)
        for file in entries:
            uri = os.path.join(path, file)
            is_file = os.path.isfile(uri)
            nodes.append(Node(file, uri, is_file))

        return nodes

    def list(self, path=None, is_prev=False):
        """Listar nodos

        Este método lista los nodos según el path que se le envíe dando la opción de devolverse al directorio anterior.

        Args:
            path (str): Ruta en la que se encuentran los nodos a listar.
            is_prev (bool): Dice si es un directorio anterior.

        Returns:
            Devuelve la lista con los nodos a listar.
        """
        uri = ""
        if path is None:
            uri = self.path
        else:
            if is_prev:
                uri = path
                self.history.pop()
            else:
                uri = os.path.join(self.history[-1], path)
                self.history.append(uri)

        return self._list(uri)

    def copy(self, copy_path, paste_path, is_cute=False):
        """Copiar, pegar o cortar un nodo.

        Este método copia, pega o corta un nodo con el path entero y teniendo en cuenta los nodos hijos que tenga.

        Args:
            copy_path (str): Ruta que se va a copiar.
            paste_path (str): Ruta que se va a pegar.
            is_cute (bool): Verifica si el nodo es cortado.
        """
        if is_cute:
            # if the action is cut and paste, copy2 keeps timestamps
            shutil.move(copy_path, paste_path, shutil.copy2)
        else:
            shutil.copy(copy_path, paste_path)

    def is_folder(self, path):
        """Verificación de tipo de nodo.

        Este método verifica si el nodo es un archivo o un directorio.

        Args:
            path (str): Ruta en la que se encuentra el nodo
        """
        return not os.path.isfile(os.path.join(self.path, path))
