from typing import List
import os
import random
import sys
import json
import time
from initial_solutions import init_solution_random
from repair_methods import greedy_repair
from destroy_logic import destroy_naive
from repair_methods import count_cost


def read_instance_json(file_path: str):
    with open(file_path) as f:
        return json.load(f)


def write_instance_json(solution: List[int], file_path: str) -> None:
    folder = os.path.dirname(file_path)
    if folder:
        os.makedirs(folder, exist_ok=True)  # Create the directory if it doesn't exist
    with open(file_path, 'w') as f:
        json.dump(solution, f)


def allDifferent(cities: List[int]) -> bool:
    return len(cities) == len(set(cities))


def accept(current_solution_cost: int, previous_solution: List[int]
           , distance_matrix: List[List[int]]):  # accept improving solutions
    return current_solution_cost < count_cost(previous_solution, distance_matrix)


def LNS_metaheuristic(instance: json, distance_matrix: List[List[int]]) -> List[int]:
    city_count: int = len(instance["Coordinates"])
    initial_solution = init_solution_random(city_count)
    print("initial solution: ", initial_solution)

    assert city_count == len(initial_solution)
    assert allDifferent(initial_solution)

    previous_solution = initial_solution
    best_solution = initial_solution
    for i in range(200):
        print(f'{i}.', end=" ")
        current_solution = previous_solution.copy()
        deleted_cities = destroy_naive(current_solution, city_count)
        print("deleted cities: ", deleted_cities)
        greedy_repair(current_solution, deleted_cities, distance_matrix)
        print("repaired solution: ", current_solution)

        current_solution_cost = count_cost(current_solution, distance_matrix)
        print("current solution cost: ", current_solution_cost)
        if current_solution_cost < count_cost(best_solution, distance_matrix):
            best_solution = current_solution
        if accept(current_solution_cost, previous_solution, distance_matrix):
            previous_solution = current_solution
        print()

    assert allDifferent(best_solution)

    return best_solution



if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 main.py <instance-file-path> <solution-file-path>")
        sys.exit(1)

    instance_path = sys.argv[1]
    output_path = sys.argv[2]

    instance = read_instance_json(instance_path)
    distance_matrix = instance["Matrix"]

    naive_solution = [i for i in range(len(instance['Matrix']))] # TODO - implement something better
    LNS_solution = LNS_metaheuristic(instance, distance_matrix)
    print("GlobalBest: ", instance["GlobalBest"], "GlobalBestVal: ", instance["GlobalBestVal"])
    print("Cost: ", count_cost(instance["GlobalBest"], distance_matrix))

    write_instance_json(LNS_solution, output_path)


#######################################################################
# Example of the required timeout mechanism within the LNS structure: #
#######################################################################
# ...
# time_limit = instance['Timeout']
# start_time = time.time()
# for iteration in range(9999999999):
#     ...logic of one search iteration...
#     if time.time() - start_time >= time_limit:
#         break
# ...
#######################################################################
#######################################################################

