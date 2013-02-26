# shape_complexity_2d.py
# Based on Estimating the Complexity of 2D Shapes
# by Yinpeng Chen and Hari Sundaram
# http://ame2.asu.edu/faculty/hs/pubs/ame-tr-2005-08.pdf
#
# This code is release under the Creative Commons Attribution-ShareAlike License.
# http://en.wikibooks.org/wiki/Wikibooks:Creative_Commons_Attribution-ShareAlike_3.0_Unported_License

import math
from rtree import index             # for the trace searching algorithm
from centroid import centroid
from convex_hull import *

alpha_1 = 0.6
alpha_2 = 0.07
alpha_3 = 0.33

# Incorporate Global Distance Factor, Local Angle Factor, Random Factor,
# and Perceptual Smoothness into one measure of shape complexity.
def shape_complexity(coords):
    gdf = global_distance_factor(coords)
    laf = local_angle_factor(coords)
    
    coords_copy = list(coords)
    coords_copy.pop()
    r = random_factor(coords_copy)
    
    p = perceptual_smoothness(coords)

    # print
    # print ' Global Distance Factor:', gdf
    # print ' Local Angle Factor:', laf
    # print ' Random Factor:', r
    # print ' Perceptual Smoothness:', p

    return (1 + r) * (alpha_1 * min(gdf, laf) + alpha_2 * max(gdf, laf) + alpha_3 * p)


# Global distance factor is a measure of the entropy of the distance
# between the points in a shape and its centroid.
def global_distance_factor(coords):
    center = centroid(coords)
    r = []

    n = len(coords)
    for i in range(n-1): # the last point in coords is a duplicate, so skip it
        r.append(distance(center, coords[i]))

    r_max = max(r)

    # normalize values in r to the interval 0 to 1
    for i in range(len(r)):
        r[i] = r[i] / r_max

    h_dist = [] # distance entropy
    e_dist = [] # quantization error
    
    j = 1
    while 2**j <= n*2:
        k = 2**j
        h = histogram(k, r, max(r))
        h_dist.append(entropy(h, n-1))
        e_dist.append(quantization_error(h, n-1))
        j += 1

    # Although Chen & Sundarum say there's a theoretical  
    # maximum constant quantization error, it isn't specified.
    # Use the calculated maximum instead.
    e_max = max_quant_error(r)
    log2n = math.log(n-1, 2)
    
    f_dist = [] # results of cost function

    for i in range(len(h_dist)):
        entropy_norm = h_dist[i] / log2n
        quant_err_norm = e_dist[i] / e_max
        f = entropy_norm + quant_err_norm
        f_dist.append(f)
        
    return min(f_dist)

# The quantization error is based on the sum of the squares of
# the differences between the r values and the quantization values.
# The maximum error is found when the quantization values are 0.
def max_quant_error(r):
    total = 0.0
    for x in r:
        total += x**2
    return math.sqrt(total / len(r))


# Local angle factor is a measure of the entropy 
# of the angles measured at each point in a shape.
def local_angle_factor(coords):
    local_angles = []
    n = len(coords)
    
    for i in range(n-1):
        xi = coords[i]
        xi_nn1 = coords[i-1] if i > 0 else coords[n-2]
        xi_nn2 = coords[i+1]
        loc_angle = local_angle(xi, xi_nn1, xi_nn2)
        local_angles.append(loc_angle)

    h_angle = [] # angle entropy
    e_angle = [] # quantization error

    j = 1
    while 2**j <= n*2:
        k = 2**j
        h = histogram(k, local_angles, math.pi)
        h_angle.append(entropy(h, n-1))
        e_angle.append(quantization_error(h, n-1))
        j += 1

    # e_max = 0.25 was specified by Chen & Sundaram,
    # but greater values were found empirically.
    e_max = max_quant_error(local_angles)
    log2n = math.log(n-1, 2)

    f_angle = [] # results of cost function

    for i in range(len(h_angle)):
        entropy_norm = h_angle[i] / log2n
        quant_err_norm = e_angle[i] / e_max
        f_angle.append(entropy_norm + quant_err_norm)
    return min(f_angle)


# Create a histogram with k bins from the values in r.
def histogram(k, r, mx):
    h = [ [] for i in range(k) ] # initialize list of k lists
    for x in r:
        i = int(math.floor((x / mx) * k))
        if i < k:
            h[i].append(x)
        else:
            h[k-1].append(x)
    return h


# Compute the entropy of a given histogram with n points.
def entropy(h, n):
    k = len(h)
    entropy = 0.0
    for i in range(k):
        pdf = len(h[i]) / float(n)
        if pdf > 0.0:
            entropy = entropy + (pdf * math.log(pdf, 2))
    return -entropy


# Computes the quantization value for the points in each bucket of a histogram,
# and the RMS of the differences between each point in the histogram and
# the quant value for the corresponding bucket.
def quantization_error(h, n):
    error = 0.0;
    for bucket in h:
        quant_value = (sum(bucket) / float(len(bucket))) if len(bucket) > 0 else 0.0
        for r in bucket:
            error = error + (r - quant_value)**2
    return math.sqrt(error / n)


# The random factor of a shape is the distance between two traces through the point set.
def random_factor(coords):
    # find the pair of points that are furthest apart
    diam = diameter(coords)

    # use each of the points found above as the starting point for a trace
    trace_a = trace_search(coords, diam[0])
    trace_b = trace_search(coords, diam[1])
    return trace_distance(trace_a, trace_b)


