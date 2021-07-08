/*
 * This file is part of the Interpolated Polyline (https://github.com/fzi-forschungszentrum-informatik/P3IV),
 * copyright by FZI Forschungszentrum Informatik, licensed under the BSD-3 license (see LICENSE file in main directory)
 */

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
