from typing import List, Callable, Tuple, Dict
import logging
import random

from initial_solutions import InitialSolutions
from destroy_methods import DestroyMethods
from repair_methods import RepairMethods


# Setup
LOG = logging.getLogger(__name__)
# logging.basicConfig(level=logging.INFO, format='[%(asctime)s][%(levelname)-5.5s][%(name)-.20s] %(message)s')


# Types
InitialMethod = Callable[
    [
        int,
        List[List[float]]
    ],
    Tuple[List[int], float]
]

DestroyMethod = Callable[
    [
        List[int],
        float, List[List[float]]
    ],
    Tuple[List[int], float]
]
RepairMethod = Callable[
    [
        List[int],
        float,
        List[int],
        List[List[float]]
    ],
    float
]


class Optimizer:
    def __init__(self, distance_matrix: List[List[float]]):
        LOG.info("Optimizer initialized!")

        self.distance_matrix = distance_matrix
        self.city_count = len(distance_matrix[0])
        self.steps_not_improved = 0
        self.cost: List[float] = []
        self.distance_quantile = self._compute_distance_qunatile()

        self.init_methods: List[InitialMethod] = [
            InitialSolutions.random,
            InitialSolutions.greedy
        ]
        self.destroy_methods: List[DestroyMethod] = [
            DestroyMethods.random,
            DestroyMethods.n_worst_cases,
            DestroyMethods.shaw_removal
        ]
        self.repair_methods: List[RepairMethod] = [
            # RepairMethods.random,
            RepairMethods.greedy,
        ]
        
        self.current_init_method: int = 1
        self.current_destroy_method: int = 1
        self.current_repair_method: int = 0
        
        self.destroy_methods_config: Dict[str, Dict[str, float]] = {
            "random": {},
            "n_worst_cases": {
                "n": 10 if self.city_count > 10 else 3
            },
            "shaw_removal": {
                "n": 10 if self.city_count > 10 else 3,
                "alpha": self.distance_quantile
            }
        }

        init_name = self.init_methods[self.current_init_method].__name__
        destroy_name = self.destroy_methods[self.current_destroy_method].__name__
        repair_name = self.repair_methods[self.current_repair_method].__name__
        LOG.info(f"Default methods: {init_name}, {destroy_name}, {repair_name}. Using 2-opt as well!")

    def _compute_distance_qunatile(self, q: float=0.2) -> float:
        distances = [self.distance_matrix[i][j] for i in range(len(self.distance_matrix)) for j in range(i + 1, len(self.distance_matrix))]
        distances.sort()

        return distances[int(q * len(distances))]
    
    def initial(self, city_count: int, distance_matrix: List[List[float]]):
        fn = self.init_methods[self.current_init_method]

        return fn(city_count, distance_matrix)

    def _change_destroy_method(self):
        last_destroy_method = self.current_destroy_method
        self.current_destroy_method = (self.current_destroy_method + 1) % len(self.destroy_methods)
        new_destroy_name = self.destroy_methods[self.current_destroy_method].__name__
        last_destroy_method_name = self.destroy_methods[last_destroy_method].__name__
        
        LOG.info(f"Changing destroy from \"{last_destroy_method_name}\" method to \"{new_destroy_name}\"!")

        if self.current_destroy_method < last_destroy_method:
            last_repair_method_name = self.repair_methods[self.current_repair_method].__name__
            self.current_repair_method = (self.current_repair_method + 1) % len(self.repair_methods)
            new_repair_name = self.repair_methods[self.current_repair_method].__name__
            LOG.info(f"Changing repair method from \"{last_repair_method_name}\" to \"{new_repair_name}\"!")
    
    def _tweak_params(self):
        LOG.info("Tweaking parameters!")

        if self.current_destroy_method == 0:
            pass 
        elif self.current_destroy_method == 1:
            self.destroy_methods_config["n_worst_cases"]["n"] = min(
                self.city_count // 2,
                self.destroy_methods_config["n_worst_cases"]["n"] + 3
            )
        elif self.current_destroy_method == 2:
            if random.choice([True, False]):
                self.destroy_methods_config["shaw_removal"]["alpha"] = \
                    self.destroy_methods_config["shaw_removal"]["alpha"] \
                    + random.uniform(0.1, 0.5) * self.distance_quantile
            else:
                self.destroy_methods_config["shaw_removal"]["n"] = min(
                    self.city_count // 2,
                    self.destroy_methods_config["shaw_removal"]["n"] + 3
                )
        
    def _check(self):
        if self.steps_not_improved in [20, 38]:
            self._tweak_params()

        if self.steps_not_improved > 60:
            self.steps_not_improved = 0

            self._change_destroy_method()

    def destroy(
        self,
        solution: List[int],
        solution_cost: float,
        distance_matrix: List[List[float]]
    ):
        # self._check()

        fn = self.destroy_methods[self.current_destroy_method]
        fn_name = fn.__name__
        config = self.destroy_methods_config[fn_name]

        res = fn(solution, solution_cost, distance_matrix, **config)

        return res
    
    def repair(
        self,
        solution: List[int],
        solution_cost: float,
        deleted_cities: List[int],
        distance_matrix: List[List[float]]
    ):
        self._check()

        fn = self.repair_methods[self.current_repair_method]

        res = fn(solution, solution_cost, deleted_cities, distance_matrix)

        res = RepairMethods.two_opt(solution, res, distance_matrix)

        return res

    def improved(self):
        self.steps_not_improved = 0
    
    def stuck(self):
        self.steps_not_improved += 1
