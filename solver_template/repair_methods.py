import math
from typing import List

def count_cost(solution: List[int], distance_matrix: List[List[int]]) -> int:
    cost = 0
    for i in range(len(solution)):
        j = (i + 1) % len(solution)
        cost += distance_matrix[solution[i]][solution[j]]
    return cost


def count_cost_after_repair(index: int, city_to_insert: int, solution: List[int],
                            solution_cost: int, distance_matrix: List[List[int]]) -> int:
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
                insertion_cost = count_cost_after_repair(insertion_point, city, solution, solution_cost, distance_matrix)

                if insertion_cost < lowest_cost:
                    lowest_cost = insertion_cost
                    best_insertion = (insertion_point, city)
                    best_deletion = city_index
                    best_insertion_cost = insertion_cost

        solution.insert(best_insertion[0], best_insertion[1])
        solution_cost += best_insertion_cost
        deleted_cities.pop(best_deletion)

    return solution_cost
