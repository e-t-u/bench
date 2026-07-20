#!/usr/bin/env python3
import os
import sys
import math
import argparse
import requests
import webbrowser
import folium
from folium.plugins import LocateControl, MiniMap, MeasureControl, Geocoder
from branca.element import Element

def get_bbox(lat, lon, size_km):
    """
    Calculate the bounding box given center coordinates and side length in km.
    Returns lat_min, lon_min, lat_max, lon_max
    """
    # Earth's radius in km
    R = 6378.1
    
    # Half size for offset calculation
    half_size = size_km / 2.0
    
    # Lat offset in degrees
    d_lat = math.degrees(half_size / R)
    # Lon offset in degrees (accounting for latitude)
    d_lon = math.degrees(half_size / (R * math.cos(math.radians(lat))))
    
    return lat - d_lat, lon - d_lon, lat + d_lat, lon + d_lon

def geocode_location(location_str):
    """
    Geocode an address or city name to coordinates using OSM Nominatim.
    """
    print(f"Resolving location '{location_str}'...")
    headers = {
        'User-Agent': 'bench-map-maker/1.0 (contact: github.com/e-t-u/bench)'
    }
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        'q': location_str,
        'format': 'json',
        'limit': 1
    }
    try:
        response = requests.get(url, headers=headers, params=params, timeout=15)
        response.raise_for_status()
        results = response.json()
        if not results:
            print(f"Error: Location '{location_str}' could not be found.")
            sys.exit(1)
        
        lat = float(results[0]['lat'])
        lon = float(results[0]['lon'])
        display_name = results[0]['display_name']
        print(f"Found: {display_name}")
        print(f"Coordinates: {lat:.6f}, {lon:.6f}")
        return lat, lon, display_name
    except Exception as e:
        print(f"Error connecting to geocoding service: {e}")
        sys.exit(1)

def resolve_location(location_str):
    """
    Tries to parse the location as raw coordinates first, then falls back to geocoding.
    """
    # Check if format is "lat,lon"
    parts = location_str.split(',')
    if len(parts) == 2:
        try:
            lat = float(parts[0].strip())
            lon = float(parts[1].strip())
            return lat, lon, f"Custom Coordinates: {lat:.5f}, {lon:.5f}"
        except ValueError:
            pass
            
    return geocode_location(location_str)

def fetch_benches(lat_min, lon_min, lat_max, lon_max):
    """
    Query Overpass API for benches inside the bounding box.
    Tries multiple public Overpass mirrors in case of failure.
    """
    print("Fetching benches data from OpenStreetMap (Overpass API)...")
    
    # List of public Overpass API endpoints to try in sequence
    endpoints = [
        "https://overpass-api.de/api/interpreter",
        "https://overpass.kumi.systems/api/interpreter",
        "https://overpass.osm.ch/api/interpreter",
        "https://overpass.nchc.org.tw/api/interpreter"
    ]
    
    overpass_query = f"""
    [out:json][timeout:25];
    (
      node["amenity"="bench"]({lat_min},{lon_min},{lat_max},{lon_max});
      way["amenity"="bench"]({lat_min},{lon_min},{lat_max},{lon_max});
      relation["amenity"="bench"]({lat_min},{lon_min},{lat_max},{lon_max});
    );
    out center;
    """
    
    headers = {
        'User-Agent': 'bench-map-maker/1.0 (contact: github.com/e-t-u/bench)'
    }
    
    for url in endpoints:
        print(f"Trying Overpass server: {url}...")
        try:
            response = requests.post(url, headers=headers, data={'data': overpass_query}, timeout=30)
            if response.status_code == 200:
                data = response.json()
                elements = data.get('elements', [])
                print(f"Successfully retrieved {len(elements)} benches.")
                return elements
            else:
                print(f"Server returned status code {response.status_code}. Trying next mirror...")
        except Exception as e:
            print(f"Error connecting to {url}: {e}. Trying next mirror...")
            
    print("Error: All public Overpass API mirrors failed or timed out.")
    sys.exit(1)

def make_popup_content(element):
    """
    Create a clean HTML popup for a bench showing any available OSM tags.
    """
    tags = element.get('tags', {})
    html = """
    <div style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; font-size: 13px; line-height: 1.6; color: #2c3e50; min-width: 160px; max-width: 250px;">
        <h4 style="margin: 0 0 6px 0; color: #1abc9c; border-bottom: 1px solid #ecf0f1; padding-bottom: 4px;">Town Bench</h4>
    """
    
    details = []
    if 'backrest' in tags:
        val = "Yes" if tags['backrest'] == 'yes' else ("No" if tags['backrest'] == 'no' else tags['backrest'])
        details.append(f"<b>Backrest:</b> {val}")
    if 'material' in tags:
        details.append(f"<b>Material:</b> {tags['material'].capitalize()}")
    if 'seats' in tags:
        details.append(f"<b>Seats:</b> {tags['seats']}")
    if 'colour' in tags:
        details.append(f"<b>Color:</b> {tags['colour']}")
    if 'operator' in tags:
        details.append(f"<b>Operator:</b> {tags['operator']}")
    if 'description' in tags:
        details.append(f"<b>Note:</b> {tags['description']}")
        
    if details:
        html += "<div style='margin-top: 5px;'>" + "<br>".join(details) + "</div>"
    else:
        html += "<div style='color: #95a5a6; font-style: italic; margin-top: 5px;'>No additional details in OSM</div>"
        
    html += "</div>"
    return html

