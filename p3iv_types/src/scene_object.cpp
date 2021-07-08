/*
 * This file is part of the Interpolated Polyline (https://github.com/fzi-forschungszentrum-informatik/P3IV),
 * copyright by FZI Forschungszentrum Informatik, licensed under the BSD-3 license (see LICENSE file in main directory)
 */

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


} // namespace p3iv_types