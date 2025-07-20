import streamlit as st
import geopandas as gpd
import pandas as pd
import io

st.title("🛣️ Analyst Gap Justification")

# Fungsi utama
def select_restricted_roads(gdf_roads, gdf_polygons, gdf_lines=None, distance_meters=100.0):
    if gdf_roads.crs.is_geographic:
        utm_crs = gdf_roads.estimate_utm_crs()
        gdf_roads = gdf_roads.to_crs(utm_crs)
        gdf_polygons = gdf_polygons.to_crs(utm_crs)
        if gdf_lines is not None:
            gdf_lines = gdf_lines.to_crs(utm_crs)

    buffered_polygons = gdf_polygons.buffer(distance_meters)
    buffered_polygons_gdf = gpd.GeoDataFrame(geometry=buffered_polygons, crs=gdf_polygons.crs)

    if gdf_lines is not None:
        combined_geometry = pd.concat([buffered_polygons_gdf.geometry, gdf_lines.geometry], ignore_index=True)
        all_combined = gpd.GeoDataFrame(geometry=combined_geometry, crs=buffered_polygons_gdf.crs)
    else:
        all_combined = buffered_polygons_gdf

    selected = gpd.sjoin(gdf_roads, all_combined, how="inner", predicate="intersects")
    selected = selected.drop_duplicates(subset=gdf_roads.columns)
    return selected.to_crs("EPSG:4326")

# Upload UI
uploaded_roads = st.file_uploader("📤 Upload Road GeoJSON", type=["geojson"])
uploaded_polygons = st.file_uploader("📤 Upload Restricted Area (Polygon GeoJSON)", type=["geojson"])
uploaded_lines = st.file_uploader("📤 Upload Restricted Road (Linestring GeoJSON)", type=["geojson"])

# Inisialisasi state
if "selected_roads" not in st.session_state:
    st.session_state.selected_roads = None

# Tampilkan tombol proses jika semua file wajib terisi
if uploaded_roads and uploaded_polygons:
    if st.button("▶️ Process"):
        try:
            gdf_roads = gpd.read_file(uploaded_roads)
            gdf_polygons = gpd.read_file(uploaded_polygons)
            gdf_lines = gpd.read_file(uploaded_lines) if uploaded_lines else None

            st.info("🔍 Processing intersections...")
            selected = select_restricted_roads(gdf_roads, gdf_polygons, gdf_lines)
            st.session_state.selected_roads = selected
            st.success(f"✅ Found {len(selected)} intersecting roads.")

        except Exception as e:
            st.error(f"❌ Error: {e}")
            st.session_state.selected_roads = None

# Tampilkan hasil jika sudah diproses
if st.session_state.selected_roads is not None:
    selected = st.session_state.selected_roads.copy()
    selected["lon"] = selected.geometry.centroid.x
    selected["lat"] = selected.geometry.centroid.y

    st.map(selected[["lat", "lon"]])

    buffer = io.BytesIO()
    selected.to_file(buffer, driver="GeoJSON")
    buffer.seek(0)

    st.download_button(
        "⬇️ Download Intersected Roads",
        buffer,
        file_name="intersected_roads.geojson",
        mime="application/geo+json"
    )
