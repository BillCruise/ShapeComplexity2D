# Congressional Districts of the United States - 112th Congress
# Data downloaded from http://www.nationalatlas.gov/atlasftp.html#cgd112p

import json
from shape_complexity_2d.shape_complexity_2d import *

print('Opening data file...')
json_data = open('data/cgd112p020.json')

print('Loading Congressional Districts data...')
data = json.load(json_data)

json_data.close()

dtype = data['type']
features = data['features']

print('Data Type:', dtype)

f_count = len(features)
print('Features:', f_count)



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

    complexity = shape_complexity(coordinates)

    print 'Complexity:', complexity
    print

    if state != None and cong_district != None:
        if (state + ':' + cong_district) in district_complexity:
            if district_complexity[state + ':' + cong_district] < complexity:
                district_complexity[state + ':' + cong_district] = complexity
        else:
            # add the coordinates for the new district
            district_complexity[state + ':' + cong_district] = complexity

sorted_districts = sorted(district_complexity, key=district_complexity.get)

for district in sorted_districts:
    print district, district_complexity[district]

                
