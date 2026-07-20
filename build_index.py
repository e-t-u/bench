#!/usr/bin/env python3
import os

# Define the places and their files
TOP_20_TOWNS = [
    {"display": "Helsinki", "file": "helsinki_map", "desc": "Capital and largest city of Finland"},
    {"display": "Espoo", "file": "espoo_map", "desc": "Second largest city, hub of innovation and technology"},
    {"display": "Tampere", "file": "tampere_map", "desc": "Major industrial and cultural center in southern Finland"},
    {"display": "Vantaa", "file": "vantaa_map", "desc": "Home to the main international airport, part of the capital region"},
    {"display": "Oulu", "file": "oulu_map", "desc": "Northern technological powerhouse and university city"},
    {"display": "Turku", "file": "turku_map", "desc": "Historical former capital on the southwest coast"},
    {"display": "Jyväskylä", "file": "jyvaskyla_map", "desc": "Major university city in the central Finnish lake district"},
    {"display": "Lahti", "file": "lahti_map", "desc": "Known for winter sports and environmental design"},
    {"display": "Kuopio", "file": "kuopio_map", "desc": "Heart of the Savo region, surrounded by Lake Kallavesi"},
    {"display": "Pori", "file": "pori_map", "desc": "West coast port city famous for Yyteri beaches and jazz"},
    {"display": "Kouvola", "file": "kouvola_map", "desc": "Key railroad junction city in southeastern Finland"},
    {"display": "Joensuu", "file": "joensuu_map", "desc": "Capital of North Karelia, active student town"},
    {"display": "Lappeenranta", "file": "lappeenranta_map", "desc": "Saimaa lake port city near the eastern border"},
    {"display": "Hämeenlinna", "file": "hameenlinna_map", "desc": "Historic city featuring the medieval Häme Castle"},
    {"display": "Vaasa", "file": "vaasa_map", "desc": "Bilingual coastal city with strong energy technology sector"},
    {"display": "Seinäjoki", "file": "seinajoki_map", "desc": "Fast-growing center of the South Ostrobothnia region"},
    {"display": "Rovaniemi", "file": "rovaniemi_map", "desc": "Official hometown of Santa Claus in Lapland"},
    {"display": "Mikkeli", "file": "mikkeli_map", "desc": "Capital of South Savo, historic military headquarters"},
    {"display": "Kotka", "file": "kotka_map", "desc": "Port and maritime park city on the Gulf of Finland"},
    {"display": "Salo", "file": "salo_map", "desc": "Southwestern hub of agriculture and former electronics hub"}
]

LOCAL_CENTERS = [
    # Helsinki
    {"display": "Kallio, Helsinki", "file": "kallio,_helsinki_map", "desc": "Vibrant and dense urban neighborhood in eastern Helsinki"},
    {"display": "Pasila, Helsinki", "file": "pasila,_helsinki_map", "desc": "Major transport and commercial hub north of the center"},
    {"display": "Malmi, Helsinki", "file": "malmi,_helsinki_map", "desc": "Key regional center and transport hub in northeast Helsinki"},
    {"display": "Itäkeskus, Helsinki", "file": "itakeskus,_helsinki_map", "desc": "Main regional center of East Helsinki, hosting Easton and Itis"},
    {"display": "Vuosaari, Helsinki", "file": "vuosaari,_helsinki_map", "desc": "Largest district of Helsinki, combining cargo port and nature parks"},
    # Espoo
    {"display": "Tapiola, Espoo", "file": "tapiola,_espoo_map", "desc": "Garden city district, cultural heart, and metro center"},
    {"display": "Leppävaara, Espoo", "file": "leppavaara,_espoo_map", "desc": "Largest district of Espoo, commercial center hosting Sello"},
    {"display": "Matinkylä, Espoo", "file": "matinkyla,_espoo_map", "desc": "Major residential and retail hub hosting Iso Omena shopping mall"},
    {"display": "Espoonlahti, Espoo", "file": "espoonlahti,_espoo_map", "desc": "Coastal district in southwest Espoo with active sea connections"},
    # Vantaa
    {"display": "Tikkurila, Vantaa", "file": "tikkurila,_vantaa_map", "desc": "Administrative and commercial heart of Vantaa near the main rail line"},
    {"display": "Myyrmäki, Vantaa", "file": "myyrmaki,_vantaa_map", "desc": "Main urban hub in West Vantaa, known for street art and services"},
    {"display": "Martinlaakso, Vantaa", "file": "martinlaakso,_vantaa_map", "desc": "Urban residential district adjacent to Myyrmäki"},
    {"display": "Koivukylä, Vantaa", "file": "koivukyla,_vantaa_map", "desc": "Residential and transport node in eastern Vantaa"}
]

