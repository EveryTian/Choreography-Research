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

function_type = type(lambda _: _)


def check_type(element, some_type) -> bool:
    compound_types = {tuple, set, list, dict}
    element_type = type(element)
    if element_type is type(some_type) and element_type in compound_types:
        if element_type is tuple:
            return len(element) == len(some_type) and \
                   all(map((lambda x: check_type(x[0], x[1])), zip(element, some_type)))
        if element_type is list:
            return all(map((lambda x: check_type(x, some_type[0])), element))
        if element_type is set:
            return all(map((lambda x: check_type(x, tuple(some_type)[0])), element))
        if element_type is dict:
            key_type = tuple(some_type)[0]
            return all(map((lambda x: check_type(x, key_type)), (i for i in element))) and \
                   all(map((lambda x: check_type(x, some_type[key_type])), (element[i] for i in element)))
        return False
    return type(element) is some_type
