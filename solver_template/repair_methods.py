from typing import List, Tuple
import math
import itertools


class RepairMethods:
    @staticmethod
    def count_cost_trivial(solution: List[int], distance_matrix: List[List[float]]) -> float:
        """
        This method computes the total cost of traveling through the cities in the order
        specified by the solution list.

        Note: Used for testing (the LNS solver uses incremental evaluation of the cost function).
        """
        cost = 0
        for i in range(len(solution)):
            j = (i + 1) % len(solution)
            cost += distance_matrix[solution[i]][solution[j]]
        return cost


    @staticmethod
    def count_cost(index: int, city_to_insert: int, solution: List[int],
                                distance_matrix: List[List[float]]) -> float:
        """
        This method incrementally calculates the updated cost of the solution after
        the insertion of the selected city. Index of the city that is to be inserted
        is specified in the argument index.

        Returns: The updated solution cost after the specified insertion (it does not modify the solution).
        """
        pred = solution[(index - 1) % len(solution)]
        succ = solution[index % len(solution)]

        return (distance_matrix[pred][city_to_insert]
                + distance_matrix[city_to_insert][succ]
                - distance_matrix[pred][succ])


    @staticmethod
    def greedy(solution: List[int], solution_cost: float, deleted_cities: List[int],
                      distance_matrix: List[List[float]]) -> float:
        """
        This method repairs a solution by greedily reinserting deleted cities at positions that minimize
        the overall solution cost.

        Returns: The updated total solution cost after all deleted cities have been reinserted.
        Note: The solution is modified in-place (the deleted cities a reinserted).
        """

        while deleted_cities:
            lowest_cost = math.inf
            best_insertion = (0, deleted_cities[0])  # (the best insertion index, the best city)
            best_deletion = 0  # index in deleted_cities to be removed
            best_insertion_cost = math.inf

            for city_index, city in enumerate(deleted_cities):

                for insertion_point in range(len(solution)):
                    insertion_cost = RepairMethods.count_cost(insertion_point, city, solution, distance_matrix)
                    if insertion_cost < lowest_cost:
                        lowest_cost = insertion_cost
                        best_insertion = (insertion_point, city)
                        best_deletion = city_index
                        best_insertion_cost = insertion_cost

            solution.insert(best_insertion[0], best_insertion[1])
            solution_cost += best_insertion_cost
            deleted_cities.pop(best_deletion)

        return solution_cost


    @staticmethod
    def count_cost_after_swap(solution: List[int], solution_cost: float, vertex_indices: Tuple[int, int],
                                  distance_matrix: List[List[float]]) -> float:
        """
        This method incrementally computes the new cost of the solution
        after reversing the order of values in the list solution between
        the edge_indices (2-opt operation).
        """

        first: int = vertex_indices[0]
        last: int = vertex_indices[1]

        reverse_cost = solution_cost
        reverse_cost -= distance_matrix[solution[first]][solution[(first + 1) % len(solution)]]
        reverse_cost -= distance_matrix[solution[last]][solution[(last + 1) % len(solution)]]
        reverse_cost += distance_matrix[solution[first]][solution[last]]
        reverse_cost += distance_matrix[solution[(first + 1) % len(solution)]][solution[(last + 1) % len(solution)]]

        return reverse_cost


    @staticmethod
    def two_opt_swap(solution: List[int], i_a: int, i_b: int) -> None:
        """
        This method performs a 2-opt swap on the given solution - it reverses
        the order of the elements between the indices i_a and i_b (included).
        It is a helper method for 2-opt.
        """
        middle = (abs(i_a - i_b) + 1) // 2
        for _ in range(middle):
            solution[i_a], solution[i_b] = solution[i_b], solution[i_a]
            i_a += 1
            i_b -= 1


    @staticmethod
    def two_opt(solution: List[int], solution_cost: float, distance_matrix: List[List[float]]) -> float:
        """
        This method iteratively examines all possible pairs of cities in the solution
        to identify the best swap of 2 edges that results in the lowest cost.
        Each combination represents the first vertices of the edges that are to be swapped.
        It applies the swap and returns the updated cost of the solution.
        """
        best_solution_cost = solution_cost
        best_swap_indices = (0, 0)

        for vertex_indices in itertools.combinations(range(len(solution)), 2):
            solution_cost_after_swap = RepairMethods.count_cost_after_swap(solution, solution_cost,
                                                                           vertex_indices, distance_matrix)
            if solution_cost_after_swap < best_solution_cost:
                best_swap_indices = ((vertex_indices[0] + 1) % len(solution), vertex_indices[1])
                best_solution_cost = solution_cost_after_swap

        RepairMethods.two_opt_swap(solution, best_swap_indices[0], best_swap_indices[1])

        return best_solution_cost

