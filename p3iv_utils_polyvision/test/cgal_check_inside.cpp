#include <iostream>
#include <CGAL/Exact_predicates_inexact_constructions_kernel.h>
#include "gtest/gtest.h"

#include "check_inside.hpp"
#include "polyvision_cgal.hpp"

#include "polyvision_cgal.hpp"

using namespace polyvision;

TEST(CGALTest, CheckInsideSimple) {

    // vector_convex_hull.cpp
    std::vector<Point_2> pointsVec;
    pointsVec.push_back(Point_2(0, 0));
    pointsVec.push_back(Point_2(10, 0));
    pointsVec.push_back(Point_2(10, 10));
    pointsVec.push_back(Point_2(6, 5));
    pointsVec.push_back(Point_2(4, 1));

    auto p = Point_2(9, 1);
    bool result = polyvision::checkInside(p, pointsVec);

    std::cout << "The point " << p;
    if (!result) {
        std::cout << " is outside the polygon.\n";
    } else {
        std::cout << " is in/on the polygon boundary.\n";
    }
}

TEST(CGALTest, CheckInsideSimplePolygonSingle) {
    Polygon_2 rect1;
    rect1.push_back(Point_2(0, 0));
    rect1.push_back(Point_2(5, 0));
    rect1.push_back(Point_2(5, 2));
    rect1.push_back(Point_2(0, 2));

    Polygon_set_2 polyset;
    polyset.insert(rect1);

    std::list<Polygon_with_holes_2> polygonList;
    polyset.polygons_with_holes(std::back_inserter(polygonList));
    std::list<Polygon_with_holes_2>::const_iterator it;

    Point_2 point(1, 1);

    bool isInside = false;

    for (it = polygonList.begin(); it != polygonList.end(); it++) {
        switch (it->outer_boundary().bounded_side(point)) {
        case CGAL::ON_BOUNDED_SIDE:
            isInside = true;
            break;
        case CGAL::ON_BOUNDARY:
            isInside = true;
            break;
        case CGAL::ON_UNBOUNDED_SIDE:
            isInside = false;
            continue;
        }
        if (isInside) {
            break;
        };
    }
    ASSERT_TRUE(isInside);
}
