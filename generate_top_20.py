#!/usr/bin/env python3
import os
import sys
import time
import subprocess

# Top 20 Finnish towns by population
TOWNS = [
    "Helsinki", "Espoo", "Tampere", "Vantaa", "Oulu",
    "Turku", "Jyväskylä", "Lahti", "Kuopio", "Pori",
    "Kouvola", "Joensuu", "Lappeenranta", "Hämeenlinna", "Vaasa",
    "Seinäjoki", "Rovaniemi", "Mikkeli", "Kotka", "Salo"
]

def clean_name(name):
    """Convert a name to a clean lowercase filename-friendly string."""
    # Replace non-ascii characters (ä -> a, ö -> o)
    trans = str.maketrans("äåöÄÅÖ", "aaoAAO")
    return name.translate(trans).lower().replace(" ", "_")

def main():
    # Create the output directory if it doesn't exist
    output_dir = "maps"
    os.makedirs(output_dir, exist_ok=True)
    
    print("=" * 60)
    print(f"Batch Generating Maps for Top {len(TOWNS)} Finnish Towns")
    print(f"Parameters: radius=150m, size=4.0km x 4.0km")
    print(f"Output directory: {os.path.abspath(output_dir)}")
    print("=" * 60)
    
    success_count = 0
    failed_towns = []
    
    for idx, town in enumerate(TOWNS, 1):
        print(f"\n[{idx}/{len(TOWNS)}] Processing {town}...")
        
        file_base = clean_name(town)
        html_out = os.path.join(output_dir, f"{file_base}_map.html")
        pdf_out = os.path.join(output_dir, f"{file_base}_map.pdf")
        svg_out = os.path.join(output_dir, f"{file_base}_map.svg")
        
        # Execute the bench.py script
        cmd = [
            sys.executable, "bench.py",
            "-l", f"{town}, Finland",
            "-r", "150",
            "-s", "4.0",
            "-o", html_out,
            "--pdf", pdf_out,
            "--svg", svg_out
        ]
        
        print(f"Running command: {' '.join(cmd)}")
        
        # We try up to 2 times for Nominatim/Overpass rate limit safety
        max_attempts = 2
        for attempt in range(1, max_attempts + 1):
            try:
                # Add NODE_PATH environment variable for Puppeteer export inside bench.py
                env = os.environ.copy()
                env["NODE_PATH"] = "/usr/local/lib/node_modules"
                
                result = subprocess.run(cmd, env=env, capture_output=True, text=True, timeout=300)
                
                print(result.stdout)
                if result.returncode == 0:
                    print(f"✓ Successfully generated map files for {town}:")
                    print(f"  - HTML: {html_out}")
                    print(f"  - PDF:  {pdf_out}")
                    print(f"  - SVG:  {svg_out}")
                    success_count += 1
                    break
                else:
                    print(f"✗ Attempt {attempt} failed for {town} with exit code {result.returncode}.")
                    print(f"Error details:\n{result.stderr}")
                    if attempt < max_attempts:
                        print("Waiting 10 seconds before retry...")
                        time.sleep(10)
                    else:
                        failed_towns.append(town)
            except subprocess.TimeoutExpired:
                print(f"✗ Attempt {attempt} timed out for {town} (limit 5 mins).")
                if attempt < max_attempts:
                    print("Waiting 10 seconds before retry...")
                    time.sleep(10)
                else:
                    failed_towns.append(town)
            except Exception as e:
                print(f"✗ Exception processing {town}: {e}")
                failed_towns.append(town)
                break
        
        # Pause slightly between towns to be polite to the geocoding and Overpass APIs
        time.sleep(5)
        
    print("\n" + "=" * 60)
    print("BATCH GENERATION COMPLETED")
    print(f"Successfully processed: {success_count} / {len(TOWNS)}")
    if failed_towns:
        print(f"Failed towns: {', '.join(failed_towns)}")
    print("=" * 60)
    
    if failed_towns:
        sys.exit(1)

if __name__ == "__main__":
    main()
