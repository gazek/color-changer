import rgb
import math
import colorfunc
import whitelevelfunc
import brightnessfunc
from functools import reduce

class Transition:
    def __init__(self):
        # initialize window size
        # int: number of LEDs in strip
        self.window = 0
        # initialize color function list
        # list<ColorFunc>
        self.color_funcs = []
        # initialize white_level function
        # the white_level function output modifies the white level of the color function output
        # a value of -1 removes all white
        # a value of 0 does not modify the color's white level
        # a value of 1 will set the white level of the color to maximum
        # list<WhiteLevelFunc>
        self.white_level_funcs = []
        # initialize brightness function
        # the brightness function output modifies the brightness of the color function output
        # a value of -1 will make the color fully black (0,0,0)
        # a value of 0 does not modify the color's brightness
        # a value of 1 will set the brightness of the color to maximum
        # list<rightnessFunc>
        self.brightness_funcs = []
        # # initialize the color transition array
        # # this is the RGB object for each step in the
        # # in the period
        # self._transition_colors
        # # initialize the white level transition array
        # # this is the white level value for each step in the
        # # in the period
        # self._transition_white_levels
        # # initialize the brightness transition array
        # # this is the brightness value for each step in the
        # # in the period
        # self._transition_brightnesses

    def get_transition_window(self, step_num):
        # get the period LCM
        period_lcm = self.get_period_lcm()
        # get the array of step numbers for the window
        window_steps = map(lambda w: (step_num + w) % period_lcm, range(len(self.window)))
        # get the window colors
        window_colors = self._get_color_transition_color_window(window_steps)
        # get the brightness values

        # get the white level values
        
        # apply white level and brightness to color

    def _get_color_transition_color_window(self, window_steps):
        # get the boundry of each functions period
        period_list = self._get_func_period_list(self.color_funcs)
        # initize the window array
        window = [0] * len(window_steps)
        # walk across all steps in the window
        for s in range(len(window_steps)):
            # walk across function ranges to find the right function
            # for the current step
            for b in range(len(period_list)):
                # find the right side (upper) boundry of the current color function
                right_boundry = period_list[b]
                # check if the requested step is within the boundary of the current function
                if window_steps[s] < right_boundry:
                    # set the direction base on the direction of the 0th function
                    if s == 0:
                        direction = self.color_funcs[0].direction
                    # get the function
                    func = self.color_funcs[b]
                    # get the left side (lower) boundary of the current function
                    left_boundry = period_list[b] - func.period
                    # get the step number relative to the current functions period
                    local_step_num = window_steps[s] - left_boundry
                    # check for direction = 0
                    if direction == 0:
                        local_step_num = s
                    # get the percent complete of the transition
                    trans_percent = func.func_value(local_step_num)
                    # get the total transition distance
                    full_dist = self._get_color_transition_distance(func.color1, func.color2, type=func.trans_type)
                    # get distance of transition
                    trans_dist = trans_percent * full_dist
                    # get color
                    color = self._get_color_transition_color(func.color1, func.color2, trans_dist, type=func.trans_type)
                    # get the window position
                    if direction == 1:
                        # window scrolls to the right (function scrolls to the left)
                        w = len(window_steps) - s - 1
                    else:
                        # direction == -1, window scrolls to the left (function scrolls to the right)
                        # direction == 0, window is stationary
                        w = s
                    # put the color in the right place in the window
                    window[w] = color
        # return the window colors
        return window

    def _lcm(self, num1, num2):
        return (num1 * num2) // math.gcd(num1, num2)

    def get_period_lcm(self):
        """Calculates the LCM of the color, white level and brightness function periods
        """
        # make sure there is at least one color function defined
        if len(self.color_funcs) == 0:
            raise ValueError('No color function specified')
        # get list of period values
        periods = []
        for f in ['color_funcs', 'white_level_funcs', 'brightness_funcs']:
            p = self._get_func_period(getattr(self, f))
            # only add values > 0 to the list
            if p > 0:
                periods.append(p)
        # find LCM of all periods
        lcm = periods[0]
        # if there is only one period then just return it
        if len(periods) == 1:
            return periods[0]
        # walk accross remaining values
        for p in periods[1:]:
            lcm = self._lcm(lcm, p)
        # return lcm
        return lcm

    def _get_func_period(self, funcs):
        """Sums the period of each function in the specified transition function
        """
        # return 0 if length is 0
        if len(funcs) == 0:
            return 0
        # sum the periods and return
        return reduce(lambda x, y: x + y, map(lambda x: x.period, funcs))

    def _get_func_period_list(self, funcs):
        """returns a list ints, each value is the end of the function period
        """
        # return 0 if length is 0
        if len(funcs) == 0:
            return []
        # list of func period ranges
        periods = [funcs[0].period]
        for f in range(1, len(funcs)):
            periods.append(funcs[f].period + periods[f-1])
        # return the list
        return periods

    def _get_color_transition_distance(self, color1, color2, type='base'):
        # get the transition pattern func
        transfunc = self._get_color_trans_func(type)
        # get total transition distance
        _, dist = transfunc(color1, color2)
        # return distance
        return dist

    def _get_color_transition_color(self, color1, color2, dist, type='base'):
        # get the transition pattern func
        transfunc = self._get_color_trans_func(type)
        # get transitioned color
        color, _ = transfunc(color1, color2, dist)
        # return color
        return color

    def _get_color_trans_func(self, type):
        # get the transition pattern func
        if type == 'base':
            return self._get_base_transition
        elif type  == 'white':
            return self._get_white_transition
        elif type  == 'black':
            return self._get_black_transition
        else:
            raise ValueError(f'Invalid transition type: {type}')

    def _get_base_transition(self, color1, color2, max_dist=rgb.MAX*4):
        """Transitions from color1 to color2 using base color algorithm, use max_distance halt the transition before reaching color2

        Positional Arguments:
        color1 -- RGB object, starting color
        color2 -- RGB object, target color

        KW Arguments:
        max_dist -- int, maximum distance to travel during the transition
        """
        # track distance of transition
        dist = 0
        d = 0
        # create a new RGB inst to track transition color
        colorX = rgb.RGB(order=color1.order)
        colorX.color = color1.color
        # avoid backtracking across the same path
        if color1.dominance[1] != color2.dominance[0]:
            # color1[c1.d1] -> 0 => colorX
            colorX.base_color, d = self._set_component_value(colorX, color1.dominance[1], rgb.MIN, set_base=True, max_dist=max_dist - dist)
        dist += d
        # colorX[c2.d0] -> 255
        colorX.base_color, d = self._set_component_value(colorX, color2.dominance[0], rgb.MAX, set_base=True, max_dist=max_dist - dist)
        dist += d
        # colorX[c2.d2] => 0
        colorX.base_color, d = self._set_component_value(colorX, color2.dominance[2], rgb.MIN, set_base=True, max_dist=max_dist - dist)
        dist += d
        # colorX[c2.d1] -> color2[c2.d1]
        colorX.base_color, d = self._set_component_value(colorX, color2.dominance[1], color2.base_color[color2.dominance[1]], set_base=True, max_dist=max_dist - dist)
        dist += d
        # return new color and dist
        return colorX, dist

    def _get_black_transition(self, color1, color2, max_dist=rgb.MAX*4):
        raise NotImplementedError

    def _get_white_transition(self, color1, color2, max_dist=rgb.MAX*4):
        raise NotImplementedError

    def _set_component_value(self, color, position, value, set_base=True, max_dist=rgb.MAX):
        # make sure its an int
        max_dist = int(round(max_dist))
        # set attribute
        if set_base:
            attr = 'base_color'
        else:
            attr, = 'color'
        # check the base case
        if max_dist <= 0:
            return getattr(color, attr), 0
        # get the color as a mutable list
        result = list(getattr(color, attr))
        # get the distance
        dist = value - result[position]
        # set the position
        if abs(dist) <= max_dist:
            result[position] = value
        else:
            if dist > 0:
                result[position] += max_dist
            else:
                result[position] -= max_dist
        # turn it into a tuple
        # and return it
        return tuple(result), abs(dist)
