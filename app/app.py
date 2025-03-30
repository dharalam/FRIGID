import os
import folium
from folium.plugins import HeatMap
import polars as pl
import json
from geopy.geocoders import Nominatim
from flask import Flask, render_template, render_template_string, request

app = Flask(__name__)

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
    
    # Add heatmap layer - Fix: Use string keys in the gradient dictionary instead of floats
    HeatMap(
        heat_data,
        radius=radius,
        blur=15,
        gradient={"0.4": 'blue', "0.65": 'lime', "0.9": 'orange', "1.0": 'red'}
    ).add_to(nj_map)
    
    return nj_map

nj_map = create_nj_map(15)
nj_map.get_root().width = "800px"
nj_map.get_root().height = "600px"
iframe = nj_map.get_root()._repr_html_()

# Base template with navbar for all pages
BASE_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>{{ title }} - FRIGID</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.0/css/bootstrap.min.css">
    <style>
        :root {
            --primary-color: #2c3e50;
            --secondary-color: #3498db;
            --accent-color: #e74c3c;
            --light-color: #ecf0f1;
            --dark-color: #2c3e50;
        }
        
        body {
            font-family: 'Roboto', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f8f9fa;
            padding: 0;
            margin: 0;
        }
        
        .navbar {
            background-color: var(--primary-color);
            padding: 1rem 2rem;
            box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
        }

        .navbar-brand {
            color: white;
            font-weight: 700;
            font-size: 1.5rem;
            text-decoration: none;
        }

        .navbar-brand:hover {
            color: var(--light-color);
        }

        .navbar .container {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .navbar-nav {
            display: flex;
            flex-direction: row; /* Ensures horizontal layout */
            list-style: none;
            margin: 0;
            padding: 0;
        }

        .nav-item {
            margin-left: 1.5rem;
            display: inline-block; /* Additional enforcement of horizontal layout */
        }

        .nav-link {
            color: white;
            font-weight: 500;
            text-decoration: none;
            padding: 0.5rem 0;
            position: relative;
            transition: color 0.3s ease;
        }

        .nav-link:hover {
            color: var(--secondary-color);
        }

        .nav-link.active {
            color: var(--secondary-color);
        }

        .nav-link.active::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            width: 100%;
            height: 3px;
            background-color: var(--secondary-color);
        }

        /* Responsive Navigation - Add hamburger menu for mobile */
        @media (max-width: 768px) {
            .navbar .container {
                flex-wrap: wrap;
            }
            
            .navbar-nav {
                margin-top: 1rem;
                width: 100%;
                justify-content: space-between;
            }
            
            .nav-item {
                margin-left: 0;
            }
        }
        
        .header {
            background-color: var(--light-color);
            padding: 2rem 0;
            text-align: center;
            margin-bottom: 2rem;
        }
        
        .header h1 {
            margin: 0;
            color: var(--primary-color);
            font-size: 2.5rem;
            font-weight: 700;
        }
        
        .header p {
            margin-top: 0.5rem;
            color: var(--dark-color);
            font-size: 1.2rem;
        }
        
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }
        
        .map-container {
            margin: 20px auto;
            border: 1px solid #ddd;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
            display: flex;
            justify-content: center;
            max-width: 800px;
        }
        
        /* Data Table Styles */
        .data-container {
            margin-top: 20px;
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
            padding: 1rem;
        }
        
        .table-container {
            max-height: 600px;
            overflow-y: auto;
            margin-top: 1rem;
        }
        
        .table {
            width: 100%;
            border-collapse: collapse;
        }
        
        .table th {
            position: sticky;
            top: 0;
            background-color: var(--primary-color);
            color: white;
            padding: 1rem;
            text-align: left;
        }
        
        .table tr:nth-child(even) {
            background-color: #f2f2f2;
        }
        
        .table td {
            padding: 0.75rem 1rem;
            border-bottom: 1px solid #ddd;
        }
        
        .data-stats {
            background-color: var(--light-color);
            padding: 1rem;
            border-radius: 8px;
            margin-bottom: 1rem;
        }
        
        .data-stats h3 {
            margin-top: 0;
            color: var(--primary-color);
        }
        
        /* Content Container Styles */
        .content-container {
            margin: 20px auto;
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
            padding: 2rem;
            max-width: 900px;
        }
        
        .content-container h2 {
            color: var(--primary-color);
            margin-bottom: 1.5rem;
            border-bottom: 2px solid var(--light-color);
            padding-bottom: 0.8rem;
        }
        
        .content-container h3 {
            color: var(--secondary-color);
            margin-top: 1.8rem;
            margin-bottom: 1rem;
        }
        
        .content-container p {
            margin-bottom: 1.2rem;
            line-height: 1.8;
        }
        
        .content-container ul, .content-container ol {
            margin-bottom: 1.5rem;
            padding-left: 1.5rem;
        }
        
        .content-container li {
            margin-bottom: 0.5rem;
            line-height: 1.7;
        }
        
        .card {
            margin-bottom: 1.5rem;
            border: none;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
            transition: transform 0.3s, box-shadow 0.3s;
        }
        
        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
        }
        
        .card-header {
            background-color: var(--primary-color);
            color: white;
            border-radius: 8px 8px 0 0 !important;
            padding: 1rem 1.5rem;
            font-weight: 600;
        }
        
        .card-body {
            padding: 1.5rem;
        }
        
        .contact-info {
            background-color: var(--light-color);
            padding: 1.5rem;
            border-radius: 8px;
            margin-top: 2rem;
        }
        
        .team-member {
            display: flex;
            align-items: center;
            margin-bottom: 1.5rem;
        }
        
        .team-member-img {
            width: 80px;
            height: 80px;
            border-radius: 50%;
            margin-right: 1.5rem;
            object-fit: cover;
            background-color: var(--light-color);
        }
        
        .alert {
            border-radius: 8px;
            margin-bottom: 1.5rem;
            padding: 1.2rem 1.5rem;
        }
        
        .alert-warning {
            background-color: #fff3cd;
            color: #856404;
            border-left: 4px solid #ffeeba;
        }
        
        .alert-info {
            background-color: #d1ecf1;
            color: #0c5460;
            border-left: 4px solid #bee5eb;
        }
        
        .alert-danger {
            background-color: #f8d7da;
            color: #721c24;
            border-left: 4px solid #f5c6cb;
        }
        
        /* Responsive Navigation */
        @media (max-width: 768px) {
            .navbar {
                padding: 1rem;
            }
            
            .navbar-brand {
                font-size: 1.2rem;
            }
            
            .nav-item {
                margin-left: 1rem;
            }
            
            .header h1 {
                font-size: 2rem;
            }
            
            .header p {
                font-size: 1rem;
            }
            
            .table-container {
                max-height: 400px;
            }
            
            .table th, .table td {
                padding: 0.5rem;
            }
            
            .content-container {
                padding: 1.5rem;
            }
        }
    </style>
    {% block additional_styles %}{% endblock %}
