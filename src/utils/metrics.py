import numpy as np

def safe_div(a, b, eps: float = 1e-9):
    return a / (b + eps)
