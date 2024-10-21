from typing import List
import os
import random
import sys
import json
import time
import math
from repair_methods import greedy_repair, two_opt, count_cost
from destroy_logic import destroy_random
from initial_solutions import init_solution_greedy
import utils


def read_instance_json(file_path: str):
    with open(file_path) as f:
        return json.load(f)


def write_instance_json(solution: List[int], file_path: str) -> None:
    folder = os.path.dirname(file_path)
    if folder:
        os.makedirs(folder, exist_ok=True)  # Create the directory if it doesn't exist
    with open(file_path, 'w') as f:
        json.dump(solution, f)


def simulated_annealing(distance_matrix: List[List[int]], time_limit: float, start_time: float, T_initial: float,
                        alpha: float, curr_solution: List[int], curr_solution_cost: int, steps = 1500) -> List[int]:

    best_solution, best_solution_cost = curr_solution.copy(), curr_solution_cost

    assert utils.allDifferent(best_solution)

    T = T_initial
    while True:
        explored_solution = curr_solution.copy()
        deleted_cities, explored_solution_cost = destroy_random(explored_solution, curr_solution_cost, distance_matrix)
        explored_solution_cost = greedy_repair(explored_solution, explored_solution_cost, deleted_cities,
                                               distance_matrix)
        explored_solution_cost = two_opt(explored_solution, explored_solution_cost, distance_matrix)

        if explored_solution_cost < best_solution_cost:
            best_solution,  best_solution_cost= explored_solution.copy(), explored_solution_cost

        delta_cost = explored_solution_cost - curr_solution_cost
        if delta_cost < 0:
            curr_solution, curr_solution_cost = explored_solution.copy(), explored_solution_cost
        else:
            acceptance_probability = math.exp(-delta_cost / T)
            if random.random() < acceptance_probability:
                curr_solution, curr_solution_cost = explored_solution.copy(), explored_solution_cost

        T *= alpha  # cool the temperature

        curr_time = time.time() - start_time
        if curr_time >= time_limit:
            break

    assert utils.allDifferent(best_solution)
    print("Best found solution: ", best_solution)
    print("Best found solution cost = ", count_cost(best_solution, distance_matrix))
    return best_solution


def LNS_metaheuristic(distance_matrix: List[List[int]], time_limit: float,
                      start_time: float, alpha = 0.997) -> List[int]:
    city_count = len(distance_matrix[0])
    curr_solution, curr_solution_cost = init_solution_greedy(city_count, distance_matrix)
    T_initial = math.sqrt(city_count)
    return simulated_annealing(distance_matrix, time_limit, start_time, T_initial, alpha, curr_solution, curr_solution_cost)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 main.py <instance-file-path> <solution-file-path>")
        sys.exit(1)

    instance_path = sys.argv[1]
    output_path = sys.argv[2]

    instance = read_instance_json(instance_path)

    LNS_solution = LNS_metaheuristic(instance["Matrix"], instance['Timeout'], time.time())

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

