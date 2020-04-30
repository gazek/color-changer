import unittest
import rgb

class TestRGB(unittest.TestCase):

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
            result = color.is_base_color(tests[t][0])
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
            result = color.get_color_dominance_indices(tests[t][0])
            self.assertEqual(result, tests[t][1], f"color: {tests[t][0]}, expected: {tests[t][1]}")

    # def test_split(self):
    #     s = 'hello world'
    #     self.assertEqual(s.split(), ['hello', 'world'])
    #     # check that s.split fails when the separator is not a string
    #     with self.assertRaises(TypeError):
    #         s.split(2)

if __name__ == '__main__':
    unittest.main()