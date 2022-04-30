from __future__ import annotations

from typing import Any, Optional


class Node:
    """Represents a node to be used in a doubly linked list."""
    def __init__(
            self,
            value: Any,
            prev: Optional[Node] = None,
            nxt: Optional[Node] = None):
        self.value = value

        # NOTE: This means that if prev and nxt are None, self.prev and
        # self.next will be self.  You may find this useful.  This means
        # that self.prev and self.next aren't Optional Nodes, they are
        # always Nodes.
        self.prev: Node = prev or self
        self.next: Node = nxt or self


class OrderedList:
    """A circular, doubly linked list of items, from lowest to highest.

    The contents of the list *must* have a accurate notation of less
    than and of equality.  That is to say, the contents of the list must
    implement both __lt__ and __eq__.
    """
    def __init__(self):
        self.head: Node = Node('dummy Node')
        self.size = 0


def insert(lst: OrderedList, value: Any) -> None:
    '''Inserts a value into the list while maitaining ascending order'''
    if lst.size == 0:
        lst.head.next = Node(value, lst.head, lst.head)
        lst.head.prev = lst.head.next
        lst.size += 1
    else:
        current_node = lst.head.next
        while not (value < current_node.value):
            if current_node.next == lst.head:
                break
            current_node = current_node.next

        if value < current_node.value:
            new_node = Node(value, current_node.prev, current_node)
            current_node.prev.next = new_node
            current_node.prev = new_node
            lst.size += 1
        else:
            new_node = Node(value, current_node, current_node.next)
            current_node.next.prev = new_node
            current_node.next = new_node
            lst.size += 1


def remove(lst: OrderedList, value: Any) -> None:
    '''Removes a value from from the list'''
    if not contains(lst, value):
        raise ValueError

    current_node = lst.head.next
    while current_node.value != value:
        current_node = current_node.next

    current_node.prev.next = current_node.next
    current_node.next.prev = current_node.prev
    lst.size -= 1


def contains(lst: OrderedList, value: Any) -> bool:
    '''Returns whether or not a value is in the list'''
    current_node = lst.head.next
    while current_node != lst.head:
        if current_node.value == value:
            return True
        current_node = current_node.next

    return False


def index(lst: OrderedList, value: Any) -> int:
    '''Returns the index of the given value if it is in the list'''
    if not contains(lst, value):
        raise ValueError

    current_node = lst.head.next
    position = 0
    while current_node.value != value:
        current_node = current_node.next
        position += 1

    return position


def get(lst: OrderedList, index: int) -> Any:
    '''Returns the value at the given index'''
    if index < 0 or index >= lst.size:
        raise IndexError

    current_node = lst.head.next
    position = index
    while position > 0:
        current_node = current_node.next
        position -= 1

    return current_node.value


def pop(lst: OrderedList, index: int) -> Any:
    '''Removes and returns the value at the given index'''
    if index < 0 or index >= lst.size:
        raise IndexError

    value = get(lst, index)

    current_node = lst.head.next
    position = index
    while position > 0:
        current_node = current_node.next
        position -= 1

    current_node.prev.next = current_node.next
    current_node.next.prev = current_node.prev
    lst.size -= 1
    return value


def is_empty(lst: OrderedList) -> bool:
    return lst.size == 0


def size(lst: OrderedList) -> int:
    return lst.size
