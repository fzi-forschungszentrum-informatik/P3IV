/*
 * This file is part of the Interpolated Polyline (https://github.com/fzi-forschungszentrum-informatik/P3IV),
 * copyright by FZI Forschungszentrum Informatik, licensed under the BSD-3 license (see LICENSE file in main directory)
 */

#pragma once

#include <cmath>
#include <limits>


namespace p3iv_utils {


/**
 * Calculates turn radius based on kinematic bicycle model
 * and differential flatness. The center of mass is on the
 * rear axle of the vehicle. The side-slip angle is assumed
 * to be zero. Very precise for very low speeds.
 * @param vx velocity in Cartesian x-direction
 * @param vy velocity in Cartesian y-direction
 * @param ax acceleration in Cartesian x-direction
 * @param ay acceleration in Cartesian y-direction
 * @return turn radius
 */
template <typename T>
T turn_curvature(T vx, T vy, T ax, T ay) {
    T kappa = (vx * ay - vy * ax) / std::pow(vx * vx + vy * vy, 3.0 / 2.0);
    return kappa;
}


/**
 * Yaw angle of the vehicle. Assumes that the vehicle rotates
 * around its rear axle.
 * @param vx velocity in Cartesian x-direction
 * @param vy velocity in Cartesian y-direction
 * @return yaw angle
 */
template <typename T>
T yaw_angle(T vx, T vy) {
    return std::atan2(vy, vx);
}


/**
 * Calculates steering angle of the front wheel based on kinematic model.
 * The side slip angle is assumed to be zero.
 * @param kappa curvature
 * @param wheelbase distance between front and rear axle
 * @return steering wheel angle
 */
template <typename T>
T steering_angle(T kappa, T wheelbase) {
    return T(std::atan2(T(wheelbase) * kappa, 1));
}


/**
 * Calculates lateral acceleration of the vehicle
 * @param kappa curvature
 * @param v speed
 * @return lateral acceleration
 */
template <typename T>
T centripetal_acceleration(T kappa, T v) {
    return T(v * v * kappa);
}


} // namespace p3iv_utils