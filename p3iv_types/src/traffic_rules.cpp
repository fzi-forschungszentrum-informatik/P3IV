#include "traffic_rules.hpp"
#include <cassert>

namespace p3iv_types {


Stopline::Stopline(double distanceToStopline, double hasToStop)
        : distanceToStopline(distanceToStopline), hasToStop(hasToStop) {
}

Speedlimit::Speedlimit(double speedlimit, double inEffectUntil) : speedlimit(speedlimit), inEffectUntil(inEffectUntil) {
}

void TrafficRules::addStopline(const Stopline& stopline) {
    stoplines_.push_back(stopline);
}

void TrafficRules::addStopline(const std::vector<double> distanceToStoplines, const std::vector<bool> hasToStops) {
    assert(distanceToStoplines.size() == hasToStops.size());
    for (int i = 0; i < distanceToStoplines.size(); i++) {
        Stopline stopline(distanceToStoplines[i], hasToStops[i]);
        addStopline(stopline);
    }
}


void TrafficRules::addSpeedlimit(const Speedlimit& speedlimit) {
    speedlimits_.push_back(speedlimit);
}

} // namespace p3iv_types