/*
 * This file is part of the Interpolated Polyline (https://github.com/fzi-forschungszentrum-informatik/P3IV),
 * copyright by FZI Forschungszentrum Informatik, licensed under the BSD-3 license (see LICENSE file in main directory)
 */

#include <iostream>
#include <list>
#include <CGAL/Arr_segment_traits_2.h>
#include <CGAL/Arrangement_2.h>
#include <CGAL/Exact_predicates_exact_constructions_kernel.h>
#include <CGAL/Polygon_2.h>
#include <CGAL/Polygon_set_2.h>
#include <CGAL/Polygon_with_holes_2.h>
#include "polyvision_cgal.hpp"

namespace polyvision {

class CGALUtils {

public:
    std::list<Polygon_with_holes_2> convertPolygonset2PolygonList(const Polygon_set_2& polygonset);
    bool segmentIntersectsSegment(const Segment_2& segment_a, const Segment_2& segment_b, Point_2& point);
    bool segmentIntersectsPolygon(const Polygon_set_2& polyset, const Segment_2& line, Point_2& point);
};
} // namespace polyvision