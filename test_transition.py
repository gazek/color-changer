import unittest
import transition as trans
import rgb
import colorfunc
import brightnessfunc
import whitelevelfunc

class TestTransition(unittest.TestCase):
    def test_get_color_trans_func_invalid_transition_type(self):
        # should raise
        with self.assertRaises(ValueError):
            t = trans.Transition()
            t._get_color_trans_func('wrong')

    def test_get_color_trans_func(self):
        t = trans.Transition()
        base = t._get_color_trans_func('base')
        black = t._get_color_trans_func('black')
        white = t._get_color_trans_func('white')
        self.assertEqual(base, t._get_base_transition)
        self.assertEqual(black, t._get_black_transition)
        self.assertEqual(white, t._get_white_transition)

    def test_get_base_transition(self):
        # define tests
        tests = [
            [(255,0,0), (0,255,0), 0.5, 510, (255,255,0)],
            [(255,0,0), (0,255,0), 0, 510, (255,0,0)],
            [(255,0,0), (0,255,0), 1, 510, (0,255,0)],
            [(255,0,0), (0,255,0), 0.333, 510, (255,170,0)],
            [(255,0,0), (0,45,255), 0.75, 555, (94, 0, 255)]
        ]
        # do the test
        for test in tests:
            c1 = rgb.RGB()
            c1.color = test[0]
            c2 = rgb.RGB()
            c2.color = test[1]
            t = trans.Transition()
            _, dist = t._get_base_transition(c1, c2, 999999999999)
            self.assertEqual(dist, test[3])
            result, _ = t._get_base_transition(c1, c2, test[2]*dist)
            self.assertEqual(result.color, test[4])

    def test_get_color_transition_distance(self):
        # define tests
        tests = [
            [(255,0,0), (0,255,0), 0.5, 510, (255,255,0)],
            [(255,0,0), (0,255,0), 0, 510, (255,0,0)],
            [(255,0,0), (0,255,0), 1, 510, (0,255,0)],
            [(255,0,0), (0,255,0), 0.333, 510, (255,170,0)],
            [(255,0,0), (0,45,255), 0.75, 555, (94, 0, 255)]
        ]
        # do the test
        for test in tests:
            c1 = rgb.RGB()
            c1.color = test[0]
            c2 = rgb.RGB()
            c2.color = test[1]
            t = trans.Transition()
            dist = t._get_color_transition_distance(c1, c2, type='base')
            self.assertEqual(dist, test[3])
            result = t._get_color_transition_color(c1, c2, test[2]*dist, type='base')
            self.assertEqual(result.color, test[4])

    def test_get_func_period(self):
        tests = [
            [3, 77, 34, 114],
            [0]
        ]
        for test in tests:
            t = trans.Transition()
            funcs = []
            for i in range(len(test)-1):
                cf = colorfunc.ColorFunc()
                cf.period = test[i]
                funcs.append(cf)
            self.assertEqual(t._get_func_period(funcs), test[len(test)-1])


    def test_get_func_period_list(self):
        tests = [
            [3, 77, 34, [3, 80, 114]],
            [[]]
        ]
        for test in tests:
            t = trans.Transition()
            funcs = []
            for i in range(len(test)-1):
                cf = colorfunc.ColorFunc()
                cf.period = test[i]
                funcs.append(cf)
            self.assertEqual(t._get_func_period_list(funcs), test[len(test)-1])

    def test_lcm(self):
        tests = [
            [2, 3, 6]
        ]
        for test in tests:
            t = trans.Transition()
            self.assertEqual(t._lcm(test[0], test[1]), test[2])

    def test_get_period_lcm(self):
        tests = [
            [[2], [3], [5], 30],
            [[17], [], [], 17],
        ]
        func_types = [
            ('color_funcs', colorfunc.ColorFunc),
            ('brightness_funcs', brightnessfunc.BrightnessFunc),
            ('white_level_funcs', whitelevelfunc.WhiteLevelFunc)
        ]
        for test in tests:
            t = trans.Transition()
            for ft in range(len(func_types)):
                for i in range(len(test[ft])):
                    cf = colorfunc.ColorFunc()
                    cf.period = test[ft][i]
                    getattr(t, func_types[ft][0]).append(cf)
            self.assertEqual(t.get_period_lcm(), test[len(test)-1])

    def test_get_period_lcm_no_funcs(self):
        # should raise
        with self.assertRaises(ValueError):
            t = trans.Transition()
            t.get_period_lcm()

    def test_get_color_transition_color_window(self):
        attributes = ['color1', 'color2', 'range', 'period', 'func', 'direction', 'trans_type', 'use_window']
        tests = [
            # [[[color1, color2, range, period, func, direction, trans_type, use_window]], step_number, window_size, result]
            [[[(255,0,0), (0,255,0), (0,10), 10, lambda x: 1 if x < 8 else 0, 1, 'base', True]], 1, 10, [(255,0,0),(255,0,0),(255,0,0),(255,0,0),(255,0,0),(255,0,0),(255,0,0),(255,0,0),(255,0,0),(255,0,0),(255,0,0)]]
        ]
        # step across the tests
        for test in tests:
            # instantiate the Transition class
            t = trans.Transition()
            # step across the color functions
            for f in test[0]:
                cf = colorfunc.ColorFunc()
                # set color1
                cf.color1 = rgb.RGB()
                cf.color1.color = f[0]
                # set color2
                cf.color2 = rgb.RGB()
                cf.color2.color = f[1]
                # set the remaining attributes
                for a in range(2,len(attributes)):
                    setattr(cf, attributes[a], f[a])
                t.color_funcs.append(cf)
            # get the window steps
            window_steps = list(map(lambda x: x + test[1], range(test[2])))
            t._get_color_transition_color_window(window_steps)


if __name__ == '__main__':
    unittest.main()