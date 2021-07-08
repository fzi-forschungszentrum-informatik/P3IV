/*
 * This file is part of the Interpolated Polyline (https://github.com/fzi-forschungszentrum-informatik/P3IV),
 * copyright by FZI Forschungszentrum Informatik, licensed under the BSD-3 license (see LICENSE file in main directory)
 */

#include <iostream>
#include <visible_area.hpp>
#include <CGAL/Arr_point_location_result.h>
#include <CGAL/Arr_walk_along_line_point_location.h>
#include <CGAL/Bbox_2.h>
#include <CGAL/Triangular_expansion_visibility_2.h>
#include "cgal_utils.hpp"
#include "internal/cgal_debug_utils.hpp"

#ifndef DEBUG
#define DEBUG 0
#endif


namespace polyvision {
// Define the used visibility class
typedef CGAL::Triangular_expansion_visibility_2<Arrangement_2> TriExpVisibility;


Polygon_2 VisibleArea::getBoundingBoxOfFovPolygonSet() const {
    Polygon_2 bbpoly;
    if (this->fieldsOfView.is_empty()) {
        return bbpoly;
    } else {
        std::list<Polygon_with_holes_2> polysInPolyset;
        this->fieldsOfView.polygons_with_holes(std::back_inserter(polysInPolyset));

        // get bounding box of all polygons in polyset
        CGAL::Bbox_2 bbox = CGAL::bbox_2(polysInPolyset.begin(), polysInPolyset.end());

        double xmin, xmax, ymin, ymax;
        double originx = CGAL::to_double(this->origin.x());
        double originy = CGAL::to_double(this->origin.y());
        xmin = (originx < bbox.xmin()) ? originx : bbox.xmin();
        xmax = (originx > bbox.xmax()) ? originx : bbox.xmax();
        ymin = (originy < bbox.ymin()) ? originy : bbox.ymin();
        ymax = (originy > bbox.xmax()) ? originy : bbox.ymax();
        // construct bounding box polygon from bbox (counter-clockwise orientation)
        bbpoly.push_back(Point_2(xmin, ymax));
        bbpoly.push_back(Point_2(xmin, ymin));
        bbpoly.push_back(Point_2(xmax, ymin));
        bbpoly.push_back(Point_2(xmax, ymax));

        return bbpoly;
    }
}

Arrangement_2 polygon_with_holes2arrangement_2(const Polygon_with_holes_2& polywh) {
    Arrangement_2 arr;
    CGAL::insert_non_intersecting_curves(
        arr, polywh.outer_boundary().edges_begin(), polywh.outer_boundary().edges_end());
    Polygon_with_holes_2::Hole_const_iterator hit;
    for (hit = polywh.holes_begin(); hit != polywh.holes_end(); hit++) {
        CGAL::insert_non_intersecting_curves(arr, hit->edges_begin(), hit->edges_end());
    }
    return arr;
}

// member functions / methods of VisibleArea

bool VisibleArea::getVisibilityBorder(const std::vector<Point_2>& line, Point_2& intersection) const {
    CGALUtils cgalUtils;
    for (size_t i = 0; i < line.size() - 1; i++) {
        Segment_2 segment(line.at(i), line.at(i + 1));
        if (cgalUtils.segmentIntersectsPolygon(this->fieldsOfView, segment, intersection)) {
            return true;
        }
    }
    return false;
}

Point_2 VisibleArea::getOrigin() const {
    return this->origin;
}

Polygon_set_2 VisibleArea::getFieldsOfView() const {
    return this->fieldsOfView;
}

Polygon_set_2 VisibleArea::getOpaquePolygons() const {
    return this->opaquePolygons;
}

Polygon_set_2 VisibleArea::getVisibleAreas() const {
    return this->visibleAreas;
}

Polygon_set_2 VisibleArea::getNonVisibleAreas() const {
    return this->nonVisibleAreas;
}

bool VisibleArea::checkInside(const Point_2& point) const {

    CGALUtils cgalUtils;
    std::list<Polygon_with_holes_2> polygonList = cgalUtils.convertPolygonset2PolygonList(this->visibleAreas);

    bool isInside = false;
    std::list<Polygon_with_holes_2>::const_iterator it;
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
        }
    }
    return isInside;
}

