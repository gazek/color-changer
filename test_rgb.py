import unittest
import rgb

class TestRGB(unittest.TestCase):
    def test_init_happy(self):
        c = (255,0,0)
        o = (2,1,0)
        color = rgb.RGB(c, order=o)
        # verify color
        self.assertEqual(color._color, c)
        # verify order
        self.assertEqual(color._order, o)

    def test_init_invalid_color(self):
        c = (555,0,0)
        o = (2,1,0)
        # should raise
        with self.assertRaises(ValueError):
            color = rgb.RGB(c, order=o)

    def test_init_invalid_order(self):
        c = (255,0,0)
        o = (9,1,0)
        # should raise
        with self.assertRaises(ValueError):
            color = rgb.RGB(c, order=o)

    def test_is_base_color(self):
        tests = [
            [(0, 0, 0), False],
            [(255, 255, 75), False],
            [(255, 100, 255), False],
            [(20, 255, 255), False],
            [(255, 255, 255), False],
            [(255, 0, 0), True],
            [(0, 255, 0), True],
            [(0, 0, 255), True],
            [(255, 255, 0), True],
            [(255, 0, 255), True],
            [(0, 255, 255), True],
            [(255, 100, 0), True],
            [(100, 255, 0), True],
            [(255, 0, 100), True],
            [(100, 0, 255), True],
            [(0, 255, 100), True],
            [(0, 100, 255), True]
        ]
        # instantiate RGB class
        color = rgb.RGB((1,0,0))
        for t in range(len(tests)):
            result = color._is_base_color(tests[t][0])
            self.assertEqual(result, tests[t][1], f"color: {tests[t][0]}, expected: {tests[t][1]}")

    def test_get_color_dominance_indices(self):
        tests = [
            [(1,2,3), (2,1,0)],
            [(3,2,1), (0,1,2)],
            [(3,1,2), (0,2,1)],
            [(1,1,1), (0,1,2)],
            [(1,3,1), (1,0,2)]
        ]
        # instantiate RGB class
        color = rgb.RGB((1,0,0))
        for t in range(len(tests)):
            result = color._get_color_dominance_indices(tests[t][0])
            self.assertEqual(result, tests[t][1], f"color: {tests[t][0]}, expected: {tests[t][1]}")

    def test_is_color_valid(self):
        tests = [
            [(0,0,0), True],
            [(255,0,0), True],
            [(255,0), False],
            [(255,0,0,0), False],
            [(-3,2,1), False],
            [(300,1,2), False],
            [[1,1,1], False]
        ]
        # instantiate RGB class
        color = rgb.RGB((1,0,0))
        for t in range(len(tests)):
            result = color._is_color_valid(tests[t][0])
            self.assertEqual(result, tests[t][1], f"color: {tests[t][0]}, expected: {tests[t][1]}")

    def test_is_order_valid(self):
        tests = [
            [(0,0,0), False],
            [(0,2,1), True],
            [(2,1,0), True],
            [(7,1,0), False],
            [(7,1,0,2), False],
            [(7,1), False],
            [[0,1,2], False]
        ]
        # instantiate RGB class
        color = rgb.RGB((1,0,0))
        for t in range(len(tests)):
            result = color._is_order_valid(tests[t][0])
            self.assertEqual(result, tests[t][1], f"order: {tests[t][0]}, expected: {tests[t][1]}")

    # def test_split(self):
    #     s = 'hello world'
    #     self.assertEqual(s.split(), ['hello', 'world'])
    #     # check that s.split fails when the separator is not a string
    #     with self.assertRaises(TypeError):
    #         s.split(2)

if __name__ == '__main__':
    unittest.main()