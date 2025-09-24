import numpy as np
import networkx as nx
from scipy.spatial.distance import cdist, pdist, squareform
from scipy.spatial import ConvexHull
from scipy.stats import linregress
from typing import List, Tuple, Dict
from .models import KolamPattern, Dot, Line
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score

class KolamAnalyzer:
    def __init__(self, image_shape):
        self.shape = image_shape

    def build_graph_advanced(self, dots: List[Dot], skeleton_image: np.ndarray) -> KolamPattern:
        """
        Advanced graph construction using multiple connection strategies and validation.
        """
        pattern = KolamPattern(dots=dots)
        if not dots or len(dots) < 2:
            return pattern

        # Add nodes with enhanced attributes
        for i, dot in enumerate(dots):
            pattern.graph.add_node(i, pos=(dot.x, dot.y), radius=dot.radius, weight=1.0)

        dot_array = np.array([[d.x, d.y] for d in dots])

        # Strategy 1: Direct line pixel analysis with improved filtering
        line_pixels = np.argwhere(skeleton_image > 0)
        if len(line_pixels) > 0:
            self._connect_via_line_pixels(pattern, dots, dot_array, line_pixels)

        # Strategy 2: Geometric proximity analysis
        self._connect_via_proximity(pattern, dots, dot_array)

        # Strategy 3: Pattern-aware connections
        self._connect_via_patterns(pattern, dots)

        # Strategy 4: Validate and optimize connections
        self._optimize_connections(pattern)

        return pattern

    def _connect_via_line_pixels(self, pattern: KolamPattern, dots: List[Dot],
                                dot_array: np.ndarray, line_pixels: np.ndarray) -> None:
        """Connect dots based on actual line pixels with advanced filtering."""
        # Use spatial indexing for efficiency
        from scipy.spatial import cKDTree
        tree = cKDTree(dot_array)

        connections = {}

        for y, x in line_pixels[::2]:  # Sample every other pixel for performance
            # Find dots within reasonable distance of this pixel
            distances, indices = tree.query([x, y], k=3, distance_upper_bound=30)

            valid_indices = indices[distances != np.inf]
            if len(valid_indices) >= 2:
                # Connect the two closest dots
                idx1, idx2 = valid_indices[:2]

                # Validate connection makes sense
                if self._validate_connection(dots[idx1], dots[idx2], (x, y)):
                    key = tuple(sorted([idx1, idx2]))
                    if key not in connections:
                        connections[key] = 0
                    connections[key] += 1

        # Create edges based on connection frequency
        for (idx1, idx2), frequency in connections.items():
            if frequency >= 2:  # Require multiple pixel confirmations
                if not pattern.graph.has_edge(idx1, idx2):
                    pattern.graph.add_edge(idx1, idx2, weight=frequency)
                    p1 = (dots[idx1].x, dots[idx1].y)
                    p2 = (dots[idx2].x, dots[idx2].y)
                    pattern.lines.append(Line(p1=p1, p2=p2))

    def _connect_via_proximity(self, pattern: KolamPattern, dots: List[Dot],
                              dot_array: np.ndarray) -> None:
        """Connect dots based on geometric proximity and pattern analysis."""
        # Calculate pairwise distances
        distances = pdist(dot_array)
        distance_matrix = squareform(distances)

        # Find reasonable connection distances based on pattern statistics
        mean_distance = np.mean(distances)
        std_distance = np.std(distances)

        # Adaptive threshold based on pattern density
        density_factor = len(dots) / (np.ptp(dot_array[:, 0]) * np.ptp(dot_array[:, 1]))
        threshold = mean_distance * (0.8 if density_factor > 0.001 else 1.2)

        # Connect dots within threshold
        n = len(dots)
        for i in range(n):
            for j in range(i + 1, n):
                if distance_matrix[i, j] <= threshold:
                    if self._validate_geometric_connection(dots[i], dots[j], pattern):
                        if not pattern.graph.has_edge(i, j):
                            pattern.graph.add_edge(i, j, weight=1.0, type='proximity')
                            pattern.lines.append(Line(
                                p1=(dots[i].x, dots[i].y),
                                p2=(dots[j].x, dots[j].y)
                            ))

    def _connect_via_patterns(self, pattern: KolamPattern, dots: List[Dot]) -> None:
        """Connect dots based on recognized kolam patterns."""
        # Detect grid patterns
        grid_info = detect_grid_pattern_advanced(dots)
        if grid_info['is_grid']:
            self._connect_grid_pattern(pattern, dots, grid_info)

        # Detect radial patterns
        radial_info = detect_radial_pattern(dots)
        if radial_info['is_radial']:
            self._connect_radial_pattern(pattern, dots, radial_info)

    def _connect_grid_pattern(self, pattern: KolamPattern, dots: List[Dot],
                             grid_info: Dict) -> None:
        """Connect dots following grid pattern rules."""
        rows, cols = grid_info['dimensions']

        # Create grid-based connections
        for i in range(rows):
            for j in range(cols):
                current_idx = i * cols + j
                if current_idx >= len(dots):
                    continue

                # Connect right
                if j < cols - 1:
                    right_idx = i * cols + (j + 1)
                    if right_idx < len(dots):
                        self._add_validated_edge(pattern, dots, current_idx, right_idx)

                # Connect down
                if i < rows - 1:
                    down_idx = (i + 1) * cols + j
                    if down_idx < len(dots):
                        self._add_validated_edge(pattern, dots, current_idx, down_idx)

    def _connect_radial_pattern(self, pattern: KolamPattern, dots: List[Dot],
                               radial_info: Dict) -> None:
        """Connect dots following radial pattern rules."""
        center = radial_info['center']

        # Sort dots by angle from center
        angles = []
        for dot in dots:
            angle = np.arctan2(dot.y - center[1], dot.x - center[0])
            angles.append((angle, dot))

        angles.sort(key=lambda x: x[0])

        # Connect dots in angular order (simplified radial pattern)
        for i in range(len(angles) - 1):
            idx1 = dots.index(angles[i][1])
            idx2 = dots.index(angles[i + 1][1])
            self._add_validated_edge(pattern, dots, idx1, idx2)

    def _add_validated_edge(self, pattern: KolamPattern, dots: List[Dot],
                           idx1: int, idx2: int) -> None:
        """Add edge only if it passes validation."""
        if not pattern.graph.has_edge(idx1, idx2):
            if self._validate_connection(dots[idx1], dots[idx2]):
                pattern.graph.add_edge(idx1, idx2, weight=1.0, type='pattern')
                pattern.lines.append(Line(
                    p1=(dots[idx1].x, dots[idx1].y),
                    p2=(dots[idx2].x, dots[idx2].y)
                ))

    def _validate_connection(self, dot1: Dot, dot2: Dot, line_point: Tuple[int, int] = None) -> bool:
        """Validate if a connection between two dots makes sense."""
        # Basic distance check
        distance = np.sqrt((dot1.x - dot2.x)**2 + (dot1.y - dot2.y)**2)
        if distance < 5 or distance > 200:  # Reasonable kolam line lengths
            return False

        # Angle diversity check (avoid too many connections from one dot)
        # This would be checked at graph level

        # Line point validation if provided
        if line_point is not None:
            # Check if line_point is reasonably on the line between dots
            # Using vector projection
            v1 = np.array([dot2.x - dot1.x, dot2.y - dot1.y])
            v2 = np.array([line_point[0] - dot1.x, line_point[1] - dot1.y])

            if np.linalg.norm(v1) > 0:
                projection = np.dot(v2, v1) / np.dot(v1, v1)
                if not (0 <= projection <= 1):
                    return False

                # Check perpendicular distance
                perp_distance = np.linalg.norm(v2 - projection * v1)
                if perp_distance > 10:  # Too far from line
                    return False

        return True

    def _validate_geometric_connection(self, dot1: Dot, dot2: Dot, pattern: KolamPattern) -> bool:
        """Validate connection based on geometric constraints."""
        # Avoid connecting dots that are too close to existing connections
        # This is a simplified version - could be enhanced with more sophisticated rules
        return self._validate_connection(dot1, dot2)

    def _optimize_connections(self, pattern: KolamPattern) -> None:
        """Optimize the graph by removing unlikely connections and adding missing ones."""
        # Remove edges that connect too many dots (hub detection)
        degrees = dict(pattern.graph.degree())
        avg_degree = np.mean(list(degrees.values()))

        edges_to_remove = []
        for node, degree in degrees.items():
            if degree > avg_degree * 2:  # Hub detection
                # Remove some edges from high-degree nodes
                neighbors = list(pattern.graph.neighbors(node))
                # Keep only the closest connections
                distances = [(np.linalg.norm(
                    np.array(pattern.graph.nodes[node]['pos']) -
                    np.array(pattern.graph.nodes[neighbor]['pos'])
                ), neighbor) for neighbor in neighbors]

                distances.sort()
                # Keep only the closest 60% of connections
                keep_count = max(2, int(len(distances) * 0.6))
                for _, neighbor in distances[keep_count:]:
                    if pattern.graph.has_edge(node, neighbor):
                        edges_to_remove.append((node, neighbor))

        for edge in edges_to_remove:
            pattern.graph.remove_edge(*edge)
            # Remove corresponding line
            pattern.lines = [line for line in pattern.lines
                           if not ((line.p1 == pattern.graph.nodes[edge[0]]['pos'] and
                                   line.p2 == pattern.graph.nodes[edge[1]]['pos']) or
                                  (line.p1 == pattern.graph.nodes[edge[1]]['pos'] and
                                   line.p2 == pattern.graph.nodes[edge[0]]['pos']))]

    # Legacy method for backward compatibility
    def build_graph(self, dots: List[Dot], skeleton_image: np.ndarray) -> KolamPattern:
        """Legacy graph building method."""
        return self.build_graph_advanced(dots, skeleton_image)

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

