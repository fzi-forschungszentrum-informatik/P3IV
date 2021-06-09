#include <iostream>
#include <list>
#include <CGAL/Arr_segment_traits_2.h>
#include <CGAL/Arrangement_2.h>
#include <CGAL/Exact_predicates_exact_constructions_kernel.h>
#include <CGAL/Polygon_2.h>
#include <CGAL/Polygon_set_2.h>
#include <CGAL/Polygon_with_holes_2.h>
#include <CGAL/intersections.h>
#include "cgal_debug_utils..hpp"
#include "cgal_utils.hpp"
#include "polyvision_cgal.hpp"
#include "gtest/gtest.h"

using namespace polyvision;


TEST(CGALTest, IntersectionLineSegment) {
    Polygon_2 rect1;
    rect1.push_back(Point_2(0, 0));
    rect1.push_back(Point_2(5, 0));
    rect1.push_back(Point_2(5, 2));
    rect1.push_back(Point_2(0, 2));

    Polygon_2 rect2;
    rect2.push_back(Point_2(2, -2));
    rect2.push_back(Point_2(4, -2));
    rect2.push_back(Point_2(4, 2));
    rect2.push_back(Point_2(2, 2));

    Polygon_2 rect3;
    rect3.push_back(Point_2(-2, -2));
    rect3.push_back(Point_2(-4, -2));
    rect3.push_back(Point_2(-4, 2));
    rect3.push_back(Point_2(-2, 2));

    Polygon_set_2 polyset;
    polyset.insert(rect1);
    polyset.join(rect2);
    polyset.join(rect3);

    Point_2 p1(2, -1);
    Point_2 p2(2, 2);
    Point_2 p3(3, -3);
    Point_2 p4(3, 3);
    Point_2 p5(3.0, -3.0);
    Point_2 p6(3.0, -6.0);
    Segment_2 segment1(p1, p2);
    Segment_2 segment2(p3, p4);
    Segment_2 segment3(p5, p6);

    CGALUtils cgalUtils{};
    Point_2 point1;
    Point_2 point2;
    Point_2 point3;

    ASSERT_TRUE(cgalUtils.segmentIntersectsPolygon(polyset, segment1, point1));
    ASSERT_TRUE(cgalUtils.segmentIntersectsPolygon(polyset, segment2, point2));
    ASSERT_FALSE(cgalUtils.segmentIntersectsPolygon(polyset, segment3, point3));

    ASSERT_DOUBLE_EQ(CGAL::to_double(point1.x()), 2.0);
    // intersection results are quite strange if a point is on the edge!
    ASSERT_DOUBLE_EQ(CGAL::to_double(point1.y()), 2.0); ///< this!! the same as p2?!
    ASSERT_DOUBLE_EQ(CGAL::to_double(point2.x()), 3.0);
    ASSERT_DOUBLE_EQ(CGAL::to_double(point2.y()), -2.0);
}


TEST(CGALTest, PolygonOperationBasics) {
    // Construct the two initial polygons and the clipping rectangle.
    Polygon_2 P;
    P.push_back(Point_2(0, 1));
    P.push_back(Point_2(2, 0));
    P.push_back(Point_2(1, 1));
    P.push_back(Point_2(2, 2));

    Polygon_2 Q;
    Q.push_back(Point_2(3, 1));
    Q.push_back(Point_2(1, 2));
    Q.push_back(Point_2(2, 1));
    Q.push_back(Point_2(1, 0));

    Polygon_2 rect;
    rect.push_back(Point_2(0, 0));
    rect.push_back(Point_2(3, 0));
    rect.push_back(Point_2(3, 2));
    rect.push_back(Point_2(0, 2));

    // Perform a sequence of operations.
    Polygon_set_2 S;
    S.insert(P);
    S.join(Q);            // Compute the union of P and Q.
    S.complement();       // Compute the complement.
    S.intersection(rect); // Intersect with the clipping rectangle.

    // Print the result.
    CGALDebugUtils cgalDebugUtils;
    std::list<Polygon_with_holes_2> res;
    std::list<Polygon_with_holes_2>::const_iterator it;
    std::cout << "The result contains " << S.number_of_polygons_with_holes() << " components:" << std::endl;
    S.polygons_with_holes(std::back_inserter(res)); // inserts all polygons with holes in the list "res"
    for (it = res.begin(); it != res.end(); ++it) { // print out list "res"
        std::cout << "--> ";
        cgalDebugUtils.printPolygon_with_holes2(*it);
    }
}


