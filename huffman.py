from __future__ import annotations

from typing import Generator, Optional

from ordered_list import (insert, pop, OrderedList)


class HuffmanNode:
    """Represents a node in a Huffman tree.

    Attributes:
        char: The character as an integer ASCII value
        frequency: The frequency of the character in the file
        left: The left Huffman sub-tree
        right: The right Huffman sub-tree
    """
    def __init__(
            self,
            char: int,
            frequency: int,
            left: Optional[HuffmanNode] = None,
            right: Optional[HuffmanNode] = None):
        self.char = char
        self.frequency = frequency
        self.left = left
        self.right = right

    def __eq__(self, other) -> bool:
        """Returns True if and only if self and other are equal."""
        return (isinstance(other, HuffmanNode) and
                self.char == other.char and
                self.frequency == other.frequency and
                self.left == other.left and
                self.right == other.right)

    def __lt__(self, other) -> bool:
        """Returns True if and only if self < other."""
        if isinstance(other, HuffmanNode) and self.frequency > other.frequency:
            return False
        else:
            return (isinstance(other, HuffmanNode) and
                    (self.frequency < other.frequency or
                     self.char < other.char))


def count_frequencies(filename: str) -> list[int]:
    """Reads the given file and counts the frequency of each character.

    The resulting Python list will be of length 256, where the indices
    are the ASCII values of the characters, and the value at a given
    index is the frequency with which that character occured.
    """
    freq_list = [0] * 256
    with open(filename) as file:
        for line in file:
            for char in line:
                freq_list[ord(char)] += 1

    return freq_list


def build_huffman_tree(frequencies: list[int]) -> Optional[HuffmanNode]:
    """Creates a Huffman tree of the characters with non-zero frequency.

    Returns the root of the tree.
    """
    huffman_list = OrderedList()
    for number in range(256):
        if frequencies[number] != 0:
            insert(huffman_list, HuffmanNode(number, frequencies[number]))

    if huffman_list.size == 0:
        return None

    while huffman_list.size > 1:
        tree1: HuffmanNode = pop(huffman_list, 0)
        tree2: HuffmanNode = pop(huffman_list, 0)
        if tree1.char < tree2.char:
            insert(huffman_list, HuffmanNode(tree1.char, tree1.frequency +
                   tree2.frequency, tree1, tree2))
        else:
            insert(huffman_list, HuffmanNode(tree2.char, tree1.frequency +
                   tree2.frequency, tree1, tree2))

    return pop(huffman_list, 0)


def create_codes(tree: Optional[HuffmanNode]) -> list[str]:
    """Traverses the tree creating the Huffman code for each character.

    The resulting Python list will be of length 256, where the indices
    are the ASCII values of the characters, and the value at a given
    index is the Huffman code for that character.
    """
    code_list = [''] * 256
    if tree is None:
        return code_list

    for code in tree_traverse(tree):
        code_list[code[1]] = code[0]

    return code_list


def tree_traverse(tree: HuffmanNode, code_string: str = '') -> Generator:
    if tree is not None:
        if tree.left is None and tree.right is None:
            yield code_string, tree.char

        if tree.left is not None:
            yield from tree_traverse(tree.left, code_string + '0')

        if tree.right is not None:
            yield from tree_traverse(tree.right, code_string + '1')


def create_header(frequencies: list[int]) -> str:
    """Returns the header for the compressed Huffman data.

    For example, given the file "aaaccbbbb", this would return:
    "97 3 98 4 99 2"
    """
    result_list = []
    for number in range(256):
        if frequencies[number] != 0:
            result_list.append(number)
            result_list.append(frequencies[number])

    return ' '.join(str(item) for item in result_list)


def huffman_encode(in_filename: str, out_filename: str) -> None:
    """Encodes the data in the input file, writing the result to the
    output file."""
    huffman_tree = build_huffman_tree(count_frequencies(in_filename))
    huffman_code = create_codes(huffman_tree)
    huffman_header = create_header(count_frequencies(in_filename))
    with open(out_filename, 'w') as file_out:
        file_out.write(huffman_header + '\n')
        with open(in_filename) as file_in:
            for line in file_in:
                for char in line:
                    file_out.write(huffman_code[ord(char)])

# functions for decoding


def parse_header(header: str) -> list[int]:
    '''Takes the header from a file, parses it, and returns
       a list of frequencies'''
    freq_list = [0] * 256
    if header == '' or header == '\n':
        return freq_list

    header_list = header.split()
    for i in range(0, len(header_list), 2):
        freq_list[int(header_list[i])] = int(header_list[i + 1])

    return freq_list


def huffman_decode(in_filename: str, out_filename: str) -> None:
    with open(in_filename) as file:
        header = file.readline()

    huffman_tree = build_huffman_tree(parse_header(header))
    if huffman_tree is None:
        with open(out_filename, 'w'):
            return

    if huffman_tree.left is None and huffman_tree.right is None:
        with open(out_filename, 'w') as out_file:
            out_file.write(chr(huffman_tree.char) * huffman_tree.frequency)
            return

    with open(out_filename, 'w') as out_file:
        with open(in_filename) as in_file:
            temp_tree = huffman_tree
            for char in in_file.readlines()[1]:
                if char == '0':
                    temp_tree = temp_tree.left

                if char == '1':
                    temp_tree = temp_tree.right

                if temp_tree.left is None and temp_tree.right is None:
                    out_file.write(chr(temp_tree.char))
                    temp_tree = huffman_tree
