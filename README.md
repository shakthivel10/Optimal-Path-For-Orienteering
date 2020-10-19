
# Optimal-Path-For-Orienteering
A python application to programmatically model different seasons of a terrain map and to find and plot the optimal path for the sport of Orienteering.

The implementation involves creating a weighted graph from an image representing the 2D terrain map, and an elevation file representing the elevations of each pixel in the image file, where the edge weights represent the time required to travel from a node to it's neighbor, and using A* search with a time heuristic on the graph to find out optimal paths between every point and its successor.

##  Orienteering
Orienteering is a sport where an athlete has to navigate through a list of points (referred to as control points) in an unfamiliar terrain. It was originally developed as an exercise in land navigation for the military. Participants are given a topographical map which they use to locate and navigate through control points. --  en.wikipedia.org/wiki/Orienteering

A smarter participant who can figure out the best way to get from one control point to the next, may beat out a more athletic competitor who makes poor choices in terms of deciding the path to move from one point to another. Hence finding the optimal path to get from one point to another can turn the tables in favor of a participant with weaker athletic abilities.  

## Implementation

### Terrain
We are given a simplified color-only terrain map of Mendon Ponds Park, Honeoye Falls, NY   [Original-Terrain-Map](http://www.vmeyer.net/gadget/cgi-bin/reitti.cgi?act=map&id=209)

The above map represents the terrain during summer. The other seasons are modeled programmatically to generate terrain maps corresponding to the other seasons. 

### Modeling different seasons

 - Fall
 During fall, foot paths adjacent to easy movement forest (white pixels) are covered by leaves making it difficult to follow the foot path.
  - Winter
 In winter the lakes freeze, we assume that any water within seven pixels of non-water is safe to walk on.
 - Spring
We model early spring / mud season when dirt paths and roads become muddy from melting snow and rain. Any pixels within fifteen pixels of water that can be reached from a water pixel without gaining more than one meter of elevation (total) are now underwater. 
