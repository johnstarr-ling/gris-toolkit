# **Toolkit Code**
All of the scripts in this directory can be individually run or imported. 

## **Experiment Design**
### `canvas.py` 
`canvas.py` helps you customize your canvas objects. Run the following to generate a blank template:

```
python canvas.py
```

Further customization options allow you to specify:
- the number of categories (in both the x- and y-dimensions).
- the colors of each category.
- the number of columns & rows (within each category), and their respective widths & heights.
- the maximum values for your boundaries 
- autofit the canvas according to the screen dimensions of your device. 

For example, running the following will generate a canvas that has 10 total rows and 10 total columns, where there will be 2 column categories and 5 row categories, and each row (across columns) will alternate between `lightgray` and `gray`.  

```
python canvas.py -nr 10 -nc 10 -c 2 5 -s lightgray gray
```
The `newCanvas` and `getCanvas` objects can be found in the `canvas_new_get.txt` file within the `data` folder; you will need to copy the corresponding chunks (which are marked by headers) into your PC Ibex script.  

A full list of customization options can be found by running:

```
python canvas.py -h
```

### `xlsx.py`
`xlsx.py` reads in a drawn canvas (downloaded from a Google Sheets link like [this one](https://docs.google.com/spreadsheets/d/1sGGG7CWqjrYFazkx4lSACYk-2peZrUHPVDiLMJD4yDc/edit?usp=sharing)), extracts the color of each cel, and translates the cel to a Canvas object on PC Ibex. 

You will need to specify the .xlsx file and the corresponding sheet. For example, if I have a file named `sample.xlsx` with a sheet called `helloworld`, then I can process this file by running the following command:

```
python xlsx.py -f sample.xlsx -s helloworld -o OUTPUT_NAME
```

As in `canvas.py`, you can specify various other features about the canvas, including: x and y bounds, the height of rows and the width of columns, etc. Run the following to see what you can tinker with:

```
python xlsx.py -h
```

These specifications are similar to those found in `canvas.py`.


### `colorize.py`
`colorize.py` changes the colors for a set of `newCanvas` objects. The script reads in a file that contains `newCanvas` objects as strings and replaces the color. 

To run this script, run:

```
python colorize.py -i OLD_COLOR -o NEW_COLOR -c CANVAS_FILE
```

which will replace the `OLD_COLOR` with the `NEW_COLOR` in the `CANVAS_FILE`.

Note that this script can only replace one color at a time and is intended for quick testing of colors. To replace many colors simultaneously, I encourage you to generate new sets of canvas objects using `canvas.py`. Depending on the situation, it may be easier to simply use the `Ctrl+F` shortcut on PC Ibex to `Replace All` instances of one color string with another. 

## **Data Processing**
### `process_raw_data.R`
`process_raw_data.R` has a pretty informative title: run this script (which has been taken from the PC Ibex website) to process your data. I use RStudio. Note that you will need to specify the file name and location in the script itself; you will also need to set your session to the source file location. *This should be the first thing you do once you've downloaded your results file.* 

### `utils.py`
`utils.py` has a number of handy functions that help you process your data. The most important ones are:
- `compute_action_times`: Determines the incremental time course of each drag-and-drop event.
- `clean_string`: Processes `Final` graphs into a more usable format.
- `expand_graphs`: Expands a trial to multiple rows, where each row reflects an object and its location.
- `compute_pairwise_distances`: Calculates the distance between object X and object Y for all possible combinations of objects (without repeats, aka comparing X with Y counts as comparing Y with X) within each trial. 
- `z_score`: Computes the z_score of a measurement based on some group(s).

The functions in `utils.py` are, for the most part, quite human readable -- I've tried my best to comment as much as possible and use informative variable names. That being said, I've also spent some time trying to optimize `compute_action_times` and `compute_pairwise_distances`, as both of these functions have to handle a LOT of data concurrently. As such, these functions may be a little less readable. 

### `pipeline.ipynb`
`pipeline.ipynb` describes three example data-processing pipelines. You should be able to adopt the approaches in these pipelines to your own. 

### `visualizer.py`
`visualizer.py` helps you construct 2D or 3D graphs of your similarity data; examples of some visuals created using the `demo-2-distances.csv` file can be found in the `outputs` folder. `visualizer.py` currently supports 2D, 3D (static), and 3D (animated gif) visuals. *This visualizer is still under development, but please let us know if there are some features that you would like to see.*

The way to run the visualizer is:
```
python visualizer.py -i YOUR_FILE -t GRAPH_TITLE -g GRAPH_TYPE(S)
```
though you can see the full list of specifications with:
```
python visualizer.py -h
```

### Folders 
- `data` has some sample canvases, along with the data needed to run the relevant sample pipelines in `pipeline.ipynb`. 
- `output` has the output files generated by `pipeline.ipynb`
