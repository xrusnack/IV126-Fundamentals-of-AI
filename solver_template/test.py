from typing import List, Dict, Tuple, Optional
import os
import json
import time
import logging
import math
import random

import matplotlib.pyplot as plt

from itypes import Instance
import initial_solutions
import destroy_logic
import repair_methods
import utils


# Setup
plt.ion()
LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='[%(asctime)s][%(levelname)-5.5s][%(name)-.20s] %(message)s')


def _plot_route(
    coords: List[Tuple[float, float]],
    route: List[int],
    color: str="black",
    zorder: int=100,
    linestyle: str="-"
):
    route_coords = [coords[i] for i in route]
    route_coords.append(route_coords[0])

    x, y = zip(*route_coords)
    plt.plot(x, y, color=color, zorder=zorder, linestyle=linestyle)


def _plot_cities(coords: List[Tuple[float, float]]):
    x, y = zip(*coords)

    plt.scatter(x, y, color='red', zorder=1000)
    for i, coord in enumerate(coords):
        plt.text(coord[0] + 0.2, coord[1] - 0.7, f"{i}", fontsize=8, color="purple", zorder=1000)  # f"{coords[0]:.2f}, {coords[1]:.2f}"


def _plot_solution(
    coords: List[Tuple[float, float]],
    solution: Optional[Tuple[List[int], float]] = None,
    global_best: Optional[Tuple[List[int], float]] = None
):
    plt.cla()

    a = math.inf
    b = -1

    if solution:
        a = solution[1]
        _plot_route(coords, solution[0])
    if global_best:
        b = global_best[1]
        _plot_route(coords, global_best[0], color="green", zorder=50, linestyle="--")
    
    _plot_cities(coords)

    plt.show(block=False)
    plt.title(f"Current cost: {a} | Global best cost: {b}")
    plt.pause(0.01)
    # plt.close()


def _load_instances() -> Dict[str, Instance]:
    instances: Dict[str, Instance] = dict()

    files = [
        file
        for file in os.listdir("data")
        if file.endswith(".json") and not file.startswith("_")
    ]

    for file in files:
        with open(f"data/{file}", "r") as f:
            instance_data = json.load(f)
            instances[file] = instance_data

    return instances


def _lsn_test(
    city_count: int,
    distance_matrix: List[List[int]],
    timeout: int,
    instance: Instance,
):
    start_time = time.time()
    prev_time = start_time

    # INIT SOL
    curr_solution, curr_solution_cost = initial_solutions.init_solution_random(city_count, distance_matrix)
    # curr_solution, curr_solution_cost = initial_solutions.init_solution_greedy(city_count, distance_matrix)

    best_solution, best_solution_cost = curr_solution.copy(), curr_solution_cost

    assert city_count == len(best_solution)
    assert utils.allDifferent(best_solution)

    # while True:
    for _ in range(100):
        explored_sol = curr_solution.copy()

        # DESTROY
        # deleted_cities, explored_sol_cost = destroy_logic.destroy_random(explored_sol, curr_solution_cost, distance_matrix)
        # deleted_cities, explored_sol_cost = destroy_logic.destroy_n_worst_cases(explored_sol, curr_solution_cost, 2, distance_matrix)
        explored_sol_cost = 1000
        # REPAIR
        # explored_sol_cost = repair_methods.random_repair(explored_sol, explored_sol_cost, deleted_cities, distance_matrix)
        # explored_sol_cost = repair_methods.greedy_repair(explored_sol, explored_sol_cost, deleted_cities, distance_matrix)
        explored_sol_cost = repair_methods.two_opt(
            explored_sol,
            random.randint(0, len(curr_solution)),
            random.randint(0, len(curr_solution)),
            explored_sol_cost,
            distance_matrix
        )

        if explored_sol_cost < curr_solution_cost:
            best_solution, best_solution_cost = explored_sol.copy(), explored_sol_cost
        
        if utils.accept(explored_sol_cost, curr_solution_cost):
            curr_solution, curr_solution_cost = explored_sol.copy(), explored_sol_cost
            LOG.info("Improving!")

        curr_time = time.time()
        if curr_time - prev_time > 5:
            LOG.info(f"Running for {int(curr_time - start_time)} seconds")
            prev_time = curr_time
        
        if curr_time - start_time > timeout:
            LOG.info("Killing after timeout reached.")
            break


        _plot_solution(instance["Coordinates"], (best_solution, best_solution_cost), (instance["GlobalBest"], instance["GlobalBestVal"]))

    assert utils.allDifferent(best_solution)

    return best_solution, best_solution_cost


def _run_single(name: str, instance: Instance):
    city_count = len(instance["Coordinates"])
    distance_matrix = instance["Matrix"]
    timeout = instance["Timeout"]

    LOG.info(f"Running LNS for instance \"{name}\" with {city_count} cities and timeout {timeout} seconds") 

    _plot_solution(instance["Coordinates"], None, (instance["GlobalBest"], instance["GlobalBestVal"]))

    best_solution, best_solution_cost = _lsn_test(city_count, distance_matrix, timeout, instance)

    LOG.info(f"Best solution found cost: {best_solution_cost}")
    LOG.info(f"Global best cost: {instance["GlobalBestVal"]}")
    LOG.info(f"Difference: {best_solution_cost - instance['GlobalBestVal']}")

    print("\n")

    _plot_solution(instance["Coordinates"], (best_solution, best_solution_cost), (instance["GlobalBest"], instance["GlobalBestVal"]))
    plt.show(block=True)

    return best_solution


def _run_all(instances: Dict[str, Instance]):
    for name, instance in instances.items():
        _run_single(name, instance)
    
    LOG.info("All instances processed.")


def _run():
    instances = _load_instances()

    # _run_all(instances)
    which = "tsp_22.json"
    sol = _run_single(which, instances[which])


if __name__ == "__main__":
    _run()
