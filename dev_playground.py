from monad import *

def add(a, b):
    if b < 0:
        return b/0
    return a + b

test = Error(2)
test = test.apply(lambda x: add(x, 1))

match test.variant:
    case "Ok":
        print(f"It's fine: {test.unwrap()}")
    case "Error":
        print(f"It errored out: {test.unwrap()}")

test2 = Error(2)
test2 = test2.apply(lambda x: add(x, -1))

match test2.variant:
    case "Ok":
        print(f"It's fine: {test2.unwrap()}")
    case "Error":
        print(f"It errored out: {test2.unwrap()}")
