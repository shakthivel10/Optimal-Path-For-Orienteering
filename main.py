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

    imageCopy = image.copy()

    # load image as a pixel array
    pix = imageCopy.load()

    imageWidth, imageHeight = image.size
    imageWidth -= 1
    imageHeight -= 1

    # the terrain file depicts the terrain during summer

    if season.lower() == "summer":
        pass

    # during fall, foot paths adjacent to easy movement forest are covered by leaves

    elif season.lower() == "fall":
        for i in range(0, imageWidth):
            for j in range(0, imageHeight):
                if pix[i, j] == (0, 0, 0, 255):
                    lowerX, lowerY, upperX, upperY = 0, 0, 0, 0

                    if i == 0:
                        lowerX = 1

                    elif i == imageWidth:
                        upperX = -1

                    if j == 0:
                        lowerY = 1

                    elif j == imageHeight:
                        upperY = -1

                    for a in range(-1 + lowerX, 2 + upperX):
                        for b in range(-1 + lowerY, 2 + upperY):
                            if a == 0 and b == 0:
                                continue

                            neighborX = i + a
                            neighborY = j + b
                            if pix[neighborX, neighborY] == (255, 255, 255, 255):
                                pix[i, j] = (255, 0, 0)
                                break

    #  In winter, the waters can freeze. we will assume that any water within
    #  seven pixels of non-water is safe to walk on.

    elif season.lower() == 'winter':
        bluePixelSet = set()
        for i in range(0, imageWidth):
            for j in range(0, imageHeight):
                currBlueXY = 1000 * i + j

                if pix[i, j] == (0, 0, 255, 255) and currBlueXY not in bluePixelSet:

                    currentPixelLakeEdges = set()
                    queue = [currBlueXY]
                    visited = set()
                    while len(queue) > 0:
                        currPixel = queue.pop(0)
                        bluePixelSet.add(currPixel)
                        lowerX, lowerY, upperX, upperY = 0, 0, 0, 0
                        i = currPixel // 1000
                        j = currPixel % 1000
                        if i == 0:
                            lowerX = 1

                        elif i == imageWidth:
                            upperX = -1

                        if j == 0:
                            lowerY = 1

                        elif j == imageHeight:
                            upperY = -1

                        for a in range(-1 + lowerX, 2 + upperX):
                            for b in range(-1 + lowerY, 2 + upperY):
                                if a == 0 and b == 0:
                                    continue

                                neighborX = i + a
                                neighborY = j + b
                                neighborXY = 1000 * neighborX + neighborY

                                if neighborXY not in visited:
                                    if pix[neighborX, neighborY] == (0, 0, 255, 255):
                                        queue.append(neighborXY)
                                    else:
                                        currentPixelLakeEdges.add(neighborXY)

                                visited.add(neighborXY)

                    for lakeEdgePixel in currentPixelLakeEdges:
                        maxLength = 7
                        lakeEdgePixelX = lakeEdgePixel // 1000
                        lakeEdgePixelY = lakeEdgePixel % 1000
                        for ai in range(-1 * maxLength, maxLength + 1):
                            for aj in range(-1 * maxLength, maxLength + 1):
                                if ai == 0 and aj == 0:
                                    continue

                                neighborX = lakeEdgePixelX + ai
                                neighborY = lakeEdgePixelY + aj
                                if 0 < neighborX <= imageWidth and 0 < neighborY <= imageHeight:
                                    if pix[neighborX, neighborY] == (0, 0, 255, 255):
                                        pix[neighborX, neighborY] = (
                                            165, 242, 243)

    # In spring season, any pixels within fifteen pixels of water that can be reached
    # from a water pixel without gaining more than one meter of elevation (total) are now underwater.

    elif season.lower() == 'spring':
        reachDistance = 15
        visited = set()
        for i in range(0, imageWidth):
            for j in range(0, imageHeight):
                if pix[i, j] != (0, 0, 255, 255):
                    lowerX, lowerY, upperX, upperY = 0, 0, 0, 0

                    if i == 0:
                        lowerX = 1

                    elif i == imageWidth:
                        upperX = -1

                    if j == 0:
                        lowerY = 1

                    elif j == imageHeight:
                        upperY = -1

                    for a in range(-1 + lowerX, 2 + upperX):
                        for b in range(-1 + lowerY, 2 + upperY):
                            if a == 0 and b == 0:
                                continue
                            neighborX = i + a
                            neighborY = j + b
                            neighborXY = 1000 * neighborX + neighborY

                            if neighborXY not in visited:
                                if pix[neighborX, neighborY] == (0, 0, 255, 255):
                                    visited.add(neighborXY)

        for i in range(0, reachDistance):
            nextLayer = set()

            for p in visited:
                lowerX, lowerY, upperX, upperY = 0, 0, 0, 0
                i = p // 1000
                j = p % 1000
                currElevation = elevation[j][i]
                if i == 0:
                    lowerX = 1

                elif i == imageWidth:
                    upperX = -1

                if j == 0:
                    lowerY = 1

                elif j == imageHeight:
                    upperY = -1

                for a in range(-1 + lowerX, 2 + upperX):
                    for b in range(-1 + lowerY, 2 + upperY):
                        if a == 0 and b == 0:
                            continue
                        neighborX = i + a
                        neighborY = j + b
                        neighborXY = 1000 * neighborX + neighborY

                        if pix[neighborX, neighborY] != (0, 0, 255, 255) and pix[neighborX, neighborY] != (
                                205, 0, 101, 255) and \
                                (elevation[neighborY][
                                    neighborX] - currElevation) <= 1 and neighborXY not in nextLayer and \
                                0 <= neighborX <= imageWidth and 0 <= neighborY <= imageHeight:
                            nextLayer.add(neighborXY)

            for p in nextLayer:
                pix[p // 1000, p % 1000] = (139, 69, 19)

            visited = nextLayer

    else:
        print("Invalid Season")
        return

    imageCopy.show()

    startPix = pix[startX, startY]
    colorList = list(startPix)
    colorCode = colorList[0] * 1000000 + colorList[1] * 1000 + colorList[2]

    if colorCode == colorLake or colorCode == colorImpassableVegetation or colorCode == colorOutOfBounds:
        print("start node is itself unreachable/impassable, no path exists")
        return

    nodes = {}

    startNode = node(startXY, colorCode, startX, startY)

    nodes[startXY] = startNode  # will also be used as the visited set

    # Create weighted graph representing terrain for that portion of the terrain
    # that can be reached from the start node, with both 3D distance between the nodes
    # and the time required to travel between the nodes (calculated based on terrain speeds,
    # and the elevation between two nodes) as the edge weights.

    queue = [startNode]

    while len(queue) > 0:
        currentNode = queue.pop(0)
        currentX = currentNode.x
        currentY = currentNode.y

        currentNodeElevation = elevation[currentY][currentX]

        currentFlatTerrainSpeed = terrainSpeed[currentNode.color]

        # OffSets
        lowerX, lowerY, upperX, upperY = 0, 0, 0, 0

        if currentX == 0:
            lowerX = 1

        elif currentX == imageWidth:
            upperX = -1

        if currentY == 0:
            lowerY = 1

        elif currentY == imageHeight:
            upperY = -1

        for i in range(-1 + lowerX, 2 + upperX):
            for j in range(-1 + lowerY, 2 + upperY):

                if i == 0 and j == 0:
                    continue

                neighborX = currentX + i
                neighborY = currentY + j
                neighborXY = 1000 * neighborX + neighborY

                if neighborXY in nodes.keys():  # already created
                    neighborNode = nodes[neighborXY]
                    neighborColorCode = neighborNode.color  # for average terrain speed

                else:
                    neighborColorList = list(pix[neighborX, neighborY])
                    neighborColorCode = neighborColorList[0] * 1000000 + neighborColorList[1] * 1000 + \
                        neighborColorList[2]

                    if neighborColorCode == colorLake or neighborColorCode == colorImpassableVegetation or neighborColorCode == colorOutOfBounds:
                        continue

                    neighborNode = node(
                        neighborXY, neighborColorCode, neighborX, neighborY)
                    nodes[neighborXY] = neighborNode
                    queue.append(neighborNode)

                neighborNodeElevation = elevation[neighborY][neighborX]

                height = neighborNodeElevation - currentNodeElevation

                combinedFlatTerrainAverageSpeed = (
                    currentFlatTerrainSpeed + terrainSpeed[neighborColorCode]) / 2

                if neighborY == currentY:

                    trueDistance = math.sqrt(
                        longitudeLengthSquared + height * height)

                    trueTime = getTrueTime(
                        trueDistance, height, longitudeLength, combinedFlatTerrainAverageSpeed)

                elif neighborX == currentX:
                    trueDistance = math.sqrt(
                        latitudeLengthSquared + height * height)

                    trueTime = getTrueTime(
                        trueDistance, height, latitudeLength, combinedFlatTerrainAverageSpeed)

                else:
                    trueDistance = math.sqrt(
                        diagonalLengthSquared + height * height)

                    trueTime = getTrueTime(
                        trueDistance, height, diagonalLength, combinedFlatTerrainAverageSpeed)

                currentNode.addNeighbor(neighborXY, trueDistance, trueTime)


def getTrueTime(trueDistance, height, flatDistance, combinedFlatTerrainAverageSpeed):

    if abs(height) > flatDistance:
        # ((>45 degrees) too steep upwards or downwards, cannot run.)
        return 9.0e+12

    else:
        elevationFactor = height / flatDistance

        # Assuming, running uphill results in a decrease in speed by upto a factor of 2 and
        # Running downhill results in a increase in speed by upto a factor of 2 (for 45 degrees)

        return trueDistance / (combinedFlatTerrainAverageSpeed * (1 - elevationFactor))


if __name__ == "__main__":
    main()
