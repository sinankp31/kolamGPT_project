from dataclasses import dataclass, field
from typing import List, Tuple, Any
import networkx as nx

# Using dataclasses is a modern Python feature that makes creating
# classes for storing data clean and simple.

@dataclass
class Dot:
    """Represents a single detected dot (pulli) with its coordinates and size."""
    x: int
    y: int
    radius: int

@dataclass
class Line:
    """Represents a line segment connecting two points."""
    p1: Tuple[int, int]
    p2: Tuple[int, int]

@dataclass
class AnalysisResult:
    """A container for all the calculated properties of the kolam."""
    dot_count: int = 0
    line_count: int = 0
    loops: int = 0
    connectivity: str = "N/A"
    has_eulerian_path: bool = False
    symmetry_score: float = 0.0
    rotational_fold: int = 1
    grid_pattern: str = "N/A"
    region: str = "N/A"

@dataclass
class KolamPattern:
    """The main data structure that holds all information about a single kolam."""
    dots: List[Dot] = field(default_factory=list)
    lines: List[Line] = field(default_factory=list)
    graph: nx.Graph = field(default_factory=nx.Graph)
    analysis: AnalysisResult = field(default_factory=AnalysisResult)