void VisibleArea::calculateVisibleArea() {
    // VisibleArea calculation with CGAL
    // Concept #2: Visibility calculation in bounding box

    // Check if origin is inside an obstacle or fields of view is empty
    Polygon_with_holes_2 polyWithOrigin;
    if (this->opaquePolygons.locate(this->origin, polyWithOrigin) || this->fieldsOfView.is_empty()) {
        // visible area is empty / there is no visible area
        return;
    }

    //! Step #1: Get bounding box of fields of view
    Polygon_2 fovBb = this->getBoundingBoxOfFovPolygonSet();

    //! Step #2: Subtract obstacles from bounding box
    Polygon_set_2 fovBbWithoutObs;
    fovBbWithoutObs.insert(fovBb);
    fovBbWithoutObs.difference(this->opaquePolygons);

    //! Step #3: get polygon with holes in which origin is located
    // since the previous step could lead to disjoint polygons
    Polygon_with_holes_2 fovBbWithoutObsOriginInside;
    fovBbWithoutObs.locate(this->origin, fovBbWithoutObsOriginInside);
    // Create Arrangement_2 from fovBbWithoutObsoriginInside Polygon_with_holes_2
    Arrangement_2 visAEnv;
    visAEnv = polygon_with_holes2arrangement_2(fovBbWithoutObsOriginInside);
    // add origin to visAEnv
    Arrangement_2::Vertex_handle originVertex = CGAL::insert_point(visAEnv, this->origin);

    //! Step #4: calculate visible area in bounding box
    TriExpVisibility visibCalculator(visAEnv);

    // output from the visibility calculation
    Arrangement_2 visAinBbArr;
    Face_handle fhVisAOut;

    // check if origin is isolated inside face or if on edge
    if (!originVertex->is_isolated()) {
        Arrangement_2::Halfedge_const_handle he = visAEnv.halfedges_begin();
        while (he->target()->point() != originVertex->point() || (he->face()->is_unbounded()))
            he++;
        // run visibility calculation
        fhVisAOut = visibCalculator.compute_visibility(originVertex->point(), he, visAinBbArr);
    } else {
        Face_const_handle fhVisAIn;
        fhVisAIn = originVertex->face();
        // run visibility calculation
        fhVisAOut = visibCalculator.compute_visibility(originVertex->point(), fhVisAIn, visAinBbArr);
    }

    // Create visible area polygon from visibility calculation
    Polygon_2 visAinBbPoly;

    Arrangement_2::Ccb_halfedge_const_circulator curr = fhVisAOut->outer_ccb();
    do {
        visAinBbPoly.push_back(curr->target()->point());
        curr++;
    } while (curr != fhVisAOut->outer_ccb());

    //! Step #5: calculate visible area (intersection between visible area in bounding box and field of view)
    Polygon_set_2 set;
    set.insert(visAinBbPoly);
    set.intersection(this->fieldsOfView);
    this->visibleAreas = set;

    //! Step #6: calculate non-visible area (fields of view minus visible area minus obstacles)
    Polygon_set_2 nonVisA(this->fieldsOfView);
    nonVisA.difference(this->visibleAreas);
    nonVisA.difference(this->opaquePolygons);
    this->nonVisibleAreas = nonVisA;

    if (DEBUG) {
        CGALDebugUtils cgalDebugUtils;
        std::cout << "Print arrangement attached to visibCalc" << std::endl;
        cgalDebugUtils.printArrangement_2Faces(visibCalculator.arrangement_2());
        std::cout << "--------------------" << std::endl;
        std::cout << "Print result arrangement" << std::endl;
        cgalDebugUtils.printArrangement_2Faces(visAinBbArr);
        std::cout << "--------------------" << std::endl;
        std::cout << "#2 fovs polygon with holes:" << std::endl;
        cgalDebugUtils.printPolygon_set_2(fovBbWithoutObs);
        std::cout << "#4 visible area in bounding box:" << std::endl;
        Polygon_set_2 printSet;
        printSet.insert(visAinBbPoly);
        cgalDebugUtils.printPolygon_set_2(printSet);
        std::cout << "#5 visible areas:" << std::endl;
        cgalDebugUtils.printPolygon_set_2(this->visibleAreas);
        std::cout << "#6 non visible areas:" << std::endl;
        cgalDebugUtils.printPolygon_set_2(this->nonVisibleAreas);
    }
}

} // namespace polyvision