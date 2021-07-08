/*
 * This file is part of the Interpolated Polyline (https://github.com/fzi-forschungszentrum-informatik/P3IV),
 * copyright by FZI Forschungszentrum Informatik, licensed under the BSD-3 license (see LICENSE file in main directory)
 */

#include "route_option.hpp"

namespace p3iv_types {


RouteOption::RouteOption(const VectorPoint2d& right, const VectorPoint2d& center, const VectorPoint2d& left)
        : corridor(DrivingCorridor(right, center, left)) {

    /*
    std::vector<double> xs;
    std::vector<double> ys;
    xs.reserve(route.size());
    ys.reserve(route.size());
    for (BasicPoint2d p : route) {
        xs.push_back(p(0));
        ys.push_back(p(1));
    }
    interpolatedPolyline_ = InterpolatedPolyline(xs, ys);
    */
}

RouteOption::RouteOption(const DrivingCorridor& drivingCorridor) : corridor(drivingCorridor) {

    /*
    std::vector<double> xs;
    std::vector<double> ys;
    xs.reserve(route.size());
    ys.reserve(route.size());
    for (BasicPoint2d p : route) {
        xs.push_back(p(0));
        ys.push_back(p(1));
    }
    interpolatedPolyline_ = InterpolatedPolyline(xs, ys);
    */
}

void RouteOption::setDrivingCorridor(const DrivingCorridor& drivingCorridor) {
    corridor = drivingCorridor;
}

/*
BasicPoint2d Route::convertToCartesian(const BasicPoint2d& frenet) {
    std::tuple<double, double> xy = interpolatedPolyline_.reconstruct(frenet(0), frenet(1));
    return BasicPoint2d(std::get<0>(xy), std::get<1>(xy));
}

BasicPoint2d Route::convertToFrenet(const BasicPoint2d& cartesian) {
    std::tuple<double, double> ld = interpolatedPolyline_.match(cartesian(0), cartesian(1));
    return BasicPoint2d(std::get<0>(ld), std::get<1>(ld));
}

const std::vector<BasicPoint2d>& Route::points() {
    return routePoints_;
}
*/

} // namespace p3iv_types