#pragma once
namespace p3iv_types {

struct TrackedObject {
    TrackedObject(const int& ObjectId) : id{ObjectId} {
    }
    const int id{-1};
    double existenceProbability{1.0};
};


struct TrackedVehicle : TrackedObject {
    TrackedVehicle(const int& id, const double& w, const double& l) : TrackedObject(id), width(w), length(l) {
    }
    const double width;
    const double length;
};


} // namespace p3iv_types