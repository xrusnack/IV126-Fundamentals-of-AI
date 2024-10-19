import math
import random
from typing import List, Tuple


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
    n = random.randint(1, max(1, len(solution) // 2))
    del_indices = random.sample(range(len(solution)), n)
    del_cities = [solution[i] for i in del_indices]
    new_cost = count_cost_after_destroy(del_indices, solution, solution_cost, distance_matrix)

    return del_cities, new_cost


def destroy_single_worst_case(solution: List[int], solution_cost: int,
                              distance_matrix: List[List[int]]) -> Tuple[List[int], int]:
    """
    This function removes the single worst city based on the distance matrix.
    The distance is calculated as a sum of distances to the two neighbours.

    Returns: A tuple (list of destroyed cities, new solution cost).
    Note: The solution is modified in-place (the cities are removed).
    """
    destroyed_city_i = solution[0]
    destroyed_city = 0
    worst_path_length = -math.inf

    for i, city in enumerate(solution):
        prev = (i - 1) % len(solution)
        next = (i + 1) % len(solution)

        length = distance_matrix[city][solution[prev]] + distance_matrix[city][solution[next]]

        if length > worst_path_length:
            worst_path_length = length
            destroyed_city = city
            destroyed_city_i = i

    new_cost = count_cost_after_destroy([destroyed_city_i], solution, solution_cost, distance_matrix)

    return [destroyed_city], new_cost