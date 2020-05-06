import unittest
import transition as t
import rgb

class TestTransition(unittest.TestCase):
    def test_invalid_transition_type(self):
        # should raise
        with self.assertRaises(ValueError):
            t.transition((1,2,3), (3,2,1), 0.5, type='wrong')

    def test_base_transition(self):
        # define tests
        tests = [
            [(255,0,0), (0,255,0), 0.5, (255,255,0)],
            [(255,0,0), (0,255,0), 0, (255,0,0)],
            [(255,0,0), (0,255,0), 1, (0,255,0)],
            [(255,0,0), (0,255,0), 0.333, (255,170,0)],
            [(255,0,0), (0,45,255), 0.75, (94, 0, 255)]
        ]
        # do the test
        for test in tests:
            c1 = rgb.RGB()
            c1.color = test[0]
            c2 = rgb.RGB()
            c2.color = test[1]
            result = t.transition(c1, c2, test[2])
            self.assertEqual(result.color, test[3])

if __name__ == '__main__':
    unittest.main()