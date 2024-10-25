from typing import List
import math
import time
import random
from initial_solutions import InitialSolutions
from repair_methods import RepairMethods
from destroy_methods import DestroyMethods


class LNSSolver:
    def __init__(self, distance_matrix: List[List[float]], time_limit: float, start_time: float, alpha: float = 0.997):
        self.distance_matrix = distance_matrix
        self.city_count = len(distance_matrix[0])
        self.T_initial = 6000
        self.alpha = alpha
        self.time_limit = time_limit
        self.start_time = start_time

        self.best_solution = list(range(self.city_count))
        self.best_solution_cost = float('inf')


    def solve(self):
        """
        This method is a LNS metaheuristic with a simulated annealing approach to accepting new solutions.
        """
        if not self.city_count > 0:
            return

        curr_solution, curr_solution_cost = InitialSolutions.greedy(self.city_count, self.distance_matrix)

        self.best_solution = curr_solution.copy()
        self.best_solution_cost = curr_solution_cost

        temperature = self.T_initial  # initialize the temperature
        while True:  # timelimit is the stopping condition
            explored_solution = curr_solution.copy()
            deleted_cities, explored_solution_cost = DestroyMethods.random(explored_solution, curr_solution_cost,
                                                                           self.distance_matrix)
            explored_solution_cost = RepairMethods.greedy(explored_solution, explored_solution_cost,
                                                          deleted_cities, self.distance_matrix)
            explored_solution_cost = RepairMethods.two_opt(explored_solution, explored_solution_cost,
                                                           self.distance_matrix)

            if explored_solution_cost < self.best_solution_cost:
                self.best_solution = explored_solution.copy()
                self.best_solution_cost = explored_solution_cost

            delta_cost = explored_solution_cost - curr_solution_cost
            if delta_cost < 0:
                curr_solution, curr_solution_cost = explored_solution.copy(), explored_solution_cost
            else:
                acceptance_prob= math.exp(-delta_cost / temperature)
                if random.random() < acceptance_prob:
                    curr_solution, curr_solution_cost = explored_solution.copy(), explored_solution_cost

            temperature *= self.alpha  # cool the temperature

            curr_time = time.time() - self.start_time
            if curr_time >= self.time_limit:
                break

        assert len(self.best_solution) == len(set(self.best_solution))

        print("Best found solution: ", self.best_solution)
        print("Best found solution cost = ", self.best_solution_cost)
        print("Best found solution cost counted = ", RepairMethods.count_cost_trivial(self.best_solution, self.distance_matrix))
