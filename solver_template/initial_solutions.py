import random
from repair_methods import count_cost
from typing import Tuple, List


def init_solution_random(city_count: int, distance_matrix: List[List[int]]) -> Tuple[List[int], int]:
    """
    The most basic initial solution - random permutation of cities.

    Returns: A tuple (initial solution, cost).
    """
    cities = list(range(city_count))
    random.shuffle(cities)
    cost = count_cost(cities, distance_matrix)
    return cities, cost


def init_solution_greedy(city_count: int, distance_matrix: List[List[int]]) -> Tuple[List[int], int]:
    """
    Slightly more complex initial solution - greedy algorithm.
    Starts with random city and iteratively adds the closest unvisited city.

    Returns: A tuple (initial solution, cost).
    """
    unvisited = set(range(city_count))
    current_city = unvisited.pop()

    solution = [current_city]
    solution_cost = 0

    while unvisited:
        next_city = min(unvisited, key=lambda city: distance_matrix[current_city][city])
        unvisited.remove(next_city)
        solution.append(next_city)
        solution_cost += distance_matrix[current_city][next_city]
        current_city = next_city

    solution_cost += distance_matrix[current_city][solution[0]]  # the route is cyclic
    return solution, solution_cost


def init_solution_greedy_foreach():
    """
    Idea to improve basic greedy algo.
    Run it for every city as a starting point and return the best solution.
    """
    pass


def init_solution_chris_serd_algo():
    pass