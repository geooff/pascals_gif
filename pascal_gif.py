"""
This program attempts to remake a gif I found from wikipedia.
The image can be found at:
https://upload.wikimedia.org/wikipedia/commons/6/66/Pascal%27s_Triangle_animated_binary_rows.gif

The gif comes with the following decription:
Each frame represents a row in Pascal's triangle.
Each column of pixels is a number in binary with the least significant bit at the bottom.
Light pixels represent ones and the dark pixels are zeroes.
"""
import sys
import shutil
import os # For system level manipulation
from math import floor, ceil, log # Rounding functions for uneven row counts
from PIL import Image # Image manipulation library
from struct import pack # Pack data for image lib
from imageio import get_writer, imread # Convery set of images to gif
from re import search

# Set size of output gif
SIZE = 100, 100


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


def gen_frame(row, filename):
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
    canvis = l_append+frame+r_append

    # If the binary_list exceeds the size of the frame than trim off the edges
    if len(canvis) > (SIZE[0]*SIZE[1]):
        offset = (((len(frame))-(SIZE[0])*SIZE[1]))/2
        power = int(-log(SIZE[0], 10))
        canvis = canvis[int(round(offset, power)):]

    # Pack the frame into a byte and generate an image with it
    data = pack('B'*len(canvis), *[pixel*255 for pixel in canvis])
    img = Image.frombuffer('L', SIZE, data)
    img = img.rotate(-90)
    img = img.resize((1024, 1024), Image.LANCZOS)
    img.save(filename)


def gen_gif(n_rows, f_time):
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
        gen_frame(row, "frame_{0}.png".format(idx))

    # Generate output gif given the files generated above
    with get_writer('pascals_triangle_{}.gif'.format(n_rows), mode='I', duration=f_time) as writer:
        filenames = [file for file in os.listdir() if file.endswith('.png')]

        # Sort files by numbers found in string containing numbers (ex. frame_6.png)
        def sortby(x):
            return int(search(r'\d+', x).group())

        filenames.sort(key=sortby)
        for filename in filenames:
            image = imread(filename)
            writer.append_data(image)


if __name__ == '__main__':

    n_rows = int(input("Please provide number of frames for gif: "))
    f_time = float(input("Please provide frame timing for gif: "))

    gen_gif(n_rows, f_time)
