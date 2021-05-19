#pragma once

#include <cmath>
#include <vector>


namespace p3iv_utils {

template <typename T>
inline T derive_1(const T& dt, const T* const p0, const T* const p1) {
    /// first order finite differences
    /// forward difference, if p0 is the current value
    /// backward difference, if p1 is the current value
    return (p1[0] - p0[0]) / (dt);
}

template <typename T>
inline T derive_1(const T& dt, const T& x0, const T& x1) {
    /// first order finite differences
    /// forward difference, if p0 is the current value
    /// backward difference, if p1 is the current value
    return (x1 - x0) / (dt);
}

template <typename T>
inline T derive_2(const T& dt, const T* const p0, const T* const p1, const T* const p2) {
    /// second order finite differences
    /// forward difference, if p0 is the current value
    /// backward difference, if p2 is the current value
    return (p0[0] - T(2) * p1[0] + p2[0]) / (dt * dt);
}

template <typename T>
inline T derive_2(const T& dt, const T& x0, const T& x1, const T& x2) {
    /// second order finite differences
    /// forward difference, if p0 is the current value
    /// backward difference, if p2 is the current value
    return (x0 - T(2) * x1 + x2) / (dt * dt);
}

template <typename T>
inline T derive_3(const T& dt, const T* const p0, const T* const p1, const T* const p2, const T* const p3) {
    /// third order finite differences
    /// forward difference, if p0 is the current value
    /// backward difference, if p3 is the current value
    return (-p0[0] + T(3) * p1[0] - T(3) * p2[0] + p3[0]) / (dt * dt * dt);
}

template <typename T>
inline T derive_3(const T& dt, const T& x0, const T& x1, const T& x2, const T& x3) {
    /// third order finite differences
    /// forward difference, if p0 is the current value
    /// backward difference, if p3 is the current value
    return (-x0 + T(3) * x1 - T(3) * x2 + x3) / (dt * dt * dt);
}
} // namespace p3iv_utils