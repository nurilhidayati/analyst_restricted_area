import streamlit as st

st.set_page_config(
    page_title="Analyst Gap Justification",
    page_icon="🌍",
    initial_sidebar_state="expanded"
)

st.title("🛠️ Analyst Gap Justification")

st.markdown("""
### 🔍 Overview

**Analyst Gap Justification** is a geospatial web application built with Streamlit that helps mapping teams analyze and validate road segments against restricted areas. It automates filtering, transforming, and evaluating road data using OpenStreetMap (OSM) — reducing the need for manual GIS work.

---

### 🎯 Purpose
To improve the speed and accuracy of analyst gap justification by automating key spatial processes — from filtering to comparing — without relying on desktop GIS tools.

---

### 🔄 Workflow Steps
**✅ Step 1: Split Data by City Name**  
This step filters and extracts rows from the uploaded CSV file based on a specific city name found within the grid_id column. The application identifies the city by splitting the grid_id string and matching the second word with the city name you enter (example: "Jakarta"). This is useful when you only want to analyze or export data from a particular city out of a larger dataset.


---

**✅ Step 2: Flatten Coordinates**  
Raw coordinate data looks like this:  
`[[(104.75, -2.97), (104.76, -2.96)]]`  

This format stores stores multiple coordinates in a single row, which makes the data hard to use. To make it easier, the coordinates are flattened — meaning each point is separated into its own row. This helps in drawing roads on the map, identifying missing or incorrect points, and preparing the data for further processing.

---

**✅ Step 3: Convert to Polylines**  
After flattening, each road is still just a list of dots.  
We now **connect the dots** to form visible road paths.

**Why this matters:**  
- Transforms points into lines (polylines)  
- Allows roads to be displayed on a map  
- Essential for checking if roads cross restricted areas  

**Analogy:**  
Dots A → B → C are just locations — but connecting them creates an actual road.

---

**✅ Step 4: Download Restricted Areas**  
In this step, the app automatically downloads restricted zones from OpenStreetMap (OSM) based on specific tags.
🏞️ Restricted Areas include:
- Land use: military, industrial, commercial, cemetery, landfill
- Leisure: nature reserves, golf courses
- Boundaries: protected areas
- Airports: aerodromes
- Buildings: schools, hospitals, warehouses, government/military buildings
- Amenities: schools, universities, police stations, hospitals
- Barriers: fences, gates, walls
- Access rules: private, permit-only, military areas

🚧 Restricted Roads include:
- Road types: service roads, tracks, alleys
- Access: private, military, permit-only
- Motorcycle access: banned or restricted
- Service tags: emergency access, driveways

🛑 These tags help the tool detect areas where roads should not go — making your validation smarter and faster.

---

**✅ Step 5: Analyst Gap Justification**  
Now we check: do any roads **intersect** with restricted zones?

**Why this matters:**  
- Highlights road segments inside or near restricted areas  
- Helps avoid routing errors or violations  
- Produces a clean GeoJSON output for further use


---

### 💬 Contact & Credits

📩 **Slack contact:** `nuril.hidayati`  
👥 **Project Team:** ID Karta IoT – 2025  
🙏 **Thanks to:** Qitfirul, Mahardi Pratomo, Annisa Dwi Maiikhsantiani, and Mochammad Fachri
""")
