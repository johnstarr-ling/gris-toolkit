# GRIS Toolkit

Welcome to the GRIS toolkit! GRIS[^1] is an experimental paradigm where participants drag and drop objects on canvases, where the space between objects denotes some meaningful relationship(s). Following the collection of data, researchers have access to the incremental drag-and-drop events (which object moved, when it moved, and where it moved to) and the final locations of all objects at the end of each trial, supporting a number of experimental designs and questions. Three demonstrations of GRIS experiments can be found at [this link](https://farm.pcibex.net/r/dxyQEL/).[^2] 

This open-source toolkit builds GRIS experiments for [PC Ibex](https://doc.pcibex.net/). Note that some experience with PC Ibex is strongly encouraged (and, arguably, expected), as this toolkit focuses on building GRIS canvases/objects and does not cover all possible customization options available on PC Ibex.

![alt text](https://github.com/johnstarr-ling/gris-toolkit/blob/main/src/outputs/image_3D.gif "Sample visualization of GRIS data, where distance ~ similarity.")


#### Table of Contents <a name="toc"></a>:
- [Installation](#installation)
- [Use](#use)
- [Standard Pipeline](#pipeline)
- [Tips & Tricks](#tat)
- [Citation](#citation)

If you have any questions or feature requests, please issue a pull request or contact me at `jrs673@cornell.edu`. Some projects that are currently in development: 
- an interactive GUI where you can draw your canvas (in a gridded, spreadsheet-like environment) and then run a quick script to build that canvas for PC Ibex.
- additional templates (particularly some that automatically fit to the size of the screen you are working with)
- variations on distance formula calculations

## Installation: <a name="installation"></a> | [back to top](#toc)
Required dependencies are (minimally) `numpy` and `pandas`. If you want to use the full capabilities of GRIS, I encourage you to run the following in your virtual environment:

```
python -m pip install -r requirements.txt
```

## Use: <a name="use"></a> | [back to top](#toc)

### Quick functionality with templates:
If you want to quickly build a GRIS experiment (or feel comfortable with the other tools in this repository), sample templates are provided in the `templates` folder. Templates are currently provided for:
- `category-text`: categorical canvases with text objects, where categories are visually distinguished through color.
- `quartile-text`: categorical canvas divided into quarters, where quarters are visually distinguished through color.
- `blank-text`: blank canvases with text objects
- `blank-shapes`: blank canvases with shape objects
- `blank-audio`: blank canvases with audio objects.[^3]

*These templates can be uploaded to PC Ibex to start experimenting right away!* Each template has extensive comments, where comments either begin with `// COMMENT:` (to provide information about a particular chunk of code) or `// ADD:` (to tell you where you can change the relevant objects/canvases).


Note that the `category-text` template can be extended into `category-shapes` or `category-audio` by drawing from the `blank-shapes` and `blank-audio` templates, respectively; the same can be said for `quartile-text`.

Also, the templates were designed with laptop functionality in mind. To support tablet use (or device general use), add the `autofit` flag when running `canvas.py`.

### Draw your own canvas:
If you'd prefer to *draw* your canvas, you can do so by filling in cels on the Google Sheet [here](https://docs.google.com/spreadsheets/d/1sGGG7CWqjrYFazkx4lSACYk-2peZrUHPVDiLMJD4yDc/edit?usp=sharing). Instructions for drawing these canvas are included on that link; instructions for how to process these drawn canvases with `xlsx.py` can be found in the `README.md` file in the `src` folder. 

### Customization with scripts:
We strongly encourage you to build your experiment using one of the provided templates or by drawing your own template using the Google Sheets link. Changes to objects (text, audio, image) are better done manually on PC Ibex; changes to the canvas are nearly always better using the `canvas.py` script (description below).

Regardless, individual modifications to GRIS code can be made using the following scripts:
- `canvas.py`: Build and modify your canvas(es).
  - Both categorical and blank canvases are supported. Categorical canvases beyond those presented in the templates (aka more than 1x5 and 2x2) are constructable using this script. 
- `colorize.py`: Change the color(s) of a canvas file.
  - Due to possible flexibilities in how canvases are named, the toolkit only supports one color change at a time. As such, multi-color changes will require repeated runs of `colorize.py` on separate canvas files, where each canvas file corresponds to the canvas blocks that you wish to change.
  - If you are using a blank canvas (and not categories), it is likely faster to use the `Replace All` functionality on PC Ibex by pressing `Ctrl+F`/`Cmd+F` when editing your `main.js`.

More information about these scripts can be found in the `README` file within the `src` folder. 


## Standard Pipeline: <a name="pipeline"></a> | [back to top](#toc)
1. Build your GRIS from a template or using `canvas.py` | [gris-toolkit!]
2. Modify the PC Ibex script according to your desiderata | [on your own!]
3. Run the experiment and download the data | [on your own!]
4. Process the raw data using R | [gris toolkit!]
5. Build your data pipeline to calculate event times and object relations | [gris toolkit! (if you're using Python)]
6. Align your cleaned data with your conditions | [on your own!]
7. Find some amazing results! | [on your own!]


## Tips and Tricks:  <a name="tat"></a> | [back to top](#toc)
- To eliminate the ability to scroll in a trial (a useful feature when running GRIS on mobile devices), ensure that your design fits within 0-100(vw/vh), and then paste the following code into the relevant `Trial` code blocks:
```
// Stop scrolling!
    newFunction(() => {
    const preventScroll = (e) => {
        e.preventDefault();
        e.stopPropagation();
        return false;
    };

    // Disable scrolling via CSS
    document.documentElement.style.overflow = 'hidden';
    document.documentElement.style.height = '100vh';
    document.documentElement.style.width = '100vw';
    document.documentElement.style.margin = '0';
    document.documentElement.style.padding = '0';

    document.body.style.overflow = 'hidden';
    document.body.style.height = '100vh';
    document.body.style.width = '100vw';
    document.body.style.margin = '0';
    document.body.style.padding = '0';

    // Scroll to top
    window.scrollTo(0, 0);

    // Disable touchmove (mobile scroll)
    document.addEventListener('touchmove', preventScroll, { passive: false });

    // Optional: prevent gestures
    document.addEventListener('gesturestart', preventScroll, { passive: false });
}).call(),
```



## Citation: <a name="citation"></a> | [back to top](#toc)
If you use GRIS, please use the following citation:
```
Starr, J.R., Winship, A, & van Schijndel, M. (2025). Generating Representations in Space with GRIS. Proceedings of the 47th Annual Conference of the Cognitive Science Society.
```


[^1]: **GRIS** stands for **G**enerating **R**epresentations **I**n **S**pace. GRIS was originally modeled to approximate human representational spaces in a way that is comparable to vector representations of language constructed by modern computational models of language, such as LLMs. According to [Yoav Artzi](https://yoavartzi.com/), you can think of GRIS as "t-SNE for humans!".
[^2]: This demonstration study does not collect any data. You should be able to access the original demo study by clicking the link towards the top of the screen  while taking the experiment. 
[^3]: Note that audio files cannot be moved in PC Ibex (to our knowledge). As such, the `blank-audio` experiment allows participants to play audio files with corresponding text labels ('AAA', 'BBB', etc.), and these (text) labels are the objects that can be moved around. 
