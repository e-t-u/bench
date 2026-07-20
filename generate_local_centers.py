#!/usr/bin/env python3
import os
import sys
import time
import subprocess

# Local centers for Helsinki, Espoo, and Vantaa
LOCAL_CENTERS = [
    # Helsinki
    {"name": "Kallio", "query": "Kallio, Helsinki"},
    {"name": "Pasila", "query": "Pasila, Helsinki"},
    {"name": "Malmi", "query": "Malmi, Helsinki"},
    {"name": "Itäkeskus", "query": "Itäkeskus, Helsinki"},
    {"name": "Vuosaari", "query": "Vuosaari, Helsinki"},
    # Espoo
    {"name": "Tapiola", "query": "Tapiola, Espoo"},
    {"name": "Leppävaara", "query": "Leppävaara, Espoo"},
    {"name": "Matinkylä", "query": "Matinkylä, Espoo"},
    {"name": "Espoonlahti", "query": "Espoonlahti, Espoo"},
    # Vantaa
    {"name": "Tikkurila", "query": "Tikkurila, Vantaa"},
    {"name": "Myyrmäki", "query": "Myyrmäki, Vantaa"},
    {"name": "Martinlaakso", "query": "Martinlaakso, Vantaa"},
    {"name": "Koivukylä", "query": "Koivukylä, Vantaa"}
]

def clean_name(name):
    """Convert a name to a clean lowercase filename-friendly string."""
    trans = str.maketrans("äåöÄÅÖ", "aaoAAO")
    return name.translate(trans).lower().replace(" ", "_")

def main():
    output_dir = "example-maps"
    os.makedirs(output_dir, exist_ok=True)
    
    print("=" * 60)
    print(f"Generating Maps for {len(LOCAL_CENTERS)} Local Centers of Helsinki/Espoo/Vantaa")
    print(f"Parameters: radius=150m, size=4.0km x 4.0km")
    print(f"Output directory: {os.path.abspath(output_dir)}")
    print("=" * 60)
    
    success_count = 0
    failed_centers = []
    
    for idx, center in enumerate(LOCAL_CENTERS, 1):
        name = center["name"]
        query = center["query"]
        print(f"\n[{idx}/{len(LOCAL_CENTERS)}] Processing {name} ({query})...")
        
        file_base = clean_name(query)
        html_out = os.path.join(output_dir, f"{file_base}_map.html")
        pdf_out = os.path.join(output_dir, f"{file_base}_map.pdf")
        svg_out = os.path.join(output_dir, f"{file_base}_map.svg")
        
        cmd = [
            sys.executable, "bench.py",
            "-l", query,
            "-r", "150",
            "-s", "4.0",
            "-o", html_out,
            "--pdf", pdf_out,
            "--svg", svg_out
        ]
        
        print(f"Running command: {' '.join(cmd)}")
        
        max_attempts = 2
        for attempt in range(1, max_attempts + 1):
            try:
                env = os.environ.copy()
                env["NODE_PATH"] = "/usr/local/lib/node_modules"
                
                result = subprocess.run(cmd, env=env, capture_output=True, text=True, timeout=300)
                
                print(result.stdout)
                if result.returncode == 0:
                    print(f"✓ Successfully generated map files for {name}.")
                    success_count += 1
                    break
                else:
                    print(f"✗ Attempt {attempt} failed for {name} with exit code {result.returncode}.")
                    print(f"Error details:\n{result.stderr}")
                    if attempt < max_attempts:
                        print("Waiting 10 seconds before retry...")
                        time.sleep(10)
                    else:
                        failed_centers.append(name)
            except subprocess.TimeoutExpired:
                print(f"✗ Attempt {attempt} timed out for {name}.")
                if attempt < max_attempts:
                    print("Waiting 10 seconds before retry...")
                    time.sleep(10)
                else:
                    failed_centers.append(name)
            except Exception as e:
                print(f"✗ Exception processing {name}: {e}")
                failed_centers.append(name)
                break
        
        # Polite delay to avoid API blocking
        time.sleep(5)
        
    print("\n" + "=" * 60)
    print("LOCAL CENTERS GENERATION COMPLETED")
    print(f"Successfully processed: {success_count} / {len(LOCAL_CENTERS)}")
    if failed_centers:
        print(f"Failed local centers: {', '.join(failed_centers)}")
    print("=" * 60)
    
    if failed_centers:
        sys.exit(1)

if __name__ == "__main__":
    main()
