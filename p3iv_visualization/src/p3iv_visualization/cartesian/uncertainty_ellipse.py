
from matplotlib.patches import Ellipse


class UncertaintyEllipse(object):
    def __init__(self, color):
        self.color = color

        self.e = None
        self.set_uncertainty_ellipse()

    def set_uncertainty_ellipse(self):
        xy = (0, 0)
        width = 10
        height = 3
        heading = 0
        self.e = Ellipse(xy, width, height, heading, zorder=5, linestyle="-.", edgecolor=self.color, facecolor="none")

    def update_transformation(self, x, y, heading):
        self.e.center = (x, y)
        self.e.angle = heading

    def update_uncertainty(self, width, height):
        self.e.width = width
        self.e.height = height