</head>
<body>
    <nav class="navbar">
        <div class="container">
            <a href="/" class="navbar-brand">FRIGID</a>
            <ul class="navbar-nav">
                <li class="nav-item">
                    <a href="/" class="nav-link {% if active_page == 'map' %}active{% endif %}">Map</a>
                </li>
                <li class="nav-item">
                    <a href="/about" class="nav-link {% if active_page == 'about' %}active{% endif %}">About</a>
                </li>
                <li class="nav-item">
                    <a href="/data" class="nav-link {% if active_page == 'data' %}active{% endif %}">Data</a>
                </li>
                <li class="nav-item">
                    <a href="/rights" class="nav-link {% if active_page == 'rights' %}active{% endif %}">Know Your Rights</a>
                </li>
            </ul>
        </div>
    </nav>
    
    <header class="header">
        <div class="container">
            <h1>FRIGID</h1>
            <p>Fetching Reliable Instances of General ICE Detainments</p>
        </div>
    </header>
    
    <script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.0/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

@app.route('/')
def map_page():
    try:
        return render_template_string(
            BASE_TEMPLATE + 
            """
            {% block content %}
            <div class="map-container">
                {{ iframe|safe }}
            </div>
            {% endblock %}
            """,
            iframe=iframe,
            title="Map",
            active_page="map"
        )
    except Exception as e:
        # Add error handling
        return render_template_string(
            """
            <!DOCTYPE html>
            <html>
            <head>
                <title>Error - FRIGID</title>
                <meta charset="utf-8">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.0/css/bootstrap.min.css">
                <style>
                    :root {
                        --primary-color: #2c3e50;
                        --secondary-color: #3498db;
                        --accent-color: #e74c3c;
                        --light-color: #ecf0f1;
                        --dark-color: #2c3e50;
                    }
                    
                    body {
                        font-family: 'Roboto', Arial, sans-serif;
                        line-height: 1.6;
                        color: #333;
                        background-color: #f8f9fa;
                        padding: 0;
                        margin: 0;
                    }
                    
                    .navbar {
                        background-color: var(--primary-color);
                        padding: 1rem 2rem;
                        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
                    }
                    
                    .navbar-brand {
                        color: white;
                        font-weight: 700;
                        font-size: 1.5rem;
                        text-decoration: none;
                    }
                    
                    .navbar-nav {
                        display: flex;
                        list-style: none;
                        margin: 0;
                        padding: 0;
                    }
                    
                    .nav-item {
                        margin-left: 1.5rem;
                    }
                    
                    .nav-link {
                        color: white;
                        font-weight: 500;
                        text-decoration: none;
                        padding: 0.5rem 0;
                    }
                    
                    .error-container {
                        max-width: 800px;
                        margin: 4rem auto;
                        text-align: center;
                        padding: 2rem;
                        background-color: white;
                        border-radius: 8px;
                        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
                    }
                    
                    .alert-heading {
                        color: var(--accent-color);
                    }
                    
                    .btn-back {
                        background-color: var(--secondary-color);
                        border: none;
                        margin-top: 1rem;
                        padding: 0.5rem 1.5rem;
                    }
                    
                    .btn-back:hover {
                        background-color: #2980b9;
                    }
                </style>
            </head>
            <body>
                <nav class="navbar">
                    <div class="container">
                        <a href="/" class="navbar-brand">FRIGID</a>
                        <ul class="navbar-nav">
                            <li class="nav-item">
                                <a href="/" class="nav-link">Map</a>
                            </li>
                            <li class="nav-item">
                                <a href="/about" class="nav-link">About</a>
                            </li>
                            <li class="nav-item">
                                <a href="/data" class="nav-link">Data</a>
                            </li>
                            <li class="nav-item">
                                <a href="/rights" class="nav-link">Know Your Rights</a>
                            </li>
                        </ul>
                    </div>
                </nav>
                
                <div class="error-container">
                    <div class="alert alert-danger">
                        <h4 class="alert-heading">Error Generating Map</h4>
                        <p>{{ error }}</p>
                    </div>
                    <a href="/" class="btn btn-primary btn-back">Back to Home</a>
                </div>
                
                <script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.3.0/js/bootstrap.bundle.min.js"></script>
            </body>
            </html>
            """,
            error=str(e)
        )

