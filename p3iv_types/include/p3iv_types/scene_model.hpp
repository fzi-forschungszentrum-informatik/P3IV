
#pragma once
#include <map>
#include <memory>
#include "route_option.hpp"
#include "scene_object.hpp"
#include "traffic_rules.hpp"
#include "visibility_information.hpp"


namespace p3iv_types {

class SceneModel {
public:
    SceneModel(const int& ObjectId) : id{ObjectId} {
    }

    SceneModel(const int& ObjectId, const RouteOption& routeOption) : id{ObjectId}, route(routeOption) {
    }

    void addSceneObject(const int id,
                        const double width,
                        const double length,
                        const MotionState& motionState,
                        const double progress,
                        std::vector<int> currentLanelets,
                        const bool hasRightOfWay);

    void addSceneObject(const SceneObject SceneObject);

    bool getSceneObject(const int agentId, SceneObject& sceneObject);

    std::map<int, SceneObject>& getSceneObjects();


protected:
    const int id;
    std::map<int, SceneObject> sceneObjects;
    RouteOption route;
    Visibility visibility;
};
} // namespace p3iv_types