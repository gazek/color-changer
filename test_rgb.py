import unittest
import rgb

class TestRGB(unittest.TestCase):
    def test_init_happy(self):
        # instantiate RGB class
        color = rgb.RGB()
        # verify color
        self.assertEqual(color._color, color._WHITE_BASE)
        # verify order
        self.assertEqual(color._order, (0,1,2))

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
            [(0, 100, 255), True],
            [(0, 100, 255, 0), False],
            [(0, 100), False]
        ]
        # instantiate RGB class
        color = rgb.RGB()
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
        color = rgb.RGB()
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
        color = rgb.RGB()
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
        color = rgb.RGB()
        for t in range(len(tests)):
            result = color._is_order_valid(tests[t][0])
            self.assertEqual(result, tests[t][1], f"order: {tests[t][0]}, expected: {tests[t][1]}")

    def test_get_color_white_level(self):
        tests = [
            [(0,0,0), 0],
            [(10,255,50), 10/255]
        ]
        # instantiate RGB class
        color = rgb.RGB()
        for t in range(len(tests)):
            result = color._get_color_white_level(tests[t][0])
            self.assertEqual(result, tests[t][1], f"color: {tests[t][0]}, expected: {tests[t][1]}")

    def test_get_color_brightness(self):
        tests = [
            [(0,0,0), 0],
            [(10,255,50), 1],
            [(10,123,50), 123/255]
        ]
        # instantiate RGB class
        color = rgb.RGB()
        for t in range(len(tests)):
            result = color._get_color_brightness(tests[t][0])
            self.assertEqual(result, tests[t][1], f"color: {tests[t][0]}, expected: {tests[t][1]}")

    def test_get_white_level_modifier(self):
        tests = [
            [(255, 0, 0), 1, (0, 255, 255)],
            [(255, 0, 0), 3, (0, 255, 255)],
            [(0, 255, 125), 0, (0, 0, 0)],
            [(0, 255, 125), -1, (0, 0, 0)]
        ]
        # instantiate RGB class
        color = rgb.RGB()
        for t in range(len(tests)):
            result = color._get_white_level_modifier(tests[t][0], tests[t][1])
            self.assertEqual(result, tests[t][2], f"color: {tests[t][0]}, white_level: {tests[t][1]} expected: {tests[t][2]}")

    def test_get_white_level_modifier_invalid_color(self):
        # instantiate RGB class
        color = rgb.RGB()
        # should raise
        with self.assertRaises(ValueError):
            color._get_white_level_modifier([], 1)

    def test_get_brightness_modifier(self):
        tests = [
            [(255, 0, 0), 1, 0, (0, 0, 0)],
            [(255, 50, 0), 0, 0, (-255, -50, 0)]
        ]
        # instantiate RGB class
        color = rgb.RGB()
        for t in range(len(tests)):
            result = color._get_brightness_modifier(tests[t][0], tests[t][1], tests[t][2])
            self.assertEqual(result, tests[t][3], f"color: {tests[t][0]}, brightness: {tests[t][1]}, white_level_modifier: {tests[t][2]} expected: {tests[t][3]}")

    def test_get_brightness_modifier_color(self):
        # instantiate RGB class
        color = rgb.RGB()
        # should raise
        with self.assertRaises(ValueError):
            color._get_brightness_modifier((1,2,3), 1, (-5000, 6, 7))

    def test_get_white_level_component(self):
        tests = [
            [(200, 157, 47), (0, 14, 47)],
            [(45, 45, 45), (45, 45, 45)]
        ]

        # instantiate RGB class
        color = rgb.RGB()
        for t in range(len(tests)):
            result = color._get_white_level_component(tests[t][0])
            self.assertEqual(result, tests[t][1], f"color: {tests[t][0]}, white_level_component expected: {tests[t][1]} actual: {result}")

    def test_get_brightness_component(self):
        tests = [
            [(200, 157, 47), (-55, -43, -13)],
            [(255, 50, 25), (0, 0, 0)],
            [(3, 1, 1), (-252, -84, -84)],
            [(0, 0, 0), (0, 0, 0)]
        ]

        # instantiate RGB class
        color = rgb.RGB()
        for t in range(len(tests)):
            result = color._get_brightness_component(tests[t][0])
            self.assertEqual(result, tests[t][1], f"color: {tests[t][0]}, brightness_component expected: {tests[t][1]} actual: {result}")

    def test_get_base_color(self):
        tests = [
            [(255, 125, 75), (255, 70, 0)],
            [(255, 50, 0), (255, 50, 0)]
        ]

        # instantiate RGB class
        color = rgb.RGB()
        for t in range(len(tests)):
            result = color._get_base_color(tests[t][0])
            self.assertEqual(result, tests[t][1], f"color: {tests[t][0]}, base expected: {tests[t][1]} actual: {result}")

    def test_get_color(self):
        tests = [
            [(255, 75, 0), 0.5, 0.75, (127, 105, 95)]
        ]
        # do tests
        # instantiate RGB class
        color = rgb.RGB()
        for t in range(len(tests)):
            result = color._get_color(tests[t][0], tests[t][1], tests[t][2])
            self.assertEqual(result, tests[t][3], f"color: {tests[t][0]}, base expected: {tests[t][3]} actual: {result}")

    def test_cycle_methods(self):
        tests = [
            (220, 134, 45),
            (54, 0, 225),
            (50, 40, 40),
            (40, 40, 40)
        ]
        color = rgb.RGB()
        for c in tests:
            result = c
            for _ in range(3):
                white_level = color._get_color_white_level(result)
                brightness = color._get_color_brightness(result)
                base_color = color._get_base_color(result)
                result = color._get_color(base_color, brightness, white_level)
            self.assertEqual(result, c, f"color: {c}, expected: {c} actual: {result}")

    def  test_cycle_setters(self):
        tests = [
            (220, 134, 45),
            (54, 0, 225),
            (0, 255, 0),
            (50, 40, 40),
            (40, 40, 40)
        ]
        for t in tests:
            c1 = rgb.RGB()
            c1.color = t
            c2 = rgb.RGB()
            c2.base_color = c1.base_color
            c2.brightness = c1.brightness
            c2.white_level = c1.white_level
            self.assertEqual(c2.color, t)

    def test_order_setter(self):
        order = (1, 2, 0)
        c = rgb.RGB()
        self.assertNotEqual(order, c.order)
        c.order = order
        self.assertEqual(order, c.order)

    def test_color_setter_exception(self):
        # instantiate RGB class
        color = rgb.RGB()
        # should raise
        with self.assertRaises(ValueError):
            color.color = ()

    def test_base_color_setter_exception(self):
        # instantiate RGB class
        color = rgb.RGB()
        # should raise
        with self.assertRaises(ValueError):
            color.base_color = ()

if __name__ == '__main__':
    unittest.main()