# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import sys

import ezdxf
from itertools import islice

from ezdxf import units


def BuildBox(filepath, height, width, depth, thickness, finger, kerf):
    doc = ezdxf.new('R2000')
    doc.units = units.MM
    msp = doc.modelspace()
    doc.layers.new(name='boxInternal', dxfattribs={'linetype': 'SOLID', 'color': 7})
    doc.layers.new(name='cut', dxfattribs={'linetype': 'SOLID', 'color': 1,'lineweight':20})

    DrawRectangle(msp, height, width, (0, 0), 'boxInternal')
    DrawSidePatternA(msp, height, width, thickness, finger, kerf, (0, 0), 'cut')
    DrawRectangle(msp, height, depth, (width + thickness * 3, 0), 'boxInternal')
    DrawSidePatternC(msp, height, depth, thickness, finger, kerf, (width + thickness * 3, 0), 'cut')
    DrawRectangle(msp, depth, width, (0, height + thickness * 3), 'boxInternal')
    DrawSidePatternB(msp, depth, width, thickness, finger, kerf, (0, height + thickness * 3), 'cut')

    doc.saveas(filepath + ".dxf")

def DrawRectangle(msp, height, width, offset, layer):
    points = [(0, 0), (width, 0), (width, height), (0, height), (0, 0)]
    offsetPoints = [(p[0] + offset[0], p[1] + offset[1]) for p in points]
    for p in zip(offsetPoints, islice(offsetPoints, 1, None)):
        msp.add_line(p[0], p[1], dxfattribs={'layer': layer})


def DrawSidePatternA(msp, height, width, thickness, finger, kerf, offset, layer):
    DrawFingerSet(msp, height, thickness, finger, kerf, False, False, False, (offset[0], offset[1]), layer)
    DrawFingerSet(msp, height, thickness, finger, kerf, False, False, True, (offset[0] + width, offset[1]), layer)
    DrawFingerSet(msp, width, thickness, finger, kerf, True, True, False, (offset[0], offset[1]), layer)
    DrawFingerSet(msp, width, thickness, finger, kerf, True, True, True, (offset[0], offset[1] + height), layer)
    hsteps = 2 * (round(0.5 * (height / finger) + 0.5) - 1) + 1
    hFingerDist = height / hsteps
    wsteps = 2 * (round(0.5 * (width / finger) + 0.5) - 1) + 1
    wFingerDist = width / wsteps

    DrawLineFromPoints(msp, [(-thickness, hFingerDist + kerf / 2),
                             (-thickness, -thickness),
                             (kerf / 2, -thickness),
                             (kerf / 2, 0),
                             (wFingerDist - kerf / 2, 0)], offset, layer)

    DrawLineFromPoints(msp, [(-thickness, (height - hFingerDist) - kerf / 2),
                             (-thickness, height + thickness),
                             (kerf / 2, height + thickness),
                             (kerf / 2, height),
                             (wFingerDist - kerf / 2, height)], offset, layer)

    DrawLineFromPoints(msp, [(width + thickness, (height - hFingerDist) - kerf / 2),
                             (width + thickness, height + thickness),
                             (width - kerf / 2, height + thickness),
                             (width - kerf / 2, height),
                             (width - wFingerDist + kerf / 2, height)], offset, layer)

    DrawLineFromPoints(msp, [(width + thickness, hFingerDist + kerf / 2),
                             (width + thickness, -thickness),
                             (width - kerf / 2, -thickness),
                             (width - kerf / 2, 0),
                             (width - wFingerDist + kerf / 2, 0)], offset, layer)


def DrawSidePatternB(msp, height, width, thickness, finger, kerf, offset, layer):
    DrawFingerSet(msp, height, thickness, finger, kerf, False, False, False, (offset[0], offset[1]), layer)
    DrawFingerSet(msp, height, thickness, finger, kerf, False, False, True, (offset[0] + width, offset[1]), layer)
    DrawFingerSet(msp, width, thickness, finger, kerf, False, True, False, (offset[0], offset[1]), layer)
    DrawFingerSet(msp, width, thickness, finger, kerf, False, True, True, (offset[0], offset[1] + height), layer)

    hsteps = 2 * (round(0.5 * (height / finger) + 0.5) - 1) + 1
    hFingerDist = height / hsteps
    wsteps = 2 * (round(0.5 * (width / finger) + 0.5) - 1) + 1
    wFingerDist = width / wsteps

    DrawLineFromPoints(msp, [(-thickness, hFingerDist + kerf / 2),
                             (-thickness, 0),
                             (-kerf / 2, 0),
                             (-kerf / 2, -thickness),
                             (wFingerDist + kerf / 2, -thickness)], offset, layer)

    DrawLineFromPoints(msp, [(-thickness, height - hFingerDist - kerf / 2),
                             (-thickness, height),
                             (-kerf / 2, height),
                             (-kerf / 2, height + thickness),
                             (wFingerDist + kerf / 2, height + thickness)], offset, layer)

    DrawLineFromPoints(msp, [(width - wFingerDist - kerf / 2, height + thickness),
                             (width + kerf / 2, height + thickness),
                             (width + kerf / 2, height),
                             (width + thickness, height),
                             (width + thickness, height - hFingerDist - kerf / 2)], offset, layer)

    DrawLineFromPoints(msp, [(width + thickness, hFingerDist + kerf / 2),
                             (width + thickness, 0),
                             (width + kerf / 2, 0),
                             (width + kerf / 2, -thickness),
                             (width - wFingerDist - kerf / 2, -thickness)], offset, layer)


