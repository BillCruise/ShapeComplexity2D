# Find the centroid of a set of coordinates.
# http://en.wikipedia.org/wiki/Centroid#Centroid_of_polygon

def centroid(coords):
    # vertex (xn, yn) is assumed to be the same as (x0, y0)
    coords_cpy = list(coords)
    if(coords[0] != coords[-1]):
        coords_cpy.append(coords[0])
    
    x, y = 0, 1
    a_tot = 0
    cx_tot = 0
    cy_tot = 0

    n = len(coords_cpy)
    for i in range(n-1):
        diff = (coords_cpy[i][x] * coords_cpy[i+1][y] - coords_cpy[i+1][x] * coords_cpy[i][y])
        a_tot = a_tot + diff
        cx_tot = cx_tot + (coords_cpy[i][x] + coords_cpy[i+1][x]) * diff
        cy_tot = cy_tot + (coords_cpy[i][y] + coords_cpy[i+1][y]) * diff
        
    area = a_tot / 2
    cx = cx_tot / (6 * area)
    cy = cy_tot / (6 * area)
    return [cx, cy]
