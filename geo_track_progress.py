import folium
import pandas as pd
from geopy.geocoders import Nominatim
from datetime import datetime

excel_file_path = r'\path\to\your\file.xlsx'

columns_to_read = ['Postcode', 'Date']
df = pd.read_excel(excel_file_path, sheet_name='Tracker', engine='openpyxl', usecols=columns_to_read)

def get_coordinates(postcode):
    geolocator = Nominatim(user_agent="postcode_mapper")
    location = geolocator.geocode(postcode)
    return (location.latitude, location.longitude) if location else None

map_center = get_coordinates("UK")  
uk_map = folium.Map(location=map_center, zoom_start=6)

for index, row in df.iterrows():
    postcode = row['Postcode']
    print(index, row)

    try:
        coordinates = get_coordinates(postcode)
        print("Coordinates: ", coordinates)
        print(f"Processing row: {index}, Postcode: {postcode}, Coordinates: {coordinates}")
        if coordinates:
            pin_date = row['Date']

            if pd.isnull(pin_date):
                pin_color = 'grey'
            else:
                if isinstance(pin_date, pd.Timestamp):
                    pin_date = pin_date.date()

                pin_color = 'red' if pin_date > datetime.today().date() else 'green'

            print(f"Adding marker for Postcode: {postcode}, Date: {pin_date}, Color: {pin_color}, Coordinates: {coordinates}")

            folium.CircleMarker(location=coordinates, radius=8, color=pin_color, fill=True, fill_color=pin_color, fill_opacity=1.0, popup=postcode).add_to(uk_map)
        else:
            print(f"No coordinates found for Postcode: {postcode}")

    except Exception as e:
        print(f"Error processing row {index}, Postcode: {postcode}: {e}")

uk_map.save(r"map.html") 
print("Map saved as HTML.")