@app.route('/about')
def about_page():
    return render_template_string(
        BASE_TEMPLATE + 
        """
        {% block content %}
        <div class="content-container">
            <h2>About FRIGID</h2>
            
            <p>FRIGID (Fetching Reliable Instances of General ICE Detainments) is a community-driven platform designed to track and visualize ICE (Immigration and Customs Enforcement) activity across New Jersey. Our mission is to provide transparent, accessible information about ICE operations to help keep communities informed.</p>
            
            <div class="alert alert-info">
                <strong>Note:</strong> This platform relies on community-reported data and should be used as an informational resource rather than definitive legal guidance.
            </div>
            
            <h3>Our Mission</h3>
            <p>We believe that accessible information is a cornerstone of community safety. FRIGID aims to:</p>
            <ul>
                <li>Collect and visualize reports of ICE activity in New Jersey</li>
                <li>Provide educational resources about immigration rights</li>
                <li>Create transparency around enforcement patterns</li>
                <li>Empower communities with knowledge to make informed decisions</li>
            </ul>
            
            <h3>How It Works</h3>
            <p>FRIGID collects data from various sources including social media reports, community organizations, and first-hand accounts. This data is verified to the best of our ability, aggregated, and displayed on an interactive map to show patterns of ICE activity.</p>
            
            <div class="row">
                <div class="col-md-4">
                    <div class="card">
                        <div class="card-header">Data Collection</div>
                        <div class="card-body">
                            <p>We gather information from Reddit and other social media platforms, filtering for reports of ICE activity in New Jersey.</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card">
                        <div class="card-header">Verification</div>
                        <div class="card-body">
                            <p>Reports are cross-referenced when possible with multiple sources to ensure accuracy.</p>
                        </div>
                    </div>
                </div>
                <div class="col-md-4">
                    <div class="card">
                        <div class="card-header">Visualization</div>
                        <div class="card-body">
                            <p>Data is plotted on interactive maps showing trends and hotspots of activity.</p>
                        </div>
                    </div>
                </div>
            </div>
            
            <h3>Data Privacy</h3>
            <p>We take privacy seriously. All personal identifying information is removed from reports before they are added to our database. We focus only on location data and the nature of enforcement actions.</p>
            
            <h3>Disclaimer</h3>
            <p>The information provided by FRIGID is for educational and informational purposes only. It is not intended to be and should not be interpreted as legal advice. For specific legal guidance regarding immigration matters, please consult with a qualified immigration attorney.</p>
            
            <div class="contact-info">
                <h3>Contact Us</h3>
                <p>If you have questions, concerns, or would like to report ICE activity, please reach out:</p>
                <p><strong>Email:</strong> contact@frigidnj.org</p>
                <p><strong>Community Hotline:</strong> (555) 123-4567</p>
            </div>
        </div>
        {% endblock %}
        """,
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
        
        return render_template_string(
            BASE_TEMPLATE + 
            """
            {% block content %}
            <div class="data-container">
                <h2>Reddit Data Analysis</h2>
                
                <div class="data-stats">
                    <h3>Data Summary</h3>
                    <div class="row">
                        <div class="col-md-4">
                            <p><strong>Total Reports:</strong> {{ total_reports }}</p>
                        </div>
                        <div class="col-md-4">
                            <p><strong>Unique Places:</strong> {{ unique_places }}</p>
                        </div>
                        <div class="col-md-4">
                            <p><strong>Data Source:</strong> Reddit</p>
                        </div>
                    </div>
                    
                    <h4>Most Reported Places</h4>
                    <div class="row">
                        {% for place, count in top_places %}
                        <div class="col-md-4 mb-2">
                            <div class="card">
                                <div class="card-body">
                                    <h5 class="card-title">{{ place }}</h5>
                                    <p class="card-text">{{ count }} reports</p>
                                </div>
                            </div>
                        </div>
                        {% endfor %}
                    </div>
                </div>
                
                <h3>Raw Data</h3>
                <div class="table-container">
                    <table class="table">
                        <thead>
                            <tr>
                                {% for col in columns %}
                                <th>{{ col }}</th>
                                {% endfor %}
                            </tr>
                        </thead>
                        <tbody>
                            {% for row in data %}
                            <tr>
                                {% for col in columns %}
                                <td>{{ row[col] }}</td>
                                {% endfor %}
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>
            {% endblock %}
            
            {% block additional_scripts %}
            <script>
                // Add any data-specific JavaScript here
                document.addEventListener('DOMContentLoaded', function() {
                    console.log('Data page loaded');
                });
            </script>
            {% endblock %}
            """,
            title="Data",
            active_page="data",
            data=data_dict,
            columns=columns,
            total_reports=total_reports,
            unique_places=unique_places,
            top_places=top_places
        )
    except Exception as e:
        return render_template_string(
            BASE_TEMPLATE + 
            """
            {% block content %}
            <div class="alert alert-danger">
                <h4 class="alert-heading">Error Loading Data</h4>
                <p>{{ error }}</p>
            </div>
            {% endblock %}
            """,
            title="Data Error",
            active_page="data",
            error=str(e)
        )

@app.route('/rights')
def rights_page():
    return render_template_string(
        BASE_TEMPLATE + 
        """
        {% block content %}
        <div class="content-container">
            <h2>Know Your Rights</h2>
            
            <div class="alert alert-warning">
                <strong>Disclaimer:</strong> The information provided here is for educational purposes only and does not constitute legal advice. Please consult with an immigration attorney for guidance specific to your situation.
            </div>
            
            <p>Understanding your rights during encounters with Immigration and Customs Enforcement (ICE) officers is crucial. Everyone in the United States, regardless of immigration status, has certain constitutional rights. Here's what you should know:</p>
            
            <div class="card mb-4">
                <div class="card-header">
                    Your Rights at Home
                </div>
                <div class="card-body">
                    <ul>
                        <li><strong>You don't have to open your door.</strong> ICE officers cannot enter your home without a valid search warrant signed by a judge or your consent.</li>
                        <li><strong>Ask to see a warrant.</strong> If officers claim to have a warrant, ask them to slide it under the door or hold it up to a window so you can inspect it before opening the door.</li>
                        <li><strong>Check if the warrant is signed by a judge.</strong> Only a judicial warrant (signed by a judge) gives ICE the legal authority to enter your home without permission.</li>
                        <li><strong>Remain silent.</strong> You have the right to remain silent and do not have to answer questions about your immigration status, birthplace, or how you entered the U.S.</li>
                    </ul>
                </div>
            </div>
            
            <div class="card mb-4">
                <div class="card-header">
                    Your Rights in Public Places
                </div>
                <div class="card-body">
                    <ul>
                        <li><strong>You have the right to remain silent.</strong> You can tell the officer you want to remain silent.</li>
                        <li><strong>You can refuse a search.</strong> If you're stopped in public, officers cannot search you or your belongings without your consent or probable cause.</li>
                        <li><strong>You can ask if you're free to go.</strong> If the officer says yes, calmly walk away.</li>
                        <li><strong>You have the right to speak to a lawyer.</strong> If detained, say that you wish to speak to an attorney.</li>
                    </ul>
                </div>
            </div>
            
            <div class="card mb-4">
                <div class="card-header">
                    Your Rights if Detained
                </div>
                <div class="card-body">
                    <ul>
                        <li><strong>You have the right to speak to an attorney.</strong> You can ask for a list of free or low-cost legal services.</li>
                        <li><strong>You have the right to contact your consulate.</strong> Foreign nationals detained in the U.S. have the right to call their consulate or have law enforcement inform the consulate of their arrest.</li>
                        <li><strong>You have the right to refuse to sign anything.</strong> Don't sign any documents without speaking to an attorney, especially if you don't understand what they say.</li>
                        <li><strong>You have the right to a hearing.</strong> If you believe you have the right to stay in the U.S., you can request a hearing before an immigration judge.</li>
                    </ul>
                </div>
            </div>
            
            <h3>What to Do During an ICE Encounter</h3>
            <ol>
                <li><strong>Stay calm and do not run.</strong> This can be used against you and may lead to arrest.</li>
                <li><strong>Document the encounter.</strong> If possible, note officers' names, badge numbers, and what occurred.</li>
                <li><strong>Report the incident.</strong> Contact local immigrant rights organizations to report ICE activity.</li>
            </ol>
            <h3>Prepare in Advance</h3>
            <p>Being prepared can help protect you and your loved ones:</p>
            <ul>
                <li><strong>Create a safety plan.</strong> Decide who will take care of your children, pets, or property if you are detained.</li>
                <li><strong>Memorize important phone numbers.</strong> Know the numbers of family members, friends, and immigration attorneys.</li>
                <li><strong>Keep important documents in a safe place.</strong> Store copies of birth certificates, immigration documents, and other important papers where a trusted person can access them.</li>
                <li><strong>Carry the phone number of an immigration attorney.</strong> Have this information readily available if you need legal assistance.</li>
            </ul>
            
            <h3>Resources for Legal Assistance</h3>
            <div class="row">
                <div class="col-md-6">
                    <div class="card">
                        <div class="card-header">
                            Legal Aid Organizations in New Jersey
                        </div>
                        <div class="card-body">
                            <ul>
                                <li>American Friends Service Committee: (973) 643-1924</li>
                                <li>Legal Services of New Jersey: (888) 576-5529</li>
                                <li>Catholic Charities Immigration Legal Services: (973) 733-3516</li>
                                <li>American Civil Liberties Union of NJ: (973) 642-2084</li>
                            </ul>
                        </div>
                    </div>
                </div>
                <div class="col-md-6">
                    <div class="card">
                        <div class="card-header">
                            Know Your Rights Materials
                        </div>
                        <div class="card-body">
                            <ul>
                                <li><a href="#">Printable Know Your Rights Card (English)</a></li>
                                <li><a href="#">Tarjeta de Derechos (Español)</a></li>
                                <li><a href="#">Family Preparedness Plan Template</a></li>
                                <li><a href="#">Immigrant Defense Project Resources</a></li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
            
            <h3>Emergency Contacts</h3>
            <div class="card">
                <div class="card-body">
                    <div class="row">
                        <div class="col-md-6">
                            <p><strong>ICE Detention Reporting Hotline:</strong> (888) XXX-XXXX</p>
                            <p><strong>NJ Immigrant Rights Coalition:</strong> (800) XXX-XXXX</p>
                        </div>
                        <div class="col-md-6">
                            <p><strong>Rapid Response Network:</strong> (555) XXX-XXXX</p>
                            <p><strong>United We Dream Hotline:</strong> (844) 363-1423</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        {% endblock %}
        """
        )

# Create templates directory if it doesn't exist
if not os.path.exists('../app/templates'):
    os.makedirs('../app/templates')

if __name__ == '__main__':
    app.run(debug=True)