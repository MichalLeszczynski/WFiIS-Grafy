from dataclasses import dataclass
from typing import Any, List, Dict, Set


Weight = int
Matrix = List[List[int]]
Node = int
AdjacencyList = Dict[int, Set[int]]
AdjacencyMatrix = List[List[int]]
IncidenceMatrix = List[List[int]]


@dataclass
class Edge:
    begin: Node
    end: Node
    weight: Weight = 1

    def __str__(self) -> str:
        s = f"{self.begin} -> {self.end} w: {self.weight}"
        return s

    def __hash__(self) -> Any:
        return hash(str(self))

    def sort(self) -> None:  # tylko do grafów prostych!
        if self.begin > self.end:
            self.begin, self.end = self.end, self.begin
