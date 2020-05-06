import rgb

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