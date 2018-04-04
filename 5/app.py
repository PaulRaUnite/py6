from typing import Iterable


def printer(f: callable) -> callable:
    def g(*args):
        try:
            print(f(args))
        except Exception as e:
            print(e)
    return g


@printer
def minimum(*args) -> int:
    stack = list(args)
    expanded = list()
    while len(stack) > 0:
        elem = stack.pop()
        if isinstance(elem, str):
            expanded.append(elem)
        if isinstance(elem, Iterable):
            if isinstance(elem, dict):
                stack += elem.items()
            stack.extend(elem)
        else:
            expanded.append(elem)

    if len(expanded) == 0:
        raise ValueError("there must be at least one value")
    try:
        numerical = map(lambda x: int(x), expanded)
    except (ValueError, TypeError):
        raise TypeError("arguments must be numeric values or their collections only")

    min: int = next(numerical)
    for elem in numerical:
        if elem < min:
            min = elem
    return min


minimum(1, 2, [1, 2, 3], {1, 2, 3}, (1, 2, 3), [[3, 3]], {1: 2, 3: -1})
minimum([[[[[[]]]]]])
minimum(tuple())
minimum(list)
