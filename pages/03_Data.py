import streamlit as st
import rasterio
from rasterio.plot import show
import matplotlib.pyplot as plt

# Judul Aplikasi
st.title('Visualisasi Data Geospasial')

# Daftar file .tiff yang tersedia
tiff_files = {
    'DEM': './input/DEM_KotaMalang.tif',
    'Aspect': './input/Aspect_test.tif',
    'Curvature': './input/Curvature_test.tif',
    'Slope': './input/Slope(degrees)_test.tif',
    'TWI': './input/TWI1.tif',
    'DTRoad': './input/Road_test.tif',
    'DTRiver': './input/River_test.tif',
    'DTDrainage': './input/Irrigation_test.tif'
}

# Pilihan Select Box
selected_data = st.selectbox('Pilih Data untuk Ditampilkan', list(tiff_files.keys()))

# Baca file .tiff yang dipilih
file_path = tiff_files[selected_data]
with rasterio.open(file_path) as src:
    fig, ax = plt.subplots(figsize=(10, 10))
    show(src, ax=ax, title=selected_data)
    st.pyplot(fig)
