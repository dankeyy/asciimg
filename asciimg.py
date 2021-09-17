from PIL import Image
from argparse import ArgumentParser
from operator import truediv
from itertools import islice
from os import linesep

GSCALE = "@%#*+=-:. "
WIDTH = 100
SCALE = 0.45
join = ''.join


def resized(img): 
    ratio = 1 / truediv(*img.size)
    dimensions = ( WIDTH, int(ratio * WIDTH * SCALE) )

    return img.resize(dimensions)


def converted(img):
    ''' lazily sending out ascii rows '''

    img = resized(img.convert('L')) # resized black and white pic
    pixels = (GSCALE[x // 30] for x in img.getdata()) # ascii chunk

    while line := join(islice(pixels, WIDTH)):
        yield line + linesep


if __name__ == "__main__":
    # argument handling stuff
    parser = ArgumentParser(description='image to ascii converter')
    parser.add_argument('--file', dest='inputfile', required=True)
    parser.add_argument('--out', dest='outputfile', required=False)
    arguments = parser.parse_args()

    # opening source image for reading, picking output file
    input_img = Image.open(arguments.inputfile)
    output_img = arguments.outputfile or 'out.txt'

    # writing
    with open(output_img, 'w') as f:
        for line in converted(input_img):
            f.write(line)
            print(line, end='')
