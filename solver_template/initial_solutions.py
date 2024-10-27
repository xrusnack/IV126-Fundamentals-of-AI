import random
from typing import Tuple, List
from itertools import permutations

from repair_methods import RepairMethods


class InitialSolutions:
    @staticmethod
    def random(city_count: int, distance_matrix: List[List[float]]) -> Tuple[List[int], float]:
        """
        The most basic initial solution - random permutation of cities.

        Returns: A tuple (initial solution, cost).
        """
        cities = list(range(city_count))
        random.shuffle(cities)
        cost = RepairMethods.count_cost_trivial(cities, distance_matrix)

        return cities, cost


    @staticmethod
    def greedy(city_count: int, distance_matrix: List[List[float]]) -> Tuple[List[int], float]:
        """
        Slightly more complex initial solution - greedy algorithm.
        Starts with random city and iteratively adds the closest unvisited city.

        Returns: A tuple (initial solution, cost).
        """
        unvisited = set(range(city_count))
        current_city = unvisited.pop()

        solution = [current_city]
        solution_cost: float = 0

        while unvisited:
            next_city = min(unvisited, key=lambda city: distance_matrix[current_city][city])
            unvisited.remove(next_city)
            solution.append(next_city)
            solution_cost += distance_matrix[current_city][next_city]
            current_city = next_city

        solution_cost += distance_matrix[current_city][solution[0]]  # the route is cyclic
        return solution, solution_cost


    @staticmethod
    def brute_force(distance_matrix: List[List[float]]):
        city_count = len(distance_matrix)

        cities = list(range(city_count))
        best_solution: List[int] = []
        best_solution_cost = float('inf')

        for route in permutations(cities):
            solution = list(route)
            current_distance = RepairMethods.count_cost_trivial(solution, distance_matrix)

            if current_distance < best_solution_cost:
                best_solution = solution
                best_solution_cost = current_distance
        
        return best_solution, best_solution_cost
