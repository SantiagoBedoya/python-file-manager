import os
import shutil

class Node:
    def __init__(self, name, is_file) -> None:
        self.name = name
        self.is_file = is_file

class Explorer:
    def __init__(self, path) -> None:
        self.path = path
        self.history = [path]

    def delete(self, path):
        uri = os.path.join(self.history[-1],  path)
        if os.path.isdir(uri):
            shutil.rmtree(uri)
        else:
            os.remove(uri)

    def create(self, path = ""):
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
            if name in item:
                items.append(
                    Node(item, os.path.isfile(os.path.join(path, item))))
            if os.path.isdir(os.path.join(path, item)):
                self.search(os.path.join(path, item), name)
        return items

    def _list(self, path):
        nodes = []
        entries = os.listdir(path)
        for file in entries:
            is_file = os.path.isfile(os.path.join(path, file))
            nodes.append(Node(file, is_file))

        return nodes

    def list(self, path = None, is_prev = False):
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
    
    def copy(self, copy_path, paste_path, is_cute = False):
        if is_cute:
            # if the action is cut and paste, copy2 keeps timestamps
            shutil.move(copy_path, paste_path, shutil.copy2)
        else:
            shutil.copy(copy_path, paste_path)

    def is_folder(self, path):
        return not os.path.isfile(os.path.join(self.path, path))