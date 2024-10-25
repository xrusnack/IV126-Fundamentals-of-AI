from typing import List, Dict, Tuple, Optional, cast
import os
import json
import time
import logging
import math

import matplotlib.pyplot as plt

from initial_solutions import InitialSolutions
from destroy_methods import DestroyMethods
from repair_methods import RepairMethods


from typing import Dict, List, Literal

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
        _plot_route(coords, global_best[0], color="green", zorder=50, linestyle="--")
    
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
    timeout: int,
):
    coords = cast(Coordinates, instance["Coordinates"])
    city_count = len(coords)
    global_best = cast(Solution, instance["GlobalBest"])
    global_best_val = cast(float, instance["GlobalBestVal"])
    distance_matrix = cast(Matrix, instance["Matrix"])

    start_time = time.time()
    prev_time = start_time

    # INIT SOL
    # curr_solution, curr_solution_cost = InitialSolutions.random(city_count, distance_matrix)
    curr_solution, curr_solution_cost = InitialSolutions.greedy(city_count, distance_matrix)

    best_solution, best_solution_cost = curr_solution.copy(), curr_solution_cost

    assert city_count == len(best_solution)
    assert _all_different(best_solution)

    while True:
    # for _ in range(100):
        explored_sol = curr_solution.copy()

        # DESTROY
        deleted_cities, explored_sol_cost = DestroyMethods.random(explored_sol, curr_solution_cost, distance_matrix)
        # deleted_cities, explored_sol_cost = DestroyMethods.n_worst_cases(explored_sol, curr_solution_cost, 2, distance_matrix)
        # REPAIR
        explored_sol_cost = RepairMethods.greedy(explored_sol, explored_sol_cost, deleted_cities, distance_matrix)
        # explored_sol_cost = RepairMethods.greedy(explored_sol, explored_sol_cost, deleted_cities, distance_matrix)
        explored_sol_cost = RepairMethods.two_opt(explored_sol, explored_sol_cost, distance_matrix)

        
        if explored_sol_cost < curr_solution_cost:
            best_solution, best_solution_cost = explored_sol.copy(), explored_sol_cost
        
        if _accept(explored_sol_cost, curr_solution_cost):
            curr_solution, curr_solution_cost = explored_sol.copy(), explored_sol_cost
            LOG.info("Improving!")

        curr_time = time.time()
        if curr_time - prev_time > 5:
            LOG.info(f"Running for {int(curr_time - start_time)} seconds")
            prev_time = curr_time
        
        if curr_time - start_time > timeout:
            LOG.info("Killing after timeout reached.")
            break


        _plot_solution(coords, (best_solution, best_solution_cost), (global_best, global_best_val))

    assert _all_different(best_solution)

    return best_solution, best_solution_cost


def _run_single(name: str, instance: Instance):
    coords = cast(Coordinates, instance["Coordinates"])
    global_best = cast(Solution, instance["GlobalBest"])
    global_best_val = cast(float, instance["GlobalBestVal"])

    city_count = len(coords)
    timeout = cast(int, instance["Timeout"])

    LOG.info(f"Running LNS for instance \"{name}\" with {city_count} cities and timeout {timeout} seconds") 

    _plot_solution(coords, None, (global_best, global_best_val))

    best_solution, best_solution_cost = _lsn_test(instance, timeout)

    LOG.info(f"Best solution found cost: {best_solution_cost}")
    LOG.info(f"Global best cost: {global_best_val}")
    LOG.info(f"Difference: {best_solution_cost - global_best_val}")

    print("\n")

    _plot_solution(coords, (best_solution, best_solution_cost), (global_best, global_best_val))
    plt.show(block=True) # type: ignore

    return best_solution


def _run_all(instances: Dict[str, Instance]):
    for name, instance in instances.items():
        _run_single(name, instance)
    
    LOG.info("All instances processed.")


def _run():
    instances = _load_instances()

    # _run_all(instances)
    which = "tsp_76.json"
    _ = _run_single(which, instances[which])


if __name__ == "__main__":
    _run()
