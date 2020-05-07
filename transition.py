import rgb
import math

class transfunc:
    def __init___(self):
        # initialize window size
        # int: number of LEDs in strip
        self._window = 0
        # initialize color function list
        # list<ColorFunc>
        self._color_funcs = []
        # initialize white_level function
        # the white_level function output modifies the white level of the color function output
        # a value of -1 removes all white
        # a value of 0 does not modify the color's white level
        # a value of 1 will set the white level of the color to maximum
        # list<WhiteLevelFunc>
        self._white_level_func = []
        # initialize brightness function
        # the brightness function output modifies the brightness of the color function output
        # a value of -1 will make the color fully black (0,0,0)
        # a value of 0 does not modify the color's brightness
        # a value of 1 will set the brightness of the color to maximum
        # list<rightnessFunc>
        self._brightness_func = []


def transition(color1, color2, traversal_percent, type='base'):
    # get the transition pattern
    if type == 'base':
        transfunc = get_base_transition
    elif type  == 'white':
        transfunc = get_white_transition
    elif type  == 'black':
        transfunc = get_black_transition
    else:
        raise ValueError(f'Invalid transition type: {type}')
    # get total transition distance
    _, dist = transfunc(color1, color2)
    # get transitioned color
    result, _ = transfunc(color1, color2, dist*traversal_percent)
    return result

def get_base_transition(color1, color2, max_dist=rgb.MAX*4):
    # track distance of transition
    dist = 0
    d = 0
    # create a new RGB inst to track transition color
    colorX = rgb.RGB(order=color1.order)
    colorX.color = color1.color
    # avoid backtracking across the same path
    if color1.dominance[1] != color2.dominance[0]:
        # color1[c1.d1] -> 0 => colorX
        colorX.base_color, d = set_component_value(colorX, color1.dominance[1], rgb.MIN, set_base=True, max_dist=max_dist - dist)
    dist += d
    # colorX[c2.d0] -> 255
    colorX.base_color, d = set_component_value(colorX, color2.dominance[0], rgb.MAX, set_base=True, max_dist=max_dist - dist)
    dist += d
    # colorX[c2.d2] => 0
    colorX.base_color, d = set_component_value(colorX, color2.dominance[2], rgb.MIN, set_base=True, max_dist=max_dist - dist)
    dist += d
    # colorX[c2.d1] -> color2[c2.d1]
    colorX.base_color, d = set_component_value(colorX, color2.dominance[1], color2.base_color[color2.dominance[1]], set_base=True, max_dist=max_dist - dist)
    dist += d
    # return new color and dist
    return colorX, dist

def set_component_value(color, position, value, set_base=True, max_dist=rgb.MAX):
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

class ColorFunc:
    def __init__(self):
        # initialize
        # color when func returns 0
        self.color = rgb.RGB()
        self.base_color = (255, 0, 255)
        # initialize
        # color when func returns 1
        self.color = rgb.RGB()
        self.base_color = (0, 0, 255)
        # intialize range
        # sets the range of values that may be used as input for the function property
        self.range = (0,1)
        # initialize period
        # number of steps to use when traversing the range property
        self.period = 20
        # initialize the color function
        # func(i) => float, bounded (0,1)
        # func(i) which returns a float within range (0,1)
        # where i is a float bounded by the range property
        self.func = lambda i: math.sin(i * math.pi)
        # initialize direction
        # specifies scanning direction of the window wrt the function's graph
        # values can be -1 || 0 || 1 (left || no motion || right)
        self.direction = 1
        # initialize trans_type
        # specifies the type of color transition to use:
        # 'base' || 'white' || 'black'
        self.trans_type = 'base'
        # initialize use_window
        # True: use scanning winodw
        # False: set all LEDs the same color, same as window = 1
        self.use_window = True


class WhiteLevelFunc:
    def __init__(self):
        # intialize range
        # sets the range of values that may be used as input for the function property
        self.range = (0,2)
        # initialize period
        # number of steps to use when traversing the range property
        self.period = 60
        # initialize the white level function
        # func(i) => float, bounded (-0,1)
        # func(i) which returns a float within range (-1,1)
        # where i is a float bounded by the range property
        self.func = lambda i: math.sin(i * math.pi)
        # initialize direction
        # specifies scanning direction of the window wrt the function's graph
        # values can be -1 || 0 || 1 (left || no motion || right)
        self.direction = 1
        # initialize use_window
        # True: use scanning winodw
        # False: set all LEDs the same white level, same as window = 1
        self.use_window = True

class BrightnessFunc:
    def __init__(self):
        # intialize range
        # sets the range of values that may be used as input for the function property
        self.range = (0,2)
        # initialize period
        # number of steps to use when traversing the range property
        self.period = 60
        # initialize the brightness function
        # func(i) => float, bounded (-0,1)
        # func(i) which returns a float within range (-1,1)
        # where i is a float bounded by the range property
        self.func = lambda i: math.sin(i * math.pi)
        # initialize direction
        # specifies scanning direction of the window wrt the function's graph
        # values can be -1 || 0 || 1 (left || no motion || right)
        self.direction = 1
        # initialize use_window
        # True: use scanning winodw
        # False: set all LEDs the same brightness, same as window = 1
        self.use_window = True
