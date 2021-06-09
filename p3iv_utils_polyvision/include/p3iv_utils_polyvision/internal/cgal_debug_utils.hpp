#include <iostream>
#include <list>
#include <CGAL/Arr_segment_traits_2.h>
#include <CGAL/Arrangement_2.h>
#include <CGAL/Exact_predicates_exact_constructions_kernel.h>
#include <CGAL/Polygon_2.h>
#include <CGAL/Polygon_set_2.h>
#include <CGAL/Polygon_with_holes_2.h>
#include "gtest/gtest.h"
#include "p3iv_utils_polyvision/polyvision_cgal.hpp"

namespace polyvision {

class CGALDebugUtils {

public:
    /**
     * @brief pretty-print a CGAL polygon.
     */
    template <class Kernel, class Container>
    void printPolygon_2(const CGAL::Polygon_2<Kernel, Container>& P) {
        typename CGAL::Polygon_2<Kernel, Container>::Vertex_const_iterator vit;

        std::cout << "[ " << P.size() << " vertices:";
        for (vit = P.vertices_begin(); vit != P.vertices_end(); ++vit)
            std::cout << " (" << *vit << ')';
        std::cout << " ]" << std::endl;

        return;
    }

    /**
     * @brief pretty-print a polygon with holes.
     */
    template <class Kernel, class Container>
    void printPolygon_with_holes2(const CGAL::Polygon_with_holes_2<Kernel, Container>& pwh) {
        if (!pwh.is_unbounded()) {
            std::cout << "{ Outer boundary = ";
            printPolygon_2(pwh.outer_boundary());
        } else
            std::cout << "{ Unbounded polygon." << std::endl;

        typename CGAL::Polygon_with_holes_2<Kernel, Container>::Hole_const_iterator hit;
        unsigned int k = 1;

        std::cout << "  " << pwh.number_of_holes() << " holes:" << std::endl;
        for (hit = pwh.holes_begin(); hit != pwh.holes_end(); ++hit, ++k) {
            std::cout << "    Hole #" << k << " = ";
            printPolygon_2(*hit);
        }
        std::cout << " }" << std::endl;
        return;
    }

    /**
     * @brief prints all polygons in a Polygon_set_2.
     */
    void printPolygon_set_2(const Polygon_set_2& polyset) {
        std::list<Polygon_with_holes_2>
            polysInPolyset; // the list, where all Polygons_with_holes from polyset will be inserted
        std::list<Polygon_with_holes_2>::const_iterator it;
        polyset.polygons_with_holes(
            std::back_inserter(polysInPolyset)); // insert all polygons from polyset in polysInPolyset
        std::cout << "-------------------print Polygon_set_2" << std::endl;
        // iterate over polysInPolyset
        int polyNum = 0;
        for (it = polysInPolyset.begin(); it != polysInPolyset.end(); it++) {
            // print vertices of boundary of polygon
            Polygon_2 poly = it->outer_boundary();
            int vertexNum = 0;
            // iterate over vertices in polygon
            for (Polygon_2::Vertex_const_iterator itv = poly.vertices_begin(); itv != poly.vertices_end(); itv++) {
                std::cout << "Poly:" << polyNum << " V:" << vertexNum << " = (" << *itv << ")" << std::endl;
                vertexNum++;
            }
            // print holes of polygon
            if (it->has_holes()) {
                int holeNum = 0;
                for (Polygon_with_holes_2::Hole_const_iterator hit = it->holes_begin(); hit != it->holes_end(); hit++) {
                    // print vertices of hole
                    vertexNum = 0;
                    for (Polygon_2::Vertex_const_iterator itv = hit->vertices_begin(); itv != hit->vertices_end();
                         itv++) {
                        std::cout << "Poly:" << polyNum << " -- Hole:" << holeNum << " V" << vertexNum << " = (" << *itv
                                  << ")" << std::endl;
                        vertexNum++;
                    }
                    holeNum++;
                }
            } else {
                std::cout << "Poly:" << polyNum << " - has no holes" << std::endl;
            }
            polyNum++;
        }
        std::cout << "-------------------" << std::endl;
    }

    /**
     * @brief print faces.
     */
    void print_face(const Arrangement_2::Face_const_handle fh) {
        if (fh->is_unbounded()) {
            std::cout << "Unbounded face! with holes: " << fh->number_of_holes() << std::endl;
            Arrangement_2::Hole_const_iterator holit;
            holit = fh->holes_begin();
            Arrangement_2::Ccb_halfedge_const_circulator curr = *holit;
            std::cout << "(" << curr->source()->point() << ")";
            do {
                Arrangement_2::Halfedge_const_handle he;
                he = curr;
                std::cout << " [" << he->curve() << "] " << std::endl;
                std::cout << "(" << he->target()->point() << ")";
            } while (++curr != *holit);
            std::cout << "\n\n\n";
        } else {
            std::cout << "Outer boundary:";
            Arrangement_2::Ccb_halfedge_const_circulator circ;
            circ = fh->outer_ccb();
            Arrangement_2::Ccb_halfedge_const_circulator curr = circ;
            std::cout << "(" << curr->source()->point() << ")";
            do {
                Arrangement_2::Halfedge_const_handle he;
                he = curr;
                std::cout << " [" << he->curve() << "] " << std::endl;
                std::cout << "(" << he->target()->point() << ")";
            } while (++curr != circ);

            std::cout << "\n\n\n";
            std::cout << "Number of Holes: " << fh->number_of_holes() << std::endl;
            Arrangement_2::Hole_const_iterator holit;
            for (holit = fh->holes_begin(); holit != fh->holes_end(); holit++) {
                Arrangement_2::Ccb_halfedge_const_circulator curr = *holit;
                std::cout << "(" << curr->source()->point() << ")";
                do {
                    Arrangement_2::Halfedge_const_handle he;
                    he = curr;
                    std::cout << " [" << he->curve() << "] " << std::endl;
                    std::cout << "(" << he->target()->point() << ")";
                } while (++curr != *holit);
                std::cout << std::endl;
            }
        }
    }

    void printArrangement_2Faces(const Arrangement_2& arr) {
        std::cout << "-------------------print Arrangement_2 faces" << std::endl;
        Arrangement_2::Face_const_iterator fit;
        int k = 0;
        for (fit = arr.faces_begin(); fit != arr.faces_end(); fit++) {
            std::cout << k << " - ";
            print_face(fit);
            k++;
        }
        std::cout << "-------------------" << std::endl;
    }
};

} // namespace polyvision