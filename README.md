# GRIS Toolkit

  Welcome to to the GRIS toolkit! GRIS[^1] is an experimental paradigm where participants drag and drop objects on canvases; four demonstrations of GRIS experiments can be found at [this link](https://farm.pcibex.net/r/vxZDAe/).[^2] This open-source toolkit builds GRIS experiments for [PC Ibex](https://doc.pcibex.net/); note that some experience with PC Ibex is strongly encouraged, as this toolkit focuses on building GRIS canvases/objects and does not cover all possible customization options available on PC Ibex.

If you have any questions or feature requests, please issue a pull request or contact me at `jrs673@cornell.edu`.  


### Installation:
The only required dependencies are `numpy` and `pandas`.

### Use:

#### Quick functionality with templates:
If you want to quickly build a GRIS experiment (or feel comfortable with the other tools in this repository), sample templates are provided in the `templates` folder. Templates are currently provided for:
- `category-text`: categorical canvases with text objects, where categories are visually distinguished through color.
- `quartile-text`: categorical canvas divided into quarters, where quarters are visually distinguished through color.
- `blank-text`: blank canvases with text objects
- `blank-shapes`: blank canvases with shape objects
- `blank-audio`: blank canvases with audio objects.[^3]

*These templates can be uploaded to PC Ibex to start experimenting right away!* Each template has extensive comments, where comments either begin with `// COMMENT:` (to provide information about a particular chunk of code) or `// ADD:` (to tell you where you can change the relevant objects/canvases).


Note that the `category-text` template can be extended into `category-shapes` or `category-audio` by drawing from the `blank-shapes` and `blank-audio` templates, respectively.

#### Customization with scripts:
<span style="color:blue">Script customization is under maintenance; accordingly, the information below is not particularly useful at the moment. We will get this to you soon! </span>.

In addition to the provided templates, you can generate your own custom GRIS experiments (or modulate existing ones) using the other scripts in this repository. This toolkit builds GRIS experiments by using Python to write PC Ibex code. Run the following script to build an experiment:


```
python main.py
```
This script will ask you a series of questions to help design your experiment. If you wish to bypass these questions, please include the corresponding variables as keyword arguments. Keyword arguments can be found by running:

```
python main.py -h
```


Individual modifications to GRIS code can be made using the following scripts:
- `canvas.py`: Build and modify your canvas(es).
  - Both categorical and blank canvases are supported.
- `objects.py`: Format your objects and how they are positioned.
  - Objects are placed at the bottom of the screen by default.
- `colorize.py`: Change the color(s) of a canvas file.
  - Due to possible flexibilities in how canvases are named, the toolkit only supports one color change at a time. As such, multi-color changes will require repeated runs of `colorize.py` on separate canvas files, where each canvas file corresponds to the canvas blocks that you wish to change.
  - If you are using a blank canvas (and not categories), it is likely faster to use the `Replace All` functionality on PC Ibex by pressing `Ctrl+F`/`Cmd+F` when editing your `main.js`.










[^1]: **GRIS** stands for **G**enerating **R**epresentations **I**n **S**pace.
[^2]: This demonstration study does not collect any data. 
[^3]: Note that audio files cannot be moved in PC Ibex. As such, the `blank-audio` experiment allows participants to play audio files with corresponding text labels ('AAA', 'BBB', etc.), and these (text) labels are the objects that can be moved around. 