def add_legend(m, radius):
    """
    Inject a modern, responsive HTML legend control into the map.
    """
    legend_html = f"""
    <div id='maplegend' class='maplegend' 
        style='position: fixed; z-index:9999; border:1px solid #bdc3c7; background-color:rgba(255, 255, 255, 0.9);
        border-radius:8px; padding: 12px; font-size:13px; right: 10px; bottom: 20px; font-family: sans-serif;
        box-shadow: 0 2px 5px rgba(0,0,0,0.15); max-width: 250px;'>
    <div style='font-weight: bold; margin-bottom: 8px; color: #2c3e50; font-size: 14px;'>Map Legend</div>
    <div style='display: flex; flex-direction: column; gap: 6px;'>
      <div style='display: flex; align-items: center;'>
        <span style='background:#2ecc71; opacity:0.4; border: 1.5px solid #27ae60; display:inline-block; width:16px; height:16px; margin-right:8px; border-radius:3px;'></span>
        <span style='color: #34495e;'>Safe zone (< {radius}m to bench)</span>
      </div>
      <div style='display: flex; align-items: center;'>
        <span style='background:#3498db; border: 1.5px solid #2980b9; border-radius:50%; display:inline-block; width:12px; height:12px; margin-right:10px; margin-left: 2px;'></span>
        <span style='color: #34495e;'>Bench location</span>
      </div>
      <div style='display: flex; align-items: center;'>
        <span style='background:#e74c3c; border: 1.5px solid #c0392b; border-radius:50%; display:inline-block; width:12px; height:12px; margin-right:10px; margin-left: 2px;'></span>
        <span style='color: #34495e;'>Search Center</span>
      </div>
      <div style='display: flex; align-items: center;'>
        <span style='border: 2px dashed #95a5a6; display:inline-block; width:16px; height:0px; margin-right:8px;'></span>
        <span style='color: #34495e;'>Search Area Boundary</span>
      </div>
    </div>
    <div style='font-size: 10px; color: #7f8c8d; margin-top: 10px; border-top: 1px solid #ecf0f1; padding-top: 4px;'>
      Data: OpenStreetMap contributors
    </div>
    </div>
    """
    m.get_root().html.add_child(Element(legend_html))

