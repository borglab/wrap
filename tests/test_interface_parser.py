"""
GTSAM Copyright 2010-2020, Georgia Tech Research Corporation,
Atlanta, Georgia 30332-0415
All Rights Reserved

See LICENSE for the license information

Tests for interface_parser.

Author: Varun Agrawal
"""

# pylint: disable=import-error,wrong-import-position

import os
import sys
import unittest

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from gtwrap.interface_parser import Module, Namespace


class TestInterfaceParser(unittest.TestCase):
    """Test driver for all classes in interface_parser.py."""

    def test_namespace(self):
        """Test for namespace parsing."""
        namespace = Namespace.rule.parseString("""
        namespace gtsam {
          #include <gtsam/geometry/Point2.h>
          class Point2 {
            Point2();
            Point2(double x, double y);
            double x() const;
            double y() const;
            int dim() const;
            char returnChar() const;
            void argChar(char a) const;
            void argUChar(unsigned char a) const;
          };

          #include <gtsam/geometry/Point3.h>
          class Point3 {
            Point3(double x, double y, double z);
            double norm() const;

            // static functions - use static keyword and uppercase
            static double staticFunction();
            static gtsam::Point3 StaticFunctionRet(double z);

            // enabling serialization functionality
            void serialize() const; // Just triggers a flag internally
          };
        }""")[0]
        self.assertEqual("gtsam", namespace.name)

    def test_module(self):
        """Test module parsing."""
        module = Module.parseString("""
        namespace one {
            namespace two {
                namespace three {
                    class Class123 {
                    };
                }
                class Class12a {
                };
            }
            namespace two_dummy {
                namespace three_dummy{

                }
                namespace fourth_dummy{

                }
            }
            namespace two {
                class Class12b {

                };
            }
            int oneVar;
        }

        class Global{
        };
        int globalVar;
        """)

        self.assertEqual(["one", "Global", "globalVar"],
                         [x.name for x in module.content])
        self.assertEqual(["two", "two_dummy", "two", "oneVar"],
                         [x.name for x in module.content[0].content])


if __name__ == '__main__':
    unittest.main()
