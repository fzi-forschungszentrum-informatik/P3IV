/*
 * This file is part of the Interpolated Polyline (https://github.com/fzi-forschungszentrum-informatik/P3IV),
 * copyright by FZI Forschungszentrum Informatik, licensed under the BSD-3 license (see LICENSE file in main directory)
 */

#pragma once

#include <polyvision_cgal.hpp>

namespace polyvision {

bool checkInside(Point_2 pt, std::vector<Point_2> points) {

    switch (CGAL::bounded_side_2(&points[0], &points[0] + points.size(), pt, Kernel())) {
    case CGAL::ON_BOUNDED_SIDE:
        return true;
    case CGAL::ON_BOUNDARY:
        return true;
    case CGAL::ON_UNBOUNDED_SIDE:
        return false;
    }
    return false; // todo: hack!
}
} // namespace polyvision