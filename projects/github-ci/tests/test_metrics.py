import math
import unittest
from research_math import rmse


class MetricsTest(unittest.TestCase):
    def test_identical(self):
        self.assertEqual(rmse([1,2,3],[1,2,3]),0)

    def test_known_error(self):
        self.assertAlmostEqual(rmse([0,0],[3,4]),math.sqrt(12.5))

    def test_invalid_input(self):
        for left,right in [([],[]),([1],[1,2]),([float('nan')],[0]),([float('inf')],[1])]:
            with self.subTest(left=left,right=right):
                with self.assertRaises(ValueError):
                    rmse(left,right)


if __name__=='__main__':
    unittest.main()
