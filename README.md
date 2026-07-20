# Bench

`bench` is a command-line tool that generates highly interactive, specialized maps designed for individuals who need to sit down frequently when walking in a town.

The map marks a "safe zone" (circle) around every bench. As long as you remain within these green translucent circles, you are guaranteed to be no further than 300 meters (or your custom adjustable limit) from the nearest bench.

## Features

- **Up-to-date OSM Data:** Dynamic geolocated retrieval of benches from OpenStreetMap via public Overpass API mirrors (with automatic failover support).
- **Interactive Visualizations:**
  - Clear markers for exact bench coordinates with popups showing additional details from OSM (e.g. backrest availability, material, seats, color, operator).
  - Semi-transparent circles highlighting the walk-safety radius (default 300m).
  - High-contrast visual boundary of the fetched search area.
- **Walker-Optimized Controls:**
  - **GPS Locate Me Button:** Real-time localization so walkers can see their position relative to the nearest benches.
  - **Address Search Bar:** Lookup streets and addresses directly on the map in the browser.
  - **Measurement Tool:** Plan and measure distances between points.
  - **Multiple Map Themes:** Switch between Cartodb Positron (clean high-contrast), OpenStreetMap (detailed), and Cartodb Dark Matter.
  - **Layer Toggle:** Independently show/hide safe circles, markers, search centers, and boundary lines.
  - **Responsive Legend:** Modern design legend clearly explaining map symbols.
- **Document & Vector Export:**
  - **PDF Export:** Render the full map (including background tiles and vector overlays) into a high-quality PDF.
  - **SVG Export:** Export the map's vector overlays (safety zones, search area boundary, search center, bench markers) directly to a standalone SVG file.

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/e-t-u/bench.git
   cd bench
   ```

2. Install python dependencies:
   ```bash
   pip install requests folium
   ```

3. **Optional (for PDF/SVG exports):** Ensure you have Node.js and Puppeteer installed.
   ```bash
   # Install Puppeteer globally or locally
   npm install -g puppeteer
   ```

## Usage

Run the program by specifying a location (an address, city, or raw coordinates as `"lat,lon"`) and other optional arguments:

```bash
./bench.py -l "Helsinki, Finland"
```

### Options

- `-l`, `--location` (Required): Bounding box center. Can be an address name (e.g. `"Central Park, New York"`) or coordinates (e.g. `"60.1699,24.9384"`).
- `-r`, `--radius` (Optional): Safe distance limit in meters (default: `300.0`).
- `-s`, `--size` (Optional): Width and height of the map square in kilometers. Minimum `0.1` (default: `1.0`). We recommend `1.0` (1km x 1km) or `2.0` (2km x 2km).
- `-o`, `--output` (Optional): Filename for the generated HTML map (default: `bench_map.html`).
- `-p`, `--open` (Optional): Automatically open the generated map in your web browser immediately.
- `--pdf` (Optional): Filename to export the full map to a high-quality PDF document (e.g. `--pdf map.pdf`).
- `--svg` (Optional): Filename to export the map's vector layers (benches, safe zones, bounds) to a standalone SVG file (e.g. `--svg map.svg`).

### Examples

**Create a 1km x 1km map of Central Park, New York with default 300m zones and open it:**
```bash
./bench.py -l "Central Park, New York" -s 1.0 -p
```

**Generate a map and export both a PDF print and an SVG vector layout:**
```bash
./bench.py -l "Paris, France" --pdf paris_map.pdf --svg paris_vectors.svg
```

## How It Works

1. Geocodes your target location via OpenStreetMap's Nominatim API.
2. Calculates a bounding box matching your specified map dimension.
3. Retrieves all bench nodes, ways, and relations inside the bounding box using the Overpass API.
4. Generates an interactive, lightweight Leaflet HTML map using Folium, embedding all markers, interactive search components, and styling.
5. If requested, runs a headless Chrome browser session via Puppeteer (`export_map.js`) to capture the map and export it as a high-quality PDF document or extract Leaflet's vector overlay layers to an SVG file.
