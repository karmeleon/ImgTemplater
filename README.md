# ImgTemplater

A quick, dirty script to generate .png files from an HTML template and a .csv file.

#Installation

Requires Python 3.6 and `google-chrome` in your path. Tested on Ubuntu, but any OS that supports headless Chrome should work, assuming you update the code to point to the executable.

```
pip install -r requirements.txt
```

#Usage

```
python3.6 imgtemplater.py -c example/data.csv -t example/template.html -x 460 -y 660 -o example
```

Reads a template from example/template.html, CSV data from example/data.csv, sets the output size to 440 by 660 pixels, and outputs the resulting images to example/[id].png.

All rows must have an `id` entry, which is the filename of the output file.

Uses multiprocessing.Pool to render images in parallel, so the more cores you have, the merrier!