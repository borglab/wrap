namespace example {
virtual class Base {};
virtual class First : example::Base { void serializable() const; };
virtual class Second : example::Base { void serializable() const; };
template<A, B> virtual class Pair : example::Base {};
@serializable typedef example::Pair<int, double> PairID;
}
