import rgb

class ColorFunc:
    def __init__(self):
        # initialize
        # color when func returns 0
        self.color1 = rgb.RGB()
        self.color1.base_color = (255, 0, 255)
        # initialize
        # color when func returns 1
        self.color2 = rgb.RGB()
        self.color2.base_color = (0, 0, 255)
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

    def func_value(self, step_num):
        # get the output of the function
        input = (step_num/self.period)*(self.range[1] - self.range[0]) + self.range[0]
        result = self.func(input)
        # the result should be between 0 and 1
        if result > 1:
            # floor to 1
            return 1
        elif result < 0:
            # ceiling to zero
            return 0
        else:
            # don't change the result
            return result
