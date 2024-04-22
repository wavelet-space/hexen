"""
Modul obsahuje třídy abstrahující ukládání a načítání entit do/z úložiště (návrhový vzor repository).
"""

from abc import abstractmethod
from typing import Protocol, Self

# from ..aggregate import Entity
from ._connection import Connection

# https://stackoverflow.com/questions/54118095/


class PersistenceError(Exception):
    def __init__(self, message, *errors):
        super().__init__(self, message)
        self.errors = errors

    
class ConflictError(PersistenceError):
    """
    Raised when entity can't be saved.
    """


# class AbstractReadableRepository: ...
# class AbstractWrietableRepository: ...


class RepositoryProtocol[Entity, Identifier](Protocol):

    # def next_id() -> Id: ...
    # def save_all(self, entities) -> None: ...
    # def find_all(self, predicate) -> Iterable[T]: ...

    def save(self, entity: Entity) -> None:
        """
        Save the entity to the storage.

        :param entity: Entity to save.
        :raises: ConflictError
        """

    def find(self, entity_id: Identifier) -> Entity:  # Entity[Identifier]
        """
        Find the entity in the storage.
        """

    def count(self) -> int:
        """
        Count the persisted entities.
        """

    def exists(self, entity: Entity) -> bool:
        """
        Check if the entity is alrady persisted.

        :param: ...
        """

    def commit(self) -> None:
        """
        Commit changes.

        :raises: ...
        """

    def revert(self) -> None:
        """
        Revert (abort) changes.

        :raises: ...
        """
        # revert/rollback

    def __enter__(self) -> Self:
        return self

    def __exit__(self, error_type, error_value, traceback) -> None:
        if error_type:
            self.revert()
        else:
            self.commit()


class AbstractSQLRepository[Entity, Identifier](RepositoryProtocol):
    _context: Connection

    def __init__(self, context: Connection = None) -> None:
        self._context = context

    @abstractmethod
    def save(self, entity: Entity) -> None:
        """
        Save the entity to the storage.
        """

    @abstractmethod
    def find(self, entity_id: Identifier) -> Entity:  # Entity[Identifier]
        """
        Find the entity in the storage.
        """
 
    @abstractmethod
    def count(self) -> int:
        """
        Count the persisted entities.
        """

    @abstractmethod
    def exists(self, entity: Entity) -> bool:
        """
        Check if the entity is alrady persisted.

        :param: ...
        """

    def commit(self) -> None:
        """
        Commit changes.

        :raises: ...
        """
        self._context.commit()

    def revert(self) -> None:
        """
        Revert (abort) changes.

        :raises: ...
        """
        # revert/rollback
        self._context.rollback()


class MemoryRepository[Entity, Identifier](RepositoryProtocol):
    """
    The repository storing entities in the computer's memory.

    Examples:

        ...
    """

    _storage: dict[Identifier, Entity]
    _current: list[Entity]

    def __init__(self, *entities) -> None:
        self._storage = {}  # Should be class variable?
        self._storage |= {e.identifier: e for e in entities}
        self._current = []

    def save(self, entity: Entity) -> None:
        if self.exists(entity):
            raise ValueError("Conflict {entity}")
        self._current.append(entity)

    def find(
        self, entity_id: Identifier
    ) -> Entity | None:  # Entity[Identifier] can!t be used?
        return self._storage.get(entity_id, None)

    def count(self) -> int:
        # NOTE: no update, so it can just sum commited and uncommited
        return len(self._storage.keys()) + len(self._current)

    def exists(self, entity: Entity) -> bool:
        return entity.identifier in self._storage

    def commit(self) -> None:
        self._storage |= {e.identifier: e for e in self._current}
        self._current = []

    def revert(self) -> None:
        self._current = []


if __name__ == "__main__":
    import doctest

    doctest.testmod()
