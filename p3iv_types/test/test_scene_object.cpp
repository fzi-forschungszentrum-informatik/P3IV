#include <numeric>
#include <vector>
#include "motion_state.hpp"
#include "scene_object.hpp"
#include "gtest/gtest.h"


using namespace p3iv_types;


TEST(SceneObject, SceneObjectDefaultCtor) {
    int agentId = 0;
    double width = 2.3;
    double length = 3.6;
    SceneObject sceneObject(agentId, width, length);
}


TEST(SceneObject, SceneObjectCtor) {
    int agentId = 0;
    double width = 2.3;
    double length = 3.6;
    MotionState state;
    double progress = 0.0;
    std::vector<int> currentLanelets{30047};
    bool hasRightOfWay = true;
    SceneObject sceneObject(agentId, width, length, state, progress, currentLanelets, hasRightOfWay);

    ASSERT_EQ(sceneObject.hasRightOfWay, true);
    ASSERT_EQ(sceneObject.length, length);
    ASSERT_EQ(sceneObject.width, width);
}


TEST(SceneObject, SceneObjectSetMotionState) {

    MotionState m{};
    m.position.setMean(6.0, 8.0);
    m.position.setCovariance(9.0, 0.0, 0.0, 16.0);
    m.yaw.setMean(0.0);
    m.yaw.setCovariance(10.0);
    m.velocity.setMean(12.0, 16.0);
    m.velocity.setCovariance(0.0, 0.0, 0.0, 0.0);

    int agentId = 0;
    double width = 2.3;
    double length = 3.6;
    SceneObject sceneObject(agentId, width, length);
    sceneObject.setMotionState(m);
}


int main(int argc, char** argv) {
    google::InitGoogleLogging(argv[0]); // NOLINT
    google::InstallFailureSignalHandler();
    FLAGS_v = 2;
    FLAGS_stderrthreshold = 0;
    FLAGS_colorlogtostderr = true;
    FLAGS_alsologtostderr = false;
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}