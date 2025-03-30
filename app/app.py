import os
import folium
from folium.plugins import HeatMap
from dotenv import load_dotenv
import polars as pl
import json
from geopy.geocoders import Nominatim
from flask import Flask, render_template, request, redirect, url_for, flash
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()

# Create Flask app
app = Flask(__name__, template_folder='templates')
app.secret_key = os.urandom(24)  # Needed for flash messages

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
ero_df = pl.read_csv("../data/ERO_Twitter.csv", has_header=True)
places = reddit_df["place"].to_list() + ero_df["Location"].to_list()
for place_names in places:
    place_names = place_names.split(",")
    for place in place_names:
        if place not in freqdict:
            freqdict[place] = 0
        freqdict[place] += 1

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
            popup=f"{city}\n# of Reports={freqdict[city]}",
            tooltip=f"{city}"
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

# Function to send email with report details
def send_report_email(report_data):
    try:
        # Configure email details
        sender_email = os.getenv("GMAIL")  # Your Gmail address
        sender_password = os.getenv("GMAIL_PSWD")  # App password, not your regular password
        receiver_email = os.getenv("PROTONMAIL") # Your ProtonMail address
        
        # Gmail SMTP server settings
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        
        # Create message
        message = MIMEMultipart()
        message["From"] = sender_email
        message["To"] = receiver_email
        message["Subject"] = f"ICE Activity Report: {report_data['location']}"
        
        # Email body
        body = f"""
        New ICE Activity Report:
        
        Location: {report_data['location']}
        Date: {report_data['date']}
        Time: {report_data['time']}
        
        Activity Description:
        {report_data['description']}
        
        Contact Information (if provided):
        Name: {report_data.get('contact_name', 'Not provided')}
        Email: {report_data.get('contact_email', 'Not provided')}
        Phone: {report_data.get('contact_phone', 'Not provided')}
        
        Additional Notes:
        {report_data.get('additional_info', 'None')}
        """
        
        message.attach(MIMEText(body, "plain"))
        
        # Connect to Gmail's SMTP server and send email
        try:
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.ehlo()
                server.starttls()
                server.ehlo()
                server.login(user=sender_email, password=sender_password)
                server.send_message(message)
                print("Email sent successfully!")
                return True
        except Exception as e:
            print(f"SMTP Error: {str(e)}")
            return False
            
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False

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
        reddit_dict = reddit_df.select(["title", "url", "place", "when"]).to_dicts()
        reddit_columns = reddit_df.select(["title", "url", "place", "when"]).columns
        
        ero_dict = ero_df.to_dicts()
        ero_columns = ero_df.columns
        
        # Get some basic stats about the data
        total_reports = len(reddit_df) + len(ero_df)
        unique_places = len(freqdict)
        
        # Most reported places (top 5)
        top_places = sorted(freqdict.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return render_template(
            'data.html',
            title="Data",
            active_page="data",
            reddit_data=reddit_dict,
            reddit_columns=reddit_columns,
            total_reports=total_reports,
            unique_places=unique_places,
            top_places=top_places,
            ero_data = ero_dict,
            ero_columns = ero_columns
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

@app.route('/report', methods=['GET', 'POST'])
def report_page():
    if request.method == 'POST':
        try:
            # Collect form data
            report_data = {
                'location': request.form.get('location', ''),
                'date': request.form.get('date', ''),
                'time': request.form.get('time', ''),
                'description': request.form.get('description', ''),
                'contact_name': request.form.get('contact_name', ''),
                'contact_email': request.form.get('contact_email', ''),
                'contact_phone': request.form.get('contact_phone', ''),
                'additional_info': request.form.get('additional_info', '')
            }
            
            # Validate required fields
            if not report_data['location'] or not report_data['date'] or not report_data['description']:
                flash('Please fill in all required fields.', 'error')
                return redirect(url_for('report_page'))
            
            # Send the report via email
            if send_report_email(report_data):
                flash('Your report has been submitted successfully. Thank you for contributing.', 'success')
                
                # Add to the frequency dictionary if it's a New Jersey location
                location = report_data['location'].strip()
                if location:
                    if location not in freqdict:
                        freqdict[location] = 0
                    freqdict[location] += 1
                
                return redirect(url_for('map_page'))
            else:
                flash('There was an error submitting your report. Please try again later.', 'error')
                return redirect(url_for('report_page'))
                
        except Exception as e:
            flash(f'An error occurred: {str(e)}', 'error')
            return redirect(url_for('report_page'))
    
    # For GET requests, just render the form
    return render_template(
        'report.html',
        title="Submit ICE Activity Report",
        active_page="report"
    )

if __name__ == '__main__':
    app.run(debug=True)