from typing import List, Callable, Tuple
import logging
import random

from initial_solutions import InitialSolutions
from destroy_methods import DestroyMethods
from repair_methods import RepairMethods


# Setup
LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='[%(asctime)s][%(levelname)-5.5s][%(name)-.20s] %(message)s')


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
    def __init__(self):
        LOG.info("Optimizer initialized!")

        self.steps_not_improved = 0

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
            RepairMethods.random,
            RepairMethods.greedy,
        ]
        
        self.current_init_method: int = 1
        self.current_destroy_method: int = 2
        self.current_repair_method: int = 1
        self.use_two_opt = False
    
    def initial(self, city_count: int, distance_matrix: List[List[float]]):
        fn = self.init_methods[self.current_init_method]

        return fn(city_count, distance_matrix)

    def _check(self):
        if self.steps_not_improved > 40:
            self.steps_not_improved = 0
            
            if self.use_two_opt == False:
                LOG.info("Enabling two_opt!")
                self.use_two_opt = True
            else:
                LOG.info("Disabling two_opt!")
                self.use_two_opt = False

                # available_options = list(
                #     set(range(len(self.destroy_methods)))
                #     - {self.current_destroy_method}
                # )
                # self.current_destroy_method = random.choice(available_options)
                last_destroy_method = self.current_destroy_method
                self.current_destroy_method = (self.current_destroy_method + 1) % len(self.destroy_methods)
                new_destroy_name = self.destroy_methods[self.current_destroy_method].__name__
                last_destroy_method_name = self.destroy_methods[last_destroy_method].__name__

                if self.current_destroy_method < last_destroy_method:
                    last_repair_method_name = self.repair_methods[self.current_repair_method].__name__
                    self.current_repair_method = (self.current_repair_method + 1) % len(self.repair_methods)
                    new_repair_name = self.repair_methods[self.current_repair_method].__name__
                    LOG.info(f"Didn't improve for a while, changing destroy method from \"{last_destroy_method_name}\" to \"{new_destroy_name}\" and repair method from \"{last_repair_method_name}\" to \"{new_repair_name}\"!") 
                else: 
                    LOG.info(f"Didn't improve for a while, changing destroy from \"{last_destroy_method_name}\" method to \"{new_destroy_name}\"!") 

    
    def destroy(
        self,
        solution: List[int],
        solution_cost: float,
        distance_matrix: List[List[float]]
    ):
        self._check()

        fn = self.destroy_methods[self.current_destroy_method]

        res = fn(solution, solution_cost, distance_matrix)

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

        if self.use_two_opt:
            res = RepairMethods.two_opt(solution, res, distance_matrix)

        return res

    def improved(self):
        # LOG.info("Improving!")
        self.steps_not_improved = 0
