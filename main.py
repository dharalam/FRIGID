import os
import folium
from folium.plugins import HeatMap
from dotenv import load_dotenv
import polars as pl
import json
from geopy.geocoders import Nominatim
import fasthtml.common as fh
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import app.ft_base as ft_base, app.ft_about as ft_about, app.ft_data as ft_data, app.ft_error as ft_error, app.ft_map as ft_map, app.ft_report as ft_report, app.ft_rights as ft_rights

load_dotenv()

# Create Flask app

app, rt = fh.fast_app()

messages = []

dark_mode = False

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
reddit_df = pl.from_dict(json.load(open("./data/reddit_final_data.json", "r")))
ero_df = pl.read_csv("./data/ERO_Twitter.csv", has_header=True)
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

def create_nj_map(radius=15, dark_mode=False):
    """Create a folium map with NJ data and heatmap"""
    # Generate map centered on New Jersey
    # Use a dark tiles option if in dark mode
    if dark_mode:
        tiles = 'CartoDB dark_matter'
    else:
        tiles = 'CartoDB positron'
    
    nj_map = folium.Map(location=NJ_CENTER, zoom_start=8, 
                      tiles=tiles)
    
    # Create state boundary
    folium.Rectangle(
        bounds=[(NJ_SOUTH, NJ_WEST), (NJ_NORTH, NJ_EAST)],
        color='blue' if not dark_mode else 'lightblue',
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
        blur=radius,
        gradient={"0.4": 'blue', "0.65": 'lime', "0.9": 'orange', "1.0": 'red'}
    ).add_to(nj_map)
    
    return nj_map

# Generate maps once at startup
# Generate light and dark maps
light_map = create_nj_map(15, dark_mode=False)
dark_map = create_nj_map(15, dark_mode=True)

light_map.get_root().width = "800px"
light_map.get_root().height = "600px"
dark_map.get_root().width = "800px"
dark_map.get_root().height = "600px"

light_iframe = light_map.get_root()._repr_html_()
dark_iframe = dark_map.get_root()._repr_html_()

# Combine them with a script to toggle visibility based on theme
combined_map = f"""
<div id="light-map" class="map-frame">
    {light_iframe}
</div>
<div id="dark-map" class="map-frame" style="display:none;">
    {dark_iframe}
</div>
<script>
document.addEventListener('DOMContentLoaded', function() {{
    const lightMap = document.getElementById('light-map');
    const darkMap = document.getElementById('dark-map');
    
    // Initial check and setup
    function updateMapTheme() {{
        const currentTheme = document.documentElement.getAttribute('data-theme');
        if (currentTheme === 'dark') {{
            lightMap.style.display = 'none';
            darkMap.style.display = 'block';
        }} else {{
            lightMap.style.display = 'block';
            darkMap.style.display = 'none';
        }}
    }}
    
    // Initial update
    updateMapTheme();
    
    // Listen for theme changes
    const observer = new MutationObserver(function(mutations) {{
        mutations.forEach(function(mutation) {{
            if (mutation.attributeName === 'data-theme') {{
                updateMapTheme();
            }}
        }});
    }});
    
    observer.observe(document.documentElement, {{ attributes: true }});
    
    // Also listen for manual theme toggle if applicable
    const themeToggle = document.getElementById('theme-toggle');
    if (themeToggle) {{
        themeToggle.addEventListener('click', function() {{
            // Let the mutation observer handle the actual change
            // This just ensures we catch direct toggle clicks too
            setTimeout(updateMapTheme, 50);
        }});
    }}
}});
</script>
"""

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
    
report_redirect = fh.RedirectResponse('/report', status_code=303)
    
@rt('/')
def get():
    try:
        page = ft_base.render_template(title="Map", active_page="map", block=ft_map.map(combined_map))
        return page
    except Exception as e:
        return ft_error.error(e)
        
@rt('/about')
def get():
    try:
        page = ft_base.render_template(title="About", active_page="about", block=ft_about.about)
        return page
    except Exception as e:
        return ft_error.error(e)

@rt('/data')
def get():
    try:
        reddit_dict = reddit_df.select(["title", "url", "place", "when"]).to_dicts()
        reddit_columns = reddit_df.select(["title", "url", "place", "when"]).columns
        
        ero_dict = ero_df.to_dicts()
        ero_columns = ero_df.columns
        
        # Get some basic stats about the data
        total_reports = len(reddit_df) + len(ero_df)
        unique_places = len(freqdict)
        
        # Most reported places (top 5)
        top_places = sorted(freqdict.items(), key=lambda x: x[1], reverse=True)[:5]
        
        data = ft_data.render_data(total_reports, unique_places, top_places, reddit_dict, reddit_columns, ero_dict, ero_columns)
        return ft_base.render_template(title="Data", active_page="data", block=data, addl=ft_data.data_script)
    
    except Exception as e:
        return ft_error.error(e)

@rt('/rights')
def get():
    try:
        page = ft_base.render_template(title="Know Your Rights", active_page="rights", block=ft_rights.rights)
        return page
    except Exception as e:
        return ft_error.error(e)

@rt('/report')
def get():
    try:
        page = ft_base.render_template(title="Submit ICE Activity Report", active_page="report", block=ft_report.create_report(messages))
        return page
    except Exception as e:
        return ft_error.error(e)

@fh.dataclass
class ReportForm: location:str; date:str; time:str; description:str; contact_name:str; contact_email:str; contact_phone:str; additional_info:str; 

@rt('/report')
def post(report:ReportForm, sess):
    try:
        if not report.location or not report.date or not report.description:
            messages.clear()
            messages.append(('error', 'Please fill in all required fields.'))
            return report_redirect
        report_data = report.__dict__
        
        if send_report_email(report_data):
            messages.clear()
            messages.append(('success', 'Your report has been submitted successfully. Thank you for contributing.'))
            return fh.RedirectResponse("/", status_code=303)
        else:
            messages.clear()
            messages.append(('error', 'There was an error submitting your report. Please try again later.'))
            return report_redirect
    except Exception as e:
        messages.clear()
        messages.append(('error', f'An error occurred: {str(e)}'))
        return report_redirect


fh.serve()
