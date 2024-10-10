import streamlit as st
from datetime import datetime
import pytz
import pandas as pd

# Function to convert time
def convert_time(input_time, input_tz, destination_tz, output_format):
    try:
        # Parse the input time with the specified input timezone
        local_time = input_tz.localize(datetime.strptime(input_time, "%y%m%d%H%M"))
        # Convert to destination timezone
        destination_time = local_time.astimezone(destination_tz)
        return (destination_time.strftime(output_format), 
                input_tz.zone, 
                local_time.strftime(output_format), 
                destination_tz.zone)
    except ValueError:
        return "Invalid input format. Please use YYMMDDHHMM.", "", "", ""

# Streamlit app layout
st.set_page_config(layout="wide")  # Set layout to wide
st.title("🌐 Time Zone Converter")
st.markdown('<h2 style="color: #FF5722;">Convert Time to Destination Timezone</h2>', unsafe_allow_html=True)
st.write("Convert input time in the format 'YYMMDDHHMM' to a specified destination timezone.")

# Section for selecting timezones and desired output format
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown('<h4 style="color: #FF5722;">🕒 Select Input Timezone</h4>', unsafe_allow_html=True)
    input_tz_name = st.selectbox("Select Input Timezone", pytz.all_timezones, index=pytz.all_timezones.index("UTC"))

with col2:
    st.markdown('<h4 style="color: #FF5722;">🌍 Select Destination Timezone</h4>', unsafe_allow_html=True)
    dest_tz_name = st.selectbox("Select Destination Timezone", pytz.all_timezones, index=pytz.all_timezones.index("Australia/Sydney"))

with col3:
    st.markdown('<h4 style="color: #FF5722;">🗓️ Select Output Date Format</h4>', unsafe_allow_html=True)
    # Popular date formats in a more user-friendly dropdown
    date_formats = {
        "YYYY-MM-DD, HH:MM": "%Y-%m-%d, %H:%M",
        "DD-MM-YYYY, HH:MM": "%d-%m-%Y, %H:%M",
        "MM/DD/YYYY, hh:mm AM/PM": "%m/%d/%Y, %I:%M %p",
        "Day, Month DD, YYYY HH:MM": "%A, %B %d, %Y %H:%M"
    }
    output_format = st.selectbox("Select Output Date Format", list(date_formats.keys()), index=0)

# Convert input timezone string to timezone object
input_tz = pytz.timezone(input_tz_name)
destination_tz = pytz.timezone(dest_tz_name)

# Text area for multiple input times
input_times = st.text_area("Enter multiple input times (YYMMDDHHMM), one per line:", value="2410180330").strip()

# Convert input timezone string to timezone object
input_times_list = [time.strip() for time in input_times.split('\n') if time.strip()]

# Prepare a list to hold the results
results = []

# Convert each input time and store the results
for input_time in input_times_list:
    if input_time:
        converted_time, input_tz_zone, input_time_formatted, dest_tz_zone = convert_time(input_time, input_tz, destination_tz, date_formats[output_format])
        results.append((input_time, input_time_formatted + f" ({input_tz_zone})", converted_time + f" ({dest_tz_zone})"))

# Display the results in a colorful table with borders
if results:
    results_df = pd.DataFrame(results, columns=["Input Time", "Input Time Formatted", "Output Time Formatted"])

    # Draw a table with both inside and outside borders and light contrasting styles
    st.write("Converted Times:")
    st.markdown(
        results_df.style.set_table_attributes('style="border-collapse: collapse; border: 2px solid #FF5722;"')
        .set_table_styles([
            {'selector': 'th', 'props': [('border', '2px solid #FF5722'), ('background-color', '#42A5F5'), ('color', 'white')]},  # Header
            {'selector': 'td', 'props': [('border', '1px solid #FF5722'), ('background-color', '#FFF9C4'), ('color', 'black')]},  # Cell
            {'selector': 'tr:nth-child(even)', 'props': [('background-color', '#FFCCBC')]},  # Alternate row color
            {'selector': 'tr:hover', 'props': [('background-color', '#FFAB40')]},  # Highlight row on hover
        ]).to_html(escape=False), unsafe_allow_html=True)
