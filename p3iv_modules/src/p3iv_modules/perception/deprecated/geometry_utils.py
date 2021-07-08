# This file is part of the P3IV Simulator (https://github.com/fzi-forschungszentrum-informatik/P3IV),
# copyright by FZI Forschungszentrum Informatik, licensed under the BSD-3 license (see LICENSE file in main directory)

import numpy as np


class PointXY(object):
    def __init__(self, *args):
        if len(args) == 1:
            try:
                self.x = args[0][0]
                self.y = args[0][1]
            except Exception as e:
                print(e)
        elif len(args) == 2:
            self.x = args[0]
            self.y = args[1]
        else:
            raise TypeError

    def __sub__(self, other):
        return PointXY(self.x - other.x, self.y - other.y)

    def __add__(self, other):
        return PointXY(self.x + other.x, self.y + other.y)

    def __mul__(self, other):
        return PointXY(self.x * other.x, self.y * other.y)

    def __div__(self, other):
        return PointXY(self.x / other.x, self.y / other.y)

    def __call__(self):
        return np.array([self.x, self.y])

    def __getitem__(self, item):
        return np.array([self.x, self.y])[item]

    def __len__(self):
        return 2

    def __repr__(self):
        return "Point(%s, %s)" % (self.x, self.y)


class Polygon(object):
    def __init__(self, pts):
        self.points = pts

    @property
    def segments(self):
        # TODO: do this with yield
        p = self.points

        ret = list(zip(p[:-1], p[1:]))
        ret.append((p[-1], p[0]))  # close polygon

        return ret

    def __len__(self):
        return len(self.points)


class Polyline(Polygon):
    @property
    def segments(self):
        # TODO: do this with yield
        p = self.points

        return list(zip(p[:-1], p[1:]))


def ray_segment_intersect(p_ray, d_ray, seg):
    """
    Check if a ray (infinite line) intersects with a line segment.

    :param d_ray: the direction of the ray: np.ndarray([x,y])
    :param seg: segment defined by its endpoints np.ndarray([[x1,y1],[x2,y2]])
    :return: coordinates of intersection point as np.ndarray or None if no intersection
    """
    d_seg = seg[1] - seg[0]

    t_max = np.linalg.norm(d_seg)

    d_seg = d_seg / t_max
    d_ray = d_ray / np.linalg.norm(d_ray)

    D = np.stack([d_ray, -d_seg], axis=1)
    b = seg[0] - p_ray

    try:
        T = np.linalg.solve(D, b)
    except np.linalg.LinAlgError as e:
        # D is a singular matrix, lines are parallel
        return None

    # 0 <= T[1] < t_max because if the ray intersects perfectly with vertices then they will
    # T[0] > 0 ray shoots only in one direction
    # be included twice because they are the end and the beginning of a two segments
    if 0 <= T[1] < t_max and T[0] > 0 and np.allclose(np.dot(D, T), b):
        return seg[0] + d_seg * T[1]
    else:
        return None


def seg_arc_intersect(seg, origin, radius, arc):
    """
    Line segment from A->C: X = A + D*t |D|=1, t in [0, |C-A|]
    Circle: |X-O| = r^2 where ang(X,O) in [T1,T2]

    Equation: |D|*t**2 + 2*D*(A-O)*t + |A-O| - R**2 = 0
    :param seg:
    :param arc:
    :return:
    """
    norm = np.linalg.norm

    O = origin
    r = radius
    arc[0] = pos_rad(arc[0])
    arc[1] = pos_rad(arc[1])

    A = seg[0]
    B = seg[1]

    D = B - A

    t_max = norm(D)
    assert t_max != 0

    D = D / t_max

    coef = np.array([1, 2 * np.dot(D, (A - O)), norm(A - O) ** 2 - r ** 2])
    coef = np.round(coef, decimals=8)

    sol = np.roots(coef)

    if np.iscomplex(sol[0]):
        # two complex roots, no intersection
        return (None, None)
    elif np.isclose(sol[0], sol[1]):
        # one root, ray touches circle
        if 0 <= sol[0] <= t_max:
            P = A + sol[0] * D
            ang = pos_rad(angle_pp(O, P))

            if on_arc(arc, ang):
                return (P, None)
        else:
            return (None,) * 2
    else:
        # two distinct roots, two possible intersection points
        ret = [None] * 2

        for i in [0, 1]:
            if 0 <= sol[i] <= t_max:
                P = A + sol[i] * D
                ang = pos_rad(angle_pp(O, P))

                if on_arc(arc, ang):
                    ret[i] = P
        return ret[0], ret[1]


def ray_poly_intersect(p_ray, d_ray, poly):
    """
    Get intersection points of ray with polygon.

    :param p_ray: point of oringin of ray
    :param d_ray: direction of ray
    :param poly: list of vertexes of polygon
    :return: list of intersection points
    """
    ret = []

    for s in poly.segments:
        p = ray_segment_intersect(p_ray, d_ray, s)

        if p is not None:
            ret.append(p)

    return ret


