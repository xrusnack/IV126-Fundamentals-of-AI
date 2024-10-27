from typing import List
import json
import os
import logging


LOG = logging.getLogger(__name__)
logging.basicConfig(level=logging.WARN, format='[%(asctime)s][%(levelname)-5.5s][%(name)-.20s] %(message)s')


def read_instance_json(file_path: str):
    LOG.info(f"Reading instance from {file_path}")
    with open(file_path) as f:
        return json.load(f)


def write_instance_json(solution: List[int], file_path: str) -> None:
    LOG.info(f"Writing solution to {file_path}")
    folder = os.path.dirname(file_path)

    if folder:
        os.makedirs(folder, exist_ok=True)  # Create the directory if it doesn't exist
    
    with open(file_path, 'w') as f:
        json.dump(solution, f)
