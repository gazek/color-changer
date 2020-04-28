def get_base_color(color, order=(0,1,2)):
    """Removes white and black from an rgb color

    Positional Arguments:
    color -- the input color specified as a tuple of ints

    Keyword Arguments:
    order -- the order of the color tuple
    default: rgb (0,1,2)

    Returns:
    {
        "base_color": (int, int, int),
        "white_level: float,
        "black_level: float
    }
    """
    # check base case
    if is_base_color(color):
        return color
    # find base color

    raise NotImplementedError

def is_base_color(color):
    """Checks that at least one of the color component values is 0

    Positional Arguments:
    color -- an RBG tuple of any ordering (int,int,int)

    Returns:
    bool
    """
    has_a_zero = color[0] == 0 or color[1] == 0 or color[2] == 0
    has_a_255 = color[0] == 255 or color[1] == 255 or color[2] == 255
    if has_a_zero and has_a_255:
        # is a base color
        return True
    # not a base color
    return False

def add_white_and_black_to_base_color(base_color, white_level, black_level, order=(0,1,2)):
    """
    """
    raise NotImplementedError

def get_intermediate_base_color(color_start, color_end, transition_progress, order=(0,1,2)):
    """
    """
    raise NotImplementedError

def get_color_dominance_indices(color):
    ordered = sorted(enumerate(color), key=lambda x: x[1], reverse=True)
    return tuple(map(lambda x: x[0], ordered))