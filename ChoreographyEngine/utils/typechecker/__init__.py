#! python3
# coding: utf-8

"""
A Type Checker for Python Data Types:
    Simple Data Types:
        Number: int, float, complex
        String: str
        Bool: bool
        Others: User-defined and so on...
    Compound Data Types:
        Tuple: tuple
        Sets: set
        List: list
        Dictionary: dict
* Some restrictions on usage:
    1. Not really Python type but static data type;
    2. Only available for the 4 compound data;
    3. Cannot check arguments' type of functions.
"""

from .typechecker import function_type, check_type

__all__ = ['function_type', 'check_type']
