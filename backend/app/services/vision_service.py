import numpy as np
from app.kolam_analysis import image_processor, analyzer

def analyze_kolam_image(cv_image: np.ndarray) -> tuple:
    """
    Orchestrates the full computer vision pipeline for a kolam image.
    Returns a dictionary with the analysis results.
    """
    import time
    start_time = time.time()
    print(f"Starting analysis at {start_time}")

    # 1. Preprocess the image to get a clean binary version
    print("Preprocessing image...")
    preprocessed_image = image_processor.preprocess_image(cv_image)
    print(f"Preprocessing done in {time.time() - start_time} seconds")
    print(f"Image shape: {cv_image.shape}, Preprocessed shape: {preprocessed_image.shape if preprocessed_image is not None else 'None'}")

    # 2. Detect the dots (pullis) from the original image for accuracy
    print("Detecting dots...")
    dots = image_processor.detect_dots(cv_image)
    print(f"Detected {len(dots)} dots in {time.time() - start_time} seconds")
    if dots:
        print(f"Sample dot positions: {[(d.x, d.y, d.radius) for d in dots[:3]]}")
    else:
        print("No dots detected - checking image properties...")
        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        print(f"Image mean intensity: {np.mean(gray):.2f}, std: {np.std(gray):.2f}")

    # 3. Initialize the analyzer and perform high-level analysis
    print("Building graph...")
    analysis_instance = analyzer.KolamAnalyzer(cv_image.shape)
    pattern = analysis_instance.build_graph(dots, preprocessed_image)
    print(f"Graph built with {len(pattern.dots)} dots, {len(pattern.lines)} lines in {time.time() - start_time} seconds")

    print("Analyzing pattern...")
    final_pattern = analysis_instance.analyze_pattern(pattern)
    print(f"Analysis done in {time.time() - start_time} seconds")

    # 4. Serialize the results into a dictionary for the AI service
    results = {
        "dot_count": final_pattern.analysis.dot_count,
        "line_count": final_pattern.analysis.line_count,
        "symmetry_score": round(final_pattern.analysis.symmetry_score, 2),
        "rotational_symmetry_fold": final_pattern.analysis.rotational_fold,
        "closed_loops": final_pattern.analysis.loops,
        "connectivity": final_pattern.analysis.connectivity,
        "is_eulerian": final_pattern.analysis.has_eulerian_path,
        "grid_pattern": final_pattern.analysis.grid_pattern,
        "region": final_pattern.analysis.region
    }
    print(f"Total analysis time: {time.time() - start_time} seconds")
    return results, final_pattern