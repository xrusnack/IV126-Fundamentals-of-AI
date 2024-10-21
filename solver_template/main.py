from typing import List
import os
import sys
import json
import time
from LNS_solver import LNSSolver


def read_instance_json(file_path: str):
    with open(file_path) as f:
        return json.load(f)


def write_instance_json(solution: List[int], file_path: str) -> None:
    folder = os.path.dirname(file_path)
    if folder:
        os.makedirs(folder, exist_ok=True)  # Create the directory if it doesn't exist
    with open(file_path, 'w') as f:
        json.dump(solution, f)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 main.py <instance-file-path> <solution-file-path>")
        sys.exit(1)

    instance_path = sys.argv[1]
    output_path = sys.argv[2]

    instance = read_instance_json(instance_path)
    LNS_solver: LNSSolver = LNSSolver(instance["Matrix"], instance['Timeout'], time.time())
    LNS_solver.solve()

    print("GlobalBest: ", instance["GlobalBest"], "GlobalBestVal: ", instance["GlobalBestVal"])

    write_instance_json(LNS_solver.best_solution, output_path)


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
