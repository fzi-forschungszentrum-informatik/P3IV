#include "visibility_information.hpp"
#include <cassert>


namespace p3iv_types {


void Visibility::setVisibility(const std::vector<double> distances,
                               const std::vector<double> visibilityOfIntersections) {
    assert(distances.size() == visibilityOfIntersections.size());
    for (int i = 0; i < distances.size(); i++) {
        visibleDistances_.push_back(VisibilityInformation(distances[i], visibilityOfIntersections[i]));
    }
}

VisibilityInformation Visibility::getVisibility(const int index) {
    return visibleDistances_[index];
}


} // namespace p3iv_types
