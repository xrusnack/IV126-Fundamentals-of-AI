import random
from itypes import Instance


def init_solution_random(cityCount: int):
    """
    The most basic initial solution - random permutation of cities.    
    """

    cities = list(range(cityCount))
    random.shuffle(cities)

    return cities


def init_solution_greedy(instance: Instance):
    """
    Slightly more complex initial solution - greedy algorithm.
    Starts with random city and iteratively adds the closest unvisited city.
    """

    unvisited = set(range(len(instance["Coordinates"])))
    current_city = unvisited.pop()

    solution = [current_city]

    while unvisited:
        next_city = min(unvisited, key=lambda city: instance["Matrix"][current_city][city])
        unvisited.remove(next_city)
        solution.append(next_city)
        current_city = next_city

    return solution


def init_solution_greedy_foreach(instance: Instance):
    """
    Idea to improve basic greedy algo.
    Run it for every city as a starting point and return the best solution.
    """
    pass


def init_solution_chris_serd_algo(instance: Instance):
    pass
