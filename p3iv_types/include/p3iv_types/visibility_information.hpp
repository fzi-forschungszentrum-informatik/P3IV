#pragma once
#include <vector>

namespace p3iv_types {


struct VisibilityInformation {
    VisibilityInformation(double distance_, double visibilityOfIntersection_)
            : distance(distance_), visibilityOfIntersection(visibilityOfIntersection_){};
    double distance;
    double visibilityOfIntersection;
};

class Visibility {
public:
    void setVisibility(const std::vector<double> distances, const std::vector<double> visibilityOfIntersections);
    VisibilityInformation getVisibility(const int index);

protected:
    std::vector<VisibilityInformation> visibleDistances_;
};


} // namespace p3iv_types