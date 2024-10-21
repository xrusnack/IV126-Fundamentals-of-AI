import random
from typing import List, Tuple, Dict


class DestroyMethods:
    @staticmethod
    def count_cost(del_indices: List[int], solution: List[int], solution_cost: float,
                       distance_matrix: List[List[float]]) -> float:
        """
        This method incrementally calculates the updated cost of the solution after
        the removal of the selected cities and returns it.
        Indices of the cities that are to be removed are specified in the argument
        del_indices.

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


    @staticmethod
    def random(solution: List[int], solution_cost: float,
                      distance_matrix: List[List[float]]) -> Tuple[List[int], float]:
        """
        This method randomly removes up to half of the cities from the current solution
        and returns  tuple (list of destroyed cities, new solution cost).

        Note: The solution is modified in-place (the cities are removed).
        """
        n = len(solution) // 2 # random.randint(1, max(1, len(solution) // 2))
        del_indices = random.sample(range(len(solution)), n)
        del_cities = [solution[i] for i in del_indices]
        new_cost = DestroyMethods.count_cost(del_indices, solution, solution_cost, distance_matrix)

        return del_cities, new_cost


    @staticmethod
    def n_worst_cases(solution: List[int], solution_cost: float, n: int,
                                  distance_matrix: List[List[float]]) -> Tuple[List[int], float]:
        """
        This method removes the specified number of cities based on the distance matrix
        and returns a tuple (list of destroyed cities, new solution cost).
        The distance is calculated as a sum of distances to the two neighbours.

        Note: The solution is modified in-place (the cities are removed).
        """
        neighbor_lengths: Dict[int, float] = {}  # city index : sum of lengths to 2 neighbors

        for i, city in enumerate(solution):
            prev = (i - 1) % len(solution)
            next = (i + 1) % len(solution)
            neighbor_lengths[i] = distance_matrix[city][solution[prev]] + distance_matrix[city][solution[next]]

        sorted_lengths = sorted(neighbor_lengths.items(), key=lambda item: item[1], reverse=True)
        del_indices = [city_index for city_index, value in sorted_lengths[:n]]
        del_cities = [solution[i] for i in del_indices]
        new_cost = DestroyMethods.count_cost(del_indices, solution, solution_cost, distance_matrix)

        return del_cities, new_cost