TEST(CGALTest, InsertNonDisjointPolygons) {
    // Polygon_set_2 check insert non-disjoint Polygons

    Polygon_2 p1;
    p1.push_back(Point_2(2, 5));
    p1.push_back(Point_2(5, 5));
    p1.push_back(Point_2(5, 2));
    p1.push_back(Point_2(2, 2));
    if (p1.is_clockwise_oriented()) {
        p1.reverse_orientation();
    }

    Polygon_2 p2;
    p2.push_back(Point_2(4, 3));
    p2.push_back(Point_2(4, 1));
    p2.push_back(Point_2(6, 1));
    p2.push_back(Point_2(6, 3));
    if (p2.is_clockwise_oriented()) {
        p2.reverse_orientation();
    }

    Polygon_set_2 ps;
    ps.insert(p1);
    ps.join(p2);

    CGALDebugUtils cgalDebugUtils;
    cgalDebugUtils.printPolygon_set_2(ps);

    ps.join(ps);
    cgalDebugUtils.printPolygon_set_2(ps);

    Polygon_2 p3;
    p3.push_back(Point_2(0, 0));
    p3.push_back(Point_2(12, 0));
    p3.push_back(Point_2(0, 9));

    Polygon_set_2 ps2;
    ps2.insert(p3);
    ps2.difference(ps);
    cgalDebugUtils.printPolygon_set_2(ps2);

    // todo: there may be memory-leak after this point while using v5.0.2
    Polygon_with_holes_2 polywh;
    std::list<Polygon_with_holes_2> polys;
    ps2.polygons_with_holes(std::back_inserter(polys));
    std::list<Polygon_with_holes_2>::const_iterator it;
    it = polys.begin();
    polywh = *it;

    Point_2 origin(1, 6);
    // Task print out face in which origin is located

    Arrangement_2 arr2;

    CGAL::insert_non_intersecting_curves(
        arr2, polywh.outer_boundary().edges_begin(), polywh.outer_boundary().edges_end());
    Polygon_with_holes_2::Hole_const_iterator hit;
    for (hit = polywh.holes_begin(); hit != polywh.holes_end(); hit++) {
        CGAL::insert_non_intersecting_curves(arr2, hit->edges_begin(), hit->edges_end());
    }

    Arrangement_2::Face_const_iterator fit;
    int k = 0;
    for (fit = arr2.faces_begin(); fit != arr2.faces_end(); fit++) {
        std::cout << k << " - ";
        if (fit->is_unbounded()) {
            std::cout << "Unbounded face!" << std::endl;
        } else {
            std::cout << "Outer boundary:";
            Arrangement_2::Ccb_halfedge_const_circulator circ;
            circ = fit->outer_ccb();
            Arrangement_2::Ccb_halfedge_const_circulator curr = circ;
            std::cout << "(" << curr->source()->point() << ")";
            do {
                Arrangement_2::Halfedge_const_handle he;
                he = curr;
                std::cout << " [" << he->curve() << "] "
                          << "(" << he->target()->point() << ")";
            } while (++curr != circ);
            std::cout << std::endl;

            Arrangement_2::Hole_const_iterator holit;
            for (holit = fit->holes_begin(); holit != fit->holes_end(); holit++) {
                Arrangement_2::Ccb_halfedge_const_circulator curr = *holit;
                std::cout << "(" << curr->source()->point() << ")";
                do {
                    Arrangement_2::Halfedge_const_handle he;
                    he = curr;
                    std::cout << " [" << he->curve() << "] "
                              << "(" << he->target()->point() << ")";
                } while (++curr != *holit);
                std::cout << std::endl;
            }
        }
        k++;
    }
}
