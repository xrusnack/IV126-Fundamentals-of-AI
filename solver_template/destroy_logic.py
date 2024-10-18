import random
from typing import List


def destroy_naive(current_solution: List[int], city_count: int) -> List[int]:
    cities_to_delete_count = random.randint(1, max(1, city_count // 2))
    delete_indices = random.sample(range(city_count), cities_to_delete_count)
    deleted_cities = [current_solution[i] for i in
                      delete_indices]  # for the repair function to know which cities have been deleted
    for index in sorted(delete_indices, reverse=True):  # destroy part of the current_solution
        del current_solution[index]
    return deleted_cities
