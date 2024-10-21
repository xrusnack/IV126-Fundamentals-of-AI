from typing import List

def allDifferent(cities: List[int]) -> bool:
    return len(cities) == len(set(cities))

