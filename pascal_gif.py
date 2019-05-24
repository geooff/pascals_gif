"""
This program attempts to remake a gif I found from wikipedia.
The image can be found at:
https://upload.wikimedia.org/wikipedia/commons/6/66/Pascal%27s_Triangle_animated_binary_rows.gif

The gif comes with the following decription:
Each frame represents a row in Pascal's triangle.
Each column of pixels is a number in binary with the least significant bit at the bottom.
Light pixels represent ones and the dark pixels are zeroes.
"""
import argparse # For fancy user input managment
import sys
import shutil
import os # For system level manipulation
from math import floor, ceil # Rounding functions for uneven row counts
from PIL import Image # Image manipulation library
from struct import pack # Pack data for image lib
from imageio import get_writer, imread # Convery set of images to gif
from re import search


def make_triangle(n_rows):
    """Return pascals triangle in binary with n_rows number of rows."""
    # Function to add binary numbers
    def bin_add(*args): return bin(sum(int(x, 2) for x in args))[2:]

    results = []
    for _ in range(n_rows):
        row = [bin(1)] # Append a binary 1 to the start of a row
        if results: # If there are existing results (row > 1)
            last_row = results[-1]
            # The following is just a fancy way to say "For each result in the last row add it with its neighbor"
            # Zip functions collects the previous row with itself and a version indexed one element ahead
            # The bin_add(*pair) unpacks the pair and calls the bin_add function with the results
            row.extend([bin_add(*pair) for pair in zip(last_row, last_row[1:])])
            row.append(bin(1)) # Append a binary 1 to the end of a row
        results.append(row)
    return results


def gen_frame(row, filename, frame_dim, interpol):
    """Return an image for a given pascal triangle."""
    frame = []

    # For each element in a row (represented as binary_strs) unpack it into a list of single 0's and 1's
    for binary_str in row:
        binary_str = ''.join(str(i) for i in binary_str if i.isdigit())
        binary_list = list(binary_str.zfill(SIZE[0]))
        binary_list = [int(i) for i in binary_list]

        # If the binary_list is longer then the output dimensions, trim off the LSBs
        if len(binary_list) > SIZE[0]:
            binary_list = binary_list[:SIZE[0]]

        # Append the binary_list of to the frame
        frame.extend(binary_list)

    # If the binary_list doesn't fill the frame than fill the blank space with 0's
    l_append = [0]*(floor((SIZE[0] - len(row))/2))*SIZE[1]
    r_append = [0]*(ceil((SIZE[0] - len(row))/2))*SIZE[1]
    canvas = l_append+frame+r_append

    # If the binary_list exceeds the size of the frame than trim off the edges
    if len(canvas) > (SIZE[0]*SIZE[1]):
        offset = (((len(frame))-(SIZE[0])*SIZE[1]))/2

        # Make sure the offset doesn't cause screen tearing
        if offset % SIZE[0] != 0:
            offset += SIZE[0]/2

        canvas = canvas[int(offset):]

    # Set image interpolation behaviour based on user input
    interpol = Image.LANCZOS if interpol else Image.NEAREST

    # Pack the frame into a byte and generate an image with it
    data = pack('B'*len(canvas), *[pixel*255 for pixel in canvas])
    img = Image.frombuffer('L', SIZE, data)
    img = img.rotate(-90)
    img = img.resize(frame_dim, interpol)
    img.save(filename)


def gen_gif(n_rows, frame_rate, frame_dim, interpol):
    """Generate a gif with n_rows number of frames and with frame timing of f_time."""
    triangle = make_triangle(n_rows) # Generate pascals triangle of n_rows

    # Make a temp folder and send all outputs to it
    temp_path = os.path.join(os.getcwd(), r'temp')
    if os.path.exists(temp_path):
        shutil.rmtree(temp_path)
        os.makedirs(temp_path)
    else:
        os.makedirs(temp_path)
    os.chdir(temp_path)

    # For each row in pascals triangle generate a frame based off it
    for idx, row in enumerate(triangle):
        gen_frame(row, "frame_{0}.png".format(idx), frame_dim, interpol)

    # Generate output gif given the files generated above
    with get_writer('pascals_triangle_{}.gif'.format(n_rows), mode='I', duration=frame_rate) as writer:
        filenames = [file for file in os.listdir() if file.endswith('.png')]

        # Sort files by numbers found in string containing numbers (ex. frame_6.png)
        def sortby(x):
            return int(search(r'\d+', x).group())

        filenames.sort(key=sortby)
        for filename in filenames:
            image = imread(filename)
            writer.append_data(image)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Generate gif using pascals triangle.')
    parser.add_argument('--num_frames', metavar='frames', type=int, nargs=1, required=True,
                        help='the total number of frames of the output gif (eg. 120)')
    parser.add_argument('--frame_rate', metavar='frame_rate', type=float, nargs=1, default=0.5,
                        help='the speed of the gif. Default: 0.5')
    parser.add_argument('--pixel_dim', metavar=('x', 'y'), type=int, nargs=2, default=(50, 50),
                        help='number of pixels contained in frame. Default 50x50')
    parser.add_argument('--frame_dim', metavar=('x', 'y'), type=int, nargs=2, default=(400, 400),
                        help='number of pixels contained in output. Default 400x400')
    parser.add_argument('--interpol', dest='interpolate', action='store_true', default=False,
                        help='round edges when upscaling frames (extra sp00ky).')
    args = parser.parse_args()

    # Set size of output gif
    SIZE = args.pixel_dim

    gen_gif(args.num_frames[0], args.frame_rate, args.frame_dim, args.interpolate)
