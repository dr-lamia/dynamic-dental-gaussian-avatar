import numpy as np
from src.rendering.wireframe_preview import projected_edges


def test_project_triangle():
    v = np.array([
        [0.,0.,10.],
        [1.,0.,10.],
        [0.,1.,10.],
    ])
    f = np.array([[0,1,2]])
    K = np.array([[100.,0.,50.],[0.,100.,50.],[0.,0.,1.]])
    W2C = np.eye(4)
    uv, edges = projected_edges(v,f,W2C,K)
    assert uv.shape == (3,2)
    assert len(edges) == 3
