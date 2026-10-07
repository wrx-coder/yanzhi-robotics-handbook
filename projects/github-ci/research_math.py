"""用于 CI 的小型科研指标函数，拒绝空值与非有限输入。"""
import math


def rmse(predicted, expected):
    predicted, expected = list(predicted), list(expected)
    if not predicted or len(predicted)!=len(expected):
        raise ValueError('输入必须非空且长度相同')
    if not all(math.isfinite(x) for x in predicted+expected):
        raise ValueError('输入必须为有限数值')
    return math.sqrt(sum((a-b)**2 for a,b in zip(predicted,expected))/len(predicted))
