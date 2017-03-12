""" Sarah Barden
    Software Design Spring 2017
    Computational Art Mini-Project"""
import math
import random
from PIL import Image

functions = ['prod', 'avg', 'cos_pi', 'sin_pi', 'quad', 'cubic']


def build_rand_func(min_depth, max_depth):
    """ Builds a random function of depth at least min_depth and depth
        at most max_depth (see assignment writeup for definition of depth
        in this context)

        min_depth: the minimum depth of the random function
        max_depth: the maximum depth of the random function
        returns: the randomly generated function represented as a nested list
                 (see assignment writeup for details on the representation of
                 these functions)

    """

    num = random.randint(0, 5)
    depth = random.randint(min_depth, max_depth)

    # when the depth is 1, i.e. only one function, choose x or y.
    if depth <= 1:
        return random.choice(['x', 'y'])

    # when depth is greater than 1, build random fucntions
    elif num == 0:
        return [functions[0], build_rand_func(min_depth-1, max_depth-1),
                              build_rand_func(min_depth-1, max_depth-1)]
    elif num == 1:
        return [functions[1], build_rand_func(min_depth-1, max_depth-1),
                              build_rand_func(min_depth-1, max_depth-1)]
    elif num == 2:
        return [functions[2], build_rand_func(min_depth-1, max_depth-1)]
    elif num == 3:
        return [functions[3], build_rand_func(min_depth-1, max_depth-1)]
    elif num == 4:
        return [functions[4], build_rand_func(min_depth-1, max_depth-1)]
    elif num == 5:
        return [functions[5], build_rand_func(min_depth-1, max_depth-1)]


def eval_rand_func(f, x, y):
    """ Evaluate the random function f with inputs x,y
        Representation of the function f is defined in the assignment writeup

        f: the function to evaluate
        x: the value of x to be used to evaluate the function
        y: the value of y to be used to evaluate the function
        returns: the function value

        >>> eval_rand_func(["x"],-0.5, 0.75)
        -0.5
        >>> eval_rand_func(["y"],0.1,0.02)
        0.02
    """

    if f[0] == 'x':
        return x
    elif f[0] == 'y':
        return y
    elif f[0] == 'prod':
        return eval_rand_func(f[1], x, y)*eval_rand_func(f[2], x, y)
    elif f[0] == 'avg':
        return 0.5*(eval_rand_func(f[1], x, y)+eval_rand_func(f[2], x, y))
    elif f[0] == 'sin_pi':
        return math.sin(math.pi * eval_rand_func(f[1], x, y))
    elif f[0] == 'cos_pi':
        return math.cos(math.pi * eval_rand_func(f[1], x, y))
    elif f[0] == 'quad':
        return eval_rand_func(f[1], x, y)**2
    elif f[0] == 'cubic':
        return eval_rand_func(f[1], x, y)**3


def remap_interval(val,
                   input_start,
                   input_end,
                   output_start,
                   output_end):
    """ Given an input value in the interval [input_interval_start,
        input_interval_end], return an output value scaled to fall within
        the output interval [output_interval_start, output_interval_end].

        val: the value to remap
        input_start: start of interval that has all possible values for val
        input_end:   end of the interval that has all possible values for val
        output_start: start of interval that contains all output values
        output_end:   end of interval that contains all output values
        returns: the value remapped from the input to the output interval

        >>> remap_interval(0.5, 0, 1, 0, 10)
        5.0
        >>> remap_interval(5, 4, 6, 0, 2)
        1.0
        >>> remap_interval(5, 4, 6, 1, 2)
        1.5
    """
    # compute lengths of each interval
    input_length = input_end - input_start
    output_length = output_end - output_start

    # how far is the value from the start
    # calculate the proporation of where it is
    val_dist_start = val - input_start
    proportion = val_dist_start / input_length

    # use the proportion to calculate its position on the output interval
    final = output_start + proportion*output_length
    return final


def color_map(val):
    """ Maps input value between -1 and 1 to an integer 0-255, suitable for
        use as an RGB color code.

        val: value to remap, must be a float in the interval [-1, 1]
        returns: integer in the interval [0,255]

        >>> color_map(-1.0)
        0
        >>> color_map(1.0)
        255
        >>> color_map(0.0)
        127
        >>> color_map(0.5)
        191
    """
    # this relies on remap_interval, which you must provide
    color_code = remap_interval(val, -1, 1, 0, 255)
    return int(color_code)


def test_image(filename, x_size=350, y_size=350):
    """ Generate test image with random pixels and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (random.randint(0, 255),  # Red channel
                            random.randint(0, 255),  # Green channel
                            random.randint(0, 255))  # Blue channel

    im.save(filename)


def generate_art(filename, x_size=350, y_size=350):
    """ Generate computational art and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Functions for red, green, and blue channels - where the magic happens!
    red_function = build_rand_func(7, 10)
    green_function = build_rand_func(7, 10)
    blue_function = build_rand_func(7, 10)

    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (
                    color_map(eval_rand_func(red_function, x, y)),
                    color_map(eval_rand_func(green_function, x, y)),
                    color_map(eval_rand_func(blue_function, x, y))
                    )

    im.save(filename)


if __name__ == '__main__':
    import doctest
    # .testmod(verbose=True)
    # doctest.run_docstring_examples(build_rand_func, globals(), verbose=True)

    # Create some computational art!
    # TODO: Un-comment the generate_art function call after you
    #       implement remap_interval and eval_rand_func
    generate_art("art2.png")

    # To test that PIL is installed correctly
    # Comment or remove this function call after testing PIL install
    # test_image("noise.png")
