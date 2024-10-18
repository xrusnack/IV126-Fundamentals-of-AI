from typing import List, Optional
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
    sol_copy: List[Optional[int]] = solution.copy()
    for _ in range(n_to_destroy):
        available_indices = [city_i for city_i in range(len(sol_copy)) if sol_copy[city_i] is not None]
        i = random.choice(available_indices)

        # assert sol_copy[i] is not None

        destroyed_cities.append(sol_copy[i])

        sol_copy[i] = None

    return sol_copy, destroyed_cities


def dl_single_worst_case(solution: List[int], instance: Instance):
    """
    Destroy logic that removes a single worst city based on the distance matrix.
    The distance is calculated as a sum of distances to the two neighbours.

    Returns the solution with None on the index of the destroyed city
    and the city that was removed.
    """

    destroyed_city_i = -1
    worst_path_length = -1

    for i, city in enumerate(solution):
        if i == 0:
            neighbours_indices = [solution[-1], solution[i+1]]
        elif i == len(solution) - 1:
            neighbours_indices = [solution[i-1], solution[0]]
        else:
            neighbours_indices = [solution[i-1], solution[i+1]]

        length = (
            instance["Matrix"][city][neighbours_indices[0]] +
            instance["Matrix"][city][neighbours_indices[1]]
        )

        if length > worst_path_length:
            worst_path_length = length
            destroyed_city_i = city

    city_i = solution.index(destroyed_city_i)
    sol_copy = solution.copy()
    sol_copy[city_i] = None

    return sol_copy, destroyed_city_i
