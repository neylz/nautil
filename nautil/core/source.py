from abc import ABC, abstractmethod
from os import path, PathLike



class Source(ABC):
    @abstractmethod
    def copy_files(self, dest: PathLike):
        pass