def make_card(place):
    display = place["display"]
    file_base = place["file"]
    desc = place["desc"]
    
    return f"""
        <div class="card">
            <div class="card-header">
                <h3>{display}</h3>
                <p class="description">{desc}</p>
            </div>
            <div class="card-meta">
                <span class="meta-item"><i class="icon-circle"></i> Radius: 150m</span>
                <span class="meta-item"><i class="icon-square"></i> Size: 4km × 4km</span>
            </div>
            <div class="card-actions">
                <a href="{file_base}.html" class="btn btn-html" target="_blank" title="Open interactive map in web browser">
                    <svg viewBox="0 0 24 24" width="16" height="16"><path fill="currentColor" d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg>
                    HTML Map
                </a>
                <a href="{file_base}.pdf" class="btn btn-pdf" target="_blank" title="Download print-ready PDF map">
                    <svg viewBox="0 0 24 24" width="16" height="16"><path fill="currentColor" d="M20 2H8c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h12c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zm-8.5 7.5c0 .83-.67 1.5-1.5 1.5H9v2H7.5V8H10c.83 0 1.5.67 1.5 1.5zm5 2c0 .83-.67 1.5-1.5 1.5h-2.5V8h2.5c.83 0 1.5.67 1.5 1.5v2zm4-3H19v1h1.5V11H19v2h-1.5V8h3v1.5zm-5 3h1c.28 0 .5-.22.5-.5v-2c0-.28-.22-.5-.5-.5h-1v3zm-5.5-3h-1v1.5h1c.28 0 .5-.22.5-.5v-.5c0-.28-.22-.5-.5-.5zM4 6H2v14c0 1.1.9 2 2 2h14v-2H4V6z"/></svg>
                    PDF Print
                </a>
                <a href="{file_base}.svg" class="btn btn-svg" target="_blank" title="Open vector SVG map in browser or download to edit">
                    <svg viewBox="0 0 24 24" width="16" height="16"><path fill="currentColor" d="M19 3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h14c1.1 0 2-.9 2-2V5c0-1.1-.9-2-2-2zm-7 13.5c-2.48 0-4.5-2.02-4.5-4.5S10.02 7.5 12 7.5s4.5 2.02 4.5 4.5-2.02 4.5-4.5 4.5zm0-7.5c-1.66 0-3 1.34-3 3s1.34 3 3 3 3-1.34 3-3-1.34-3-3-3z"/></svg>
                    SVG Vector
                </a>
            </div>
        </div>
    """

