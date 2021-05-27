#include <numeric>
#include <vector>
#include "scene_model.hpp"
#include "gtest/gtest.h"


using namespace p3iv_types;


TEST(SceneModel, SceneModelDefaultCtor) {
    int id = 0;
    SceneModel sceneModel(id);
}

TEST(SceneModel, SceneModeAddSceneObject) {
    int id = 0;
    SceneModel sceneModel(id);

    SceneObject sceneObject(5, 2.3, 3.7);
    MotionState m{};
    m.position.setMean(6.0, 8.0);
    m.position.setCovariance(9.0, 0.0, 0.0, 16.0);
    sceneObject.state = m;
    sceneModel.addSceneObject(sceneObject);
}