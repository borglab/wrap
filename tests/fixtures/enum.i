enum Color { Red, Green, Blue };

class Pet {
  enum Kind { Dog, Cat };

  Pet(const string &name, Kind type);
  void setColor(const Color& color);
  Color getColor() const;

  string name;
  Kind type;
};

namespace gtsam {
// Test global enums
enum VerbosityLM {
  SILENT,
  SUMMARY,
  TERMINATION,
  LAMBDA,
  TRYLAMBDA,
  TRYCONFIG,
  DAMPED,
  TRYDELTA
};

// Test multiple enums in a classs
class MCU {
  MCU();

  enum Avengers {
    CaptainAmerica,
    IronMan,
    Hulk,
    Hawkeye,
    Thor
  };

  enum GotG {
    Starlord,
    Gamorra,
    Rocket,
    Drax,
    Groot
  };

};

template<PARAMS>
class Optimizer {
  enum Verbosity {
    SILENT,
    SUMMARY,
    VERBOSE
  };

  void setVerbosity(const This::Verbosity value);
};

typedef gtsam::Optimizer<gtsam::GaussNewtonParams> OptimizerGaussNewtonParams;

}  // namespace gtsam
