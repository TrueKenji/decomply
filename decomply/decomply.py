from typing import List, Union
import copy
import numpy as np
from decomply.enumerable import EnumerableHandler, ListHandler, DictHandler


class Decomply:
    """
    Decomply class allows unified processing of nested dictionaries (or any enumerable objects). Main method is decomply
    """

    def __init__(
        self,
        traverse: callable = lambda trace, item: True,
        apply: callable = lambda trace, item: item,
        delete: callable = lambda trace, item: str(trace[-1]).startswith("_"),
        handlers: set[EnumerableHandler] = None
    ):
        """
        Initialize the Decomply object

        Args:
        traverse (callable, optional): A callable function that determines whether
            to traverse further into nested objects during cascading. It takes
            two arguments: `trace` (list) - the current trace of keys, and `item`
            (any) - the current item being evaluated. Defaults to always return True.
        apply (callable, optional): A callable function that applies a transformation
            or operation on an item during cascading when `traverse` condition is not
            met. It takes two arguments: `trace` (list) - the current trace of keys,
            and `item` (any) - the current item being evaluated. Defaults to returning
            the item unchanged.
        delete (callable, optional): A callable function that determines whether to
            delete a key/value pair during cascading based on the key and value. It
            takes two arguments: `trace` (list) - the current trace, and `item` (any) -
            the current item associated with the trace. Defaults to deleting keys that
            start with an underscore (`key.startswith("_")`).
        handlers (set[EnumerableHandler], optional): A set of @EnumerableHandlers. 
            Such a handler must implement methods to allow handling of an enumerable 
            object. Users may write their own handlers and supply them here, to 
            extend support. In basekit, only list and dict is supported.
        """
        self.traverse = lambda trace, item: self._is_enumerable(
            item) and traverse(trace, item)
        self.apply = apply
        self.delete = delete

        self.handlers: set[EnumerableHandler] = {ListHandler(), DictHandler()}
        if handlers:
            self.handlers.update(handlers)

    def decomply(self, item: Union[dict, list, any], trace: List[Union[str, int, any]] = None, initial_check: bool = True) -> Union[dict, list, any]:
        """
        Decomply the supplied `item`

        Args:
            item (Union[dict, list, any]): The object to be decomplied. Supported is list and dict, but 
                using your own handlers, you may pass any object your handlers support
            trace (List[Union[str, int, any]], optional): A list representing the current trace of keys
                during traversing. Defaults to None.
            initial_check (bool, optional): Flag indicating whether to perform the initial check
                with the `traverse` condition defined in the constructor (`__init__` method).
                Defaults to True.

        Returns:
            Union[dict, list, any]: An object with the same structure as `item`, modified according to the
                configured `traverse`, `apply`, and `delete` behaviors.

        Notes:
            - The `traverse`, `apply`, and `delete` behaviors are configured during the initialization
            of the Decomply object (`__init__` method).
            - If `trace` is not provided (`None`), it defaults to an empty list

        """
        if isinstance(trace, type(None)):
            trace = list()
        if initial_check and not self.traverse(trace, item):
            return self.apply(item, copy.deepcopy(trace))
        return self._decomply(trace, item)

    def _decomply(self, trace: List[Union[str, int]], item: Union[dict, list, any]) -> Union[dict, list, any]:
        """
        Traverse the item's items in a depth-first search style (DFS)
        Apply if traverse evaluates to False.
        Build the output object iteratively.

        Returns:
            Union[dict, list, any]: see @decomply
        """
        _trace = copy.deepcopy(trace)  # prevent side effects
        handler = self._get_handler(item)
        out = handler.copy_type()
        for key, value in handler.iterate(item):
            _trace.append(key)
            if not self.delete(_trace, value):
                if self.traverse(_trace, value):
                    handler.put(out, key, self._decomply(_trace, value))
                else:
                    handler.put(out, key, self.apply(
                        copy.deepcopy(_trace), value))
            _trace.pop()
        return out

    def _get_handler(self, item) -> EnumerableHandler:
        for handler in self.handlers:
            if handler.can_handle(item):
                return handler
        raise Exception("No handler found for type %s" % type(item))

    def _is_enumerable(self, item: any) -> bool:
        return np.any([handler.can_handle(item) for handler in self.handlers])
