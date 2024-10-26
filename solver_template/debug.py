from typing import List, Dict, Tuple, Optional, cast, Literal
import os
import json
import time
import logging
import math
import random

import matplotlib.pyplot as plt

from optimizer import Optimizer

Root = Literal["Coordinates"] \
    | Literal["Matrix"] \
    | Literal["GlobalBest"] \
    | Literal["GlobalBestVal"] \
    | Literal["Timeout"]

Coordinates = List[Tuple[float, float]]
Matrix = List[List[float]]
Solution = List[int]

Data = List[List[int]] | List[int] | int

Instance = Dict[Root, Data] 


# Setup
plt.ion() # type: ignore
LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='[%(asctime)s][%(levelname)-5.5s][%(name)-.20s] %(message)s')


def _all_different(cities: Solution) -> bool:
    return len(cities) == len(set(cities))


def _accept(explored_solution_cost: float, current_solution_cost: float):  # accept improving solutions
    return explored_solution_cost < current_solution_cost


def _plot_route(
    coords: Coordinates,
    route: Solution,
    color: str="black",
    zorder: int=100,
    linestyle: str="-"
):
    route_coords = [coords[i] for i in route]
    route_coords.append(route_coords[0])

    x, y = zip(*route_coords)
    plt.plot(x, y, color=color, zorder=zorder, linestyle=linestyle) # type: ignore


def _plot_cities(coords: Coordinates):
    x, y = zip(*coords)

    plt.scatter(x, y, color='red', zorder=1000) # type: ignore
    for i, coord in enumerate(coords):
        plt.text(coord[0] + 0.2, coord[1] - 0.7, f"{i}", fontsize=8, color="purple", zorder=1000)  # type: ignore


def _plot_solution(
    coords: Coordinates,
    solution: Optional[Tuple[Solution, float]] = None,
    global_best: Optional[Tuple[Solution, float]] = None
):
    plt.cla()

    a = math.inf
    b: float = -1

    if solution:
        a = solution[1]
        _plot_route(coords, solution[0])
    if global_best:
        b = global_best[1]
        _plot_route(coords, global_best[0], color="orange", zorder=101, linestyle="--")
    
    _plot_cities(coords)

    plt.show(block=False) # type: ignore
    plt.title(f"Current cost: {a} | Global best cost: {b}") # type: ignore
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
    instance: Instance,
    timeout: int
):

    coords = cast(Coordinates, instance["Coordinates"])
    city_count = len(coords)
    global_best = cast(Solution, instance["GlobalBest"])
    global_best_val = cast(float, instance["GlobalBestVal"])
    distance_matrix = cast(Matrix, instance["Matrix"])

    optimizer = Optimizer(distance_matrix)

    start_time = time.time()
    prev_time = start_time
    delta_time: float = 0
    temperature: float = 100

    # INITIAL SOL
    curr_solution, curr_solution_cost = optimizer.initial(city_count, distance_matrix)
    best_solution, best_solution_cost = curr_solution.copy(), curr_solution_cost

    assert city_count == len(best_solution)
    assert _all_different(best_solution)

    while delta_time < timeout:
    # for _ in range(100):
        optimizer.cost.append(curr_solution_cost)
        explored_sol = curr_solution.copy()

        # DESTROY
        deleted_cities, explored_sol_cost = optimizer.destroy(explored_sol, curr_solution_cost, distance_matrix)
        # REPAIR
        explored_sol_cost = optimizer.repair(explored_sol, explored_sol_cost, deleted_cities, distance_matrix)
        
        if explored_sol_cost < curr_solution_cost:
            best_solution, best_solution_cost = explored_sol.copy(), explored_sol_cost
        else:
            # optimizer.steps_not_improved += 1
            optimizer.stuck()
        
        delta_cost = explored_sol_cost - curr_solution_cost
        if (
            delta_cost < 0 \
            or random.random() < math.exp(-delta_cost / temperature)
        ):
            curr_solution, curr_solution_cost = explored_sol.copy(), explored_sol_cost

        curr_time = time.time()
        if curr_time - prev_time > 5:
            LOG.info(f"Running for {int(curr_time - start_time)} seconds")
            prev_time = curr_time
        
        _plot_solution(coords, (curr_solution, curr_solution_cost), (global_best, global_best_val))

        temperature *= 0.97
        delta_time = time.time() - start_time
    
    LOG.info("Killing after timeout reached.")

    assert _all_different(best_solution)

    optimizer.cost.append(curr_solution_cost)
    
    return best_solution, best_solution_cost, optimizer


def _run_single(name: str, instance: Instance, block: bool =False):
    coords = cast(Coordinates, instance["Coordinates"])
    global_best = cast(Solution, instance["GlobalBest"])
    global_best_val = cast(float, instance["GlobalBestVal"])

    city_count = len(coords)
    timeout = cast(int, instance["Timeout"])

    LOG.info(f"Running LNS for instance \"{name}\" with {city_count} cities and timeout {timeout} seconds") 

    _plot_solution(coords, None, (global_best, global_best_val))

    best_solution, best_solution_cost, optimizer = _lsn_test(instance, timeout)

    LOG.info(f"Best solution found cost: {best_solution_cost}")
    LOG.info(f"Global best cost: {global_best_val}")
    LOG.info(f"Difference: {best_solution_cost - global_best_val}")

    print("\n")

    _plot_solution(coords, (best_solution, best_solution_cost), (global_best, global_best_val))
    plt.show(block=block) # type: ignore

    plt.plot(optimizer.cost, label="Cost")
    plt.show(block=block) # type: ignore

    return best_solution


def _run_all(instances: Dict[str, Instance]):
    for name, instance in instances.items():
        _run_single(name, instance)
    
    LOG.info("All instances processed.")


def _run():
    instances = _load_instances()

    # _run_all(instances)

    # which = "tsp_280.json"
    # which = "tsp_100_C.json"
    which = "tsp_280.json"
    _ = _run_single(which, instances[which], block=True)


if __name__ == "__main__":
    _run()
