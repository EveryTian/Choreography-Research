#! python3
# coding: utf-8

"""
A Type Checker for Python Basic Data Types:
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
* Some restriction of usage:
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


# Simple tests:
if __name__ == '__main__':
    test_cases = {
        'Basic data type': [
            (1, int, True),
            (2, float, False),
            ('', str, True),
            ('str', complex, False),
            (False, bool, True),
            (check_type, function_type, True)
        ],
        'Simple compound data type - list': [
            ([], [int], True),
            ([], [str], True),
            ([], [[[str]]], True),
            ([1, 2, 3], [int], True),
            ([1, ''], [str], False),
            (1, [str], False)
        ],
        'Simple compound data type - set': [
            (set(), {int}, True),
            (set(), {(str, str)}, True),
            ({1, 2, 3}, {int}, True),
            ('', {str}, False),
            ([1, 2, 3], {int}, False)
        ],
        'Simple compound data type - dict': [
            ({}, {str: float}, True),
            ({1: 1, 2: 2}, {int: int}, True),
            ({'': False, ' ': True}, {str: bool}, True),
            (False, {bool: bool}, False)
        ],
        'Simple compound data type - tuple': [
            ((True,), (bool,), True),
            ((False, 1), (bool, int), True),
            ((1, 2, 3, 4), (int,), False),
            ((2, '', 1, ''), (int, str, int, int), False),
            (1, (int,), False),
            ({}, (int,), False)
        ],
        'Complex compound data type': [
            ((1, {2: [1]}), (int, {int: [int]}), True),
            ({1: (1, 2, 3)}, bool, False),
            ({'': [1, 23], 'qwe': [2], '//': []}, {str: [int]}, True),
            ({'': [1, 23], 'qwe': [2], '//': ['']}, {str: [int]}, False),
            ({'': {}, ' ': {}, '  ': {}}, {str: {int: int}}, True),
            ({'': {}, ' ': {}, '  ': {}}, {str: {str: (int, int, [str])}}, True),
            ({'12': {'23': (1, 2, [(1, 2, '', False)])}}, {str: {str: (int, int, [(int, int, str, bool)])}}, True),
            ({'12': {'23': (check_type, [(check_type,)])}}, {str: {str: (function_type, [(function_type,)])}}, True)

        ],
        'Test compound types as simple data types': [
            ({}, dict, True),
            ({1: '', '': 2,  None: None}, dict, True),
            ([], list, True),
            ([1, ''], list, True),
            ((1, 2, 3), tuple, True),
            ({1, ''}, set, True),
            ({'12': {'23': (1, 2, [1, (1, 2, '', False)])}}, {str: {str: (int, int, list)}}, True)
        ],
        'Type as type': [
            (int, type, True),
            (function_type, type, True),
            ({int}, {type}, True),
            ({type}, {type}, True)
        ]
    }
    for description in test_cases:
        print(description)
        for test_case in test_cases[description]:
            arg0 = test_case[0]
            arg1 = test_case[1]
            expected_result = test_case[2]
            print(' ', arg0, arg1, 'should_be', expected_result, end=' | ')
            real_result = check_type(arg0, arg1)
            if real_result == expected_result:
                print('PASSED')
            else:
                print('FAILED')
                import sys
                sys.stderr.write("    EXPECTED: %s\n    BUT GOT: %s\n" %
                                 (str(expected_result), str(real_result)))
                sys.exit(2)
