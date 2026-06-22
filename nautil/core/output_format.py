import warnings

from abc import ABC, ABCMeta, abstractmethod
from os import path, PathLike, remove
from shutil import copytree, make_archive, rmtree




class _OutputFormatMeta(ABCMeta):
    def __getattr__(cls, name):
        aliases = {"ZIP": Zip, "DIRECTORY": Directory}
        if cls is OutputFormat and name in aliases:
            target = aliases[name]
            warnings.warn(
                f"OutputFormat.{name} is deprecated, use {target.__name__}() instead",
                DeprecationWarning,
                stacklevel=2,
            )
            return target()
        raise AttributeError(name)


class OutputFormat(ABC, metaclass=_OutputFormatMeta):
    @property
    @abstractmethod
    def name(self) -> str:
        ...

    @abstractmethod
    def write(self, source_path: PathLike, output_path: PathLike):
        ...

    @staticmethod
    def _pre_output_cleanup(target_path: PathLike):
        if path.isdir(target_path):
            rmtree(target_path)
        elif path.isfile(target_path):
            remove(target_path)


class Directory(OutputFormat):
    @property
    def name(self) -> str:
        return "directory"

    def write(self, source_path: PathLike, output_path: PathLike):
        self._pre_output_cleanup(output_path)
        copytree(source_path, output_path)


class Zip(OutputFormat):
    @property
    def name(self) -> str:
        return "zip"

    def write(self, source_path: PathLike, output_path: PathLike):
        archive_base = output_path[:-4] if output_path.endswith(".zip") else output_path
        archive_path = f"{archive_base}.zip"

        self._pre_output_cleanup(archive_path)
        make_archive(archive_base, "zip", source_path)
