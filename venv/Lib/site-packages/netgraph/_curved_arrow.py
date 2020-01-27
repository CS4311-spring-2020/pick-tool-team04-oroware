#!/usr/bin/env python
import numpy as np
import matplotlib.patches
import matplotlib.pyplot as plt


def _get_parallel_path(path, delta):
    # initialise output
    orthogonal_unit_vector = np.zeros_like(path)

    tangents = path[2:] - path[:-2] # using the central difference approximation
    orthogonal_unit_vector[1:-1] = _get_orthogonal_unit_vector(tangents)

    # handle start and end points
    orthogonal_unit_vector[ 0] = _get_orthogonal_unit_vector(np.atleast_2d([path[ 1] - path[ 0]]))
    orthogonal_unit_vector[-1] = _get_orthogonal_unit_vector(np.atleast_2d([path[-1] - path[-2]]))

    return path + delta * orthogonal_unit_vector


def _get_orthogonal_unit_vector(v):
    # adapted from https://stackoverflow.com/a/16890776/2912349
    v = v / np.linalg.norm(v, axis=-1)[:, None] # unit vector
    w = np.c_[-v[:,1], v[:,0]]                  # orthogonal vector
    w = w / np.linalg.norm(w, axis=-1)[:, None] # orthogonal unit vector
    return w


def _shorten_path_by(path, distance):
    """
    Cut path off at the end by `distance`.
    """
    distance_to_end = np.linalg.norm(path - path[-1], axis=1)
    idx = np.where(distance_to_end - distance >= 0)[0][-1] # i.e. the last valid point

    # We could truncate the  path using `path[:idx+1]` and return here.
    # However, if the path is not densely sampled, the error will be large.
    # Therefor, we compute a point that is on the line from the last valid point to
    # the end point, and append it to the truncated path.
    vector = path[idx] - path[-1]
    unit_vector = vector / np.linalg.norm(vector)
    new_end_point = path[-1] + distance * unit_vector

    return np.concatenate([path[:idx+1], new_end_point[None, :]], axis=0)


class CurvedArrow(matplotlib.patches.Polygon):

    def __init__(self, path,
                 width       = 0.05,
                 head_width  = 0.10,
                 head_length = 0.15,
                 offset      = 0.,
                 shape       = 'full',
                 *args, **kwargs):

        # book keeping
        self.path        = path
        self.width       = width
        self.head_width  = head_width
        self.head_length = head_length
        self.shape       = shape
        self.offset      = offset

        vertices = self._get_vertices()
        matplotlib.patches.Polygon.__init__(self, list(map(tuple, vertices)),
                                            closed=True, *args, **kwargs)


    def _get_vertices(self):
        # Determine the actual endpoint (and hence path) of the arrow given the offset;
        # assume an ordered path from source to target, i.e. from arrow base to arrow head.
        arrow_path      = _shorten_path_by(self.path, self.offset)
        arrow_tail_path = _shorten_path_by(arrow_path, self.head_length)

        head_vertex_tip  = arrow_path[-1]
        head_vertex_base = arrow_tail_path[-1]
        (dx, dy), = _get_orthogonal_unit_vector(np.atleast_2d(head_vertex_tip - head_vertex_base)) * self.head_width / 2.

        if self.shape is 'full':
            tail_vertices_right = _get_parallel_path(arrow_tail_path, -self.width / 2.)
            tail_vertices_left  = _get_parallel_path(arrow_tail_path,  self.width / 2.)
            head_vertex_right = head_vertex_base - np.array([dx, dy])
            head_vertex_left  = head_vertex_base + np.array([dx, dy])

            vertices = np.concatenate([
                tail_vertices_right[::-1],
                tail_vertices_left,
                head_vertex_left[None,:],
                head_vertex_tip[None,:],
                head_vertex_right[None,:],
            ])

        elif self.shape is 'right':
            tail_vertices_right = _get_parallel_path(arrow_tail_path, -self.width / 2.)
            head_vertex_right  = head_vertex_base - np.array([dx, dy])

            vertices = np.concatenate([
                tail_vertices_right[::-1],
                arrow_tail_path,
                head_vertex_tip[None,:],
                head_vertex_right[None,:],
            ])

        elif self.shape is 'left':
            tail_vertices_left = _get_parallel_path(arrow_tail_path,  self.width / 2.)
            head_vertex_left = head_vertex_base + np.array([dx, dy])

            vertices = np.concatenate([
                arrow_tail_path[::-1],
                tail_vertices_left,
                head_vertex_left[None,:],
                head_vertex_tip[None,:],
            ])

        else:
            raise ValueError("Argument 'shape' needs to one of: 'left', 'right', 'full', not '{}'.".format(self.shape))

        return vertices


def test_simple_line():
    x = np.linspace(-1, 1, 1000)
    y = np.sqrt(1. - x**2)
    plot_arrow(x, y)


def test_complicated_line():

    random_points = np.random.rand(5, 2)

    # Adapted from https://stackoverflow.com/a/35007804/2912349
    import scipy.interpolate as si

    def scipy_bspline(cv, n=100, degree=3, periodic=False):
        """ Calculate n samples on a bspline

            cv :      Array ov control vertices
            n  :      Number of samples to return
            degree:   Curve degree
            periodic: True - Curve is closed
        """
        cv = np.asarray(cv)
        count = cv.shape[0]

        # Closed curve
        if periodic:
            kv = np.arange(-degree,count+degree+1)
            factor, fraction = divmod(count+degree+1, count)
            cv = np.roll(np.concatenate((cv,) * factor + (cv[:fraction],)),-1,axis=0)
            degree = np.clip(degree,1,degree)

        # Opened curve
        else:
            degree = np.clip(degree,1,count-1)
            kv = np.clip(np.arange(count+degree+1)-degree,0,count-degree)

        # Return samples
        max_param = count - (degree * (1-periodic))
        spl = si.BSpline(kv, cv, degree)
        return spl(np.linspace(0,max_param,n))

    x, y = scipy_bspline(random_points, n=1000).T
    plot_arrow(x, y)


def plot_arrow(x, y):
    path = np.c_[x, y]
    arrow = CurvedArrow(path,
                        width       = 0.05,
                        head_width  = 0.1,
                        head_length = 0.15,
                        offset      = 0.1,
                        facecolor   = 'red',
                        edgecolor   = 'black',
                        alpha       = 0.5,
                        shape       = 'full',
    )
    fig, ax = plt.subplots(1,1)
    ax.add_artist(arrow)
    ax.plot(x, y, color='black', alpha=0.1) # plot path for reference
    ax.set_aspect("equal")
    plt.show()


if __name__ == '__main__':
    plt.ion()
    test_simple_line()
    test_complicated_line()
