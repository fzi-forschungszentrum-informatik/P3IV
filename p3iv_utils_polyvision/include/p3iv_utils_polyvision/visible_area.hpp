#pragma once

#include <polyvision_cgal.hpp>

namespace polyvision {

class VisibleArea {
public:
    /**
     * @brief Construct a new Visible Area object
     *
     * @param origin
     * @param fieldsOfView
     * @param opaquePolygons
     */
    VisibleArea(const Point_2& origin, const Polygon_set_2& fieldsOfView, const Polygon_set_2& opaquePolygons)
            : origin(origin), fieldsOfView(fieldsOfView), opaquePolygons(opaquePolygons) {
    }

    /**
     * @brief calculates the visible area
     *
     * @param printEachStep verbose output of intermediate steps
     */
    void calculateVisibleArea();

    /**
     * @brief Get the border of visible region
     *
     * @return Point_2
     */
    bool getVisibilityBorder(const std::vector<Point_2>& line, Point_2& intersection) const;

    /**
     * @brief Get the Origin object
     *
     * @return Point_2
     */
    Point_2 getOrigin() const;

    /**
     * @brief Get the Fields Of View object
     *
     * @return Polygon_set_2
     */
    Polygon_set_2 getFieldsOfView() const;

    /**
     * @brief Get the Opaque Polygons object
     *
     * @return Polygon_set_2
     */
    Polygon_set_2 getOpaquePolygons() const;

    /**
     * @brief Get the Visible Areas object
     *
     * @return Polygon_set_2
     */
    Polygon_set_2 getVisibleAreas() const;

    /**
     * @brief Get the Non Visible Areas object
     *
     * @return Polygon_set_2
     */
    Polygon_set_2 getNonVisibleAreas() const;

    /**
     * @brief Check if a point is inside visible areas
     *
     * @return bool
     */
    bool checkInside(const Point_2& pt) const;

private:
    // Inputs
    Point_2 origin;
    Polygon_set_2 fieldsOfView;
    Polygon_set_2 opaquePolygons;

    // Computation results / Outputs
    Polygon_set_2 visibleAreas;
    Polygon_set_2 nonVisibleAreas;

    Polygon_2 getBoundingBoxOfFovPolygonSet() const;
};

} // namespace polyvision