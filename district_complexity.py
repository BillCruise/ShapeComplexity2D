# Congressional Districts of the United States - 112th Congress
# Data downloaded from http://www.nationalatlas.gov/atlasftp.html#cgd112p

import json
from shape_complexity_2d.shape_complexity_2d import *
from shape_complexity_2d.centroid import area

print('Opening data file...')
json_data = open('data/cgd112p020-AK00.json')

print('Loading Congressional Districts data...')
data = json.load(json_data)

json_data.close()

dtype = data['type']
features = data['features']

print('Data Type:', dtype)

f_count = len(features)
print('Features:', f_count)

# create an empty dictionary where the key is 'state+district'
# and the value is the shape for that district with the
# maximum area.
primary_land_masses = {}

# create an empty dictionary where the key is 'state+district'
# and the value is the district complexity.
district_complexity = {}

count = 1

for feature in features:
    properties = feature['properties']
    state = properties['STATE']
    cong_district = properties['CONG_DIST']

    print 'Count:', count, 'of', f_count
    count += 1
    print state, 'District:', cong_district
    
    geometry = feature['geometry']
    coordinates = geometry['coordinates'][0]
    print 'Coordinates:', len(coordinates)

    # complexity = shape_complexity(coordinates)
    # print 'Complexity:', complexity
    
    a = area(coordinates)
    print 'Area:', a
    
    print

    if state != None and cong_district != None:
        if (state + ':' + cong_district) in primary_land_masses:
            if primary_land_masses[state + ':' + cong_district][0] < a:
                primary_land_masses[state + ':' + cong_district] = [a, coordinates]
        else:
            # add the [area, coordinates] for the new district
            primary_land_masses[state + ':' + cong_district] = [a, coordinates]

count = 1
total = len(primary_land_masses)

print
print 'Calculating complexity of primary district shapes...'
for key, value in primary_land_masses.iteritems():
    print count, 'of', total
    print key, value[0]
    print 'First Coordinate:', value[1][0]
    complexity = shape_complexity(value[1])
    district_complexity[key] = complexity
    print 'Complexity:', complexity
    print
    count += 1
            

    #if state != None and cong_district != None:
    #    if (state + ':' + cong_district) in district_complexity:
    #        if district_complexity[state + ':' + cong_district] < complexity:
    #            district_complexity[state + ':' + cong_district] = complexity
    #    else:
    #        # add the coordinates for the new district
    #        district_complexity[state + ':' + cong_district] = complexity

print
sorted_districts = sorted(district_complexity, key=district_complexity.get)

for district in sorted_districts:
    print district, district_complexity[district]

                