def DrawSidePatternC(msp, height, width, thickness, finger, kerf, offset, layer):
    DrawFingerSet(msp, height, thickness, finger, kerf, True, False, False, (offset[0], offset[1]), layer)
    DrawFingerSet(msp, height, thickness, finger, kerf, True, False, True, (offset[0] + width, offset[1]), layer)
    DrawFingerSet(msp, width, thickness, finger, kerf, True, True, False, (offset[0], offset[1]), layer)
    DrawFingerSet(msp, width, thickness, finger, kerf, True, True, True, (offset[0], offset[1] + height), layer)

    hsteps = 2 * (round(0.5 * (height / finger) + 0.5) - 1) + 1
    hFingerDist = height / hsteps
    wsteps = 2 * (round(0.5 * (width / finger) + 0.5) - 1) + 1
    wFingerDist = width / wsteps
    DrawLineFromPoints(msp, [(0, hFingerDist - kerf / 2), (0, 0), (wFingerDist - kerf / 2, 0)], offset, layer)
    DrawLineFromPoints(msp, [(0, height - hFingerDist + kerf / 2), (0, height), (wFingerDist + kerf / 2, height)],
                       offset, layer)
    DrawLineFromPoints(msp, [(width, height - hFingerDist + kerf / 2), (width, height),
                             (width - wFingerDist + kerf / 2, height)], offset, layer)
    DrawLineFromPoints(msp, [(width, hFingerDist - kerf / 2), (width, 0), (width - wFingerDist + kerf / 2, 0)], offset,
                       layer)


def DrawFingerSet(msp, distance, thickness, finger, kerf, sigmo, horiz, mirror, offset, layer):
    steps = 2 * (round(0.5 * (distance / finger) + 0.5) - 1) + 1
    fingerDist = distance / steps
    points = []
    for i in range(1, steps):
        if horiz:
            y0 = (thickness if mirror else -thickness) if i % 2 != 0 ^ sigmo else 0
            y1 = (thickness if mirror else -thickness) if i % 2 == 0 ^ sigmo else 0
            x = i * fingerDist + (-kerf / 2 if i % 2 == 0 ^ sigmo else kerf / 2)
            points.append((x, y0))
            points.append((x, y1))
        else:
            x0 = (thickness if mirror else -thickness) if i % 2 != 0 ^ sigmo else 0
            x1 = (thickness if mirror else -thickness) if i % 2 == 0 ^ sigmo else 0
            y = i * fingerDist + (-kerf / 2 if i % 2 == 0 ^ sigmo else kerf / 2)
            points.append((x0, y))
            points.append((x1, y))
    DrawLineFromPoints(msp, points, offset, layer)


def DrawLineFromPoints(msp, points, offset, layer):
    offsetPoints = [(p[0] + offset[0], p[1] + offset[1]) for p in points]
    for p in zip(offsetPoints, islice(offsetPoints, 1, None)):
        msp.add_line(p[0], p[1], dxfattribs={'layer': layer})


# Press the green button in the gutter to run the script.
#if __name__ == '__main__':
if(sys.argv.__len__() == 8 ):
    BuildBox(sys.argv[1],float(sys.argv[2]),float(sys.argv[3]),float(sys.argv[4]),float(sys.argv[5]),float(sys.argv[6]),float(sys.argv[7]))
    print('Successfully build box with parameters:')
    print(sys.argv)
elif(sys.argv.__len__() > 1 or sys.argv.__contains__('help')):
    print('Correct usage: python3 AutoBoxer.py [newFilePath] [x] [y] [z] [sheet thickness] [finger width] [laser kerf]')
    print('example: python3 AutoBoxer.py newfile 100 200 300 6 10 0.2')
else:
    BuildBox('example',310,410,510,6.5,20,0.2)



