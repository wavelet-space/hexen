from abc import ABC, abstractmethod
from pathlib import Path
from typing import Self


def transactional():
    """A decorator for functions to run in transaction."""
    ...


class Transaction(ABC):
    """
    The transaction represents a group of actions that should be executed as a unit.
    When something goes wrong, everything should be reverted to its original state.
    Use this class to implement the Unit of Work pattern.
    """

    def __enter__(self) -> Self:
        return self

    @abstractmethod
    def __exit__(self, exc_type, exc_value, exc_traceback) -> None:
        if exc_type:
            self.revert()
        else:
            self.commit()

    @abstractmethod
    def commit(self):
        raise NotImplementedError

    @abstractmethod
    def revert(self):
        raise NotImplementedError


class PostgreSQLTransaction(Transaction):
    def __enter__(self) -> Self:
        ...

    def __exit__(self) -> None:
        ...


class FileSystemTransaction(Transaction):
    """
    An atomic operation for file system.
    """

    def __init__(self, path: Path, timeout=42):
        if not path.is_dir():
            raise ValueError(f"The provided path `{path}` is not a directory.")

    def __enter__(self) -> Self:
        ...

    def __exit__(self) -> None:
        ...
