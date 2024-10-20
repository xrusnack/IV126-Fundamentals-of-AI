import math
import random
from typing import List, Tuple, Dict


def count_cost_after_destroy(del_indices: List[int], solution: List[int], solution_cost: int,
                   distance_matrix: List[List[int]]) -> int:
    """
    This function incrementally calculates the updated cost of the solution after
    the removal of the selected cities. Indices of the cities that are to be removed
    are specified in the argument del_indices.

    Returns: The updated solution cost after the specified cities have been removed.
    Note: The solution is modified in-place (the cities are removed).
    """

    for i in sorted(del_indices, reverse=True):  # destroy a part of the solution
        curr = solution[i]
        pred = solution[(i - 1) % len(solution)]
        succ = solution[(i + 1) % len(solution)]

        solution_cost -= distance_matrix[curr][pred]
        solution_cost -= distance_matrix[curr][succ]
        solution_cost += distance_matrix[pred][succ]

        del solution[i]

    return solution_cost


def destroy_random(solution: List[int], solution_cost: int,
                  distance_matrix: List[List[int]]) -> Tuple[List[int], int]:
    """
    This function randomly removes up to half of the cities from the current solution.

    Returns: A tuple (list of destroyed cities, new solution cost).
    Note: The solution is modified in-place (the cities are removed).
    """
    n = len(solution) // 2 #random.randint(1, max(1, len(solution) // 2))
    del_indices = random.sample(range(len(solution)), n)
    del_cities = [solution[i] for i in del_indices]
    new_cost = count_cost_after_destroy(del_indices, solution, solution_cost, distance_matrix)

    return del_cities, new_cost


def destroy_n_worst_cases(solution: List[int], solution_cost: int, n: int,
                              distance_matrix: List[List[int]]) -> Tuple[List[int], int]:
    """
    This function removes the specified number of cities based on the distance matrix.
    The distance is calculated as a sum of distances to the two neighbours.

    Returns: A tuple (list of destroyed cities, new solution cost).
    Note: The solution is modified in-place (the cities are removed).
    """
    assert n > 0

    neighbor_lengths: Dict[int, int] = {}  # city index : sum of lengths to 2 neighbors

    for i, city in enumerate(solution):
        prev = (i - 1) % len(solution)
        next = (i + 1) % len(solution)
        neighbor_lengths[i] = distance_matrix[city][solution[prev]] + distance_matrix[city][solution[next]]

    sorted_lengths = sorted(neighbor_lengths.items(), key=lambda item: item[1], reverse=True)
    del_indices = [city_index for city_index, value in sorted_lengths[:n]]
    del_cities = [solution[i] for i in del_indices]
    new_cost = count_cost_after_destroy(del_indices, solution, solution_cost, distance_matrix)

    return del_cities, new_cost
