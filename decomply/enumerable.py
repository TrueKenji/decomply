from typing import Hashable, ItemsView
from abc import ABC, abstractmethod


class EnumerableHandler(ABC):
    """EnumerableHandler is a base class for concrete enumerable object handlers.
    Such a handler must implement all abstract methods to allow handling of enumerable objects
    """

    @abstractmethod
    def copy_type(self):
        """return an empty instance of the object type associated with this handler
        """
        pass

    @abstractmethod
    def iterate(self, item: any) -> ItemsView[any, any]:
        """return a view on the key/value pairs of the given item

        Args:
            item (any): an object supported by this handler
        """
        pass

    @abstractmethod
    def put(self, target: any, key: any, value: any) -> None:
        """insert the given key & value into the target

        Args:
            target (any): the object to insert into
            key (any): the key
            value (any): the value
        """
        pass

    @abstractmethod
    def can_handle(self, item: any) -> bool:
        """return whether this handler supports the given item

        Args:
            item (any): the object to test

        Returns:
            bool: whether this handler supports the given item
        """
        pass

    @abstractmethod
    def contains_key(self, key: any, item: any) -> bool:
        """whether the given item contains the given key

        Args:
            key (any): the key to test
            item (any): the item to test against

        Returns:
            bool: whether the given item contains the given key
        """
        pass


class ListHandler(EnumerableHandler):

    def copy_type(self):
        return list()

    def iterate(self, item: list) -> ItemsView[int, any]:
        return enumerate(item)

    def put(self, target: list, key: int, value: any) -> None:
        if isinstance(key, int) and 0 <= key < len(target):
            target[key] = value
        else:
            target.append(value)

    def can_handle(self, item: any) -> bool:
        return isinstance(item, list)

    def contains_key(self, key: int, item: list) -> bool:
        if isinstance(key, int):
            return 0 <= key < len(item)
        return False


class DictHandler(EnumerableHandler):

    def copy_type(self) -> dict:
        return dict()

    def iterate(self, item: dict) -> ItemsView[Hashable, any]:
        return item.items()

    def put(self, target: dict, key: Hashable, value: any) -> None:
        target[key] = value

    def can_handle(self, item) -> bool:
        return isinstance(item, dict)

    def contains_key(self, key: Hashable, item: dict) -> bool:
        return key in item


_handlers: set[EnumerableHandler] = {ListHandler(), DictHandler()}


def get_handler(item):
    for handler in _handlers:
        if handler.can_handle(item):
            return handler
    raise Exception("No handler found for type %s" % type(item))
