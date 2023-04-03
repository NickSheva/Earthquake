import json
from plotly.graph_objs import Scattergeo, Layout
from plotly import offline
import pandas as pd
import numpy as np

filename = 'compPrint1.json'
with open(filename) as f:
    all_json_data = json.load(f)

readable_file = 'readable_json_data.json'
with open(readable_file, 'w') as f:
    json.dump(all_json_data, f, indent=4)
all_json_data = {}
df2 = pd.read_html("https://www.latlong.net/category/cities-235-15.html")[0].rename(
    columns={"Latitude": "Lat", "Longitude": "Lon"}
)
df2 = df2.rename(
    columns={"Place Name": "company", "Lat": "Latitude", "Lon": "Longitude"}
).assign(carbonprint=np.random.uniform(1, 4, len(df2)), location=df2["Place Name"])
all_json_data = df2.to_dict("records")

#  cfp = Carbon FootPrint
companies, cfp, locations, lats, longs = [], [], [], [], []
for json_data in all_json_data:
    company = json_data["company"]
    cp = json_data["carbonprint"]
    location = json_data["location"]
    lat = json_data["Latitude"]
    long = json_data["Longitude"]
    companies.append(company)
    cfp.append(cp)
    locations.append(location)
    lats.append(lat)
    longs.append(long)

companycfp = []
for json_data in all_json_data:
    comp = json_data["company"]
    fp = json_data["carbonprint"]
    stringfp = str(fp)
    compfp = f"{comp}, {stringfp} Million Metric Tons"
    companycfp.append(compfp)

data = [
    {
        "type": "scattergeo",
        "lon": longs,
        "lat": lats,
        "text": companycfp,
        "marker": {
            "size": [0.4 * cp for cp in cfp],
            "color": cfp,
            "colorscale": "fall",
        },
    }
]

my_layout = Layout(title="How you measure up: Companies")

fig = {"data": data, "layout": my_layout}

offline.plot(fig)
#go.Figure(fig)