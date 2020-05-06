from collections import defaultdict
from math import ceil

# max RGB component value
MAX = 255
# min RGB component value
MIN = 0
# white base color cuz I like purple
WHITE_BASE = (MAX, MIN, MAX)

class RGB():
    def __init__(self, order=(0,1,2)):
        # store the order
        self._order = order
        # set color to white base default
        self._color_setter(WHITE_BASE)
        # set default brightness
        self._brightness = 1
        # set default white level
        self._white_level = 0

    @property
    def color(self):
        return tuple(map(lambda i: self._color[i], self._order))

    @color.setter
    def color(self, value):
        self._color_setter(value)

    @property
    def base_color(self):
        return tuple(map(lambda i: self._base_color[i], self._order))

    @base_color.setter
    def base_color(self, value):
        self._base_color_setter(value)

    @property
    def brightness(self):
        return self._brightness

    @brightness.setter
    def brightness(self, value):
        self._brightness_setter(value)

    @property
    def white_level(self):
        return self._white_level

    @white_level.setter
    def white_level(self, value):
        self._white_level_setter(value)

    @property
    def order(self):
        return self._order

    @order.setter
    def order(self, value):
        self._order = value

    @property
    def dominance(self):
        return self._get_color_dominance_indices(self.color)

    def _color_setter(self, color):
        # make sure the color is valid
        if not self._is_color_valid(color):
            raise ValueError(f'invalid RGB color provided: {color}')
        # store the color
        self._color = color
        # determine brightness
        self._brightness = self._get_color_brightness(self._color)
        # determine white level
        self._white_level = self._get_color_white_level(self._color)
        # determine base color
        self._base_color = self._get_base_color(color)

    def _base_color_setter(self, base_color):
        # make sure the base_color is valid
        if not self._is_base_color(base_color):
            raise ValueError(f'invalid RGB base color provided: {base_color}')
        # store the base color
        self._base_color = base_color
        # determine color
        self._color = self._get_color(self._base_color, self._brightness, self._white_level)

    def _brightness_setter(self, brightness):
        # store the brightness value
        self._brightness = brightness
        # determine color
        self._color = self._get_color(self._base_color, self._brightness, self._white_level)

    def _white_level_setter(self, white_level):
        # store the white_level value
        self._white_level = white_level
        # determine color
        self._color = self._get_color(self._base_color, self._brightness, self._white_level)

    def _is_color_valid(self, color):
        """Verifies the a tuple is a valid RGB color

        Positional Arguments:
        color -- an RBG tuple of ints in any order

        Returns: bool
        """
        # make sure it is a tuple
        if type(color).__name__ != 'tuple':
            return False
        # check the length of the tuple
        if len(color) != 3:
            return False
        # verify that component colors are between _MIN and _MAX
        for c in color:
            if c < MIN or c > MAX:
                return False
        return True

    def _is_order_valid(self, order):
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

    def _get_color_dominance_indices(self, color):
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

    def _get_base_color(self, color):
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
        if self._is_base_color(color):
            return color
        # is it true white or true black
        if self._is_white(color):
            return WHITE_BASE

        # find base color
        base = tuple(map(lambda x, y: x-y, color, self._get_white_level_component(color)))
        base = tuple(map(lambda x, y: x-y, base, self._get_brightness_component(base)))
        return base

    def _is_white(self, color):
        if color[0] == color[1] and color[0] == color[2]:
            # is true white or true black
            return True
        # not white or black
        return False

    def _is_base_color(self, color):
        """Checks that at least one of the color component values is 0 and at least one color component is 255

        Positional Arguments:
        color -- an RBG tuple of ints in any order

        Returns:
        bool
        """
        # is it a valid color
        if not self._is_color_valid(color):
            return False
        # general logic
        has_a_min = color[0] == MIN or color[1] == MIN or color[2] == MIN
        has_a_max = color[0] == MAX or color[1] == MAX or color[2] == MAX
        if has_a_min and has_a_max:
            # is a base color
            return True
        # not a base color
        return False

    def _get_color_white_level(self, color):
        """Returns a value between 0 - 1 indicating the amount of white in a color

        Positional Arguments:
        color -- an RBG tuple of ints in any order

        Returns:
        int
        """
        d0, _, d2 = self._get_color_dominance_indices(color)
        if color[d0] == 0:
            return 0
        return color[d2]/color[d0]

    def _get_color_brightness(self, color):
        """Returns a value between 0 - 1 indicating the brightness of a color

        Positional Arguments:
        color -- an RBG tuple of ints in any order

        Returns:
        int
        """
        d0, _, _ = self._get_color_dominance_indices(color)
        return color[d0]/MAX

    def _get_white_level_component(self, color):
        """Calculates an RGB tuple that represents the white components of the color.
        """
        if color[0] == color[1] and color[0] == color[2]:
            return color
        d0, d1, d2 = self._get_color_dominance_indices(color)
        result = [0] * len(color)
        # set the easy ones
        result[d0] = 0
        result[d2] = color[d2]
        # get the hard one
        wl = self._get_color_white_level(color)
        result[d1] = int(ceil(color[d1] - ((color[d1] - (color[d0] * wl)) / (1 - wl))))
        return tuple(result)

    def _get_brightness_component(self, color):
        """This really should be called the dimness component because when it is
            subtracted from the color it results in the color at full brightness
        """
        brightness = self._get_color_brightness(color)
        if brightness == 0:
            return tuple(map(lambda x: -x, color))
        result = [0] * len(color)
        for i in range(len(color)):
            result[i] = color[i] - int(round(color[i]/brightness))
        return tuple(result)

    def _get_white_level_modifier(self, base_color, white_level):
        """Calculates the component changes needed to apply the white level to the base color
        """
        # make sure base_color is valid
        if not self._is_base_color(base_color):
            raise ValueError(f"Invalid base color: {base_color}")
        # make sure white level is valid
        if white_level < 0:
            white_level = 0
        elif white_level > 1:
            white_level = 1
        # general case
        result = [0] * 3
        d0, d1, d2 = self._get_color_dominance_indices(base_color)
        for d in (d1, d2):
            result[d] = int(round((base_color[d0] - base_color[d]) * white_level))
        return tuple(result)

    def _get_brightness_modifier(self, base_color, brightness, white_level):
        """Calculates the component changes needed to apply the brightness to the base color
        """
        # make sure base_color is valid
        if not self._is_base_color(base_color):
            raise ValueError(f"Invalid base color: {base_color}")
        # get the white level modifier
        white_level_modifier = self._get_white_level_modifier(base_color, white_level)
        # add in the white level component modifiers
        color = tuple(map(lambda c, m: c + m, base_color, white_level_modifier))
        # full brightness
        if brightness >= 1:
            return (MIN, MIN, MIN)
        # general case
        result = [0] * 3
        for d in self._get_color_dominance_indices(color):
            result[d] = int(round((brightness - 1) * color[d]))
        return tuple(result)

    def _get_color(self, base_color, brightness, white_level):
        # white level modifier
        white_level_modifier = self._get_white_level_modifier(base_color, white_level)
        # brightness modifier
        brightness_modifier = self._get_brightness_modifier(base_color, brightness, white_level)
        # modify base color
        return tuple(map(lambda x, y, z: x+y+z, base_color, white_level_modifier, brightness_modifier))
