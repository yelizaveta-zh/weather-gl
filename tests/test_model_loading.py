def test_model_loading():
    """Test function showing how to load a simple model"""

    vertices = [
        [0.0, 1.0, 0.0],
        [-1.0, -1.0, 1.0],
        [1.0, -1.0, 1.0],
        [0.0, -1.0, -1.0]
    ]

    faces = [
        [0, 1, 2],
        [0, 2, 3],
        [0, 3, 1],
        [1, 3, 2]
    ]

    normals = None

    return vertices, normals, faces
