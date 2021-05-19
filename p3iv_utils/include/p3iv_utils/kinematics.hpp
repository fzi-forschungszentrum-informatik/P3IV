#pragma once

#include "kinematic_bicycle_model.hpp"

namespace p3iv_utils {


template <typename T>
class Kinematics {

public:
    Kinematics() = default;

    Kinematics(T wheelbase) : wheelbase_{wheelbase} {};

    T turnCurvature(T vx, T vy, T ax, T ay) {
        return turn_curvature(vx, vy, ax, ay);
    }

    T yawAngle(T vx, T vy) {
        return yaw_angle(vx, vy);
    }

    T steeringAngle(T vx, T vy, T ax, T ay) {
        auto kappa = this->turnCurvature(vx, vy, ax, ay);
        return steering_angle(kappa, T(wheelbase_));
    }

    T speed(T vx, T vy) {
        return T(std::pow(T(vx * vx + vy * vy), 0.5));
    }

    T acceleration(T ax, T ay) {
        return T(std::pow(T(ax * ax + ay * ay), 0.5));
    }

    T centripetalAcceleration(T vx, T vy, T ax, T ay) {
        T kappa = this->turnCurvature(vx, vy, ax, ay);
        T speed = this->speed(vx, vy);
        return centripetal_acceleration(kappa, speed);
    }

private:
    T wheelbase_{};
};

} // namespace p3iv_utils