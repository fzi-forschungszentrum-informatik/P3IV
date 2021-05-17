#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
import matplotlib.pyplot as plt
import matplotlib.patches as mplpatches
from matplotlib.collections import PatchCollection
from collections import namedtuple
from geometry_utils import *
from copy import deepcopy


class VisibilityPolygon(namedtuple("VisibilityPolygon", ('cartesian', 'polar'))):
   pass
# obsolete: see _test()
#class StaticObjects(namedtuple('StaticObjects', ('poly', 'polyline'))):
#    pass


def _update_change_dec(func):
    '''
    Decorator to track property changes in class. Apply @property.setter after @_update_change_dec
    :param func: function object to decorate
    :return: decorated function
    '''
    def _wrapper(self, val):
        self._changed = True
        func(self, val)

    return _wrapper


class VisibilityModel(object):
    def __init__(self, radius, fov, objects=None, eps_corner=1e-9):
        self._radius = radius
        self.fov = np.deg2rad(fov)
        self._heading = None
        self._origin = None

        self._objects = objects
        self._eps_corner = eps_corner

        self._changed = True
        self._visibility_polygon = None
        self._visible_poly_points = None

    def _force_computation(self):
        if self._changed:
            self._compute_visibility_polygon()
            self._changed = False

    def _compute_visibility_polygon(self):
        """
        Return the visibility polygon of based on the scene.
        Currently only poly obstacles are allowed.
        Corner checking is based on small angles approximation.

        :param orig: origin of observer np.ndarray([x,y])
        :param bearing: direction of observer in radians
        :param fov: field of view of observer, [fov+, fov-] in radians
        :param range: range of observer
        :param static_objects: contains the obstacles, dict(poly = [np.ndarray([[], [], ...])])
        :param eps_corner: precision of corner checks in radians
        :return: dict(edge=ray_points_cart, pol=ray_points, origin=o, r=r, fov=fov, bearing=b)
        """
        o = self._origin
        b = pos_rad(self._heading)
        r = self._radius
        fov = self._fov
        eps_corner = self._eps_corner

        static_objects = self._objects

        # angles in anticlockwise order
        arc = np.array([pos_rad(b + fov[1]),
                        pos_rad(b + fov[0])])

        # points which will be evaluated, start with extrema defined by FOV cone
        ray_points = [[r, pos_rad(b + fov[1])],
                      [r, pos_rad(b + fov[0])]]

        ray_points_poly = [-1, -1]  # the two extrema are not taken from a poly

        # add points from lines intersecting with cone cap
        for ip, p in enumerate(static_objects):
            for s in p.segments:
                ret = seg_arc_intersect(s, o, r, arc)

                for rp in ret:
                    if rp is not None:
                        ang = pos_rad(angle_pp(o, rp))

                        ray_points.append([r, ang])
                        ray_points_poly.append(ip)

        # add regular poly points
        for ip, p in enumerate(static_objects):
            for v in p.points:
                d_ray = v - o
                a_ray = pos_rad(np.arctan2(d_ray[1], d_ray[0]))
                r_v = np.linalg.norm(d_ray)

                if in_fov(fov, b, a_ray) and r_v <= r:
                    # TODO: handle edge cases, instead of using epsilons
                    a_ray_corner = [pos_rad(a_ray + eps_corner),
                                    pos_rad(a_ray - eps_corner)]

                    vert = [r_v, a_ray]
                    vert_corner = map(list, zip([r, r], a_ray_corner))

                    ray_points.append(vert)
                    ray_points_poly.append(None)

                    ray_points += vert_corner
                    ray_points_poly.extend([-1, -1])

        ray_points_old = deepcopy(ray_points)

        # polygon points which remain unchanged --> are visible
        for iv, v in enumerate(ray_points):
            for iq, q in enumerate(static_objects):
                d_ray = ang2vec(v[1])
                poly_sec = ray_poly_intersect(o, d_ray, q)

                for ps in poly_sec:
                    r_ps = dist_p2p(ps, o)
                    v[0] = np.min([r_ps, v[0]])

                # for the get_poly_visible_points
                if ray_points_old[iv][0] > ray_points[iv][0]:
                    ray_points_poly[iv] = iq
                    ray_points_old[iv][0] = ray_points[iv][0]

        ray_points = np.array(ray_points)
        ray_points_poly = np.array(ray_points_poly)
        # sort by angle
        a2 = pos_rad(b + fov[0])
        a1 = pos_rad(b + fov[1])

        # handle 2pi wraparound for correct anti-clockwise sorting
        rp = ray_points[:, 1]
        if a1 > a2:
            if b < a1:
                idx = (rp >= a1)
                offset = -2 * np.pi
            else:
                idx = (rp <= a2)
                offset = 2 * np.pi

            rp_slice = ray_points[idx]
            rp_slice[:, 1] += offset
            ray_points[idx] = rp_slice


        rp_argsort = ray_points[:, 1].argsort()

        ray_points = ray_points[rp_argsort]
        ray_points_poly = ray_points_poly[rp_argsort]
        # filter points not in fov, they may be produced by the corner approximation
        # ray_points = ray_points[(ray_points[:, 1] <= pos_rad(b+fov)) & (ray_points[:, 1] >= pos_rad(b-fov))]

        # polar to cartesian
        ray_points_cart = np.stack([np.cos(ray_points[:, 1]), np.sin(ray_points[:, 1])], axis=1)
        ray_points_cart *= np.stack([ray_points[:, 0]] * 2, axis=1)
        ray_points_cart += o

        self._visible_poly_points = ray_points_poly
        self._visibility_polygon = VisibilityPolygon(cartesian=ray_points_cart, polar=ray_points)

    @property
    def visibility_polygon(self):
        self._force_computation()

        return self._visibility_polygon

    @property
    def pyplot_patches(self):
        '''
        Get a pyplot.PatchCollection representing the visibility polygon, made up of Wedge and triangles as Polygon
        objects
        :return: PatchCollection
        '''
        self._force_computation()

        vis_poly = self.visibility_polygon

        patches = []

        for i in range(0, len(vis_poly.cartesian) - 1):
            draw_wedge = np.isclose(vis_poly.polar[i, 0], self._radius) and \
                         np.isclose(vis_poly.polar[i + 1, 0], self._radius)

            if draw_wedge:
                ang1 = vis_poly.polar[i, 1]
                ang2 = vis_poly.polar[i + 1, 1]

                patches.append(mplpatches.Wedge(self._origin,
                                                self._radius,
                                                ang1 * 180.0 / np.pi,
                                                ang2 * 180.0 / np.pi))
            else:
                patches.append(mplpatches.Polygon([self._origin,
                                                   vis_poly.cartesian[i],
                                                   vis_poly.cartesian[i + 1]]))

        return PatchCollection(patches)

    def is_visible(self, p):
        vis_poly = self.visibility_polygon

        dist_p = dist_p2p(p, self._origin)

        if dist_p > self._radius:
            return False

        for i in range(0, len(vis_poly.cartesian) - 1):
            is_wedge = np.isclose(vis_poly.polar[i, 0], self._radius) and \
                        np.isclose(vis_poly.polar[i + 1, 0], self._radius)

            if is_wedge:
                ang1 = pos_rad(vis_poly.polar[i, 1])
                ang2 = pos_rad(vis_poly.polar[i + 1, 1])
                wedge = (self._origin, ang1, ang2)

                if p_in_wedge(p, wedge):
                    return True
            else:
                tri = (self._origin,
                       vis_poly.cartesian[i],
                       vis_poly.cartesian[i+1])

                if p_in_tri(p, tri):
                    return True

        return False


    def get_polyline_visible_points(self, poly, interp_dx=0, extremal=''):
        '''

        :param poly:
        :param extremal:
        :return:
        '''
        vis_poly = self.visibility_polygon

        ret = []
        ret_pol = []

        if True:
            for i, p in enumerate(poly[:-1]):
                for j in segment_interpolation_points(poly[i], poly[i+1], interp_dx, inc_end=(i==len(poly)-2)):
                    if self.is_visible(j):
                        ret.append(j)
                        ret_pol.append(dist_p2p(self._origin, PointXY(j)))

        if False:
            from py_distance_transform import PyPseudoDistanceFunction as PDF
            pdf = PDF(poly, True, True)
            upsampled_cartesian_points = np.asarray(
                [pdf.reconstruct(x, 0.0) for x in np.arange(0.1, pdf.max_arclength(), interp_dx)]).reshape(-1, 2)

            for p in upsampled_cartesian_points:
                if self.is_visible(p):
                    ret.append(p)
                    ret_pol.append(dist_p2p(self._origin, PointXY(p)))

        ret_pol = np.array(ret_pol)

        if extremal == '':
            return ret
        elif extremal == 'r':
            minpol = np.argmin(ret_pol)
            maxpol = np.argmax(ret_pol)
            print minpol, maxpol

            return [ret[minpol], ret[maxpol]]
        else:
            raise ValueError



    def get_polygon_visible_points(self, poly, extremal='', store = False):
        '''
        Get the visibe 'angle' points of a polygon. The polygon is trated as part of the scene, and depending on param
        store will be stored in self.objects.
        :param poly: polygon to calculate
        :param store: store polygon in self.objects?
        :return: list of points of polygon visible
        '''
        old_objects = deepcopy(self._objects)
        self._objects.append(Polyline(poly))

        poly_idx = len(self._objects) - 1
        self._compute_visibility_polygon()

        ret = []
        ret_pol = []

        for i, v in enumerate(self._visible_poly_points):
            if v == poly_idx:
                ret.append(self._visibility_polygon.cartesian[i])
                ret_pol.append(self._visibility_polygon.polar[i])

        if not store:
            self._objects = old_objects
            self._changed = True
        else:
            self._changed = False

        ret_pol = np.array(ret_pol)
        ret = np.array(ret)

        if extremal == '':
            return ret
        else:
            if extremal == 'r':
                ax1 = 0
            elif extremal == 'a':
                ax1 = 1
            else:
                raise ValueError

            minpol = np.argmin(ret_pol[:, ax1])
            maxpol = np.argmax(ret_pol[:, ax1])
            return ret[[minpol, maxpol]]

    @property
    def radius(self):
        return self._radius

    @radius.setter
    @_update_change_dec
    def radius(self, val):
        self._radius = val

    @property
    def fov(self):
        return self._fov

    @fov.setter
    @_update_change_dec
    def fov(self, val):
        self._fov = val

    @property
    def heading(self):
        return self._heading

    @heading.setter
    @_update_change_dec
    def heading(self, val):
        self._heading = pos_rad(np.deg2rad(val))

    @property
    def origin(self):
        return self._origin

    @origin.setter
    @_update_change_dec
    def origin(self, val):
        self._origin = val

    @property
    def objects(self):
        return self._objects

    @objects.setter
    @_update_change_dec
    def objects(self, val):
        self._objects = val


