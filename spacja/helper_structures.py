from dataclasses import dataclass
from typing import Any, List


Weight = int
Matrix = List[List[int]]

@dataclass
class Node:
    index: int = 0

    def __str__(self) -> str:
        return str(self.index)

    def __hash__(self) -> Any:
        return hash(str(self))

    def __repr__(self):
        return self.__str__()


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

    def __repr__(self):
        return self.__str__()

    def sort(self) -> None:  # tylko do grafów prostych!
        if self.begin.index > self.end.index:
            self.begin, self.end = self.end, self.begin