def main():
    # Build sections
    towns_html = "\n".join(make_card(t) for t in TOP_20_TOWNS)
    centers_html = "\n".join(make_card(c) for c in LOCAL_CENTERS)
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Walk-Safety Bench Maps for Major Finnish Cities and Local Centers. Interactive HTML, print-ready PDF, and editable vector SVG.">
    <title>Walk-Safety Bench Maps Directory — Esa Turtiainen</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-primary: #0b132b;
            --bg-secondary: #1c2541;
            --bg-tertiary: rgba(28, 37, 65, 0.6);
            --accent-primary: #5bc0be;
            --accent-hover: #6fffe9;
            --text-main: #f4f6fc;
            --text-muted: #a5b4fc;
            --border-color: rgba(91, 192, 190, 0.15);
            --border-hover: rgba(111, 255, 233, 0.4);
            
            --shadow-sm: 0 2px 8px rgba(0,0,0,0.3);
            --shadow-md: 0 10px 30px rgba(0,0,0,0.5);
            --transition-smooth: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            background-color: var(--bg-primary);
            color: var(--text-main);
            font-family: 'Plus Jakarta Sans', sans-serif;
            line-height: 1.6;
            min-height: 100vh;
            padding: 2rem 1.5rem;
            position: relative;
            overflow-x: hidden;
        }}

        /* Subtle glowing background decorations */
        body::before, body::after {{
            content: '';
            position: fixed;
            width: 400px;
            height: 400px;
            border-radius: 50%;
            background: radial-gradient(circle, rgba(91,192,190,0.12) 0%, rgba(0,0,0,0) 70%);
            z-index: -1;
            pointer-events: none;
        }}
        body::before {{
            top: -100px;
            left: -100px;
        }}
        body::after {{
            bottom: -100px;
            right: -100px;
        }}

        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}

        /* Header styling */
        header {{
            text-align: center;
            margin-bottom: 4rem;
            padding: 2rem 0;
            position: relative;
        }}

        h1 {{
            font-family: 'Outfit', sans-serif;
            font-size: clamp(2.5rem, 5vw, 4rem);
            font-weight: 700;
            background: linear-gradient(135deg, var(--text-main) 30%, var(--accent-primary) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 1rem;
            letter-spacing: -0.02em;
        }}

        .subtitle {{
            font-size: clamp(1rem, 2vw, 1.25rem);
            color: var(--text-muted);
            max-width: 800px;
            margin: 0 auto 2rem;
            font-weight: 300;
        }}

        .stats-bar {{
            display: inline-flex;
            gap: 2rem;
            background: var(--bg-tertiary);
            backdrop-filter: blur(10px);
            border: 1px solid var(--border-color);
            border-radius: 50px;
            padding: 0.75rem 2rem;
            box-shadow: var(--shadow-sm);
        }}

        .stat-item {{
            display: flex;
            align-items: center;
            gap: 0.5rem;
            font-size: 0.9rem;
            color: var(--accent-primary);
            font-weight: 500;
        }}

        .stat-val {{
            color: var(--text-main);
            font-weight: 700;
            font-size: 1.1rem;
        }}

        /* Section layout */
        section {{
            margin-bottom: 5rem;
        }}

        h2 {{
            font-family: 'Outfit', sans-serif;
            font-size: 1.8rem;
            font-weight: 600;
            margin-bottom: 2rem;
            display: flex;
            align-items: center;
            gap: 0.75rem;
            color: var(--accent-primary);
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 0.75rem;
        }}

        h2 span {{
            font-size: 0.9rem;
            font-weight: 400;
            color: var(--text-muted);
            background: rgba(91, 192, 190, 0.1);
            padding: 0.25rem 0.75rem;
            border-radius: 20px;
        }}

        /* Card grid */
        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
            gap: 1.5rem;
        }}

        /* Card styling */
        .card {{
            background: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 16px;
            padding: 1.75rem;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            box-shadow: var(--shadow-sm);
            transition: var(--transition-smooth);
            position: relative;
        }}

        .card:hover {{
            transform: translateY(-5px);
            border-color: var(--border-hover);
            box-shadow: var(--shadow-md), 0 0 20px rgba(111, 255, 233, 0.05);
        }}

        .card-header h3 {{
            font-family: 'Outfit', sans-serif;
            font-size: 1.35rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
            letter-spacing: -0.01em;
        }}

        .description {{
            font-size: 0.9rem;
            color: var(--text-muted);
            margin-bottom: 1.5rem;
            font-weight: 300;
            min-height: 44px; /* Align heights */
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }}

        .card-meta {{
            display: flex;
            gap: 1rem;
            margin-bottom: 1.5rem;
            font-size: 0.8rem;
            color: var(--text-muted);
            border-top: 1px dashed rgba(255, 255, 255, 0.05);
            padding-top: 1rem;
        }}

        .meta-item {{
            display: flex;
            align-items: center;
            gap: 0.4rem;
        }}

        .icon-circle {{
            width: 8px;
            height: 8px;
            border-radius: 50%;
            background-color: var(--accent-primary);
            display: inline-block;
        }}

        .icon-square {{
            width: 8px;
            height: 8px;
            background-color: #818cf8;
            display: inline-block;
        }}

        /* Buttons and links */
        .card-actions {{
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 0.5rem;
        }}

        .btn {{
            display: inline-flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            gap: 0.35rem;
            padding: 0.6rem 0.25rem;
            font-size: 0.75rem;
            font-weight: 600;
            text-decoration: none;
            border-radius: 8px;
            transition: var(--transition-smooth);
            text-align: center;
            border: 1px solid rgba(255, 255, 255, 0.05);
        }}

        .btn svg {{
            transition: transform 0.2s ease;
        }}

        .btn:hover svg {{
            transform: scale(1.15);
        }}

        .btn-html {{
            background-color: rgba(91, 192, 190, 0.1);
            color: var(--accent-primary);
        }}

        .btn-html:hover {{
            background-color: var(--accent-primary);
            color: var(--bg-primary);
        }}

        .btn-pdf {{
            background-color: rgba(244, 63, 94, 0.1);
            color: #fb7185;
            border-color: rgba(244, 63, 94, 0.15);
        }}

        .btn-pdf:hover {{
            background-color: #f43f5e;
            color: #ffffff;
            border-color: #f43f5e;
        }}

        .btn-svg {{
            background-color: rgba(129, 140, 248, 0.1);
            color: #a5b4fc;
            border-color: rgba(129, 140, 248, 0.15);
        }}

        .btn-svg:hover {{
            background-color: #6366f1;
            color: #ffffff;
            border-color: #6366f1;
        }}

        footer {{
            text-align: center;
            padding: 4rem 0 2rem;
            font-size: 0.85rem;
            color: var(--text-muted);
            border-top: 1px solid var(--border-color);
            margin-top: 6rem;
        }}

        footer a {{
            color: var(--accent-primary);
            text-decoration: none;
            transition: var(--transition-smooth);
        }}

        footer a:hover {{
            color: var(--accent-hover);
            text-decoration: underline;
        }}

        /* Responsive styling offsets */
        @media (max-width: 768px) {{
            body {{
                padding: 1.5rem 1rem;
            }}
            header {{
                margin-bottom: 2.5rem;
            }}
            .stats-bar {{
                flex-direction: column;
                gap: 0.75rem;
                border-radius: 16px;
                padding: 1rem 2rem;
                width: 100%;
            }}
            .grid {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>OSM Walk-Safety Bench Maps</h1>
            <p class="subtitle">Walkable safety zones plotted within 150m of benches in public spaces, calculated using bounding box dimensions of 4km × 4km on real-time OpenStreetMap data.</p>
            <div class="stats-bar">
                <div class="stat-item"><i class="icon-circle"></i> Cities Indexed: <span class="stat-val">20</span></div>
                <div class="stat-item"><i class="icon-square"></i> Local Districts: <span class="stat-val">13</span></div>
                <div class="stat-item"><i class="icon-circle" style="background-color: #818cf8;"></i> File Formats: <span class="stat-val">HTML, PDF, SVG</span></div>
            </div>
        </header>

        <section id="major-towns">
            <h2>Major Finnish Cities <span>20 Maps</span></h2>
            <div class="grid">
                {towns_html}
            </div>
        </section>

        <section id="local-centers">
            <h2>Local Neighborhoods & Centers <span>13 Maps</span></h2>
            <div class="grid">
                {centers_html}
            </div>
        </section>

        <footer>
            <p>&copy; 2026 Esa Turtiainen. Powered by OpenStreetMap contributors, Folium, and Puppeteer.</p>
            <p style="margin-top: 0.5rem;"><a href="https://github.com/e-t-u/bench" target="_blank">View GitHub Repository</a></p>
        </footer>
    </div>
</body>
</html>
"""
    
    output_file = os.path.join("example-maps", "index.html")
    with open(output_file, "w") as f:
        f.write(html_content)
    print(f"✓ Premium index page successfully generated at: {output_file}")

if __name__ == "__main__":
    main()