def _test():
    '''
    Test and show usage of code within this module
    :return:
    '''
    h = 105

    dir = ang2vec(np.deg2rad(h))

    o = PointXY([5.2, 1])
    r = 10
    fov = [45, -45]

    fig, ax = plt.subplots()


    # plot obstacles
    sq1pts = np.array([PointXY([5.0, 5.0]),
                    PointXY([4.5, 5.5]),
                    PointXY([5.0, 6.0]),
                    PointXY([6.0, 6.0]),
                    PointXY([6.0, 5.0])])
    sq1 = Polygon(sq1pts)


    # one can also use a numpy array, this works because point implements __getitem__
    sq2pts = np.array([[0, 10],
                        [0, 11],
                        [1, 11],
                        [1, 10]])
    sq2 = Polygon(sq2pts)

    sq3pts = np.array([PointXY([-10, 17]),
                    PointXY([-10, 20]),
                    PointXY([20, 20]),
                    PointXY([20, 17]),
                    PointXY([5, 15])])
    sq3 = Polygon(sq3pts)

    line1pts = np.array([[0, 7],
                         [-5, 7],
                         [-7, 5]])
    line1 = line1pts

    ax.add_patch(mplpatches.Polygon(sq1.points, facecolor='black', linewidth=0, alpha=0.5))
    ax.add_patch(mplpatches.Polygon(sq2.points, facecolor='black', linewidth=0, alpha=0.5))
    ax.add_patch(mplpatches.Polygon(sq3.points, facecolor='black', linewidth=0, alpha=0.5))
    plt.plot(line1pts[:, 0], line1pts[:, 1])

    # plot heading
    plt.plot([o[0], o[0] + dir[0] * 3],
             [o[1], o[1] + dir[1] * 3], '-', color='orange')

    # plot position
    plt.plot(o[0], o[1], 'o', color='red')

    ##########
    # why to add line1 in objects? See line #242
    model = VisibilityModel(r, fov, [sq1, sq2, sq3, Polyline(line1)])

    # set current position and heading
    model.origin = o
    model.heading = h
    # calculate and return corresponding pyplot patches as Patchcollectiion
    p = model.pyplot_patches

    # calculate again, test if property update works
    # model.fov = [60, -60]
    model.radius = 20
    # check polygon visibility code
    model.objects = [sq1, sq2, sq3]

    pts = model.get_polygon_visible_points(line1, store=True)
    for i in pts:
        plt.plot(i[0], i[1], 'o', color='orange')

    # this doesn't recalculate because nothing has changed, simply returns the patches of the plygon calculeted
    # in model.get_polygon_visible_points, because store=True. For store=False, the next call recalculates because
    # the polygon passed to model.get_polygon_visible_points isn't treated as part of the scene
    p = model.pyplot_patches

    p.set_alpha(0.2)
    p.set_linewidth(0)

    # alternating patch colors for debugging
    cols = []
    for i in range(len(model.visibility_polygon.cartesian)-1):
        cols.append(('black','blue')[i%2])
    p.set_color(cols)

    ax.add_collection(p)


    # check visibility code
    x = np.linspace(-19, 20, 80)
    y = np.linspace(0, 20, 40)

    mg = np.meshgrid(x,y)
    mg = np.dstack(mg)
    mg = mg.reshape(-1, 2) # list of xy coordinates

    for i in range(mg.shape[0]):
        p = mg[i]
        if model.is_visible(p):
            plt.plot(p[0], p[1], '.', ms=0.5, color='b')



    ax.grid()
    plt.axis('equal')
    plt.show()


if __name__ == '__main__':
    _test()


