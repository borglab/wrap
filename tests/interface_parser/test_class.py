import unittest

from gtwrap.interface_parser.classes import (Class, Constructor, DunderMethod,
                                             Method, Operator, StaticMethod)
from gtwrap.template_instantiator.classes import InstantiatedClass


class TestClass(unittest.TestCase):
    """Unit tests for the Class class."""

    def test_constructor(self):
        """Test for class constructor."""
        ret = Constructor.rule.parseString("f();")[0]
        self.assertEqual("f", ret.name)
        self.assertEqual(0, len(ret.args))

        ret = Constructor.rule.parseString(
            "f(const int x, const Class& c, Class* t);")[0]
        print(ret.args)
        self.assertEqual("f", ret.name)
        self.assertEqual(3, len(ret.args))

        ret = Constructor.rule.parseString(
            """ForwardKinematics(const gtdynamics::Robot& robot,
                    const string& start_link_name, const string& end_link_name,
                    const gtsam::Values& joint_angles,
                    const gtsam::Pose3& l2Tp = gtsam::Pose3());""")[0]
        self.assertEqual("ForwardKinematics", ret.name)
        self.assertEqual(5, len(ret.args))
        self.assertEqual("gtsam::Pose3()", ret.args[4].default_value)

    def test_constructor_templated(self):
        """Test for templated class constructor."""
        f = """
        template<T = {double, int}>
        Class();
        """
        ret = Constructor.rule.parseString(f)[0]
        self.assertEqual("Class", ret.name)
        self.assertEqual(0, len(ret.args))

        f = """
        template<T = {double, int}>
        Class(const T& name);
        """
        ret = Constructor.rule.parseString(f)[0]
        self.assertEqual("Class", ret.name)
        self.assertEqual(1, len(ret.args))
        print(type(ret.args.args_list[0]))
        print(ret.args.args_list[0].to_cpp())
        self.assertEqual("const T& name", ret.args.args_list[0].to_cpp())
        self.assertEqual("const T& name", ret.args.args_list[0].to_cpp())

    def test_method(self):
        """Test for a class method."""
        ret = Method.rule.parseString("int f();")[0]
        self.assertEqual("f", ret.name)
        self.assertEqual(0, len(ret.args))
        self.assertTrue(not ret.is_const)

        ret = Method.rule.parseString("int f() const;")[0]
        self.assertEqual("f", ret.name)
        self.assertEqual(0, len(ret.args))
        self.assertTrue(ret.is_const)

        ret = Method.rule.parseString(
            "int f(const int x, const Class& c, Class* t) const;")[0]
        self.assertEqual("f", ret.name)
        self.assertEqual(3, len(ret.args))

        ret = Method.rule.parseString(
            "pair<First ,Second*> create_MixedPtrs();")[0]
        self.assertEqual("create_MixedPtrs", ret.name)
        self.assertEqual(0, len(ret.args))
        self.assertEqual("First", ret.return_type.type1.name)
        self.assertEqual("Second", ret.return_type.type2.name)

    def test_static_method(self):
        """Test for static methods."""
        ret = StaticMethod.rule.parseString("static int f();")[0]
        self.assertEqual("f", ret.name)
        self.assertEqual(0, len(ret.args))

        ret = StaticMethod.rule.parseString(
            "static int f(const int x, const Class& c, Class* t);")[0]
        self.assertEqual("f", ret.name)
        self.assertEqual(3, len(ret.args))

    def test_dunder_method(self):
        """Test for special python dunder methods."""
        iter_string = "__iter__();"
        ret = DunderMethod.rule.parse_string(iter_string)[0]
        self.assertEqual("iter", ret.name)

        contains_string = "__contains__(size_t key);"
        ret = DunderMethod.rule.parse_string(contains_string)[0]
        self.assertEqual("contains", ret.name)
        self.assertTrue(len(ret.args) == 1)

    def test_unary_operator_overload(self):
        """Test for unary operator overloading."""
        wrap_string = "gtsam::Vector2 operator-() const;"
        ret = Operator.rule.parseString(wrap_string)[0]
        self.assertEqual("operator", ret.name)
        self.assertEqual("-", ret.operator)
        self.assertEqual("Vector2", ret.return_type.type1.name)
        self.assertEqual("gtsam::Vector2", ret.return_type.type1.to_cpp())
        self.assertTrue(len(ret.args) == 0)
        self.assertTrue(ret.is_unary)

    def test_binary_operator_overload(self):
        """Test for binary operator overloading."""
        wrap_string = "gtsam::Vector2 operator*(const gtsam::Vector2 &v) const;"
        ret = Operator.rule.parseString(wrap_string)[0]
        self.assertEqual("operator", ret.name)
        self.assertEqual("*", ret.operator)
        self.assertEqual("Vector2", ret.return_type.type1.name)
        self.assertEqual("gtsam::Vector2", ret.return_type.type1.to_cpp())
        self.assertTrue(len(ret.args) == 1)
        self.assertEqual("const gtsam::Vector2&", ret.args[0].type.to_cpp())
        self.assertTrue(not ret.is_unary)
        self.assertTrue(not ret.is_unary)

    def test_base_class(self):
        """Test a base class."""
        ret = Class.rule.parseString("""
            virtual class Base {
            };
            """)[0]
        self.assertEqual("Base", ret.name)
        self.assertEqual(0, len(ret.ctors))
        self.assertEqual(0, len(ret.methods))
        self.assertEqual(0, len(ret.static_methods))
        self.assertEqual(0, len(ret.properties))
        self.assertTrue(ret.is_virtual)

    def test_empty_class(self):
        """Test an empty class declaration."""
        ret = Class.rule.parseString("""
            class FactorIndices {};
        """)[0]
        self.assertEqual("FactorIndices", ret.name)
        self.assertEqual(0, len(ret.ctors))
        self.assertEqual(0, len(ret.methods))
        self.assertEqual(0, len(ret.static_methods))
        self.assertEqual(0, len(ret.properties))
        self.assertTrue(not ret.is_virtual)

    def test_class(self):
        """Test a non-trivial class."""
        ret = Class.rule.parseString("""
        class SymbolicFactorGraph {
            SymbolicFactorGraph();
            SymbolicFactorGraph(const gtsam::SymbolicBayesNet& bayesNet);
            SymbolicFactorGraph(const gtsam::SymbolicBayesTree& bayesTree);

            // Dummy static method
            static gtsam::SymbolidFactorGraph CreateGraph();

            void push_back(gtsam::SymbolicFactor* factor);
            void print(string s) const;
            bool equals(const gtsam::SymbolicFactorGraph& rhs, double tol) const;
            size_t size() const;
            bool exists(size_t idx) const;

            // Standard interface
            gtsam::KeySet keys() const;
            void push_back(const gtsam::SymbolicFactorGraph& graph);
            void push_back(const gtsam::SymbolicBayesNet& bayesNet);
            void push_back(const gtsam::SymbolicBayesTree& bayesTree);

            /* Advanced interface */
            void push_factor(size_t key);
            void push_factor(size_t key1, size_t key2);
            void push_factor(size_t key1, size_t key2, size_t key3);
            void push_factor(size_t key1, size_t key2, size_t key3, size_t key4);

            gtsam::SymbolicBayesNet* eliminateSequential();
            gtsam::SymbolicBayesNet* eliminateSequential(
                const gtsam::Ordering& ordering);
            gtsam::SymbolicBayesTree* eliminateMultifrontal();
            gtsam::SymbolicBayesTree* eliminateMultifrontal(
                const gtsam::Ordering& ordering);
            pair<gtsam::SymbolicBayesNet*, gtsam::SymbolicFactorGraph*>
                eliminatePartialSequential(const gtsam::Ordering& ordering);
            pair<gtsam::SymbolicBayesNet*, gtsam::SymbolicFactorGraph*>
                eliminatePartialSequential(const gtsam::KeyVector& keys);
            pair<gtsam::SymbolicBayesTree*, gtsam::SymbolicFactorGraph*>
                eliminatePartialMultifrontal(const gtsam::Ordering& ordering);
            gtsam::SymbolicBayesNet* marginalMultifrontalBayesNet(
                const gtsam::Ordering& ordering);
            gtsam::SymbolicBayesNet* marginalMultifrontalBayesNet(
                const gtsam::KeyVector& key_vector,
                const gtsam::Ordering& marginalizedVariableOrdering);
            gtsam::SymbolicFactorGraph* marginal(const gtsam::KeyVector& key_vector);
            };
        """)[0]

        self.assertEqual("SymbolicFactorGraph", ret.name)
        self.assertEqual(3, len(ret.ctors))
        self.assertEqual(23, len(ret.methods))
        self.assertEqual(1, len(ret.static_methods))
        self.assertEqual(0, len(ret.properties))
        self.assertTrue(not ret.is_virtual)

    def test_templated_class(self):
        """Test a templated class."""
        ret = Class.rule.parseString("""
        template<POSE, POINT>
        class MyFactor {};
        """)[0]

        self.assertEqual("MyFactor", ret.name)
        self.assertEqual("<POSE, POINT>", ret.template.to_cpp())

    def test_class_inheritance(self):
        """Test for class inheritance."""
        ret = Class.rule.parseString("""
        virtual class Null: gtsam::noiseModel::mEstimator::Base {
          Null();
          void print(string s) const;
          static gtsam::noiseModel::mEstimator::Null* Create();

          // enabling serialization functionality
          void serializable() const;
        };
        """)[0]
        self.assertEqual("Null", ret.name)
        self.assertEqual(1, len(ret.ctors))
        self.assertEqual(2, len(ret.methods))
        self.assertEqual(1, len(ret.static_methods))
        self.assertEqual(0, len(ret.properties))
        self.assertEqual("Base", ret.parent_class.name)
        self.assertEqual(["gtsam", "noiseModel", "mEstimator"],
                         ret.parent_class.namespaces)
        self.assertTrue(ret.is_virtual)

        ret = Class.rule.parseString(
            "class ForwardKinematicsFactor : gtsam::BetweenFactor<gtsam::Pose3> {};"
        )[0]
        ret = InstantiatedClass(ret,
                                [])  # Needed to correctly parse parent class
        self.assertEqual("ForwardKinematicsFactor", ret.name)
        self.assertEqual("BetweenFactor", ret.parent_class.name)
        self.assertEqual(["gtsam"], ret.parent_class.namespaces)
        self.assertEqual("Pose3", ret.parent_class.template_params[0].name)
        self.assertEqual(["gtsam"],
                         ret.parent_class.template_params[0].namespaces)

    def test_class_with_enum(self):
        """Test for class with nested enum."""
        ret = Class.rule.parseString("""
        class Pet {
            Pet(const string &name, Kind type);
            enum Kind { Dog, Cat };
        };
        """)[0]
        self.assertEqual(ret.name, "Pet")
        self.assertEqual(ret.enums[0].name, "Kind")