def dist_p2p(p1, p2):
    return np.linalg.norm(p1 - p2)


def angle_pp(p1, p2):
    diff = p2 - p1
    return np.arctan2(diff[1], diff[0])


def ang2vec(a):
    return np.array([np.cos(a), np.sin(a)])


def pos_rad(r):
    return r % (2 * np.pi)


def on_arc(arc, ang):
    a1 = pos_rad(arc[0])
    a2 = pos_rad(arc[1])
    a = pos_rad(ang)

    if a1 < a2:
        return a1 < a < a2
    else:
        return (a > a1) or (a < a2)


def in_fov(fov, b, a):
    assert (fov[0] > 0) and (fov[1] < 0)

    a1 = pos_rad(b + fov[0])
    a2 = pos_rad(b + fov[1])
    a = pos_rad(a)

    if a2 > a1:
        return (a > a2) or (a < a1)
    else:
        # why not return "a2 < a < a1"?
        return a2 < a < a1


def p_in_tri(p, tri):
    """
    Interiority test for triangle.

    See https://en.wikipedia.org/wiki/Barycentric_coordinate_system for details.

    :param p: [x, y]
    :param tri: numpy array of points
    :return: True if p in tri, False otherwise
    """
    tri = np.array(tri)

    x = p[0]
    y = p[1]

    x1 = tri[0, 0]
    y1 = tri[0, 1]

    x2 = tri[1, 0]
    y2 = tri[1, 1]

    x3 = tri[2, 0]
    y3 = tri[2, 1]

    a = ((y2 - y3) * (x - x3) + (x3 - x2) * (y - y3)) / ((y2 - y3) * (x1 - x3) + (x3 - x2) * (y1 - y3))
    b = ((y3 - y1) * (x - x3) + (x1 - x3) * (y - y3)) / ((y2 - y3) * (x1 - x3) + (x3 - x2) * (y1 - y3))
    c = 1 - a - b

    return (0 <= a <= 1) and (0 <= b <= 1) and (0 <= c <= 1)


def p_in_wedge(p, wedge):
    """
    Interiority test for wedge.

    :param p: (x,y)
    :param wedge: ((x,y), angle1, angle2)  TODO: make a class?
    :return: True if p is in wedge, False otherwise
    """

    o = wedge[0]
    ang1 = pos_rad(wedge[1])
    ang2 = pos_rad(wedge[2])

    ang_p = pos_rad(angle_pp(o, p))

    if ang1 < ang2:
        if ang1 < ang_p < ang2:
            return True
    else:
        if (ang_p > ang1) or (ang_p < ang2):
            return True

    return False


def segment_interpolation_points(beg, end, dx, n=0, equal=True, inc_end=True):
    """
    Generator that returns segment interpolation points.
    Can be either used by specifying an increment dx, or number of interpolated points.
    If no interpolation can be done due to the dx or n given, the beg and end points will still be iterated upon.

    :param beg: start point
    :param end: end point
    :param dx: distance increment to use
    :param n: override dx and use n number of points
    :param equal: if dx was used, and it does not divide the distance precisely, distribute the error symmetrically,
                which means: dist(1st interp. pt., beg) == dist(last interp. pt., end),
                dist(interp. pt. N, interp. pt. N+1) == dx
    :return: yield an interpolated point
    """
    beg = np.array(beg)
    end = np.array(end)

    d = dist_p2p(beg, end)

    direction = (end - beg) / d

    precise = True

    if n > 0:
        dx = d / (n + 1)
    elif n == 0:
        if dx <= 0:
            raise ValueError
        elif dx > d:
            n = 1
        else:
            n = np.ceil(d / dx)
            precise = False
    elif n < 0:
        raise ValueError

    if not precise and equal:
        offset = (d - n * dx) / 2
    else:
        offset = 0

    yield beg

    for i in range(1, int(n)):
        yield beg + (i * dx + offset) * direction

    if inc_end:
        yield end


def _test_segment_interp():
    beg = [0, 0]
    end = [0, 1]

    print("\ndx =", 0.07)
    for i in segment_interpolation_points(beg, end, 0.07):
        print(i)

    print("\nn =", 5)
    for i in segment_interpolation_points(beg, end, 0.1, n=5):
        print(i)


def _test_arc():
    origin = PointXY([0.0, 0.0])
    rad = 1
    seg = np.array([PointXY([-np.sqrt(2), 0]), PointXY([0, np.sqrt(2)])])

    arc = np.array([np.pi / 2, np.pi])
    pts = seg_arc_intersect(seg, origin, rad, arc)

    print(pts)

    origin = np.array([0.0, 0.0])
    rad = 1
    seg = np.array([[-1, 0.5], [1, 0.5]])
    arc = np.array([0, np.pi])
    pts = seg_arc_intersect(seg, origin, rad, arc)

    print(pts)


if __name__ == "__main__":
    _test_arc()

    print("segment interp")
    _test_segment_interp()
