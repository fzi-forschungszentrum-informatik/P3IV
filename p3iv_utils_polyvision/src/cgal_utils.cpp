/*
 * This file is part of the Interpolated Polyline (https://github.com/fzi-forschungszentrum-informatik/P3IV),
 * copyright by FZI Forschungszentrum Informatik, licensed under the BSD-3 license (see LICENSE file in main directory)
 */

#include "cgal_utils.hpp"
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

std::list<Polygon_with_holes_2> CGALUtils::convertPolygonset2PolygonList(const Polygon_set_2& polygonset) {
    std::list<Polygon_with_holes_2> polygonList;
    // insert all Polygons_with_holes from polygonset
    polygonset.polygons_with_holes(std::back_inserter(polygonList));
    return polygonList;
}

bool CGALUtils::segmentIntersectsSegment(const Segment_2& segment_a, const Segment_2& segment_b, Point_2& point) {
    CGAL::cpp11::result_of<Intersect_2(Segment_2, Segment_2)>::type result = intersection(segment_a, segment_b);
    if (result) {
        if (const Segment_2* s = boost::get<Segment_2>(&*result)) {
            point = s->point(0);
        } else {
            point = *boost::get<Point_2>(&*result);
        }
        return true;
    } else {
        return false;
    }
}

bool CGALUtils::segmentIntersectsPolygon(const Polygon_set_2& polygonset, const Segment_2& segment, Point_2& point) {
    std::list<Polygon_with_holes_2> polygonList = convertPolygonset2PolygonList(polygonset);
    std::list<Polygon_with_holes_2>::const_iterator it;

    for (it = polygonList.begin(); it != polygonList.end(); it++) {
        if (!it->is_unbounded()) {

            size_t i = 0;
            Polygon_2::Edge_const_iterator eit;
            for (eit = it->outer_boundary().edges_begin(); eit != it->outer_boundary().edges_end(); eit++) {
                Segment_2 seg(eit->point(0), eit->point(1));
                bool valid = segmentIntersectsSegment(seg, segment, point);
                if (valid) {
                    return true;
                }
                i++;
            }
        }
    }
    return false;
}

} // namespace polyvision