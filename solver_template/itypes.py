from typing import Dict, List, Literal

type Root = Literal["Coodinates"] \
    | Literal["Matrix"] \
    | Literal["GlobalBest"] \
    | Literal["GlobalBestVal"] \
    | Literal["Timeout"]

type Data = List[List[int]] | List[int] | int

type Instance = Dict[Root, Data]
