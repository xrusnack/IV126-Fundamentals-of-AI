import math
from typing import List


def count_cost(solution: List[int], distance_matrix: List[List[int]]) -> int:
    cost = 0
    for i in range(len(solution)):
        j = (i + 1) % len(solution)
        cost += distance_matrix[solution[i]][solution[j]]
    return cost


def greedy_repair(current_solution: List[int], deleted_cities: List[int], distance_matrix: List[List[int ]]) -> None:
    while deleted_cities:
        lowest_cost_global = math.inf
        best_insertion = (0, deleted_cities[0])  # (insertion index, city)
        best_deletion = 0

        for city_index, city in enumerate(deleted_cities):

            lowest_cost = math.inf
            best_insertion_point = 0

            for insertion_point in range(len(current_solution)):
                explored_solution = current_solution[:]
                explored_solution.insert(insertion_point, city)
                current_cost = count_cost(explored_solution, distance_matrix)
                if current_cost < lowest_cost:
                    lowest_cost = current_cost
                    best_insertion_point = insertion_point

            if lowest_cost < lowest_cost_global:
                lowest_cost_global = lowest_cost
                best_insertion = (best_insertion_point, city)
                best_deletion = city_index

        current_solution.insert(best_insertion[0], best_insertion[1])

        assert city_index < len(deleted_cities)
        deleted_cities.pop(best_deletion)





