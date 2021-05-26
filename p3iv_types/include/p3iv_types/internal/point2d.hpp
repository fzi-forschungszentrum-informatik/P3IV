#pragma once
#include <cassert>
#include <cmath>
#include <iostream>
#include <stdexcept>
#include <unistd.h>
#include <vector>


namespace p3iv_types {
namespace internal {


template <typename T>
struct Point2d {
    T x0, x1;
};

template <typename T>
Point2d<T> operator+(const Point2d<T>& lhs, const Point2d<T>& rhs) {
    return {lhs.x0 + rhs.x0, lhs.x1 + rhs.x1};
}

template <typename T>
Point2d<T> operator-(const Point2d<T>& lhs, const Point2d<T>& rhs) {
    return {lhs.x0 - rhs.x0, lhs.x1 - rhs.x1};
}

template <typename T>
Point2d<T> operator/(const Point2d<T>& lhs, const double& rhs) {
    return {lhs.x0 / rhs, lhs.x1 / rhs};
}

template <typename T>
std::ostream& operator<<(std::ostream& os, const Point2d<T>& p) {
    os << p.x0 << "," << p.x1;
    return os;
}

template <typename T>
bool operator==(const Point2d<T>& a, const Point2d<T>& b) {
    return a.x0 == b.x0 && a.x1 == b.x1;
}

template <typename T>
T dot(const Point2d<T>& lhs, const Point2d<T>& rhs) {
    return lhs.x0 * rhs.x0 + lhs.x1 * rhs.x1;
}

template <typename T>
T norm2(const Point2d<T>& p) {
    return std::sqrt(p.x0 * p.x0 + p.x1 * p.x1);
}

template <typename T>
std::vector<T> getValues(const std::vector<Point2d<T>>& points, int component = 0) {
    std::vector<T> x;
    x.reserve(points.size());

    if (component == 0) {
        for (int i = 0; i < points.size(); i++) {
            x.emplace_back(points[i].x0);
        }
    } else if (component == 1) {
        for (int i = 0; i < points.size(); i++) {
            x.emplace_back(points[i].x1);
        }
    } else {
        throw std::runtime_error("error");
    }
    return x;
}

template <typename T>
struct VectorPoint2d {
    VectorPoint2d() = default;

    VectorPoint2d(const std::vector<T>& x, const std::vector<T>& y) {
        assert(x.size() == y.size());
        v_.reserve(x.size());
        for (int i = 0; i < x.size(); i++) {
            Point2d<T> p;
            p.x0 = x[i];
            p.x1 = y[i];
            v_.emplace_back(p);
        }
    }

    std::vector<double> x() {
        return getValues<T>(v_, 0);
    }

    std::vector<double> y() {
        return getValues<T>(v_, 1);
    }

private:
    std::vector<Point2d<T>> v_;
};

} // namespace internal
} // namespace p3iv_types