#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""

"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

from _main import DraggableArtists

if __name__ == "__main__":

    c1 = Circle(np.random.rand(2), np.random.rand(), fc='b')
    c2 = Circle(np.random.rand(2), np.random.rand(), fc='r')
    c3 = Circle(np.random.rand(2), np.random.rand(), fc='g')
    circles = [c1,c2,c3]

    plt.ion()
    fig, ax = plt.subplots(1,1)
    ax.set(xlim=(-2,2), ylim=(-2,2))
    for c in circles:
        ax.add_artist(c)

    instance = DraggableArtists(circles)
