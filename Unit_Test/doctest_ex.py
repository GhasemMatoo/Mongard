"""
    >>> add(6, 5)
    11
    >>> add(5 , 'x')
    Traceback (most recent call last):
    TypeError: unsupported operand type(s) for +: 'int' and 'str'
    >>> subtract(6, 9)
    -3
    >>> subtract(5, y)
    Traceback (most recent call last):
    NameError: name 'y' is not defined
    >>> multiply(5, 'b')
    'bbbbb'
    >>> multiply(0, y)
    Traceback (most recent call last):
    NameError: name 'y' is not defined
"""


def add(x, y):
    """
    >>> add(5, 5)
    10
    >>> add(5, -5)
    0
    >>> add(5 , 'x')
    Traceback (most recent call last):
    TypeError: unsupported operand type(s) for +: 'int' and 'str'
    """
    return x + y


def subtract(x, y):
    """
    >>> subtract(5, 4)
    1
    >>> subtract(6, 9)
    -3
    >>> subtract(5, y)
    Traceback (most recent call last):
    NameError: name 'y' is not defined
    """
    return x - y


def multiply(x, y):
    """
    >>> multiply(5, 5)
    25
    >>> multiply(5, 'b')
    'bbbbb'
    >>> multiply(0, y)
    Traceback (most recent call last):
    NameError: name 'y' is not defined
    """
    return x * y