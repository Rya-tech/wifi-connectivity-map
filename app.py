
import folium
import pandas as pd
from folium.plugins import HeatMap

# Sample Wi-Fi connectivity data
# Replace these coordinates with actual survey data

wifi_data = [
    {"name": "Area 1", "lat": 12.9716, "lon": 77.5946,
     "signal": -35, "router": "Router 1"},

    {"name": "Area 2", "lat": 12.9750, "lon": 77.6000,
     "signal": -55, "router": "Router 2"},

    {"name": "Area 3", "lat": 12.9800, "lon": 77.5850,
     "signal": -72, "router": "Router 3"},

    {"name": "Area 4", "lat": 12.9650, "lon": 77.6100,
     "signal": -88, "router": "No nearby router"},

    {"name": "Area 5", "lat": 12.9900, "lon": 77.5800,
     "signal": -45, "router": "Router 5"},

    {"name": "Area 6", "lat": 12.9550, "lon": 77.6200,
     "signal": -95, "router": "No nearby router"}
]

# Create map
wifi_map = folium.Map(
    location=[12.9716, 77.5946],
    zoom_start=14,
    tiles=None
)

# Add Esri map without an API key
folium.TileLayer(
    tiles="https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}",
    attr="Tiles © Esri",
    name="Esri World Street Map"
).add_to(wifi_map)

# Function to identify signal quality
def get_quality(signal):
    if signal >= -50:
        return "Good", "green"
    elif signal >= -70:
        return "Medium", "orange"
    elif signal >= -85:
        return "Weak", "red"
    else:
        return "No/Very Poor Signal", "darkred"

# Add Wi-Fi locations
heat_points = []

for point in wifi_data:

    quality, color = get_quality(point["signal"])

    popup_text = f"""
    <b>Location:</b> {point['name']}<br>
    <b>Signal:</b> {point['signal']} dBm<br>
    <b>Quality:</b> {quality}<br>
    <b>Router:</b> {point['router']}
    """

    folium.CircleMarker(
        location=[point["lat"], point["lon"]],
        radius=10,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.8,
        popup=folium.Popup(popup_text, max_width=250),
        tooltip=point["name"] + " - " + quality
    ).add_to(wifi_map)

    # Convert signal strength into heatmap intensity
    intensity = max(0, min(1, (abs(point["signal"]) - 30) / 70))

    heat_points.append([
        point["lat"],
        point["lon"],
        intensity
    ])

# Add connectivity heatmap
HeatMap(
    heat_points,
    radius=30,
    blur=20,
    min_opacity=0.3
).add_to(wifi_map)

# Add router markers
for point in wifi_data:
    if point["router"] != "No nearby router":
        folium.Marker(
            location=[point["lat"], point["lon"]],
            tooltip=point["router"],
            popup=point["router"],
            icon=folium.Icon(
                color="blue",
                icon="wifi",
                prefix="fa"
            )
        ).add_to(wifi_map)

# Add map title
title_html = """
<h3 align="center">
Wi-Fi Connectivity Infrastructure Map
</h3>
"""
wifi_map.get_root().html.add_child(
    folium.Element(title_html)
)

# Save map
wifi_map.save("map.html")

print("Wi-Fi map created successfully!")
print("Open map.html in your browser.")
