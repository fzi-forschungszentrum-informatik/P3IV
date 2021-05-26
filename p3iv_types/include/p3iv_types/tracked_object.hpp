#pragma once
namespace p3iv_types {

struct TrackedObject {
    int id{-1};
    double existenceProbability{1.0};
};


struct TrackedVehicle : TrackedObject {
    double width;
    double length;
};


} // namespace p3iv_types