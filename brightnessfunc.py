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

    def func_value(self, step_num):
        # get the input to the function
        input = (step_num/self.period)*(self.range[1] - self.range[0]) + self.range[0]
        # get the output of the function
        result = self.func(input)
        # the result should be between 0 and 1
        if result > 1:
            # floor to 1
            return 1
        elif result < -1:
            # ceiling to -1
            return -1
        else:
            # don't change the result
            return result