/*
 * This file is part of the Interpolated Polyline (https://github.com/...),
 * copyright by FZI Forschungszentrum Informatik, licensed under the BSD-3 license (see LICENSE file in main directory)
 */

#pragma once
#include <cassert>
#include <cmath>
#include <iostream>
#include <limits>
#include <string>
#include <tuple>
#include <vector>
#include "interpolated_line_segment.hpp"

namespace interpolated_polyline {


class InterpolatedPolyline {
public:
    static constexpr double MaximumValue = std::numeric_limits<double>::max();

    InterpolatedPolyline() = default;

    InterpolatedPolyline(const std::vector<double>& xy) {
        auto xys = unzipVector<std::vector<double>>(xy);
        init(std::get<0>(xys), std::get<1>(xys));
    }

    InterpolatedPolyline(const std::vector<double>& xs, const std::vector<double>& ys) {
        init(xs, ys);
    }

    /**
     * Calculate distance of a point (x,y) to all line segments and get min
     */
    template <typename T>
    T signedDistance(const T& x, const T& y) const {
        T d, lambda;
        getClosestLineSegment(x, y, d, lambda);
        return d;
    }

    /**
     * Calculate distance of a point (x,y) and its tangent
     */
    template <typename T>
    std::tuple<T, T> tangent(const T& x, const T& y) const {
        T d, lambda;
        int ind = getClosestLineSegment(x, y, d, lambda);
        T tangent = segments_[ind].tangent(x, y, d, lambda);
        return std::make_tuple(d, tangent);
    }

    /**
     * Match a point (x, y) to line (arc-length, normal-distance)
     */
    template <typename T>
    std::tuple<T, T> match(T x, T y) const {
        T d, lambda;
        int ind = getClosestLineSegment(x, y, d, lambda);
        // arclengths_[ind] is the arc-length up until that segment (0 was added to arclengths_)
        T arcl = T(arclengths_[ind]) + T(segments_[ind].length(lambda));
        return std::make_tuple(arcl, d);
    }

    /**
     * Match a point (x, y) to line with tangent at that point (arc-length, normal-distance, tangent)
     */
    template <typename T>
    std::tuple<T, T, T> orientedMatch(T x, T y) const {
        T d, lambda;
        int ind = getClosestLineSegment(x, y, d, lambda);
        T arcl = T(arclengths_[ind]) + T(segments_[ind].length(lambda));
        T tangent = segments_[ind].tangent(x, y, d, lambda);
        return std::make_tuple(arcl, d, tangent);
    }

    /**
     * Reconstruct a point (x, y) from (arc-length, normal-distance)
     */
    template <typename T>
    std::tuple<T, T> reconstruct(T l, T d) {

        int i_base;
        if (l < arclengths_[1]) {
            i_base = 0;
        } else {
            for (i_base = 1; i_base < arclengths_.size(); i_base++) {
                if (l <= arclengths_[i_base]) {
                    break;
                }
            }
            i_base = i_base - 1;
        }

        double arcl_base = arclengths_[i_base];
        double arcl_remain = l - arcl_base;

        assert(arcl_remain >= 0);

        T x = segments_[i_base].xB();
        T y = segments_.at(i_base).yB();
        double theta = segments_[i_base].theta();

        x += arcl_remain * cos(theta);
        y += arcl_remain * sin(theta);

        x += d * (-sin(theta));
        y += d * (cos(theta));
        return std::make_tuple(x, y);
    }

    /**
     * Match arclength and offset to x y
     */
    double maxArclength() {
        return arclengths_.back();
    }

protected:
    /**
     * Internal initialization helper function
     */
    void init(const std::vector<double>& xs, const std::vector<double>& ys) {

        size_t N = ys.size();
        assert(N > 1);
        std::vector<double> ths(N);

        // fill angles
        for (size_t i = 1; i < N - 1; ++i) {
            double dx = xs[i + 1] - xs[i - 1];
            double dy = ys[i + 1] - ys[i - 1];
            ths[i] = atan2(dy, dx);
        }
        ths[0] = atan2(ys[1] - ys[0], xs[1] - xs[0]);
        ths[N - 1] = atan2(ys[N - 1] - ys[N - 2], xs[N - 1] - xs[N - 2]);

        // fill segments
        segments_.reserve(N);
        for (size_t i = 0; i < N - 1; ++i) {
            SegmentMode mode = SegmentMode::MIDDLE;
            if (i == 0)
                mode = SegmentMode::FIRST;
            if (i == N - 2)
                mode = SegmentMode::LAST;

            segments_.emplace_back(
                InterpolatedLineSegment(xs[i], ys[i], ths[i], xs[i + 1], ys[i + 1], ths[i + 1], mode));
        }

        // fill arclength
        arclengths_.resize(segments_.size() + 1);

        arclengths_[0] = 0;
        for (size_t i = 1; i < arclengths_.size(); ++i) {
            arclengths_[i] = arclengths_[i - 1] + (segments_[i - 1]).length();
        }
    }

    /**
     * Internal helper function to get closest line segment to a point
     */
    template <typename T>
    int getClosestLineSegment(const T& x, const T& y, T& d, T& lambda) const {
        int ind = 0;
        d = T(MaximumValue);
        lambda = T(-1);

        for (size_t i = 0; i < segments_.size(); ++i) {
            T tmp_lambda, tmp_tangent;
            T tmp_d = segments_[i](x, y, tmp_lambda);

            if (abs(tmp_d) < abs(d)) {
                ind = i;
                d = tmp_d;
                lambda = tmp_lambda;
            }
        }
        return ind;
    }

    /**
     * Internal helper function to unzip dimension reduced 2D-vector into two 1D-vectors
     */
    template <typename VectorT>
    static std::tuple<VectorT, VectorT> unzipVector(const VectorT xy) {
        size_t N = xy.size() / 2;
        VectorT xs, ys;
        xs.reserve(N);
        ys.reserve(N);

        for (size_t i = 0; i < N; ++i) {
            xs.emplace_back(xy[2 * i]);
            ys.emplace_back(xy[2 * i + 1]);
        }

        return std::make_tuple(xs, ys);
    }

    /**
     * Implement own absolute value calculation for templated stuff
     */
    template <class T>
    static inline T abs(T v) {
        return v < 0 ? -v : v;
    }


private:
    std::vector<InterpolatedLineSegment> segments_;
    std::vector<double> arclengths_;
};
} // namespace interpolated_polyline