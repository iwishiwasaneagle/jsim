import os


class Map:
    path: int

    def __init__(self, path: str):
        if not os.path.isfile(path):
            raise FileNotFoundError(f'file "{path}" does not exist')
        self.path = path
