import time
import random


def measure(func, *args):
    time_start = time.time()
    result = func(*args)
    time_end = time.time()
    print(
        "{name} took {time:.0f}s.".format(
            name=func.__name__, time=time_end - time_start
        )
    )
    return result


# Source: https://stackoverflow.com/a/17907695/6798201
def random_choice_except_index(choices, except_index):
    assert len(choices) > 1
    assert except_index >= 0 and except_index < len(choices)
    random_index = random.randint(0, len(choices) - 2)
    if random_index >= except_index:
        random_index += 1
    return choices[random_index]
