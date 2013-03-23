from math import sqrt, floor
import numpy as np
import random

class PerlinNoise:
    """
    This class encapsulates the implementation of Perlin Noise. Application of noise
    requires you call "apply" on an instance of this class. 

    The overall algorithm can be summarized as such:
        * Create a "gradient" map containing direction vectors (permutation of -1..1 for each dimension is fine)
        * Create a permutation table of randomized values within a range that will serve as indices of the 
        gradient map. This emulates storing random vectors. 
        * For any given point P, find its surrounding points within a unit of its dimension (unit sq, cube, etc)
        * For each surrounding point SP, retrieve a "gradient" G via the permutation table
        * Dot product each G and the distance of P from its corresponding SP to produce noise values V for each
          surrounding point
        * Interpolate each V to produce resulting noise N
    """
    PERMUTATION_SIZE = 255

    gradient_map = [(-1, -1), (0, -1), (1, -1),
                    (-1, 0), (0, 0), (1, 0),
                    (-1, 1), (0, 1), (1, 1)]
    def __init__(self):
        self.create_permutation_table()

    """
        #the following generates smoother noise, rather than default direction map
        #it's not really necesary, but I left it there to play around with

        self.generate_gradient_table()

    def generate_gradient_table(self):
        # between -1 and 1
        self.gradient_map = []

        for i in range(self.PERMUTATION_SIZE):
            self.gradient_map.append([random.random() / 0.5 - 1.0, random.random() / 0.5 - 1.0])
    """

    def create_permutation_table(self):
        table = [i for i in range(self.PERMUTATION_SIZE)]
        random.shuffle(table)

        self.permutation_table = table

    def get_surrounding_points(self, x, y):
        x0 = int(floor(x))
        x1 = x0 + 1

        y0 = int(floor(y))
        y1 = y0 + 1

        return (x0, y0), (x1, y0), (x0, y1), (x1, y1)

    def get_gradient(self, *points):
        for point in points:
            x_index = self.permutation_table[point[0] % self.PERMUTATION_SIZE]
            xy_index = self.permutation_table[(point[1] + x_index) % self.PERMUTATION_SIZE]

            yield self.gradient_map[xy_index % len(self.gradient_map)]

    def dist_from_corners(self, x, y):
        # fraction is distance since the whole numbers are boundaries of bounding unit square
        x_dist = x - floor(x)
        x_dist_right = x_dist - 1

        y_dist = y - floor(y)
        y_dist_bottom = y_dist - 1

        return (x_dist, y_dist), (x_dist_right, y_dist), (x_dist, y_dist_bottom), (x_dist_right, y_dist_bottom)

    def bicubic_interpolation(self, dot0, dot1, dot2, dot3, dist_x, dist_y):
        """
        Pretty sure scipy has a good way of doing this, but here's taken from
        http://www.angelcode.com/dev/perlin/perlin.html
        """
        wx = (3 - 2 * dist_x) * dist_x**2
        v0 = dot0 - wx * (dot0 - dot1)
        v1 = dot2 - wx * (dot2 - dot3)

        wy = (3 - 2 * dist_y) * dist_y**2

        return v0 - wy * (v0 - v1)

    def apply(self, x, y):
        """
        Apply perlin noise to a given 2-dimensional vector
        """
        point = (x, y) 
        x0y0, x1y0, x0y1, x1y1 = self.get_surrounding_points(point[0], point[1])

        x0y0_gradient, x1y0_gradient, x0y1_gradient, x1y1_gradient = \
            tuple(self.get_gradient(x0y0, x1y0, x0y1, x1y1))

        dist_top_left, dist_top_right, dist_bot_left, dist_bot_right = \
            self.dist_from_corners(point[0], point[1])

        #dot product distance and gradients
        dot_x0y0 = np.dot(x0y0_gradient, dist_top_left) 
        dot_x1y0 = np.dot(x1y0_gradient, dist_top_right)
        dot_x0y1 = np.dot(x0y1_gradient, dist_bot_left)
        dot_x1y1 = np.dot(x1y1_gradient, dist_bot_right)

        noise_value = \
            self.bicubic_interpolation(dot_x0y0, dot_x1y0, dot_x0y1, dot_x1y1, \
                                       dist_top_left[0], dist_top_left[1])
        
        return noise_value 

