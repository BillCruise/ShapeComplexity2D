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

keys = ['NC:12', 'CA:23', 'CA:11', 'CA:38', 'TX:22', 'IL:04', 'IL:17', 'TX:07', 'TX:20', 'TX:09', 'TX:26', 'TX:21', 'TX:15', 'CA:09', 'GA:08', 'CA:13', 'TX:19', 'TX:03', 'TX:11', 'GA:04', 'NY:08', 'CO:01', 'NY:15', 'GA:05', 'TX:25']

print
print 'Calculating complexity of primary district shapes...'
for key in keys:
    print count, 'of', total
    a = primary_land_masses[key][0]
    print key, 'Area:', a

    coordinates = primary_land_masses[key][1]
    print 'Coordinates:', len(coordinates)
    print 'First Coordinate:', coordinates[0]
    complexity = shape_complexity(coordinates)
    district_complexity[key] = complexity
    print 'Complexity:', complexity
    print
    count += 1
            


                
