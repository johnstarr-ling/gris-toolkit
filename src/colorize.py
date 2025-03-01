import argparse


###############################################################################
# Load arguments 
###############################################################################

parser = argparse.ArgumentParser()

parser.add_argument('-i', '--input_hex', type=str,
                    default='lightgray',
                    help='Input/current color.')

parser.add_argument('-o', '--output_hex', type=str,
                    default='darkgray',
                    help='Output/new color.')

parser.add_argument('-c', '--input_canvas', type=str,
                    default='./data/sample_canvas_input.txt',
                    help='Input canvas file.')

parser.add_argument('-n', '--output_name', type=str,
                    default='./data/sample_canvas_output.txt', 
                    help='Output canvas file.')

args = parser.parse_args()




###############################################################################
# Change colors
###############################################################################

# Colorize function
def colorize(canvas_string, input_hex, output_hex):
    return canvas_string.replace(f".color('{input_hex}')", f".color('{output_hex}')")

if __name__ == '__main__':

    with open(args.input_canvas) as inp:
        canvas = inp.read()

    with open(args.output_name, 'w') as out:
        out.write(colorize(canvas, args.input_hex, args.output_hex))

