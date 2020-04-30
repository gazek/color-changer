from collections import defaultdict

class RGB():
    def __init__(self, color=None, order=(0,1,2)):
        # max RGB component value
        self._MAX = 255
        # min RGB component value
        self._MIN = 0
        # make sure the color is valid
        if not self.is_color_valid(color):
            print(color)
            raise ValueError(f'invalid RGB color provided: {color}')
        # make sure the order is valid
        if not self.is_order_valid(order):
            print(order)
            raise ValueError(f'invalid RGB order provided: {order}')
        # store the color
        self.color = color
        self._order = order
        # determine base color
        # determine brightness
        # determine white level

    def is_color_valid(self, color):
        """Verifies the a tuple is a valid RGB color

        Positional Arguments:
        color -- an RBG tuple of ints in any order

        Returns: bool
        """
        for c in color:
            if c < self._MIN or c > self._MAX:
                return False
        return True

    def is_order_valid(self, order):
        """
        """
        # make sure it is a tuple
        if type(order).__name__ != 'tuple':
            return False
        # check the length of the tuple
        if len(order) != 3:
            return False
        # make sure the values in the tuple are only 0, 1 & 2
        sorted_order = sorted(order)
        for i in range(3):
            if sorted_order[i] != i:
                return False
        return True

    def get_color_dominance_indices(self, color):
        """Orders the color component indices in descending order by underlying component color value

        Positional Arguments:
        color -- an RBG tuple of ints in any order

        Returns:
        (int, int, int)
        """
        # create a dict where the
        # key is the component color value and the
        # value is a list of indices that hav the component color value
        value_map = defaultdict(list)
        # populate the dictionary
        for c in range(len(color)):
            value_map[color[c]].append(c)
        # sort the dictionary keys (color component values) in descending order
        ordered = sorted(value_map.keys(), reverse=True)
        # create a list to hold the color component indices
        # in descending order by color component value
        # if the underlying component color valuea are equal
        # then the indices will be ordered in ascending order by index value
        result = []
        for k in ordered:
            result = result + value_map[k]
        # convert to a tuple before returning
        return tuple(result)

    def get_base_color(self, color):
        """Removes white and black from an rgb color

        Positional Arguments:
        color -- an RBG tuple of ints in any order

        Returns:
        {
            "base_color": (int, int, int),
            "white_level: float,
            "black_level: float
        }
        """
        # check base case
        if self.is_base_color(color):
            return color
        # find base color
        raise NotImplementedError

    def is_base_color(self, color):
        """Checks that at least one of the color component values is 0 and at least one color component is 255

        Positional Arguments:
        color -- an RBG tuple of ints in any order

        Returns:
        bool
        """
        has_a_min = color[0] == self._MIN or color[1] == self._MIN or color[2] == self._MIN
        has_a_max = color[0] == self._MAX or color[1] == self._MAX or color[2] == self._MAX
        if has_a_min and has_a_max:
            # is a base color
            return True
        # not a base color
        return False

    # @property
    # def x(self):
    #     """I'm the 'x' property."""
    #     print("getter of x called")
    #     return self._x

    # @x.setter
    # def x(self, value):
    #     print("setter of x called")
    #     self._x = value


# TODO: turn these into class methods




def get_color_white_level(color):
    """Returns a value between 0 - 1 indicating the amount of white in a color

    Positional Arguments:
    color -- an RBG tuple of ints in any order

    Returns:
    int
    """
    raise NotImplementedError

def get_color_brightness(color):
    """Returns a value between 0 - 1 indicating the brightness of a color

    Positional Arguments:
    color -- an RBG tuple of ints in any order

    Returns:
    int
    """
    raise NotImplementedError

def modify_base_color_white_level_and_brightness(base_color, white_level, brightness):
    """
    """
    raise NotImplementedError

def get_brightness_modifier(base_color, brightness):
    raise NotImplementedError

def get_white_level_modifier(base_color, white_level):
    raise NotImplementedError

