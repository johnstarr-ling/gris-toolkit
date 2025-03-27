# GRIS Toolkit

  Welcome to the GRIS toolkit! GRIS[^1] is an experimental paradigm where participants drag and drop objects on canvases; four demonstrations of GRIS experiments can be found at [this link](https://farm.pcibex.net/r/dxyQEL/).[^2] This open-source toolkit builds GRIS experiments for [PC Ibex](https://doc.pcibex.net/). Note that some experience with PC Ibex is strongly encouraged (and, arguably, expected), as this toolkit focuses on building GRIS canvases/objects and does not cover all possible customization options available on PC Ibex.

If you have any questions or feature requests, please issue a pull request or contact me at `jrs673@cornell.edu`.  


## Installation:
The only required dependencies are `numpy` and `pandas`.

## Use:

### Quick functionality with templates:
If you want to quickly build a GRIS experiment (or feel comfortable with the other tools in this repository), sample templates are provided in the `templates` folder. Templates are currently provided for:
- `category-text`: categorical canvases with text objects, where categories are visually distinguished through color.
- `quartile-text`: categorical canvas divided into quarters, where quarters are visually distinguished through color.
- `blank-text`: blank canvases with text objects
- `blank-shapes`: blank canvases with shape objects
- `blank-audio`: blank canvases with audio objects.[^3]

*These templates can be uploaded to PC Ibex to start experimenting right away!* Each template has extensive comments, where comments either begin with `// COMMENT:` (to provide information about a particular chunk of code) or `// ADD:` (to tell you where you can change the relevant objects/canvases).


Note that the `category-text` template can be extended into `category-shapes` or `category-audio` by drawing from the `blank-shapes` and `blank-audio` templates, respectively; the same can be said for `quartile-text`.


### Customization with scripts:
We strongly encourage you to build your experiment using one of the provided templates. Changes to objects (text, audio, image) are better done manually on PC Ibex; changes to the canvas are nearly always better using the `canvas.py` script (description below).

Regardless, individual modifications to GRIS code can be made using the following scripts:
- `canvas.py`: Build and modify your canvas(es).
  - Both categorical and blank canvases are supported. Categorical canvases beyond those presented in the templates (aka more than 1x5 and 2x2) are constructable using this script. 
- `colorize.py`: Change the color(s) of a canvas file.
  - Due to possible flexibilities in how canvases are named, the toolkit only supports one color change at a time. As such, multi-color changes will require repeated runs of `colorize.py` on separate canvas files, where each canvas file corresponds to the canvas blocks that you wish to change.
  - If you are using a blank canvas (and not categories), it is likely faster to use the `Replace All` functionality on PC Ibex by pressing `Ctrl+F`/`Cmd+F` when editing your `main.js`.

More information about these scripts can be found in the `README` file within the `src` folder. 








[^1]: **GRIS** stands for **G**enerating **R**epresentations **I**n **S**pace.
[^2]: This demonstration study does not collect any data. You should be able to access the original demo study by clicking the link towards the top of the screen  while taking the experiment. 
[^3]: Note that audio files cannot be moved in PC Ibex. As such, the `blank-audio` experiment allows participants to play audio files with corresponding text labels ('AAA', 'BBB', etc.), and these (text) labels are the objects that can be moved around. 
