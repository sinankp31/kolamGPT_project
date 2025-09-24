import numpy as np
import networkx as nx
from scipy.spatial.distance import cdist
from typing import List
from .models import KolamPattern, Dot, Line

class KolamAnalyzer:
    def __init__(self, image_shape):
        self.shape = image_shape

    def build_graph(self, dots: List[Dot], skeleton_image: np.ndarray) -> KolamPattern:
        """Builds a graph representation of the kolam by connecting the dots."""
        pattern = KolamPattern(dots=dots)
        if not dots: 
            return pattern

        # Add all detected dots as nodes in the graph
        dot_positions = {i: (dot.x, dot.y) for i, dot in enumerate(dots)}
        for i, pos in dot_positions.items():
            pattern.graph.add_node(i, pos=pos)
        
        dot_array = np.array([[d.x, d.y] for d in dots])
        # Get the coordinates of all "on" pixels in the processed line drawing
        line_pixels = np.argwhere(skeleton_image > 0)
        
        # A simple but effective method: for each pixel on a line, find the two
        # closest dots and create an edge between them. This connects the dots
        # that form the endpoints of the lines.
        for y, x in line_pixels:
            distances = cdist(np.array([[x, y]]), dot_array)
            if distances.shape[1] < 2: 
                continue # Not enough dots to form a line
            
            idx1, idx2 = np.argsort(distances[0])[:2]
            
            # Add the edge if it's not already in the graph
            if not pattern.graph.has_edge(idx1, idx2):
                pattern.graph.add_edge(idx1, idx2)
                p1 = (dots[idx1].x, dots[idx1].y)
                p2 = (dots[idx2].x, dots[idx2].y)
                pattern.lines.append(Line(p1=p1, p2=p2))
        return pattern

    def analyze_pattern(self, pattern: KolamPattern) -> KolamPattern:
        """Performs mathematical analysis on the generated graph."""
        if not pattern.dots or not pattern.graph.nodes:
            return pattern

        # --- Mathematical Principles using NetworkX ---
        try:
            pattern.analysis.loops = len(list(nx.cycle_basis(pattern.graph)))
            pattern.analysis.connectivity = "Connected" if nx.is_connected(pattern.graph) else "Disconnected"
            odd_degree_nodes = [n for n, d in pattern.graph.degree() if d % 2 != 0]
            # A graph has an Eulerian path if it has at most two nodes of odd degree.
            pattern.analysis.has_eulerian_path = len(odd_degree_nodes) <= 2
        except Exception as e:
            print(f"Graph analysis failed: {e}")

        pattern.analysis.dot_count = len(pattern.dots)
        pattern.analysis.line_count = len(pattern.lines)

        # Enhanced symmetry and grid calculations
        pattern.analysis.symmetry_score = calculate_symmetry_score(pattern)
        pattern.analysis.rotational_fold = detect_rotational_symmetry(pattern)
        pattern.analysis.grid_pattern = detect_grid_pattern(pattern.dots)
        pattern.analysis.region = detect_region(pattern)

        return pattern

def calculate_symmetry_score(pattern: KolamPattern) -> float:
    """Calculate a symmetry score based on graph properties and dot positions."""
    if not pattern.dots:
        return 0.0

    # Simple symmetry check: count symmetric edges
    symmetric_edges = 0
    total_edges = len(pattern.graph.edges)

    if total_edges == 0:
        return 0.0

    # For each edge, check if there's a symmetric counterpart
    for u, v in pattern.graph.edges:
        pos_u = pattern.graph.nodes[u]['pos']
        pos_v = pattern.graph.nodes[v]['pos']
        # Check reflection over vertical axis (simple approximation)
        reflected_u = (-pos_u[0], pos_u[1])
        reflected_v = (-pos_v[0], pos_v[1])

        # Find nodes at reflected positions
        reflected_u_node = None
        reflected_v_node = None
        for node, data in pattern.graph.nodes(data=True):
            if data['pos'] == reflected_u:
                reflected_u_node = node
            if data['pos'] == reflected_v:
                reflected_v_node = node

        if reflected_u_node is not None and reflected_v_node is not None:
            if pattern.graph.has_edge(reflected_u_node, reflected_v_node):
                symmetric_edges += 1

    return symmetric_edges / total_edges

def detect_rotational_symmetry(pattern: KolamPattern) -> int:
    """Detect the order of rotational symmetry."""
    if not pattern.dots:
        return 1

    # Simple check for 180 degree symmetry
    center = np.mean([[d.x, d.y] for d in pattern.dots], axis=0)
    rotated_positions = []
    for dot in pattern.dots:
        # Rotate 180 degrees around center
        dx = dot.x - center[0]
        dy = dot.y - center[1]
        rotated_x = center[0] - dx
        rotated_y = center[1] - dy
        rotated_positions.append((rotated_x, rotated_y))

    # Check if all rotated positions have corresponding dots
    matches = 0
    for rx, ry in rotated_positions:
        for dot in pattern.dots:
            if abs(dot.x - rx) < 5 and abs(dot.y - ry) < 5:  # tolerance
                matches += 1
                break

    if matches == len(pattern.dots):
        return 2  # 180 degree symmetry
    return 1  # no rotational symmetry detected

def detect_grid_pattern(dots: List[Dot]) -> str:
    """Detect if dots form a regular grid pattern."""
    if len(dots) < 4:
        return "Irregular"

    # Extract positions
    positions = np.array([[d.x, d.y] for d in dots])

    # Try to find grid dimensions
    # Sort by x and y
    x_coords = sorted(set(p[0] for p in positions))
    y_coords = sorted(set(p[1] for p in positions))

    if len(x_coords) > 1 and len(y_coords) > 1:
        # Check if spacing is regular
        x_diffs = [x_coords[i+1] - x_coords[i] for i in range(len(x_coords)-1)]
        y_diffs = [y_coords[i+1] - y_coords[i] for i in range(len(y_coords)-1)]

        x_regular = len(set(round(d, 1) for d in x_diffs)) == 1
        y_regular = len(set(round(d, 1) for d in y_diffs)) == 1

        if x_regular and y_regular:
            return f"{len(x_coords)}x{len(y_coords)} grid"
        elif x_regular:
            return f"{len(x_coords)} columns"
        elif y_regular:
            return f"{len(y_coords)} rows"

    return "Irregular"

def detect_region(pattern: KolamPattern) -> str:
    """Detect likely region of origin based on pattern characteristics."""
    dot_count = len(pattern.dots)
    line_count = len(pattern.lines)
    symmetry_score = pattern.analysis.symmetry_score
    loops = pattern.analysis.loops
    grid_pattern = pattern.analysis.grid_pattern

    # Basic region classification based on common characteristics
    # These are generalizations and may not be 100% accurate

    # Tamil Nadu: Often simple daily kolams, moderate complexity
    if dot_count <= 15 and symmetry_score < 0.5 and "irregular" in grid_pattern.lower():
        return "Tamil Nadu (simple daily kolam style)"

    # Karnataka: More decorative, higher symmetry
    elif symmetry_score >= 0.5 and loops > 2:
        return "Karnataka (decorative symmetrical style)"

    # Andhra Pradesh: Geometric, structured grids
    elif "grid" in grid_pattern.lower() and symmetry_score >= 0.3:
        return "Andhra Pradesh (geometric grid-based style)"

    # Kerala: Nature-inspired, often more complex
    elif dot_count > 20 or (line_count > 30 and loops > 3):
        return "Kerala (complex nature-inspired style)"

    # Default: Cannot determine with confidence
    else:
        return "Region undetermined - requires cultural context for accurate classification"