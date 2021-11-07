/*
 * This file is part of the Interpolated Polyline (https://github.com/fzi-forschungszentrum-informatik/P3IV),
 * copyright by FZI Forschungszentrum Informatik, licensed under the BSD-3 license (see LICENSE file in main directory)
 */

#pragma once
#include <cmath>
#include <iostream>
#include <limits>


namespace interpolated_polyline {

/**
 * Implement own hypothenuse calculation for templated stuff
 */
template <typename T>
inline T hypot(T x, T y) {
    return T(sqrt(x * x + y * y));
}

/**
 * Implement own absolute value calculation for templated stuff
 */
template <class T>
static inline T abs(T a) {
    return a < 0 ? -a : a;
}

/**
 * Find the mode (type) of segments
 */
enum class SegmentMode { FIRST, MIDDLE, LAST };


class InterpolatedLineSegment {
public:
    static constexpr double MaximumValue = std::numeric_limits<double>::max();

    InterpolatedLineSegment(double x0, double y0, double th0, double x1, double y1, double th1, SegmentMode mode)
            : xB_(x0), yB_(y0), thetaB_(th0), thetaT_(th1), theta_(std::atan2(y1 - y0, x1 - x0)),
              cosTheta_(std::cos(theta_)), sinTheta_(std::sin(theta_)), hyp_(std::hypot(y1 - y0, x1 - x0)),
              mB_(std::tan(thetaB_ - theta_)), mT_(std::tan(thetaT_ - theta_)), mode_(mode) {
    }

    // Calculate distance of point x, y to this segment
    template <typename T>
    T operator()(const T x, const T y, T& lambda) const {
        T xH, yH;
        convertHesseNormal(x, y, xH, yH);

        T signum = getSign(yH);
        lambda = getLambda(T(hyp_), T(mB_), T(mT_), xH, yH);

        T d;
        if (clipLambda(lambda)) {
            d = T(signum * normalDistance(T(hyp_), xH, yH, lambda));
        } else {
            // invalid case; return very big distance
            d = T(signum * T(MaximumValue));
        }
        return d;
    }

    /**
     * Get Cartesian x of base
     */
    double xB() const {
        return xB_;
    }

    /**
     * Get Cartesian y of base
     */
    double yB() const {
        return yB_;
    }

    /**
     * Get incline of line segment
     */
    double theta() const {
        return theta_;
    }

    /**
     * Get length of line segment
     */
    double length(const double lambda = 1.0) const {
        return lambda * hyp_;
    }

    /**
     * Get interpolated tangent at that point
     */
    template <typename T>
    T tangent(const T& x, const T& y, const T& d, const T& lambda) const {
        T xH, yH;
        convertHesseNormal(x, y, xH, yH);
        // add 'theta_' to get tangent in global Cartesian frame
        T tangent = getTangent(hyp_, xH, yH, d, lambda, mB_, mT_) + theta_;
        return tangent;
    }


protected:
    /**
     * Check interpolation factor if it is valid and clip it
     */
    template <typename T>
    bool clipLambda(T& lambda) const {
        bool valid = true;
        if (lambda < T(0.0) || lambda > T(1.0)) {
            if (mode_ == SegmentMode::MIDDLE) {
                // skip to the next segment in polyline
                valid = false;
            } else if (mode_ == SegmentMode::FIRST) {
                if (lambda < T(0.)) {
                    lambda = T(0.0);
                } else {
                    valid = false;
                }
            } else if (mode_ == SegmentMode::LAST) {
                // let the last segment's lambda be flexible
                if (lambda > T(1.)) {
                    lambda = T(1.0);
                } else if (lambda < T(0.0)) {
                    valid = false;
                }
            } else {
                // dummy; won't jump here
                valid = false;
            }
        }
        return valid;
    }

    /**
     * Convert to Hesse-normal form; aka line-aligned coordinate frame
     */
    template <typename T>
    void convertHesseNormal(const T& x, const T& y, T& xH, T& yH) const {
        // calculate the difference of the given point to the one end of the line
        T xx = x - T(xB_);
        T yy = y - T(yB_);

        // rotate point Theta clockwise for line-referenced coordinates
        xH = xx * T(cosTheta_) + yy * T(sinTheta_);
        yH = -xx * T(sinTheta_) + yy * T(cosTheta_);
    }

    /**
     * Get tangent vector angle in line-aligned coordinates
     */
    template <typename T>
    static T getTangent(const T& l, const T& xH, const T& yH, const T& d, const T& lambda, const T& mB, const T& mT) {

        if (d == T(0.0)) {
            return T(lambda * mB + (1 - lambda) * mT);
        }

        T dx = T(-1.) * (lambda * l - xH) / d;
        T dy = T(-1.) * (-yH) / d;
        T dTheta = atan2(dy, dx);         ///< normal vector
        T tangent = dTheta - T(M_PI) / 2; ///< tangent vector
        return tangent;
    }

    /**
     * Calculate interpolation factor lambda
     */
    template <typename T>
    inline static T getLambda(T l, T mb, T mt, T xH, T yH) {
        const T nominator = xH + yH * mb; ///< Eq. (3.9) in Diss. Ziegler
        const T denominator = l - yH * (mt - mb);
        T lambda = nominator / denominator;
        return lambda;
    }

    /**
     * Find the normal distance in Hesse normal form
     */
    template <typename T>
    inline static T normalDistance(const T l, const T xH, const T yH, const T lambda) {
        return hypot((lambda * l - xH), yH);
    }

    /**
     * Calculate sign of a templated type
     */
    template <typename T>
    inline static T getSign(T yH) {
        T signum = yH > T(0.0) ? T(1.0) : T(-1.);
        return signum;
    }

private:
    /**
     * Member variables
     */
    double xB_, yB_, thetaB_, thetaT_, theta_, cosTheta_, sinTheta_, hyp_, mB_, mT_;
    SegmentMode mode_;
};
} // namespace interpolated_polyline
