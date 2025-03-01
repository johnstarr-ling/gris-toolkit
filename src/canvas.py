import argparse
import numpy as np
import pandas as pd
import math

###############################################################################
# Load arguments 
###############################################################################

parser = argparse.ArgumentParser()

parser.add_argument('-o', '--output_name', type=str,
                    default='./data/canvas_new_get.txt', 
                    help='Output data file.')

parser.add_argument('-c', '--categories', type=int,
                    default=[1,1],
                    nargs=2,
                    help='Specify distinct number of categories for rows X and columns Y in form X Y.')

parser.add_argument('-s', '--shades', type=list,
                    nargs='+', 
                    default=['lightgray'],
                    help='Number of colors for canvas.')

parser.add_argument('-nc', '--num_columns', type=int,
                    default=34,
                    help='Number of columns.')

parser.add_argument('-nr', '--num_rows', type=int,
                    default=14,
                    help='Number of rows.')

parser.add_argument('-cw', '--width', type=str,
                    default=30,
                    help='Column width (in pixels.')

parser.add_argument('-hr', '--height', type=str, 
                    default=30,
                    help='Row height (in pixels).')

parser.add_argument('-xmin', '--x_minimum', type=int,
                    default=250,
                    help='Leftmost bound of the canvas on the screen.')

parser.add_argument('-xmax', '--x_maximum', type=int,
                    default=1270,
                    help='Rightmost bound of canvas on the screen.')

parser.add_argument('-ymin', '--y_minimum', type=int,
                    default=50,
                    help='Topmost bound of the canvas on the screen.')

parser.add_argument('-ymax', '--y_maximum', type=int,
                    default=470,
                    help='Bottommost bound of the canvas on the screen.')


args = parser.parse_args()


OUTPUT_NAME = args.output_name
CATEGORIES = args.categories
COLORS = args.shades 
NUM_COLS = args.num_columns
NUM_ROWS = args.num_rows
WIDTH = args.width 
HEIGHT = args.height
XMIN = args.x_minimum 
XMAX = args.x_maximum
YMIN = args.y_minimum
YMAX = args.y_maximum

# Ensure non-zero amount of categories
if 0 in set(CATEGORIES):
    raise Exception('Failed to specify number of rows or columns.')

# Multiple shades should be whole strings 
if len(COLORS) > 1: 
    COLORS = [''.join(shade) for shade in COLORS]
    
# Ensure subdivisions for both rows and cols 
if (CATEGORIES[0] != 0) and (NUM_COLS % CATEGORIES[0] != 0):
    raise Exception('Specified number of columns cannot be evenly divided by the number of column categories.')

if (CATEGORIES[1] != 0) and (NUM_ROWS % CATEGORIES[1] != 0):
    raise Exception('Specified number of rows cannot be evenly divided by the number of row categories.')





###############################################################################
# Functions
###############################################################################

##### WRITING IBEX CODE 
# Constructs newCanvas objects
def make_newCanvas(label, xlocation, ylocation, color, 
                   width=WIDTH, height=HEIGHT):
    return f'newCanvas("{label}", {width}, {height}).color("{color}").print({xlocation}, {ylocation}),'

# Constructs getCanvas objects
def make_getCanvas(label):
    return f'getCanvas("{label}"),'



##### CANVAS OPERATIONS

# Find the locations for all canvas values
def generate_range(midpoint, step, num_X):
    
    # num_X is the number of rows/columns that we want.
    # Repetitions is the number of canvases we want on each side
    # of the midpoint.

    repetitions = num_X/2 

    # If repetitions isn't an integer, set the first cell to cross the midpoint.
    if repetitions != int(repetitions):
        midpoint = midpoint - (step / 2)
    
    # Calculate steps from the midpoint 
    int_repetitions = math.floor(repetitions)
    left_steps = [midpoint - i * step for i in range(int_repetitions, -1, -1)]
    
    # Odd number of repetitions have extra value (center)
    if repetitions != int(repetitions):
        right_steps = [midpoint + i * step for i in range(1, int_repetitions + 1)]
    
    # Even number of repetitions have the same number of X on other side of the midpoint
    else:
        right_steps = [midpoint + i * step for i in range(1, int_repetitions)]
    
    return left_steps + right_steps



