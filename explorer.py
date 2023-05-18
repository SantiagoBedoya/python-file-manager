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

    def is_folder(self, path):
        return not os.path.isfile(os.path.join(self.path, path))