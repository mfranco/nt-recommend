import math
import statistics


def msd(x, y):
    """
    Mean square difference
    https://en.wikipedia.org/wiki/Mean_squared_displacement
    """
    assert len(x) == len(y)
    assert len(x) > 0

    items = [
        (x[0] - x[1]) ** 2 for x in zip(x, y)
    ]
    return sum(items) / len(items)


def cosine(x, y):
    """
    cosine similarity
    https://en.wikipedia.org/wiki/Cosine_similarity
    """
    assert len(x) == len(y)
    above = []
    below_x = []
    below_y = []

    for i in zip(x, y):
        above.append(i[0] * i[1])
        below_x.append(i[0] ** 2)
        below_y.append(i[1] ** 2)

    below = math.sqrt(sum(below_x)) * math.sqrt(sum(below_y))

    if below == 0:
        return 0
    else:
        return sum(above) / below


def euclidean(x, y):
    """
    euclidean simiarity
    https://en.wikipedia.org/wiki/Euclidean_distance
    """
    assert len(y) == len(y)

    return math.sqrt(sum([
        (i[0] - i[1]) ** 2 for i in zip(x, y)
    ]))


def pearson(x, y):
    """
    https://en.wikipedia.org/wiki/Pearson_correlation_coefficient
    """
    assert len(y) == len(y)

    avg_x = statistics.mean(x)
    avg_y = statistics.mean(y)

    above = []
    below_x = []
    below_y = []

    for i in zip(x, y):
        above.append((i[0] - avg_x) * (i[1] - avg_y))
        below_x.append((i[0] - avg_x) ** 2)
        below_y.append((i[1] - avg_y) ** 2)
    below = math.sqrt(sum(below_x)) * math.sqrt(sum(below_y))

    if below == 0:
        return 0
    else:
        return sum(above) / below
