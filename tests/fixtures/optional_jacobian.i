namespace gtsam {

#include <gtsam/geometry/Pose3.h>

class Pose3 {
  Pose3();

  gtsam::Point3 transformFrom(
      const gtsam::Point3& point,
      gtsam::OptionalJacobian<3, 6> Hself = nullptr,
      gtsam::OptionalJacobian<3, 3> Hpoint = nullptr) const;

  gtsam::Pose3 inverse(
      gtsam::OptionalJacobian<6, 6> H = nullptr) const;

  static gtsam::Pose3 Expmap(
      gtsam::Vector xi,
      gtsam::OptionalJacobian<6, 6> Hxi = nullptr);
};

}
