import unittest
import colorfunc as func

class TestColorFunc(unittest.TestCase):
    def test_func_value(self):
        tests = [
            # [period, range, function, step_num, expected]
            [10, (0, 10), lambda x: (10 - x) / 10, 2, 0.8],
            [10, (0, 10), lambda x: 9, 2, 1],
            [10, (0, 10), lambda x: -20, 2, 0]
        ]
        for t in tests:
            # instantiate func class
            f = func.ColorFunc()
            f.period = t[0]
            f.range = t[1]
            f.func = t[2]
            result = f.func_value(t[3])
            self.assertEqual(result, t[4])
