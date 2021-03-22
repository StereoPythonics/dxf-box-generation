# dxf-box-generation
A python project to programatically generate .dxf files for laser cut boxes.

# Setup
You'll need python 3 installed along with some packages that handle writing to the DXF format.
You can check if you already have python installed by running this in your terminal
```
python3 --version
```
Once you've managed to get python 3 installed you'll need to grab a few packages. I used PIP ("Pip Installs Packages") to install mine.
You can check if pip is installed for python 3 my running the following:
```
pip3 --version
```
Once you've got pip installed, run the following commands to install the required dxf writing library
```
pip3 install ezdxf
```
# Usage 
Copy AutoBoxer.py to the directory where you're working and open a terminal window there. Create new boxes using the following:
```
python3 AutoBoxer.py [newFilePath] [x] [y] [z] [sheetThickness] [fingerWidth] [laserKerf]
```
All units are in mm, for example: 
```
python3 AutoBoxer.py newfile 30 50 70 6 10 0.2
```
Will create a new file "newFile.dxf" for a box of internal dimensions 30mm x 50mm x 70mm. For the edges of the box, the generated interlocking fingers will be generated based on a 6mm sheet thickness, with 10mm wide fingers.

The script can also account for laser kerf (the material lost to the cutting laser) and tweak the finger widths subtly to ensure a snug interference fit. I've found that 0.2mm is a good kerf compensation value to use with professional laser cutting services such as http://www.cutlasercut.com/

![Example](https://raw.githubusercontent.com/StereoPythonics/dxf-box-generation/main/ExampleBox.png)

# Smart finger widths
If you request box dimensions that are incompatible with your desired finger width, the script will do it's best by rounding to the nearest odd integer number of fingers based on your target finger width.

For example, running:

```
python3 AutoBoxer.py smartFingers 40 50 60 6 10 0
```

produces the following results.

![Smart finger widths](https://raw.githubusercontent.com/StereoPythonics/dxf-box-generation/main/SmartFingers.png)

