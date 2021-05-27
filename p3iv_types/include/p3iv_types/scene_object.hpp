#pragma once
#include <memory>
#include "motion_state.hpp"
#include "tracked_object.hpp"

namespace p3iv_types {


class SceneModel;
class RouteOption;


struct SceneObject : TrackedVehicle {
public:
    SceneObject(const int id, const double width, const double length);

    SceneObject(const int id,
                const double width,
                const double length,
                const MotionState& motionState,
                const double progress,
                std::vector<int> currentLanelets,
                const bool hasRightOfWay);

    void setMotionState(const MotionState& motionState);


    MotionState state;
    double progress;
    std::vector<int> currentLanelets;
    std::vector<std::shared_ptr<RouteOption>> routeOptions;
    std::vector<std::shared_ptr<SceneModel>> routeScenes;
    bool hasRightOfWay;
};

} // namespace p3iv_types