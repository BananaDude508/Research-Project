def clamped(value, min, max) -> float:
    if min <= value <= max:
        return value
    if min >= value:
        return min
    if max <= value:
        return max

def sign(value) -> int:
    return value/abs(value)