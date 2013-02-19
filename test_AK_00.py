# The main land mass of Alaska is defined by over 70,000 coordinates.
# This is by far the largest polygon in the congressional districts file,
# so it makes a good test case for MemoryErrors.

import json
from shape_complexity_2d.shape_complexity_2d import *

def main():
    print 'Opening data file...'
    json_data = open('data/AK_00.txt')

    print 'Loading Texas 14th Congressional District data...'
    data = json.load(json_data)

    json_data.close()

    dtype = data['type']
    properties = data['properties']
    geometry = data['geometry']
    coords = geometry['coordinates'][0]

    print 'Data Type:', dtype
    print 'Properties:', len(properties)
    print 'Geometry:', len(geometry)
    print 'Coords:', len(coords)

    complexity = shape_complexity(coords)

    print 'Complexity:', complexity
        

if __name__ == "__main__":
    main()
