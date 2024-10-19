from typing import Dict, List, Literal

Root = Literal["Coordinates"] \
    | Literal["Matrix"] \
    | Literal["GlobalBest"] \
    | Literal["GlobalBestVal"] \
    | Literal["Timeout"]

Data = List[List[int]] | List[int] | int

Instance = Dict[Root, Data]
