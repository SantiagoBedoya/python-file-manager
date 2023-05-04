import os

class Node:
    def __init__(self, name, is_file) -> None:
        self.name = name
        self.is_file = is_file

class Explorer:
    def __init__(self, path) -> None:
        self.path = path
        self.history = [path]

    def list(self, path = None):
        nodes = []
        uri = ""
        if path is None:
            uri = self.path 
        elif self.history[-1] == path:
            uri = path
        else:
            uri = os.path.join(self.history[-1], path)

        print("printing -- ", uri)
        entries = os.listdir(uri)
        for file in entries:
            is_file = os.path.isfile(os.path.join(uri, file))
            nodes.append(Node(file, is_file))

        return nodes

    def is_folder(self, path):
        return not os.path.isfile(os.path.join(self.path, path))