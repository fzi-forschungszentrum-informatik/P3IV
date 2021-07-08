/*
 * This file is part of the Interpolated Polyline (https://github.com/fzi-forschungszentrum-informatik/P3IV),
 * copyright by FZI Forschungszentrum Informatik, licensed under the BSD-3 license (see LICENSE file in main directory)
 */

#pragma once

#include <chrono>
#include <boost/math/interpolators/barycentric_rational.hpp>

namespace p3iv_utils {

std::vector<double> chrono2double(const std::vector<std::chrono::milliseconds>& t) {
    std::vector<double> x;
    x.reserve(t.size());
    for (auto t_ : t) {
        x.push_back(t_.count());
    }
    return x;
}

template <typename T>
inline std::vector<T> interpolate(const std::vector<T>& xBase,
                                  const std::vector<T>& yBase,
                                  const std::vector<T>& xIntrp) {

    boost::math::barycentric_rational<T> interpolant(xBase.data(), yBase.data(), yBase.size());
    std::vector<T> yIntrp;
    yIntrp.reserve(xIntrp.size());

    for (auto& x : xIntrp) {
        yIntrp.push_back(interpolant(x));
    }

    return yIntrp;
}

template <typename T>
inline std::vector<T> interpolate(const std::vector<std::chrono::milliseconds>& tBase,
                                  const std::vector<T>& yBase,
                                  const std::vector<std::chrono::milliseconds>& tIntrp) {

    std::vector<double> xBase = chrono2double(tBase);
    std::vector<double> xIntrp = chrono2double(tIntrp);

    auto yIntrp = interpolate(xBase, yBase, xIntrp);

    return yIntrp;
}


} // namespace p3iv_utils