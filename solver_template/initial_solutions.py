import random

def init_solution_random(cityCount: int):
    cities = list(range(cityCount))
    random.shuffle(cities)

    return cities


def init_solution_spanning_tree():
    raise NotImplementedError


def init_solution_dijkstra():
    raise NotImplementedError
