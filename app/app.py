import os
import folium
from folium.plugins import HeatMap
import polars as pl
import json
from geopy.geocoders import Nominatim
from flask import Flask, render_template, request

# Create Flask app
app = Flask(__name__, template_folder='templates')

# Create templates directory if it doesn't exist
if not os.path.exists('templates'):
    os.makedirs('templates')

# New Jersey geographic boundaries (approximate)
NJ_SOUTH = 38.9  # Southern boundary latitude
NJ_NORTH = 41.4  # Northern boundary latitude
NJ_WEST = -75.6  # Western boundary longitude
NJ_EAST = -73.9  # Eastern boundary longitude

# NJ center point for initial map view
NJ_CENTER = [(NJ_NORTH + NJ_SOUTH) / 2, (NJ_EAST + NJ_WEST) / 2]

# Sample data locations (major cities in New Jersey)
NJ_CITIES = {}

freqdict = {}
reddit_df = pl.from_dict(json.load(open("../data/reddit_final_data.json", "r+")))
places = reddit_df["place"].to_list()
for place_names in places:
    place_names = place_names.split(",")
    for place in place_names:
        if place not in freqdict:
            freqdict[place] = 0
        freqdict[place] += 1

print(freqdict)

def get_coords_from_name(name):
    geolocator = Nominatim(user_agent="FRIGID_App")
    location = geolocator.geocode(name)
    if location:
        return [location.latitude, location.longitude]
    else:
        return [None, None]


def generate_intensity_data():
    data = []
    minfreq = min(freqdict.values())
    maxfreq = max(freqdict.values())
    for place, freq in freqdict.items():
        scaled = (freq - minfreq)/(maxfreq - minfreq)
        point = get_coords_from_name(place+", New Jersey")
        NJ_CITIES[place] = point
        data.append(point+[scaled])
    return data

def create_nj_map(radius=15):
    """Create a folium map with NJ data and heatmap"""
    # Generate map centered on New Jersey
    nj_map = folium.Map(location=NJ_CENTER, zoom_start=8, 
                      tiles='CartoDB positron')
    
    # Create state boundary
    folium.Rectangle(
        bounds=[(NJ_SOUTH, NJ_WEST), (NJ_NORTH, NJ_EAST)],
        color='blue',
        fill=False,
        weight=2
    ).add_to(nj_map)
    
    # Generate heatmap data
    heat_data = generate_intensity_data()
    
    # Add city markers
    for city, coords in NJ_CITIES.items():
        folium.CircleMarker(
            location=coords,
            radius=4,
            color='red',
            fill=True,
            fill_color='red',
            fill_opacity=0.7,
            popup=f"# of Reports={freqdict[city]}",
            tooltip=f"{city}\n# of Reports={freqdict[city]}"
        ).add_to(nj_map)
    
    # Add heatmap layer
    HeatMap(
        heat_data,
        radius=radius,
        blur=15,
        gradient={"0.4": 'blue', "0.65": 'lime', "0.9": 'orange', "1.0": 'red'}
    ).add_to(nj_map)
    
    return nj_map

# Generate map once at startup
nj_map = create_nj_map(15)
nj_map.get_root().width = "800px"
nj_map.get_root().height = "600px"
iframe = nj_map.get_root()._repr_html_()

@app.route('/')
def map_page():
    try:
        return render_template(
            'map.html',
            iframe=iframe,
            title="Map",
            active_page="map"
        )
    except Exception as e:
        return render_template(
            'error.html',
            error=str(e)
        )

@app.route('/about')
def about_page():
    return render_template(
        'about.html',
        title="About",
        active_page="about"
    )

@app.route('/data')
def data_page():
    try:
        # Convert Polars DataFrame to dict for rendering
        data_dict = reddit_df.to_dicts()
        columns = reddit_df.columns
        
        # Get some basic stats about the data
        total_reports = len(reddit_df)
        unique_places = len(freqdict)
        
        # Most reported places (top 5)
        top_places = sorted(freqdict.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return render_template(
            'data.html',
            title="Data",
            active_page="data",
            data=data_dict,
            columns=columns,
            total_reports=total_reports,
            unique_places=unique_places,
            top_places=top_places
        )
    except Exception as e:
        return render_template(
            'error.html',
            title="Data Error",
            active_page="data",
            error=str(e)
        )

@app.route('/rights')
def rights_page():
    return render_template(
        'rights.html',
        title="Know Your Rights",
        active_page="rights"
    )

if __name__ == '__main__':
    app.run(debug=True)