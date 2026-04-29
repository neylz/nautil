import tempfile
import uuid
import weakref

from enum import Enum, auto
from os import path, PathLike, makedirs, remove
from shutil import copytree, make_archive, rmtree
from string import Template

from nautil.core.source import Source




class Artifact:
    class OutputFormat(Enum):
        DIRECTORY = auto()
        ZIP = auto()

    def __init__(self, vars: dict):
        self._vars = dict(vars)
        self._temp_dir = tempfile.TemporaryDirectory(prefix="nautil-")
        self._finalizer = weakref.finalize(self, self._temp_dir.cleanup)

    @property
    def vars(self) -> dict:
        return self._vars
    
    @property
    def path(self) -> str:
        return self._temp_dir.name
    
    # == default actions ==

    def use(self, src: Source, dest: PathLike = ".", src_path: PathLike = ".", overwrite: bool = False):
        """
        Import files from a source-like object into the artifact.
        
        :param src: A source-like object that has a copy_files(dest, src_path) method.
        :param dest: The destination path within the artifact where the files will be copied.
        :param src_path: The path within the source where the files will be copied from.
        :param overwrite: Whether to overwrite existing files at the destination.
        """
        target_path = path.join(self.path, dest)


        copy_files = getattr(src, "copy_files", None)
        if not callable(copy_files):
            raise TypeError(
                "Artifact.use expected a Source-like object with copy_files(dest, src_path) method, but got an object of type {}".format(type(src).__name__)
            )

        copy_files(target_path, src_path, overwrite)
        return self

    def clone(self):
        """Create an independent artifact copy with the same current workspace content."""
        cloned_artifact = Artifact(self.vars)
        copytree(self.path, cloned_artifact.path, dirs_exist_ok=True)
        return cloned_artifact


    @staticmethod
    def _pre_output_cleanup(target_path: PathLike):
        if path.isdir(target_path):
            rmtree(target_path)
        elif path.isfile(target_path):
            remove(target_path)

    def output(
        self,
        output_path: PathLike = "dist",
        name: str = None,
        format: OutputFormat = OutputFormat.ZIP
    ):
        """
        Output the artifact to the specified path.
        
        Args:
            output_path: The path where the artifact will be output.
            name: The name template of the artifact. Can use context variables. eg. `"$NAME-$VERSION-$PLATFORM.zip"`
            format: The format of the artifact output.
        """


        if name is None:
            name = "artifact-" + uuid.uuid4().hex[:8]
        else:
            name = self.parset(name)
        output_path = path.join(output_path, name)


        self.log(f"Outputting artifact to {output_path} as {format.name.lower()}")

        parent_dir = path.dirname(output_path)
        if parent_dir:
            makedirs(parent_dir, exist_ok=True)


        if format == self.OutputFormat.DIRECTORY:
            self._pre_output_cleanup(output_path)
            copytree(self.path, output_path)

        elif format == self.OutputFormat.ZIP:
            archive_base = output_path[:-4] if output_path.endswith(".zip") else output_path
            archive_path = f"{archive_base}.zip"

            self._pre_output_cleanup(archive_path)
            make_archive(archive_base, "zip", self.path)
        
        return self
    

    # == libs helper ==
    def parset(self, template_str: str) -> str:
        """Parse a string template with the artifact's context variables."""
        return Template(template_str).substitute(self.vars)
    
    
    def log(self, message: str):
        """Log a message with the artifact's context variables."""
        
        prefix = "-".join([
            "$TARGET" if self.vars.get("TARGET") else "",
            "$ARTIFACT" if self.vars.get("ARTIFACT") else "",
        ]).strip("-")
        prefix = f"[{prefix}] " if prefix else "[?] "

        message = prefix + message        

        print(self.parset(message))