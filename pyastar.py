import ctypes
import numpy as np

lib = ctypes.cdll.LoadLibrary('astar.so')

astar = lib.astar
ndmat_f_type = np.ctypeslib.ndpointer(
    dtype=np.float32, ndim=1, flags='C_CONTIGUOUS')
ndmat_i_type = np.ctypeslib.ndpointer(
    dtype=np.int32, ndim=1, flags='C_CONTIGUOUS')
astar.restype = ctypes.c_float
astar.argtypes = [ndmat_f_type, ctypes.c_int, ctypes.c_int,
                  ctypes.c_int, ctypes.c_int,
                  ndmat_i_type]


def astar_path(weights, start, goal):
    assert weights.min(axis=None) >= 1., (
        'weights.min() = %.2f' % weights.min(axis=None))
    height, width = weights.shape
    start_idx = np.ravel_multi_index(start, (height, width))
    goal_idx = np.ravel_multi_index(goal, (height, width))

    paths = np.full(height * width, -1, dtype=np.int32)

    astar(weights.flatten(), height, width, start_idx, goal_idx, paths)

    coordinates = []
    path_idx = goal_idx
    while path_idx != start_idx:
        pi, pj = np.unravel_index(path_idx, (height, width))
        coordinates.append((pi, pj))

        path_idx = paths[path_idx]

    if coordinates:
        return np.vstack(coordinates[::-1])
    else:
        return np.array([])
