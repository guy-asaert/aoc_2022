"""
Advent of Code 2022 - Day 21
Puzzle Solution
Author: Guy
Date: 7 November 2024
"""

import copy
from dataclasses import dataclass
from utils import iter_lines

PUZZLE_INPUT_SAMPLE = '''root: pppw - sjmn
dbpl: 5
cczh: sllz + lgvd
zczc: 2
ptdq: humn - dvpt
dvpt: 3
lfqf: 4
humn: 5
ljgn: 2
sjmn: drzm * dbpl
sllz: 4
pppw: cczh / lfqf
lgvd: ljgn * ptdq
drzm: hmdt - zczc
hmdt: 32'''


class NodeBase:
    """
    Base class for all nodes in the puzzle.
    """
    _nodes = dict()

    def value():
        """
        Method to be implemented by subclasses to return the node's value.
        """
        raise NotImplementedError


class ValueNode(NodeBase):
    """
    Class representing a node with a fixed value.
    """
   
    def __init__(self, value):
        """
        Initialize the ValueNode with a specific value.
        
        :param value: The value of the node.
        """
        self._value = value

    def value(self):
        """
        Return the value of the node.
        
        :return: The value of the node.
        """
        return self._value
    
    @property
    def value_prop(self):
        """
        Property to get the value of the node.
        
        :return: The value of the node.
        """
        return self._value
    
    @value_prop.setter
    def value_prop(self, value):
        """
        Property setter to set the value of the node.
        
        :param value: The new value of the node.
        """
        self._value = value
    

class OperatorNode(NodeBase):
    """
    Class representing a node that performs an operation on two other nodes.
    """
    
    def __init__(self, operator, left, right):
        """
        Initialize the OperatorNode with an operator and two operands.
        
        :param operator: The operator to be applied ('+', '-', '*', '/').
        :param left: The left operand (another node).
        :param right: The right operand (another node).
        """
        self._operator = operator
        self._left = left
        self._right = right

    def value(self):
        left = NodeBase._nodes[self._left].value()
        right = NodeBase._nodes[self._right].value()
        if self._operator == '+':
            return left + right
        elif self._operator == '-':
            return left - right
        elif self._operator == '*':
            return left * right
        elif self._operator == '/':
            return left / right
        else:
            raise ValueError(f'Unknown operator: {self._operator}')

def run():
    """
    Main function to execute the puzzle solution.
    
    This function reads the puzzle input, initializes the nodes, and solves the puzzle
    by adjusting the value of the 'humn' node until the root node's value is zero.
    """
    # for x in PUZZLE_INPUT_SAMPLE.split('\n'):
    for x in iter_lines(__file__, '_puzzle.txt'):
        name, code = x.split(': ')
        try:
            value = int(code)
            NodeBase._nodes[name] = ValueNode(value)
        except:
            left, operator, right = code.split()
            NodeBase._nodes[name] = OperatorNode(operator, left, right)

    root = NodeBase._nodes['root']

    # solve for 0
    current_x = NodeBase._nodes['humn'].value()
    current_y = root.value()

    adjust = 100000
    NodeBase._nodes['humn'].value_prop += adjust
    
    while root.value() != 0:
        next_x = NodeBase._nodes['humn'].value()
        next_y = root.value()
        b = - (next_x - current_x) / (next_y - current_y)
        c = current_x + b * current_y
        NodeBase._nodes['humn'].value_prop = c
        print(f'CHECK {c} -> {root.value()}')
        current_x = next_x
        current_y = next_y

    # data = [int(x) * DECRYPTION_KEY for x in iter_lines(__file__, '_puzzle.txt')]



if __name__ == "__main__":
    run()
