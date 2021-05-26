#pragma once
#include <vector>

namespace p3iv_types {


struct Stopline {
    Stopline(double distanceToStopline, double hasToStop);
    double distanceToStopline; ///< stopline denoted on the map: the vehicle may right-of-way (see below)
    bool hasToStop;            ///< whether the vehicle has to stop at stopline
};


struct Speedlimit {
    Speedlimit(double speedlimit, double inEffectUntil);
    double speedlimit;    // in m/s
    double inEffectUntil; // in Frenet-CS
};


class TrafficRules {
public:
    void addStopline(const Stopline& stopline);
    void addStopline(const std::vector<double> distanceToStoplines, const std::vector<bool> hasToStops);
    void addSpeedlimit(const Speedlimit& speedlimit);

protected:
    std::vector<Stopline> stoplines_;
    std::vector<Speedlimit> speedlimits_;
};


} // namespace p3iv_types