import os
import shutil


class Node:
    def __init__(self, name, path, is_file) -> None:
        self.name = name
        self.is_file = is_file
        self.path = path
        self.children = []


class Explorer:
    def __init__(self, path) -> None:
        self.path = path
        self.history = [path]
        self.root_node = None

        self.get_nodes()


    def get_nodes(self):
        self.root_node = Node('root', self.path, False)
        self._get_nodes(self.path, self.root_node)

    def _get_nodes(self, path, node):
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
        uri = os.path.join(self.history[-1],  path)
        if os.path.isdir(uri):
            shutil.rmtree(uri)
        else:
            os.remove(uri)

    def create(self, path=""):
        if path.startswith("/"):
            path = path.removeprefix("/")
            uri = os.path.join(self.history[-1], path)
            os.makedirs(uri)
        else:
            uri = os.path.join(self.history[-1], path)
            f = open(uri, "w+")
            f.close()

    def rename(self, path, new_name):
        uri = os.path.join(self.history[-1],  path)
        new_uri = os.path.join(self.history[-1],  new_name)
        os.rename(uri, new_uri)

    def search(self, path, name):
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
        nodes = []
        entries = os.listdir(path)
        for file in entries:
            uri = os.path.join(path, file)
            is_file = os.path.isfile(uri)
            nodes.append(Node(file, uri, is_file))

        return nodes

    def list(self, path=None, is_prev=False):
        uri = ""
        if path is None:
            uri = self.path
        else:
            if is_prev:
                uri = path
                self.history.pop()
            else:
                uri = os.path.join(self.history[-1],  path)
                self.history.append(uri)

        return self._list(uri)

    def copy(self, copy_path, paste_path, is_cute=False):
        if is_cute:
            # if the action is cut and paste, copy2 keeps timestamps
            shutil.move(copy_path, paste_path, shutil.copy2)
        else:
            shutil.copy(copy_path, paste_path)

    def is_folder(self, path):
        return not os.path.isfile(os.path.join(self.path, path))