def create_map(lat, lon, display_name, benches, radius, size_km, output_path):
    """
    Generate and save the Folium HTML map.
    """
    print("Generating map...")
    
    # Calculate bounding box coordinates
    lat_min, lon_min, lat_max, lon_max = get_bbox(lat, lon, size_km)
    
    # Create map centered at search location
    # We add CartoDB Positron as standard tile and others as options
    m = folium.Map(
        location=[lat, lon],
        zoom_start=15,
        tiles="CartoDB Positron",
        name="CartoDB Positron (Clean)"
    )
    
    # Add other basemaps
    folium.TileLayer("OpenStreetMap", name="OpenStreetMap (Detailed)").add_to(m)
    folium.TileLayer("Cartodb Dark Matter", name="CartoDB Dark Matter (Dark)").add_to(m)
    
    # Add bounding box representation
    boundary_points = [
        [lat_min, lon_min],
        [lat_max, lon_min],
        [lat_max, lon_max],
        [lat_min, lon_max],
        [lat_min, lon_min]
    ]
    
    folium.PolyLine(
        locations=boundary_points,
        color="#7f8c8d",
        weight=2.5,
        dash_array="6, 6",
        tooltip="Search Area Boundary",
        popup=f"Search area boundary: {size_km}km x {size_km}km"
    ).add_to(m)
    
    # Create FeatureGroups
    fg_safe_zones = folium.FeatureGroup(name=f"Bench Safe Zones ({radius}m)", show=True)
    fg_benches = folium.FeatureGroup(name="Benches Markers", show=True)
    fg_center = folium.FeatureGroup(name="Search Center", show=True)
    
    # Add center marker
    folium.Marker(
        location=[lat, lon],
        popup=f"<b>Search Center</b><br>{display_name}",
        tooltip="Search Center",
        icon=folium.Icon(color="red", icon="home")
    ).add_to(fg_center)
    
    # Draw benches and circles
    for b in benches:
        # Get coordinates (Overpass 'out center' guarantees center exists for ways/relations)
        b_lat = b.get('lat')
        b_lon = b.get('lon')
        
        if b_lat is None or b_lon is None:
            # Fallback to center if normal way or relation
            center = b.get('center', {})
            b_lat = center.get('lat')
            b_lon = center.get('lon')
            
        if b_lat is None or b_lon is None:
            continue
            
        # Draw the 300m (or adjustable) safe zone circle around the bench
        folium.Circle(
            location=[b_lat, b_lon],
            radius=radius,
            color="#27ae60",
            fill=True,
            fill_color="#2ecc71",
            fill_opacity=0.18,
            weight=1.2,
            tooltip=f"Safe zone ({radius}m radius)",
        ).add_to(fg_safe_zones)
        
        # Bench marker
        popup_html = make_popup_content(b)
        folium.CircleMarker(
            location=[b_lat, b_lon],
            radius=7,
            color="#1b4f72",
            fill=True,
            fill_color="#3498db",
            fill_opacity=0.9,
            weight=2,
            popup=folium.Popup(popup_html, max_width=250),
            tooltip="Click for bench details"
        ).add_to(fg_benches)
        
    # Add FeatureGroups to map
    fg_safe_zones.add_to(m)
    fg_benches.add_to(m)
    fg_center.add_to(m)
    
    # Add Leaflet Control Geocoder to allow live search in browser
    Geocoder(position='topright').add_to(m)
    
    # Add GPS locate button for mobile/field walkers
    LocateControl(
        auto_start=False,
        keepCurrentZoomLevel=True,
        drawCircle=True,
        circleStyle={'fillColor': '#3498db', 'fillOpacity': 0.15, 'color': '#2980b9', 'weight': 1},
        markerStyle={'color': '#2980b9', 'fillColor': '#3498db'}
    ).add_to(m)
    
    # Add distance measuring tool
    MeasureControl(
        position='topleft',
        primary_length_unit='meters',
        secondary_length_unit='kilometers'
    ).add_to(m)
    
    # Add Overview/MiniMap
    MiniMap(toggle_display=True, position='bottomleft').add_to(m)
    
    # Add Layer Control
    folium.LayerControl(position='topright').add_to(m)
    
    # Fit map to boundary bounds
    m.fit_bounds([[lat_min, lon_min], [lat_max, lon_max]])
    
    # Add CSS Legend
    add_legend(m, radius)
    
    # Save file
    try:
        m.save(output_path)
        print(f"Map successfully generated and saved to: {os.path.abspath(output_path)}")
    except Exception as e:
        print(f"Error saving map: {e}")
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(
        description="Bench: Generate interactive maps marking bench safety zones for walkers."
    )
    parser.add_argument(
        "-l", "--location",
        type=str,
        required=True,
        help="Search location (address/city name) or coordinates as 'lat,lon'"
    )
    parser.add_argument(
        "-r", "--radius",
        type=float,
        default=300.0,
        help="Maximum distance to a bench in meters. Marks a circle of this radius (default: 300)"
    )
    parser.add_argument(
        "-s", "--size",
        type=float,
        default=1.0,
        help="Map dimension in km (e.g. 1.0 for 1x1 km, 2.0 for 2x2 km. Default: 1.0)"
    )
    parser.add_argument(
        "-o", "--output",
        type=str,
        default="bench_map.html",
        help="Output filename for the HTML map (default: bench_map.html)"
    )
    parser.add_argument(
        "-p", "--open",
        action="store_true",
        help="Open the generated map in your web browser immediately"
    )
    
    args = parser.parse_args()
    
    # Enforce minimum sizes matching instructions if needed, but allow floats
    if args.size < 0.1:
        print("Warning: Size is very small. Resetting size to minimum of 0.1 km.")
        args.size = 0.1
        
    lat, lon, display_name = resolve_location(args.location)
    
    # Calculate bounding box
    lat_min, lon_min, lat_max, lon_max = get_bbox(lat, lon, args.size)
    
    # Fetch OSM data
    benches = fetch_benches(lat_min, lon_min, lat_max, lon_max)
    
    if not benches:
        print("\n========================================================")
        print("WARNING: No benches were found in this area on OpenStreetMap!")
        print("This means the OSM database contains no elements tagged as 'amenity=bench'")
        print("inside the requested coordinates.")
        print("Suggestions:")
        print("  1. Increase the search area size with '-s' or '--size' (e.g. -s 2.0 or -s 5.0)")
        print("  2. Try a different, more populated urban location (e.g., Helsinki, Paris, New York)")
        print("========================================================\n")
    else:
        # Print a short debug list of the first 3 benches coordinates
        print(f"Sample of retrieved benches:")
        for b in benches[:3]:
            b_lat = b.get('lat') or b.get('center', {}).get('lat')
            b_lon = b.get('lon') or b.get('center', {}).get('lon')
            tags = b.get('tags', {})
            desc = tags.get('material', 'unknown material')
            print(f"  - Bench #{b.get('id')}: lat={b_lat}, lon={b_lon} ({desc})")
        if len(benches) > 3:
            print(f"  - ... and {len(benches) - 3} more benches.")
            
    # Generate Map
    create_map(lat, lon, display_name, benches, args.radius, args.size, args.output)
    
    # Open browser
    if args.open:
        abs_path = os.path.abspath(args.output)
        print(f"Opening browser to {abs_path}...")
        webbrowser.open("file://" + abs_path)

if __name__ == "__main__":
    main()