# Centers canvas both horizontally/vertically; x-range (250, 1270) | y-range (50, 470)
def canvas_positions(num_rows=NUM_ROWS, num_cols=NUM_COLS,
                     col_width=WIDTH, row_height=HEIGHT,
                     x_min=XMIN, x_max=XMAX, 
                     y_min=YMIN, y_max=YMAX):
    
    # Spread outward from the center:
    x_mid = (x_max+x_min)/2 
    y_mid = (y_max+y_min)/2
    
    # Column positions 
    col_positions = generate_range(x_mid, col_width, num_cols) 
    
    # Row positions    
    row_positions = generate_range(y_mid, row_height, num_rows)

    return col_positions, row_positions 



# Make (grid) labels for categorical canvases
def canvas_labels(num_rows=NUM_ROWS, num_cols=NUM_COLS,
                  categories = CATEGORIES):
    
    # Blank canvas condition | Covers case where people leave default
    # category specification, or choose its flip ([0,1])
    if np.prod(categories) == 1:
        return [(1, 1, x, y) for x in range(num_cols) for y in range(num_rows)]

    # Category canvas condition

    cat_cols = args.categories[0]
    cat_rows = args.categories[1]
    
    # Building arrays that are easy to loop through (ugly, but clean) |
    # accounts for 0 specification
    col_bins = np.array_split([x for x in range(num_cols)], max(cat_cols, 1))
    row_bins = np.array_split([y for y in range(num_rows)], max(cat_rows, 1))
    
    # More ugliness, but accounts for 0 specification
    labels = []
    for c_idx, c_bin in enumerate(col_bins):
        for r_idx, r_bin in enumerate(row_bins):
            c_vals = c_bin if c_bin.size else [0]
            r_vals = r_bin if r_bin.size else [0]
            for c_val in c_vals:
                for r_val in r_vals:
                    labels.append((c_idx, r_idx, c_val, r_val))
    
    return labels 


# Assign colors to categories:
def assign_colors(colors=COLORS, cat_cols = CATEGORIES[0], cat_rows = CATEGORIES[1]):
    color_count = len(colors)
    pos2color = dict()
    
    print('# COLOR-CATEGORY MATCHING #')
    
    # Handling blank canvas case
    if (cat_cols == 1) and (cat_rows == 1):
        pos2color[(1, 1)] = colors[0]
        print(1, 1, colors[0])
        return pos2color 
    
    # All other cases
    for x in range(cat_cols):
        for y in range(cat_rows):
            shade = colors[(x * cat_rows + y) % color_count]
            print(x, y, shade)
            pos2color[(x, y)] = shade 
    
    return pos2color 






###############################################################################
# Generate canvas code 
###############################################################################

if __name__ == '__main__':

    # Build positions
    x_positions, y_positions = canvas_positions()

    if (max(set(x_positions)) > XMAX) or (min(set(x_positions)) < XMIN):
        raise Exception('Columns do not fit within bounds. Either specify fewer columns, increase horizontal bounds, or decrease column width.')

    if (max(set(y_positions)) > YMAX) or (min(set(y_positions)) < YMIN):
        raise Exception('Rows do not fit within bounds. Either specify fewer rows, increase vertical bounds, or decrease row height.')

    positions = [(x_pos, y_pos) for y_pos in y_positions for x_pos in x_positions]
    
    # Build labels
    labels = canvas_labels()
    
    # Build color_dict
    color_dict = assign_colors()

    # Ensure that the number of positions are identical to the number of labels
    assert len(positions) == len(labels)

    # Adding newCanvas Header
    canvas_string = '############### NEW CANVAS ###############\n'
    
    # Building newCanvas items
    idx1 = 0
    for label in labels:
        if label[0] != idx1:
            idx1 += 1 
            canvas_string += '\n'
        canvas_string += make_newCanvas(label, x_positions[label[2]], y_positions[label[3]], color_dict[(label[0], label[1])])

    # Adding getCanvas Header
    canvas_string += '\n\n\n\n\n############### GET CANVAS ###############\n'

    # Building getCanvas items
    idx2 = 0 
    for label in labels:
        if label[0] != idx2:
            idx2 += 1
            canvas_string += '\n'

        canvas_string += make_getCanvas(label)

    # Write to file
    with open(OUTPUT_NAME, 'w') as w:
        w.write(canvas_string)
