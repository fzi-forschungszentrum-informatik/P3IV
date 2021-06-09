#include <iostream>
#include <CGAL/Exact_predicates_inexact_constructions_kernel.h>
#include <CGAL/convex_hull_2.h>
#include "gtest/gtest.h"
typedef CGAL::Exact_predicates_inexact_constructions_kernel K;

typedef K::Point_2 Point_2;
typedef std::vector<Point_2> Points;


TEST(CGALTest, ConvexHull) {
    // array_convex_hull.cpp
    Point_2 points[5] = {Point_2(0, 0), Point_2(10, 0), Point_2(10, 10), Point_2(6, 5), Point_2(4, 1)};
    Point_2 result[5];
    Point_2* ptr = CGAL::convex_hull_2(points, points + 5, result);
    std::cout << ptr - result << " points on the convex hull:" << std::endl;
    for (int i = 0; i < ptr - result; i++) {
        std::cout << result[i] << std::endl;
    }

    // vector_convex_hull.cpp
    Points pointsVec, resultVec;
    pointsVec.push_back(Point_2(0, 0));
    pointsVec.push_back(Point_2(10, 0));
    pointsVec.push_back(Point_2(10, 10));
    pointsVec.push_back(Point_2(6, 5));
    pointsVec.push_back(Point_2(4, 1));
    CGAL::convex_hull_2(pointsVec.begin(), pointsVec.end(), std::back_inserter(resultVec));
    std::cout << resultVec.size() << " points on the convex hull" << std::endl;
}
