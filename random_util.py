import random



# From https://stackoverflow.com/questions/14992521/python-weighted-random
def weighted_random(pairs):
    if len(pairs) == 0:
        raise ValueError("Pairs can't be zero")
    total = sum(pair[0] for pair in pairs)
    r = random.uniform(0, total)
    for (weight, value) in pairs:
        r -= weight
        if r <= 0:
            return value


def choice_optional(list):
    """" Returns random.choice if there are elements, None otherwise """
    if len(list) > 0:
        return random.choice(list)
    return None
