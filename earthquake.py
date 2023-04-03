''' построение карты с последними землятресениями  в мире'''
import json
from plotly.graph_objs import Scattergeo, Layout
from plotly import offline


filename = 'data/eq.json'
with open(filename, encoding='utf-8') as f:
    eq_map = json.load(f)
# загрузка читамего файла
#new_file = 'data/get_eq.json'
#with open(new_file, 'w', encoding='utf-8') as f:
#    json.dump(eq_map, f, indent=8)

eq_dicts = eq_map['features']
mags, lons, lats, hover_text = [], [], [], []
for eq in eq_dicts:
    mags.append(eq["properties"]['mag'])
    lons.append(eq["geometry"]["coordinates"][0])
    lats.append(eq["geometry"]["coordinates"][1])
    hover_text.append(eq['properties']['title'])

data = [{'type': 'scattergeo', 'lon': lons, 'lat': lats, 'text': hover_text,
         'marker': {
             'size': [5* mag for mag in mags],
             'color' : mags,
             'colorscale': 'Viridis',
             'reversescale': True,
             'colorbar': {'title': 'Magnitude'},
         }

         }]

my_layout = Layout(title='EARTHQUAKE MAP')
figers = {'data': data, 'layout': my_layout}
offline.plot(figers, filename='eq.html')
