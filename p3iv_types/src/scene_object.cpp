#include "scene_object.hpp"


namespace p3iv_types {

SceneObject::SceneObject(const int id, const double width, const double length) : TrackedVehicle(id, width, length) {
}


SceneObject::SceneObject(const int id,
                         const double width,
                         const double length,
                         const MotionState& motionState,
                         const double progress,
                         std::vector<int> currentLanelets,
                         const bool hasRightOfWay)
        : TrackedVehicle(id, width, length), state(motionState), progress(progress), currentLanelets(currentLanelets),
          hasRightOfWay(hasRightOfWay) {
}

void SceneObject::setMotionState(const MotionState& motionState) {
    state = motionState;
}


} // namespace p3iv_types