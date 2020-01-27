#!/usr/bin/env python
import numpy as np
import matplotlib.patches
import matplotlib.pyplot as plt

from bspline import scipy_bspline


class StraightArrow(matplotlib.patches.Polygon):
    pass


class CurvedPatch(matplotlib.patches.Polygon):
    def __init__(self, path, width, *args, **kwargs):
        vertices = self.get_vertices(path, width)
        matplotlib.patches.Polygon.__init__(self, list(map(tuple, vertices)),
                                            closed=True,
                                            *args, **kwargs)

    def get_vertices(self, path, width):
        left = _get_parallel_path(path, -width/2)
        right = _get_parallel_path(path, width/2)
        full = np.concatenate([left, right[::-1]])
        return full


class CurvedArrow(matplotlib.patches.Polygon):

    def __init__(self, path,
                 width       = 0.001,
                 head_width  = None,
                 head_length = None,
                 offset      = 0.,
                 shape       = 'full',
                 *args, **kwargs):

        # book keeping
        self.path = path
        self.width = width
        self.head_width = head_width
        self.head_length = head_length
        self.shape = shape
        self.offset = offset

        vertices = self.set_vertices(path)

        matplotlib.patches.Polygon.__init__(self, list(map(tuple, vertices)), closed=True, *args, **kwargs)


    def set_vertices(self, path):

        # # Determine actual path given offset;
        # # this assumes an ordered path from source to target,
        # # or equivalently, from arrow base to to arrow head.
        # # TODO: we really should use interpolation here to find the
        # distance_to_endpoint = np.linalg.norm(path - path[:, -1])
        # idx = np.argmin(distance_to_endpoint - self.offset)
        # path = path[:idx]

        left = _get_parallel_path(path, -self.width/2)
        right = _get_parallel_path(path, self.width/2)
        full = np.concatenate([left, right[::-1]])

        return full


def _get_parallel_path(path, delta):
    # initialise output
    offset = np.zeros_like(path)

    # use the previous and the following point to
    # determine the tangent at each point in the path
    for ii in range(1, len(path)-1):
        offset[ii] += _get_shift(path[ii-1], path[ii+1], delta)

    # handle start and end points
    offset[0] = _get_shift(path[0], path[1], delta)
    offset[-1] = _get_shift(path[-2], path[-1], delta)

    return path + offset


def _get_shift(p1, p2, delta):
    # unpack coordinates
    x1, y1 = p1
    x2, y2 = p2

    # get orthogonal unit vector
    v = np.r_[x2-x1, y2-y1]   # vector between points
    v = np.r_[-v[1], v[0]]    # orthogonal vector
    v = v / np.linalg.norm(v) # orthogonal unit vector

    # rescale unit vector
    dx, dy = delta * v

    return dx, dy


def test():

    fig, ax = plt.subplots(1,1)

    x = np.linspace(-1, 1, 1000)
    y = np.sqrt(1. - x**2)

    path = np.c_[x, y]

    arrow = CurvedPatch(path, 0.1, facecolor='red', alpha=0.5)
    ax.add_artist(arrow)

    ax.plot(x, y)
    plt.show()


if __name__ == '__main__':
    test()
