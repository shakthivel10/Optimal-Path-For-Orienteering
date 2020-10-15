from PIL import Image

import math
from queue import PriorityQueue
import sys


class node:
    __slots__ = "id", "color", "adjList", "x", "y"

    def __init__(self, id, color, x, y):
        self.id = id
        self.color = color
        self.adjList = dict()
        self.x = x
        self.y = y

    def addNeighbor(self, nbr, distance, trueTime=-1):
        self.adjList[nbr] = [distance, trueTime]

    def getAdjList(self):
        return self.adjList

    def getNeighbors(self):
        return self.adjList.keys()

    def getDistance(self, nbr):
        return self.adjList[nbr][0]

    def getTime(self, nbr):
        return self.adjList[nbr][1]

    def __str__(self):
        return "x,y=" + str(self.x) + "," + str(self.y) + "  " + "Color Code=" + str(self.color) + " Neighbors:" + str(
            ["x,y=" + str(xy // 1000) + "," + str(xy % 1000) + "  distance=" + str(
                self.adjList[xy][0]) + "  time=" + str(self.adjList[xy][1]) for xy in self.adjList])


def main():

    # terrain speeds (meters/second), color codes (r*1000000+g*1000+b )

    terrainSpeed = {
        255192000: 1,  # Light Orange: Rough Meadow
        255000000: 2,   # Red: Leaves Covering Foot Path, Fall
        165242243: 1,   # Pale Turquoise: Lake, Winter
        139069019: 2,   # Dark Brown: Mud, Spring
        2136040: 2,     # Green: Walk Forest
        2208060: 3,     # Light Green: Slow Run Forest
        255255255: 4,   # White : Easy Movement Forest
        248148018: 5,   # Dark Orange :Open Land
        0: 5,           # Black: Foot Path
        71051003: 6     # Brown : Paved Road
    }

    maxSpeed = max(terrainSpeed.values())

    # Impassable Regions
    colorLake = 255                     # Blue : Water
    colorImpassableVegetation = 5073024  # Dark Green : Impassable Vegetation
    colorOutOfBounds = 205000101        # Pink : Out Of Bounds

    # latitude & longitude lengths determined by that of the National Elevation Dataset
    longitudeLength = 10.29
    latitudeLength = 7.55

    longitudeLengthSquared = longitudeLength * longitudeLength
    latitudeLengthSquared = latitudeLength * latitudeLength

    diagonalLength = math.sqrt(longitudeLengthSquared + latitudeLengthSquared)
    diagonalLengthSquared = diagonalLength * diagonalLength

    image = Image.open(sys.argv[1])

    # read elevation file
    elevationFile = open(sys.argv[2], 'r')

    i = 0
    elevation = list()
    for line in elevationFile:
        elevation.append(list())
        for val in line.split():
            elevation[i].append(float(val))
        i += 1

    elevationFile.close()

    # read controls file
    controlsFile = open(sys.argv[3], "r")

    i = 0
    controls = list()
    for line in controlsFile:
        controls.append(list())
        for val in line.split():
            controls[i].append(int(val))
        # print(len(controls[i]),controls[i])
        i += 1

    controlsFile.close()

    season = sys.argv[4]
    outputFileName = sys.argv[5]

    # get X and Y co-ordinates of the starting point
    startControls = controls.pop(0)
    startX = startControls[0]
    startY = startControls[1]
    startXY = 1000 * startX + startY

    nodes = {}
    imageCopy = image.copy()

    # load image as a pixel array
    pix = imageCopy.load()

    imageWidth, imageHeight = image.size
    imageWidth -= 1
    imageHeight -= 1


if __name__ == "__main__":
    main()
