import math


def mean_squared_error(y_true, y_pred):

    assert len(y_pred) == len(y_true)
    l_ds = len(y_pred)
    if l_ds < 1:
        return 0

    return sum([
        ((x[0] - x[1]) ** 2) for x in zip(y_true, y_pred)
    ]) / l_ds


def root_mean_squared_error(y_true, y_pred):
    return math.sqrt(mean_squared_error(y_true, y_pred))
