from typing import List
import os
import random
import sys
import json
import time
from initial_solutions import init_solution_greedy
from repair_methods import count_cost, greedy_repair
from destroy_logic import destroy_random, destroy_n_worst_cases


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


def accept(explored_solution_cost: int, current_solution_cost: int):  # accept improving solutions
    return explored_solution_cost < current_solution_cost


def LNS_metaheuristic(
    city_count: int,
    distance_matrix: List[List[int]],
    time_limit: int,
    start_time: int,
    steps: int=1500
) -> List[int]:
    curr_solution, curr_solution_cost = init_solution_greedy(city_count, distance_matrix)
    best_solution, best_solution_cost = curr_solution.copy(), curr_solution_cost

    assert city_count == len(best_solution)
    assert allDifferent(best_solution)

    for _ in range(steps):
        print(f'current solution ({len(curr_solution)}): ', curr_solution)
        print("current solution cost: ", curr_solution_cost)

        explored_solution = curr_solution.copy()
        #deleted_cities, explored_solution_cost = destroy_n_worst_cases(explored_solution, curr_solution_cost,
        #                                                               len(explored_solution) // 2, distance_matrix)
        deleted_cities, explored_solution_cost = destroy_random(explored_solution, curr_solution_cost, distance_matrix)

        print(f'deleted cities ({len(deleted_cities)}): {deleted_cities}')
        print(f'explored solution ({len(explored_solution)}): ', explored_solution)
        print("new cost: ", explored_solution_cost)
        #print("counted cost: ", count_cost(explored_solution, distance_matrix))
        #print()

        explored_solution_cost = greedy_repair(explored_solution, explored_solution_cost, deleted_cities, distance_matrix)
        print("repaired solution: ", explored_solution)
        print("repaired solution cost: ", explored_solution_cost)
        if explored_solution_cost < best_solution_cost:
            best_solution = explored_solution
            best_solution_cost = explored_solution_cost
        if accept(explored_solution_cost, curr_solution_cost):
            curr_solution = explored_solution
            curr_solution_cost = explored_solution_cost
        curr_time = time.time() - start_time
        if curr_time >= time_limit:
            print(curr_time, time_limit)
            break
        print()

    assert allDifferent(best_solution)
    print("Best found solution: ", best_solution)
    print("Best found solution cost = ", count_cost(best_solution, distance_matrix))
    print()

    return best_solution



if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 main.py <instance-file-path> <solution-file-path>")
        sys.exit(1)

    instance_path = sys.argv[1]
    output_path = sys.argv[2]

    instance = read_instance_json(instance_path)
    city_count = len(instance["Coordinates"])
    distance_matrix = instance["Matrix"]

    LNS_solution = LNS_metaheuristic(city_count, distance_matrix, instance['Timeout'], time.time())
    print("GlobalBest: ", instance["GlobalBest"], "GlobalBestVal: ", instance["GlobalBestVal"])

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

