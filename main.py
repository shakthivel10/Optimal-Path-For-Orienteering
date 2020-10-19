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

    image = Image.open("terrain/"+sys.argv[1])

    # read elevation file
    elevationFile = open("terrain/"+sys.argv[2], 'r')

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

    # during fall, foot paths adjacent to easy movement forest (white pixels) are covered by leaves (red pixels)

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

    # imageCopy.show()

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

    # A* Search Algorithm to find the path that takes the shortest time from the current
    # control point to the next until the last control point is reached.

    # since we do not know in advance, which terrains form the optimal path between the origin and destinations,
    # we divide the displacement between the two terrains by the maximum speed among all terrains,
    # and again divide by 2 to account for the best case elevation factor, to get a heuristic for time.

    timeTaken = {}

    controlsSet = set()

    distanceAccumulator = 0
    timeAccumulator = 0
    startControlX, startControlY = startX, startY
    startControlXY = 1000 * startControlX + startControlY

    controlsSet.add(startControlXY)

    while len(controls) > 0:

        for e in nodes:
            timeTaken[nodes[e].id] = 9.0e+15

        timeTaken[startControlXY] = 0

        endControlArr = controls.pop(0)
        endControlX, endControlY = endControlArr[0], endControlArr[1]

        pq = PriorityQueue()
        pq.put((0, startControlXY))

        known = set()
        found = False

        parent = {startControlXY: None}
        endControlZ = elevation[endControlY][endControlX]

        while not pq.empty():
            currentNodeXY = pq.get()[1]

            currentNode = nodes[currentNodeXY]
            x1 = currentNode.x
            y1 = currentNode.y

            if x1 == endControlX and y1 == endControlY:
                found = True
                break

            adj = currentNode.getAdjList()

            for neighborNodeXY in adj.keys():
                if neighborNodeXY not in known:
                    known.add(neighborNodeXY)

                    neighborNode = nodes[neighborNodeXY]
                    x2 = neighborNode.x
                    y2 = neighborNode.y
                    z2 = elevation[y2][x2]

                    h = math.sqrt(((endControlX - x2) ** 2 + (endControlY - y2) ** 2 + (endControlZ - z2) ** 2)) / (
                        maxSpeed * 2)  # heuristic, least possible time

                    potentialTime = timeTaken[currentNodeXY] + \
                        adj[neighborNodeXY][1]
                    if timeTaken[neighborNodeXY] > potentialTime:
                        timeTaken[neighborNodeXY] = potentialTime

                    pq.put((h + timeTaken[neighborNodeXY], neighborNodeXY))

                    if neighborNodeXY not in parent.keys():
                        parent[neighborNodeXY] = currentNodeXY

        if not found:
            print("no path found!")
            return

    # plot optimal path on image

        currXY = 1000 * endControlX + endControlY
        controlsSet.add(currXY)

        timeAccumulator += timeTaken[currXY]

        while True:

            if not parent[currXY]:
                break

            distanceAccumulator += nodes[currXY].adjList[parent[currXY]][0]

            currXY = parent[currXY]

            pix[currXY // 1000, currXY % 1000] = (255, 79, 0)

        startControlX, startControlY = endControlX, endControlY
        startControlXY = 1000 * startControlX + startControlY

    for control in controlsSet:
        pix[control // 1000, control % 1000] = (105, 50, 255)

    imageCopy.show()
    imageCopy.save("output/"+outputFileName)

    print("Total length of the path:", int(
        round(distanceAccumulator)), "meters")
    print("Total time required to run through this path:",
          int(round(timeAccumulator)), "seconds")

    avgSpeed = distanceAccumulator / timeAccumulator
    print("Average speed:", round(avgSpeed, 2), "meters/second")


def getTrueTime(trueDistance, height, flatDistance, combinedFlatTerrainAverageSpeed):

    # If (slope angle is >=45 degrees), we assume it is too steep and the athlete cannot run)
    if abs(height) >= flatDistance:
        return 9.0e+12

    else:
        # will take positive values between (0, 1) for uphill & negative values between (-1, 0) for downhill slopes.
        tanX = height / flatDistance

        # Assuming, running uphill results in a decrease in speed, and (1 - tanX)
        # running downhill results in a increase in speed by upto a factor of (1 + tanX).

        elevationAdjustedSpeed = (combinedFlatTerrainAverageSpeed * (1 - tanX))

        return trueDistance / elevationAdjustedSpeed


if __name__ == "__main__":
    main()
