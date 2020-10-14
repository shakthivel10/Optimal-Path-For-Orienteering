from PIL import Image

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
    # speed in m/s
    terrainSpeed = {
        255192000: 10,  # light orange: colorRoughMeadow
        192192192: 1,  # silver : fall, leaves covered FootPath
        165242243: 2,  # snow blue: winter, walkable lake
        139069019: 2,  # mud brown, spring mud
        2136040: 2,  # medium green: colorWalkForest
        2208060: 3,  # light green: colorSlowRunForest
        255255255: 4,  # white : colorEasyMovementForest
        248148018: 5,  # dark orange :colorOpenLand
        0: 5,  # black: colorFootPath
        71051003: 6  # brown : colorPavedRoad
    }

    maxSpeed = 0
    for terrain in terrainSpeed:
        if terrainSpeed[terrain] > maxSpeed:
            maxSpeed = terrainSpeed[terrain]

    # color codes ( r*1000000+g*1000+b )

    colorImpassableVegetation = 5073024
    colorLake = 255
    colorOutOfBounds = 205000101

    longitudeLength = 10.29
    latitudeLength = 7.55

    longitudeLengthSquared = longitudeLength * longitudeLength
    latitudeLengthSquared = latitudeLength * latitudeLength

    diagonalLength = math.sqrt(longitudeLengthSquared + latitudeLengthSquared)
    diagonalLengthSquared = diagonalLength * diagonalLength

if __name__ == "__main__":
    main()
