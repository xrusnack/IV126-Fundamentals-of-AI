from typing import List
import math
import time
import random
import logging

from utils import write_instance_json
from initial_solutions import InitialSolutions
from repair_methods import RepairMethods
from destroy_methods import DestroyMethods


LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.WARN, format='[%(asctime)s][%(levelname)-5.5s][%(name)-.20s] %(message)s')


class LNSSolver:
    def __init__(self, distance_matrix: List[List[float]], time_limit: float,
                 output_path: str, alpha: float = 0.997):

        self.distance_matrix = distance_matrix
        self.city_count = len(distance_matrix[0])
        self.T_initial = 6000
        self.alpha = alpha
        self.time_limit = time_limit
        self.output_path = output_path

        self.best_solution = list(range(self.city_count))
        self.best_solution_cost = float('inf')


    def solve(self):
        """
        This method is a LNS metaheuristic with a simulated annealing approach to accepting new solutions.
        It uses random destroy method and greedy repair followed by 2-opt.
        """
        start_time = time.time()
        if not self.city_count > 0:
            return

        curr_solution, curr_solution_cost = InitialSolutions.greedy(self.city_count, self.distance_matrix)
        self.best_solution = curr_solution.copy()
        self.best_solution_cost = curr_solution_cost

        T = self.T_initial  # initialize the temperature

        delta_time = time.time() - start_time
        while delta_time < self.time_limit: # timelimit is the stopping condition
            explored_solution = curr_solution.copy()
            deleted_cities, explored_solution_cost = DestroyMethods.random(
                explored_solution, curr_solution_cost,self.distance_matrix
            )
            explored_solution_cost = RepairMethods.greedy(
                explored_solution, explored_solution_cost, deleted_cities, self.distance_matrix
            )
            explored_solution_cost = RepairMethods.two_opt(
                explored_solution, explored_solution_cost, self.distance_matrix
            )
            if explored_solution_cost < self.best_solution_cost:
                self.best_solution = explored_solution.copy()
                self.best_solution_cost = explored_solution_cost

                # Checkpoint the best solution
                write_instance_json(self.best_solution, self.output_path)

            # Solution acceptance:
            delta_cost = explored_solution_cost - curr_solution_cost
            if delta_cost < 0:
                curr_solution, curr_solution_cost = explored_solution.copy(), explored_solution_cost
            else:
                acceptance_prob = math.exp(-delta_cost / T)
                if random.random() < acceptance_prob:
                    curr_solution, curr_solution_cost = explored_solution.copy(), explored_solution_cost

            T *= self.alpha  # cool the temperature
            delta_time = time.time() - start_time

        assert len(self.best_solution) == len(set(self.best_solution))

        LOG.info(f"Best found solution: {self.best_solution}")
        LOG.info(f"Best found solution cost = {self.best_solution_cost}")
        LOG.info(f"Best found solution cost trivial count = {RepairMethods.count_cost_trivial(self.best_solution, self.distance_matrix)}")
