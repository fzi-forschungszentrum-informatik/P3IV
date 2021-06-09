#include "pypolyvision.hpp"
#include <CGAL/number_utils.h>
#include "cgal_utils.hpp"

static const double LARGE_VALUE = 1e8;

namespace polyvision {

// member functions of VisibleAreaPythonWrapper
VisibleAreaPythonWrapper::VisibleAreaPythonWrapper(const py::array_t<double>& origin,
                                                   const py::list& fieldsOfView,
                                                   const py::list& opaquePolygons) {
    Point_2 orig = numpyArray2Point_2(origin);
    Polygon_set_2 fovs = listOfNumpyArrays2Polygon_set_2(fieldsOfView);
    Polygon_set_2 polys = listOfNumpyArrays2Polygon_set_2(opaquePolygons);
    this->visibleArea = new VisibleArea(orig, fovs, polys);
}

void VisibleAreaPythonWrapper::calculateVisibleArea() {
    this->visibleArea->calculateVisibleArea();
}

py::list VisibleAreaPythonWrapper::getVisibleAreas() const {
    Polygon_set_2 visAs = this->visibleArea->getVisibleAreas();
    return polygon_set_2_2ListOfNumpyArrays(visAs);
}

py::list VisibleAreaPythonWrapper::getNonVisibleAreas() const {
    Polygon_set_2 nonVisAs = this->visibleArea->getNonVisibleAreas();
    return polygon_set_2_2ListOfNumpyArrays(nonVisAs);
}

bool VisibleAreaPythonWrapper::checkInside(py::array_t<double>& point) const {
    Point_2 point2check = numpyArray2Point_2(point);
    bool inside = this->visibleArea->checkInside(point2check);
    return inside;
}

py::list VisibleAreaPythonWrapper::getOpaquePolygons() const {
    Polygon_set_2 opaquePolys = this->visibleArea->getOpaquePolygons();
    return polygon_set_2_2ListOfNumpyArrays(opaquePolys);
}

py::list VisibleAreaPythonWrapper::getFieldsOfView() const {
    Polygon_set_2 fovs = this->visibleArea->getFieldsOfView();
    return polygon_set_2_2ListOfNumpyArrays(fovs);
}

py::array_t<double> VisibleAreaPythonWrapper::getVisibilityBorder(const py::array_t<double>& line_xys) const {
    std::vector<Point_2> line;
    line.reserve(line_xys.size()/2);

    for (size_t i = 0; i < line_xys.size()/2; i++){
        line.push_back(Point_2(line_xys.at(2*i), line_xys.at(2*i + 1)));
    }

    Point_2 intersection(LARGE_VALUE, LARGE_VALUE);
    this->visibleArea->getVisibilityBorder(line, intersection);
    return point_2_2NumpyArray(intersection);
}

py::array_t<double> VisibleAreaPythonWrapper::getOrigin() const {
    Point_2 origin = this->visibleArea->getOrigin();
    return point_2_2NumpyArray(origin);
}

// functions
// CGAL conversion functions
Point_2 numpyArray2Point_2(const py::array_t<double>& point) {
    return Point_2(point.at(0), point.at(1));
}

py::array_t<double> point_2_2NumpyArray(const Point_2& point) {
    py::array_t<double> p;
    p.resize({1, 2});
    *p.mutable_data(0, 0) = CGAL::to_double(point.x());
    *p.mutable_data(0, 1) = CGAL::to_double(point.y());
    // also possible
    // p.mutable_at(0,0) = ... (checks index bounds)
    return p;
}

// this function cannot handle polygons with holes
py::array_t<double> polygon_2_2NumpyArray(const Polygon_2& polygon) {
    // create py::array_t with dimensions (N,2)
    py::array_t<double> polygonArray;
    polygonArray.resize({static_cast<ssize_t>(polygon.size()), static_cast<ssize_t>(2)});
    auto rawPolygonArray = polygonArray.mutable_unchecked<2>(); // get mutable raw pointer to data
    // also possible:
    // py::buffer_info b = polygonArray.request();
    // double *ptr = reinterpret_cast<double*>(b.ptr);
    // ptr[...access correct element... (consider dimensions)]

    // iterate over polygon and do conversion to double
    size_t i = 0;
    for (Polygon_2::Vertex_const_iterator vit = polygon.vertices_begin(); vit != polygon.vertices_end(); vit++) {
        rawPolygonArray(i, 0) = CGAL::to_double(vit->x());
        rawPolygonArray(i, 1) = CGAL::to_double(vit->y());
        i++;
    }
    return polygonArray;
}

Polygon_2 numpyArray2Polygon_2(const py::array_t<double>& polygonArray) {
    // check dimensions first
    if (polygonArray.ndim() != 2) {
        throw std::invalid_argument((std::string("Number of dimension must be 2, but is ") +
                                     std::to_string(polygonArray.ndim()) + std::string(".\n"))
                                        .c_str());
    }
    // optional: add check for shape of pathArray to be (n,2)
    // OR: just take only first two columns (done here!)
    auto rawPolygonArray = polygonArray.unchecked<2>();
    ssize_t numberOfPoints = rawPolygonArray.shape(0);
    Polygon_2 polygon;
    // polygon.resize(numberOfPoints); // this creates a std::vector<IntPoint> with numberOfPoints (0,0) IntPoints in it
    // --> do not
    // use p.push_back()! (since it will add points at the end of the vector, but overwrite
    // points with p[i])

    // iterate over polygonArray
    for (ssize_t i = 0; i < numberOfPoints; i++) {
        polygon.push_back(Point_2(rawPolygonArray(i, 0), rawPolygonArray(i, 1)));
    }

    bool clockwise = polygon.is_clockwise_oriented();
    if (clockwise) {
        polygon.reverse_orientation();
    }
    return polygon;
}

// this function cannot handle polygons with holes
py::list polygon_set_2_2ListOfNumpyArrays(const Polygon_set_2& polygons) {

    CGALUtils cgalUtils;
    std::list<Polygon_with_holes_2> polygonList = cgalUtils.convertPolygonset2PolygonList(polygons);

    py::list l;
    std::list<Polygon_with_holes_2>::const_iterator it;
    for (it = polygonList.begin(); it != polygonList.end(); it++) {
        if (!it->is_unbounded()) {
            l.append(polygon_2_2NumpyArray(it->outer_boundary()));
        }
    }
    return l;
}

// the polygons in polygonArrays can overlap / can be non-disjoint
Polygon_set_2 listOfNumpyArrays2Polygon_set_2(const py::list& polygonArrays) {
    Polygon_set_2 polySet;
    for (auto item : polygonArrays) {
        // use join instead of insert so that polygons can overlap
        polySet.join(numpyArray2Polygon_2(item.cast<py::array_t<double>>()));
    }
    return polySet;
}


bool checkInsidePythonWrapper(const py::array_t<double>& point, const py::list& points) {
    Point_2 point_ = numpyArray2Point_2(point);

    std::vector<Point_2> points_;
    for (auto item : points) {
        points_.push_back(numpyArray2Point_2(point));
    }
    points_.push_back(points_[0]);
    return checkInside(point_, points_);
}


PYBIND11_MODULE(PYTHON_API_MODULE_NAME, m) {
    m.doc() = R"pbdoc(
        Pybind11 VisibleArea
        -----------------------
        .. currentmodule:: PYTHON_API_MODULE_NAME
        .. autosummary::
           :toctree: _generate

    )pbdoc";

