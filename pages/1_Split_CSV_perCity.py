import streamlit as st
import pandas as pd

def filter_by_city(df, city_name):
    return df[df['grid_id'].str.split().str[1] == city_name]

def split_dataframe(df, chunk_size=5000):
    return [df[i:i+chunk_size] for i in range(0, len(df), chunk_size)]

st.title("✅ Step 1: Split CSV by City Name & Chunked Download")

uploaded_file = st.file_uploader("📤 Upload your CSV file", type=["csv"])
city_name = st.text_input("🏙️ Please Enter City Name (e.g., Jakarta)")

if "processed" not in st.session_state:
    st.session_state.processed = False

if st.button("🚀 Process") and uploaded_file and city_name:
    with st.spinner("⏳ Processing data... Please wait."):
        df = pd.read_csv(uploaded_file)

        if "grid_id" not in df.columns:
            st.error("❌ The uploaded CSV must contain a 'grid_id' column.")
            st.session_state.processed = False
        else:
            filtered_df = filter_by_city(df, city_name)
            st.session_state.filtered_df = filtered_df
            st.session_state.city_name = city_name
            st.session_state.processed = True

if st.session_state.processed:
    filtered_df = st.session_state.filtered_df
    city_name = st.session_state.city_name

    st.success(f"✅ Found {len(filtered_df)} rows for city: {city_name}")
    st.dataframe(filtered_df)

    chunks = split_dataframe(filtered_df, chunk_size=5000)

    for i, chunk in enumerate(chunks, start=1):
        csv_data = chunk.to_csv(index=False).encode("utf-8")
        st.download_button(
            label=f"📥 Download {city_name}_data_part{i}.csv ({len(chunk)} rows)",
            data=csv_data,
            file_name=f"{city_name}_data_part{i}.csv",
            mime="text/csv"
        )
