#include <iostream>
#include <list>
#include <CGAL/Arr_segment_traits_2.h>
#include <CGAL/Arrangement_2.h>
#include <CGAL/Exact_predicates_exact_constructions_kernel.h>
#include <CGAL/Polygon_2.h>
#include <CGAL/Polygon_set_2.h>
#include <CGAL/Polygon_with_holes_2.h>
#include "polyvision_cgal.hpp"
#include "gtest/gtest.h"

namespace polyvision {

class CGALUtils {

public:
    std::list<Polygon_with_holes_2> convertPolygonset2PolygonList(const Polygon_set_2& polygonset);
    bool segmentIntersectsSegment(const Segment_2& segment_a, const Segment_2& segment_b, Point_2& point);
    bool segmentIntersectsPolygon(const Polygon_set_2& polyset, const Segment_2& line, Point_2& point);
};
} // namespace polyvision