    m.def("checkInside", &checkInsidePythonWrapper, "A function which adds two numbers");

    py::class_<VisibleAreaPythonWrapper>(m, "VisibleArea", py::module_local())
        .def(py::init<const py::array_t<double>&, const py::list&, const py::list&>(),
             py::arg("origin"),
             py::arg("fieldsOfView"),
             py::arg("opaquePolygons"))

        .def("calculateVisibleArea",
             &VisibleAreaPythonWrapper::calculateVisibleArea,
             "Function to calculate the visible area.")

        .def("getVisibleAreas",
             &VisibleAreaPythonWrapper::getVisibleAreas,
             "Returns the visible areas as list of numpy arrays.")

        .def("getNonVisibleAreas",
             &VisibleAreaPythonWrapper::getNonVisibleAreas,
             "Returns the non-visible areas as list of numpy arrays.")

        .def("checkInside",
             &VisibleAreaPythonWrapper::checkInside,
             "Returns the non-visible areas as list of numpy arrays.")

        .def("getOpaquePolygons",
             &VisibleAreaPythonWrapper::getOpaquePolygons,
             "Returns the opaque polygons (obstacles) as list of numpy arrays.")

        .def("getFieldsOfView",
             &VisibleAreaPythonWrapper::getFieldsOfView,
             "Returns the fields of view as list of numpy arrays.")

        .def("getVisibilityBorder",
             &VisibleAreaPythonWrapper::getVisibilityBorder,
             "Returns the border of visible area and given linestring a numpy array of shape (1,2).")

        .def("getOrigin", &VisibleAreaPythonWrapper::getOrigin, "Returns the origin as a numpy array of shape (1,2).");

#ifdef VERSION_INFO
    m.attr("__version__") = VERSION_INFO;
#else
    m.attr("__version__") = "dev";
#endif
}

} // namespace polyvision