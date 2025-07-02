from PySide6.scripts.project_lib import Singleton


class Config(metaclass=Singleton):
    def set(self, key, value):
        pass
    def get(self, key, default=None):
        pass