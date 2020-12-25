from PIL import Image
from argparse import ArgumentParser
from operator import truediv
from os import linesep

GSCALE = "@%#*+=-:. "
WIDTH = 100
SCALE = 0.45


def resized(img):
    ratio = 1 / truediv(*img.size)
    dimensions = ( WIDTH, int(ratio * WIDTH * SCALE) )

    return img.resize(dimensions)


def converted(img):
    img = resized( img.convert('L') ) # resized black and white pic
    pixels = ''.join( GSCALE[x // 30] for x in img.getdata() ) # ascii chunk

    yield from ( pixels[i: i + WIDTH] + linesep for i in range(0, len(pixels), WIDTH) ) # full ascii pic


def main():
    parser = ArgumentParser(description='image to ascii converter')
    parser.add_argument('--file', dest='inputfile', required=True)
    parser.add_argument('--out', dest='outputfile', required=False)
    arguments = parser.parse_args()

    input_img = Image.open(arguments.inputfile)
    output_img = arguments.outputfile or 'out.txt'

    with open(output_img, 'w') as f:
        for line in converted(input_img):
            f.writelines(line)
            print(line, end='')


if __name__ == "__main__":
    main()