# Tookit Scripts
All of the scripts in this directory can be run individually or imported elsewhere. 

## `canvas.py` 
`canvas.py` helps you customize your canvas objects. Run the following to generate a blank template:

```
python canvas.py
```

Further customization options allow you to specify:
- the number of categories (in both the x- and y-dimensions).
- the colors of each category.
- the number of columns & rows (within each category), and their respective widths & heights.
- the maximum values for your boundaries 

For example, running the following will generate a canvas that has 10 total rows and 10 total columns, where there will be 2 column categories and 5 row categories, and each row (across columns) will alternate between `lightgray` and `gray`.  

```
python canvas.py -nr 10 -nc 10 -c 2 5 -s lightgray gray
```
The `newCanvas` and `getCanvas` objects can be found in the `canvas_new_get.txt` file within the `data` folder; you will need to copy the corresponding chunks (which are marked by headers) into your PC Ibex script.  

A full list of customization options can be found by running:

```
python canvas.py -h
```

## `colorize.py`
`colorize.py` changes the colors for a set of `newCanvas` objects. The script reads in a file that contains `newCanvas` objects as strings and replaces the color. 

To run this script, run:

```
python colorize.py -i OLD_COLOR -o NEW_COLOR -c CANVAS_FILE
```

which will replace the `OLD_COLOR` with the `NEW_COLOR` in the `CANVAS_FILE`.

Note that this script can only replace one color at a time and is intended for quick testing of colors. To replace many colors, I encourage you to generate new sets of canvas objects using `canvas.py`. Depending on the situation, it may be easier to simply use the `Ctrl+F` shortcut on PC Ibex to `Replace All` instances of one color string with another. 
