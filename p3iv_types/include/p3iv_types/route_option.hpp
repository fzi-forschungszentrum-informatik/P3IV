#pragma once

#include <memory>
#include <vector>
#include "driving_corridor.hpp"
#include "traffic_rules.hpp"
#include "internal/point2d.hpp"

namespace p3iv_types {


struct Crossing {
    double begin;
    double end;
};


class RouteOption {
public:
    RouteOption() = default;

    RouteOption(const VectorPoint2d& right, const VectorPoint2d& center, const VectorPoint2d& left);

    RouteOption(const DrivingCorridor& drivingCorridor);

    void setDrivingCorridor(const DrivingCorridor& drivingCorridor);

protected:
    std::string uuid;
    DrivingCorridor corridor;
    Crossing crossing;
    TrafficRules trafficRules;
};


} // namespace p3iv_types