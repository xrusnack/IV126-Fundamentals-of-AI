import sys
from solver_template.lns_solver import LNSSolver

from utils import read_instance_json, write_instance_json


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 main.py <instance-file-path> <solution-file-path>")
        sys.exit(1)

    instance_path = sys.argv[1]
    output_path = sys.argv[2]

    instance = read_instance_json(instance_path)

    LNS_solver: LNSSolver = LNSSolver(instance["Matrix"], instance['Timeout'], output_path)
    LNS_solver.solve()

    print("GlobalBest: ", instance["GlobalBest"], "GlobalBestVal: ", instance["GlobalBestVal"])

    write_instance_json(LNS_solver.best_solution, output_path)
