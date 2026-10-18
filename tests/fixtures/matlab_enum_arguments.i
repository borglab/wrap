namespace demo {
namespace nested {

class NoLocalEnum {
  static demo::nested::Owner::Mode Echo(demo::nested::Owner::Mode mode);
};

// The owner is declared later, and Consumer has its own enum of the same name.
class Consumer {
  enum Mode { Local };
  Consumer(demo::nested::Owner::Mode mode);
  static demo::nested::Owner::Mode Echo(demo::nested::Owner::Mode mode);
  demo::nested::Owner::Mode get() const;
  void set(const demo::nested::Owner::Mode& mode);
  std::optional<demo::nested::Owner::Mode> maybe(
      std::optional<demo::nested::Owner::Mode> mode) const;
  pair<demo::nested::Owner::Mode, demo::nested::Owner::Mode> pair() const;
  demo::nested::Owner::Mode mode;
};

class Owner {
  enum Mode { First, Second };
  Owner();
};

demo::nested::Owner::Mode echo(demo::nested::Owner::Mode mode);

} // namespace nested
} // namespace demo
