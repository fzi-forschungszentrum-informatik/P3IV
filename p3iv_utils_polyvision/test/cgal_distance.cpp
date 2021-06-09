#include <iostream>
#include <CGAL/Simple_cartesian.h>
#include "gtest/gtest.h"
typedef CGAL::Simple_cartesian<double> Kernel;
typedef Kernel::Point_2 Point_2;
typedef Kernel::Segment_2 Segment_2;

// exact Kernel
#include <CGAL/Exact_predicates_exact_constructions_kernel.h>
typedef CGAL::Exact_predicates_exact_constructions_kernel Kernel2;
typedef Kernel2::Point_2 Point_22;


TEST(CGALTest, TestSquaredDistance1) {
    // points_and_segment.cpp
    Point_2 p(1, 1), q(10, 10);
    std::cout << "p = " << p << std::endl;
    std::cout << "q = " << q.x() << " " << q.y() << std::endl;
    std::cout << "sqdist(p,q) = " << CGAL::squared_distance(p, q) << std::endl;
}

TEST(CGALTest, TestSquaredDistance2) {
    // points_and_segment.cpp
    Point_2 p(1, 1), q(10, 10);
    Segment_2 s(p, q);

    Point_2 m(5, 9);

    std::cout << "m = " << m << std::endl;
    std::cout << "sqdist(Segment_2(p,q), m) = " << CGAL::squared_distance(s, m) << std::endl;
    std::cout << "p, q, and m ";
    switch (CGAL::orientation(p, q, m)) {
    case CGAL::COLLINEAR:
        std::cout << "are collinear\n";
        break;
    case CGAL::LEFT_TURN:
        std::cout << "make a left turn\n";
        break;
    case CGAL::RIGHT_TURN:
        std::cout << "make a right turn\n";
        break;
    }
    std::cout << " midpoint(p,q) = " << CGAL::midpoint(p, q) << std::endl;
}

TEST(CGALTest, Colinearity1) {

    Point_2 p(0, 0.3), q(1, 0.6), r(2, 0.9);
    std::cout << (CGAL::collinear(p, q, r) ? "collinear\n" : "not collinear\n");
}


TEST(CGALTest, Colinearity2) {


    Point_2 p(0, 1.0 / 3.0), q(1, 2.0 / 3.0), r(2, 1);
    std::cout << (CGAL::collinear(p, q, r) ? "collinear\n" : "not collinear\n");
}

TEST(CGALTest, Colinearity3) {


    Point_2 p(0, 0), q(1, 1), r(2, 2);
    std::cout << (CGAL::collinear(p, q, r) ? "collinear\n" : "not collinear\n");
}

TEST(CGALTest, ColinearityCombined) {

    // exact.cpp
    Point_22 a(0, 0.3);
    Point_22 b;
    Point_22 c(2, 0.9);

    b = Point_22(1, 0.6);
    std::cout << (CGAL::collinear(a, b, c) ? "collinear\n" : "not collinear\n");


    std::istringstream input("0 0.3   1 0.6   2 0.9");
    input >> a >> b >> c;
    std::cout << (CGAL::collinear(a, b, c) ? "collinear\n" : "not collinear\n");


    b = CGAL::midpoint(a, c);
    std::cout << (CGAL::collinear(a, b, c) ? "collinear\n" : "not collinear\n");
}