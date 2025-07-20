import streamlit as st
import pandas as pd

def filter_by_city(df, city_name):
    return df[df['grid_id'].str.split().str[1] == city_name]

def split_dataframe(df, chunk_size=5000):
    return [df[i:i+chunk_size] for i in range(0, len(df), chunk_size)]

st.title("Split Data by City Name")

# Upload + input
uploaded_file = st.file_uploader("📤 Upload your CSV file", type=["csv"])
city_name = st.text_input("🏙️ Please Enter City Name (e.g., Jakarta)")

download_option = st.radio(
    "📎 Choose Download Option:",
    ("Download All in One File", "Download in Batches (5000 rows each)")
)

# Initialize session state
if "processed" not in st.session_state:
    st.session_state.processed = False

# Process button logic
if st.button("🚀 Process"):
    st.session_state.processed = False  # Reset flag

    if not uploaded_file:
        st.warning("📤 Please upload a CSV file first!")
    elif not city_name.strip():
        st.warning("🏙️ Please enter a city name before processing!")
    else:
        with st.spinner("⏳ Processing data... Please wait."):
            df = pd.read_csv(uploaded_file)

            if "grid_id" not in df.columns:
                st.error("❌ The uploaded CSV must contain a 'grid_id' column.")
            else:
                filtered_df = filter_by_city(df, city_name)

                if len(filtered_df) == 0:
                    st.warning("⚠️ No data found for the entered city name.")
                else:
                    st.success(f"✅ {len(filtered_df)} rows found for city: {city_name}")
                    st.session_state.processed = True
                    st.session_state.filtered_df = filtered_df
                    st.session_state.city_name = city_name
                    st.session_state.download_option = download_option

# Show download options only if processing is complete
if st.session_state.get("processed", False):
    filtered_df = st.session_state.filtered_df
    city_name = st.session_state.city_name
    download_option = st.session_state.download_option

    if download_option == "Download All in One File":
        csv_data = filtered_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            label=f"📥 Download Full {city_name} Data",
            data=csv_data,
            file_name=f"{city_name}_full_data.csv",
            mime="text/csv"
        )
    else:
        chunks = split_dataframe(filtered_df, chunk_size=5000)
        for i, chunk in enumerate(chunks, start=1):
            csv_data = chunk.to_csv(index=False).encode("utf-8")
            st.download_button(
                label=f"📥 Download {city_name}_part{i}.csv ({len(chunk)} rows)",
                data=csv_data,
                file_name=f"{city_name}_data_part{i}.csv",
                mime="text/csv"
            )
