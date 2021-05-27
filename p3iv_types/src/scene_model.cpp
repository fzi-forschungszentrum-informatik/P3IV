#include "scene_model.hpp"


namespace p3iv_types {


void SceneModel::addSceneObject(const int agentId,
                                const double width,
                                const double length,
                                const MotionState& motionState,
                                const double progress,
                                std::vector<int> currentLanelets,
                                const bool hasRightOfWay) {

    SceneObject sceneObject(agentId, width, length);
    sceneObject.state = motionState;
    sceneObject.progress = progress;
    sceneObject.currentLanelets = currentLanelets;
    sceneObject.hasRightOfWay = hasRightOfWay;
    sceneObjects.insert({agentId, sceneObject});
}

void SceneModel::addSceneObject(const SceneObject sceneObject) {
    sceneObjects.insert({sceneObject.id, sceneObject});
}

bool SceneModel::getSceneObject(const int agentId, SceneObject& sceneObject) {
    if (sceneObjects.find(agentId) == sceneObjects.end()) {
        return false;
    } else {
        sceneObject = sceneObjects.find(agentId)->second;
        return true;
    }
}

std::map<int, SceneObject>& SceneModel::getSceneObjects() {
    return sceneObjects;
}

} // namespace p3iv_types