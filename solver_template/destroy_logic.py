from typing import List, cast
from itypes import Instance
import random


def dl_random(solution: List[int], instance: Instance, n: int=5):
    """
    Most basic destroy logic - remove random cities.

    Returns the solution with None on the indices of destroyed cities
    and the list of indices (what cities were removed).
    """

    destroyed_cities: List[int] = []

    # Make sure there is enough "cities" to destroy
    n_to_destroy = min(n, len(solution))
    x = random.sample(list(enumerate(solution)), n_to_destroy)

    for i, city in x:
        destroyed_cities.append(city)
        solution[i] = None

    return solution, destroyed_cities


def dl_single_worst_case(
    solution: List[int],
    instance: Instance,
):
    """
    Destroy logic that removes a single worst city based on the distance matrix.
    The distance is calculated as a sum of distances to the two neighbours.

    Returns tuple (solution, destroyed_city, worst_path_length).
    With solution update such that the destroyed city has None on its index.
    worst_path_length is negative and equal to the length of the path
    destroyed.
    """

    destroyed_city_i = -1
    destroyed_city = -1
    worst_path_length = -1

    for i, city in enumerate(solution):
        prev = (i + len(solution) - 1) % len(solution)
        next = (i + 1) % len(solution)
        neighbours_indices = [solution[prev], solution[next]]

        length = (
            cast(int, instance["Matrix"][city][neighbours_indices[0]]) +
            cast(int, instance["Matrix"][city][neighbours_indices[1]])
        )

        if length > worst_path_length:
            worst_path_length = length
            destroyed_city = city
            destroyed_city_i = i

    solution[destroyed_city_i] = None

    return solution, destroyed_city, -worst_path_length
