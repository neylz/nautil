
from os import PathLike
import shutil
import git
import tempfile

from nautil.core.source import Source


class GitSource(Source):
    def __init__(self, git_url: str, branch: str = "main", specific_commit: str = None, depth: int = 1):
        self.git_url = git_url
        self.branch = branch
        self.specific_commit = specific_commit
        self.depth = depth

    def copy_files(self, dest: PathLike):
        with tempfile.TemporaryDirectory() as tmp_dir:
            repo = git.Repo.clone_from(self.git_url, tmp_dir, branch=self.branch, depth=self.depth)

            if self.specific_commit:
                repo.git.checkout(self.specific_commit)

            shutil.copytree(
                tmp_dir,
                dest,
                dirs_exist_ok=True,
                ignore=shutil.ignore_patterns(".git"),
            )

