#pragma once
namespace p3iv_types {

struct TrackedObject {
    TrackedObject(const int& ObjectId) : id{ObjectId} {
    }
    int id{-1};
    // todo!
    // const int id{-1};
    double existenceProbability{1.0};
};


struct TrackedVehicle : TrackedObject {
    TrackedVehicle(const int& id, const double& w, const double& l) : TrackedObject(id), width(w), length(l) {
    }
    // length and width might be updated upon better measurements or inference
    // therefore, do not define them as 'const'
    double length;
    double width;
};


} // namespace p3iv_types