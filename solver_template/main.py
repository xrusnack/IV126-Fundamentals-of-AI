from typing import Any
import random
import sys
import json
import time


def read_instance_json(file_path: str):
    with open(file_path) as f:
        return json.load(f)


def write_instance_json(solution: Any, file_path: str):
    with open(file_path, 'w') as f:
        json.dump(solution, f)


if __name__ == "__main__":
    # Check if the correct number of arguments were provided
    if len(sys.argv) != 3:
        print("Usage: python3 main.py <instance-file-path> <solution-file-path>")
        sys.exit(1)

    instance_path = sys.argv[1]
    output_path = sys.argv[2]

    instance = read_instance_json(instance_path)
    naive_solution = [i for i in range(len(instance['Matrix']))] # TODO - implement something better
    write_instance_json(naive_solution, output_path)


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