# Build a trace (spanning tree) of the coordinates starting at the specified point.
def trace_search(coords, start_point):
    # initialize a "matrix" to represent a spanning tree
    span_tree = [[] for i in range(len(coords))]
    
    # create a 2D index of non-passed points and populate it
    props = index.Property()
    props.dimension = 2
    idx_non_passed = index.Index(properties=props, interleaved=True)

    ident = 0
    for p in coords:
        idx_non_passed.insert(ident, (p[0], p[1]))
        ident += 1

    # create a list of passed points
    passed_indices = []

    # get the index of the starting point and its nearest neighbor
    nn_i = list(idx_non_passed.nearest((start_point[0], start_point[1]), 2))
    v_c_i = nn_i[1]
    v_c = coords[v_c_i]
    passed_indices.append(nn_i[0])
    passed_indices.append(v_c_i)

    # connect the start point to its nearest neighbor
    span_tree[nn_i[0]].append(v_c_i)
    span_tree[v_c_i].append(nn_i[0])

    # initialize the previous point to the start point
    v_prev = start_point

    # remove points from the non-passed index
    idx_non_passed.delete(nn_i[0], (v_prev[0], v_prev[1], v_prev[0], v_prev[1]))
    idx_non_passed.delete(nn_i[1], (v_c[0], v_c[1], v_c[0], v_c[1]))

    # everything is initialized. we can fill in the rest of the spanning tree now.
    for i in range(1, len(coords)-1):
        # Chen & Sundarum don't specify a value for delta, so we're
        # using the distance between the previous & current points
        delta = distance(v_prev, v_c)

        # find the nearest neighbor to the predicted next point, v_p
        v_p = next_point(v_prev, v_c)
        nn_i = list(idx_non_passed.nearest((v_p[0], v_p[1]), 1))
        v_nn1 = coords[nn_i[0]]

        if(distance(v_p, v_nn1) < delta):
            span_tree[nn_i[0]].append(v_c_i)
            span_tree[v_c_i].append(nn_i[0])
            idx_non_passed.delete(nn_i[0], (v_nn1[0], v_nn1[1], v_nn1[0], v_nn1[1]))
            v_prev = v_c
            v_c_i = nn_i[0]
            v_c = v_nn1
            passed_indices.append(v_c_i)
        else:
            # find the nearest neighbor to the current point
            nn_i = list(idx_non_passed.nearest((v_c[0], v_c[1]), 1))
            v_nn2 = coords[nn_i[0]]
            if(distance(v_c, v_nn2) < delta):
                span_tree[nn_i[0]].append(v_c_i)
                span_tree[v_c_i].append(nn_i[0])
                idx_non_passed.delete(nn_i[0], (v_nn2[0], v_nn2[1], v_nn2[0], v_nn2[1]))
                v_prev = v_c
                v_c_i = nn_i[0]
                v_c = v_nn2
                passed_indices.append(v_c_i)
            else:
                # Search for a passed point (v_st) with minimum distance between
                # itself and its nearest neighbor (v_nn3) from non-passed points.
                v_st = None
                v_st_i = 0
                v_nn3 = None
                v_nn3_i = 0
                min_dist = float("inf")

                for v_i in passed_indices:
                    v = coords[v_i]
                    nn_i = list(idx_non_passed.nearest((v[0], v[1]), 1))
                    v_nn3_i = nn_i[0]
                    v_nn3 = coords[v_nn3_i]
                    d = distance(v, v_nn3)
                    if(d < min_dist):
                        min_dist = d
                        v_st = v
                        v_st_i = v_i
                        
                # update the span tree
                span_tree[v_st_i].append(v_nn3_i)
                span_tree[v_nn3_i].append(v_st_i)
                idx_non_passed.delete(v_nn3_i, (v_nn3[0], v_nn3[1], v_nn3[0], v_nn3[1]))
                v_prev = v_st
                v_c_i = v_nn3_i
                v_c = v_nn3
                passed_indices.append(v_c_i)
    return span_tree


# calculate the distance between two traces (spanning trees).
def trace_distance(trace_a, trace_b):
    sum_of_diffs = 0
    for i in range(0, len(trace_a)):
        if not trace_a[i]:
            for val in trace_b[i]:
                sum_of_diffs += 1
        for val in trace_a[i]:
            if not val in trace_b[i]:
                sum_of_diffs += 1

    return sum_of_diffs / (4.0 * (len(trace_a) - 1))


# An aggregate measure of the perceptual smoothness of all angles in the shape.
# The smaller the value, the smoother the shape.
def perceptual_smoothness(coords):
    n = len(coords)
    total = 0.0
    for i in range(n-1):
        xi = coords[i]
        xi_nn1 = coords[i-1] if i > 0 else coords[n-2]
        xi_nn2 = coords[i+1]
        angle = local_angle(xi, xi_nn1, xi_nn2)
        smoothness = ((math.e**(-angle / math.pi)) - math.e**-1) / (1 - math.e**-1)
        total += smoothness
    return total / (n-1)


# find the straight-line distance between two (x, y) coordinates
def distance(p1, p2):
    return math.sqrt( (p2[0] - p1[0])**2 + (p2[1] - p1[1])**2 )


# predict the next point on a straight line given two starting points.
# points are assumed to the same distance apart.
def next_point(p1, p2):
    dx = p1[0] - p2[0]
    dy = p1[1] - p2[1]
    return [p2[0] - dx, p2[1] - dy]


# find the local angle at a point (p1) given it's two neighbors
# using the law of cosines.
# http://en.wikipedia.org/wiki/Law_of_cosines
def local_angle(p1, p2, p3):
    a = distance(p1, p2)
    b = distance(p1, p3)
    c = distance(p2, p3)
    num = (a**2 + b**2 - c**2)
    den = (2 * a * b)
    val = num / den
    
    # this coercion is here because of floating point imprecision
    val = min(1.0, max(val, -1.0))
    local_angle = math.acos(val)
    if local_angle > math.pi:
        local_angle = 2 * math.pi - local_angle
    return local_angle


