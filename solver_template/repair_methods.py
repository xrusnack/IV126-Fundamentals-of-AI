import math
from typing import List, Tuple
import random


def count_cost(solution: List[int], distance_matrix: List[List[int]]) -> int:
    cost = 0
    for i in range(len(solution)):
        j = (i + 1) % len(solution)
        cost += distance_matrix[solution[i]][solution[j]]
    return cost


def count_cost_after_repair(index: int, city_to_insert: int, solution: List[int], distance_matrix: List[List[int]]) -> int:
    """
    This function incrementally calculates the updated cost of the solution after
    the insertion of the selected city. Index of the city that is to be inserted
    is specified in the argument index.

    Returns: The updated solution cost after the specified insertion (it does not modify the solution).
    """
    pred = solution[(index - 1) % len(solution)]
    succ = solution[index % len(solution)]

    insertion_cost = (distance_matrix[pred][city_to_insert] +
                      distance_matrix[city_to_insert][succ] -
                      distance_matrix[pred][succ])
    return insertion_cost


def random_repair(
    solution: List[int],
    solution_cost: int,
    deleted_cities: List[int],
    distance_matrix: List[List[int]]) -> int:
    """
    """

    while deleted_cities:
        city = deleted_cities.pop()

        index = random.randint(0, len(solution))
        insertion_cost = count_cost_after_repair(index, city, solution, distance_matrix)

        solution.insert(index, city)
        solution_cost += insertion_cost
    
    return solution_cost


def greedy_repair(solution: List[int], solution_cost: int, deleted_cities: List[int],
                  distance_matrix: List[List[int]]) -> int:
    """
    Repairs a solution by greedily reinserting deleted cities at positions that minimize
    the overall solution cost.

    Returns: The updated total solution cost after all deleted cities have been reinserted.
    Note: The solution is modified in-place (the deleted cities a reinserted).
    """

    while deleted_cities:
        lowest_cost = math.inf
        best_insertion = (0, deleted_cities[0])  # (best insertion index, best city)
        best_deletion = 0  # index in deleted_cities to be removed
        best_insertion_cost = math.inf

        for city_index, city in enumerate(deleted_cities):

            for insertion_point in range(len(solution)):
                insertion_cost = count_cost_after_repair(insertion_point, city, solution, distance_matrix)

                if insertion_cost < lowest_cost:
                    lowest_cost = insertion_cost
                    best_insertion = (insertion_point, city)
                    best_deletion = city_index
                    best_insertion_cost = insertion_cost

        solution.insert(best_insertion[0], best_insertion[1])
        solution_cost += best_insertion_cost
        deleted_cities.pop(best_deletion)

    return solution_cost


def two_opt_swap(solution: List[int], i_a: int, i_b: int):
    """
    Perform a 2-opt move on the route. The move swaps the order of the cities
    between the indices i_a and i_b (inclusive).
    """

    solution[i_a:i_b + 1] = solution[i_a:i_b + 1][::-1]


def _euclidean_distance(city_a: int, city_b: int, coords: List[Tuple[float, float]]) -> float:
    x1, y1 = coords[city_a]
    x2, y2 = coords[city_b]

    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def _distance(route: List[int], coords: List[Tuple[float, float]]) -> float:
    return sum(_euclidean_distance(route[i], route[i + 1], coords) for i in range(len(route) - 1))


def two_opt(
    solution: List[int],
    coords: List[Tuple[float, float]],
):
    best_solution = solution.copy()
    best_distance = _distance(best_solution, coords)

    for i in range(1, len(solution) - 1):
        for j in range(i + 1, len(solution)):
            # print(i, j)
            copy = best_solution.copy()
            two_opt_swap(copy, i, j)
            print(best_solution, copy)
            new_distance = _distance(best_solution, coords)

            if new_distance < best_distance:
                best_distance = new_distance
                best_solution = copy

    return best_solution