def detect_grid_pattern_advanced(dots: List[Dot]) -> Dict:
    """
    Advanced grid pattern detection using clustering and statistical analysis.
    """
    if len(dots) < 4:
        return {'is_grid': False, 'dimensions': (0, 0), 'confidence': 0.0}

    positions = np.array([[d.x, d.y] for d in dots])

    # Method 1: K-means clustering to find rows and columns
    max_clusters = min(len(dots) // 2, 10)
    best_score = -1
    best_dims = (0, 0)

    for n_clusters in range(2, max_clusters + 1):
        try:
            kmeans = KMeans(n_clusters=n_clusters, n_init=10, random_state=42)
            labels = kmeans.fit_predict(positions)

            if len(set(labels)) > 1:
                score = silhouette_score(positions, labels)
                if score > best_score:
                    best_score = score
                    # Estimate grid dimensions
                    rows = len(set(positions[:, 1]))  # Unique Y coordinates
                    cols = len(set(positions[:, 0]))  # Unique X coordinates
                    best_dims = (rows, cols)
        except:
            continue

    # Method 2: Statistical analysis of spacing
    x_coords = sorted(positions[:, 0])
    y_coords = sorted(positions[:, 1])

    x_diffs = np.diff(x_coords)
    y_diffs = np.diff(y_coords)

    # Check coefficient of variation (lower is more regular)
    x_cv = np.std(x_diffs) / np.mean(x_diffs) if len(x_diffs) > 0 else 1.0
    y_cv = np.std(y_diffs) / np.mean(y_diffs) if len(y_diffs) > 0 else 1.0

    regularity_score = 1.0 - min(x_cv, y_cv)

    # Determine if it's a grid
    is_grid = regularity_score > 0.7 and best_score > 0.3

    confidence = (regularity_score + min(best_score, 1.0)) / 2

    return {
        'is_grid': is_grid,
        'dimensions': best_dims,
        'confidence': confidence,
        'regularity_score': regularity_score
    }

def detect_radial_pattern(dots: List[Dot]) -> Dict:
    """
    Detect radial patterns common in kolam designs.
    """
    if len(dots) < 5:
        return {'is_radial': False, 'center': (0, 0), 'confidence': 0.0}

    positions = np.array([[d.x, d.y] for d in dots])

    # Find potential centers (centroid, median, etc.)
    centers = [
        np.mean(positions, axis=0),  # Centroid
        np.median(positions, axis=0),  # Median center
    ]

    best_center = None
    best_score = 0

    for center in centers:
        # Calculate distances and angles from center
        distances = np.linalg.norm(positions - center, axis=1)
        angles = np.arctan2(positions[:, 1] - center[1], positions[:, 0] - center[0])

        # Check for radial symmetry
        # Look for patterns in angle distributions
        angle_hist, _ = np.histogram(angles, bins=12)
        angle_uniformity = 1.0 - (np.std(angle_hist) / np.mean(angle_hist))

        # Check distance regularity (concentric circles)
        distance_hist, _ = np.histogram(distances, bins=5)
        distance_uniformity = 1.0 - (np.std(distance_hist) / np.mean(distance_hist))

        radial_score = (angle_uniformity + distance_uniformity) / 2

        if radial_score > best_score:
            best_score = radial_score
            best_center = center

    is_radial = best_score > 0.6

    return {
        'is_radial': is_radial,
        'center': tuple(best_center) if best_center is not None else (0, 0),
        'confidence': best_score
    }

def detect_grid_pattern(dots: List[Dot]) -> str:
    """Legacy function for backward compatibility."""
    result = detect_grid_pattern_advanced(dots)
    if result['is_grid']:
        rows, cols = result['dimensions']
        return f"{rows}x{cols} grid"
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