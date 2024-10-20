from typing import List


def allDifferent(cities: List[int]) -> bool:
    return len(cities) == len(set(cities))


def accept(explored_solution_cost: int, current_solution_cost: int):  # accept improving solutions
    return explored_solution_cost < current_solution_cost
