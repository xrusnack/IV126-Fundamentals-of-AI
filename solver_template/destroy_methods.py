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
    def n_worst_cases(
        solution: List[int],
        solution_cost: float,
        distance_matrix: List[List[float]],
        n: int=10
    ) -> Tuple[List[int], float]:
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
        del_indices = [city_index for city_index, _ in sorted_lengths[:n]]
        del_cities = [solution[i] for i in del_indices]
        new_cost = DestroyMethods.count_cost(del_indices, solution, solution_cost, distance_matrix)

        return del_cities, new_cost

    @staticmethod
    def shaw_removal(
        solution: List[int],
        solution_cost: float,
        distance_matrix: List[List[float]],
        n: int=30,
        alpha: float=200
    ) -> Tuple[List[int], float]:
        """
        """
        assert len(solution) > 3

        # Setup reference values
        seed_city_i = random.randint(0, len(solution) - 1)
        seed_city_prev_i = (seed_city_i - 1) % len(solution)
        seed_city_next_i = (seed_city_i + 1) % len(solution)
        seed_city = solution[seed_city_i]
        seed_city_sum_distance = (
            distance_matrix[seed_city][solution[seed_city_prev_i]]
            + distance_matrix[seed_city][solution[seed_city_next_i]]
        )

        related_cities: List[Tuple[int, int, float]] = []

        # Calculate related cities
        for city_i, city in enumerate(solution):
            if city == seed_city:
                continue

            city_prev_i = (city_i - 1) % len(solution)
            city_next_i = (city_i + 1) % len(solution)
            city_sum_distance = (
                distance_matrix[city][solution[city_prev_i]]
                + distance_matrix[city][solution[city_next_i]]
            )
            related_cities.append((
                city,
                city_i,
                abs(city_sum_distance - seed_city_sum_distance),
            ))
        related_cities.sort(key=lambda x: x[2], reverse=True)

        deleted_cities: List[int] = [seed_city]
        deleted_cities_i: List[int] = [seed_city_i]

        popped = related_cities.pop()
        while n > 0 and popped[2] < alpha:
            deleted_cities.append(popped[0])
            deleted_cities_i.append(popped[1])
            n -= 1
            popped = related_cities.pop()

        return deleted_cities, DestroyMethods.count_cost(deleted_cities_i, solution, solution_cost, distance_matrix)
