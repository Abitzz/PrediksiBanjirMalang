import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import RocCurveDisplay
from geocube.api.core import make_geocube
import streamlit as st

# Define paths to the five files
file_paths = [
    "input/studyarea_blimbing.pkl",
    "input/studyarea_kedungkandang.pkl",
    "input/studyarea_klojen.pkl",
    "input/studyarea_lowokwaru.pkl",
    "input/studyarea_sukun.pkl"
]

def load_and_merge_files(file_paths):
    # Load and merge the files into a single GeoDataFrame
    dfs = [pd.read_pickle(file) for file in file_paths]
    merged_df = pd.concat(dfs, ignore_index=True)
    return merged_df

sidebar_logo=("images/logoUMMsaja.png")
main_body_logo=("images/logoUMMsaja.png")

#st.logo(sidebar_logo, icon_image=main_body_logo)

def main():
    st.title('Pemetaan Kerentanan Banjir')

    # Pilihan halaman
    page_options = ['Random Forest', 'Support Vector Machine']

    # Pilihan halaman menggunakan selectbox
    selected_page = st.selectbox('Machine Learning', page_options)

    # Menampilkan konten halaman yang dipilih
    if selected_page == 'Random Forest':
        show_page_1()
    elif selected_page == 'Support Vector Machine':
        show_page_2()

def show_page_1():
    st.subheader('Menggunakan Machine Learning RF')
    st.write("Random forest merupakan metode bagging yaitu metode yang membangkitkan "
         "sejumlah tree dari data sample dimana pembuatan satu tree pada saat training tidak "
         "bergantung pada tree sebelumnya kemudian keputusan diambil berdasarkan voting "
         "terbanyak (Wibowo, Saikhu, & Soelaiman, 2016).")

    # Input dari pengguna untuk persentase pembagian data
    st.sidebar.header("Pengaturan Pembagian Data")
    test_size = st.sidebar.slider('Persentase Data Testing', 0.1, 1.0, 0.2)
    val_size = st.sidebar.slider('Persentase Data Validasi dari Data Training', 0.1, 1.0, 0.2)

    # Input Jumlah Pohon(tree)
    st.sidebar.header("Atur Banyaknya Pohon")
    jum_pohon = st.sidebar.number_input('Masukkan Jumlah Pohon:', min_value=0, max_value=10000, value=100)

    # Fungsi untuk melatih model dan menampilkan peta
    def train_and_display_map():
        # Baca file shapefile atau pickle yang telah kita buat di artikel sebelumnya
        df = gpd.read_file("input/points_data_new.shp")

        # Gabungan shapefile digunakan sebagai area studi
        df_SA = load_and_merge_files(file_paths)

        # Definisikan variabel dependen yang perlu diprediksi (label)
        Y = df["ID"].values

        # Definisikan variabel independen. Juga hapus geometri dan label
        X = df.drop(labels=["ID", "geometry"], axis=1)
        features_list = list(X.columns)  # Daftar fitur untuk merangking kepentingannya nanti

        # Bagi data menjadi pelatihan (training), validasi (validation), dan pengujian (testing)
        X_train_val, X_test, y_train_val, y_test = train_test_split(X, Y, test_size=test_size, shuffle=True, random_state=42)
        val_size_adjusted = val_size / (1 - test_size)  # Adjust validation size relative to the training set
        X_train, X_val, y_train, y_val = train_test_split(X_train_val, y_train_val, test_size=val_size_adjusted, shuffle=True, random_state=42)

        # RANDOM FOREST
        model = RandomForestClassifier(n_estimators=jum_pohon, random_state=42)  # Menggunakan nilai default dari parameter.

        # Latih model pada data pelatihan
        model.fit(X_train, y_train)

        # Persiapkan data untuk prediksi
        X_SA = df_SA.drop(labels=["ID", "geometry"], axis=1)

        # Prediksi kerentanan banjir
        prediction_SA = model.predict(X_SA)
        prediction_prob = model.predict_proba(X_SA)

        # Tambahkan probabilitas prediksi ke GeoDataFrame
        df_SA['FSM'] = prediction_prob[:, 1]

        # Konversi shapefile titik menjadi grid (raster dalam memori)
        out_grid = make_geocube(vector_data=df_SA, measurements=["FSM"], resolution=(-0.0001, 0.0001))

        # Konversi xarray DataArray menjadi array NumPy untuk plotting
        flood_susceptibility = out_grid["FSM"].data

        # Tampilkan hasil langsung tanpa menyimpan ke file
        st.subheader('Peta Kerentanan Banjir')
        st.write("Peta Kerentanan Banjir menunjukkan area dengan berbagai tingkat kerentanan terhadap banjir. "
                "Peta ini dihasilkan berdasarkan probabilitas prediksi dari model Random Forest. Area dengan nilai lebih tinggi "
                "(berwarna merah) lebih rentan terhadap banjir.")

        # Membuat colormap dengan gradasi halus
        cmap = plt.get_cmap('RdYlGn_r')

        fig, ax = plt.subplots(figsize=(10, 10))
        cax = ax.imshow(flood_susceptibility, cmap=cmap, origin='upper')
        ax.set_title('Peta Kerentanan Banjir')
        ax.set_xlabel('Longitude')
        ax.set_ylabel('Latitude')
        fig.colorbar(cax, ax=ax, label='Kerentanan Banjir')
        st.pyplot(fig)

        # Tampilkan matriks korelasi untuk dataset
        numeric_df = df.select_dtypes(include=['number'])
        corrMatrix = numeric_df.corr()

        # Tampilkan matriks korelasi
        st.subheader('Matriks Korelasi')
        st.write("Matriks korelasi menunjukkan koefisien korelasi antara variabel-variabel dalam dataset. "
                "Setiap sel dalam matriks menunjukkan korelasi antara dua variabel. Ini membantu memahami "
                "bagaimana perubahan dalam satu variabel berhubungan dengan perubahan dalam variabel lain.")
        fig_corr, ax_corr = plt.subplots(figsize=(10, 10))
        sns.heatmap(corrMatrix, annot=True, linewidths=.5, ax=ax_corr)
        st.pyplot(fig_corr)

        # Plot Kurva ROC
        st.subheader('Kurva ROC')
        st.write("Kurva ROC (Receiver Operating Characteristic) adalah plot grafis yang mengilustrasikan kemampuan diagnostik "
                "dari sistem klasifikasi biner saat ambang batas diskriminasi bervariasi. Plot ini menunjukkan trade-off antara "
                "sensitivitas (atau TPR) dan spesifisitas (1 - FPR). Model dengan kurva ROC yang lebih dekat ke sudut kiri atas "
                "menunjukkan performa yang lebih baik.")
        fig_roc, ax_roc = plt.subplots()
        model_disp = RocCurveDisplay.from_estimator(model, X_test, y_test, ax=ax_roc, alpha=0.8)
        st.pyplot(fig_roc)

        # Tombol untuk melatih model dan menampilkan peta
    if st.sidebar.button('Latih Model dan Tampilkan Peta'):
        train_and_display_map()


def show_page_2():
    st.subheader('Menggunakan Machine Learning SVM')
    st.write("Metode Support Vector Machine(SVM) merupakan sistem pembelajaran yang "
            "menggunakan ruang hipotesis yang berupa fungsi-fungsi linear di dalam sebuah "
            "fitur yang memiliki dimensi tinggi dan dilatih dengan menggunakan algoritma "
            "pembelajaran berdasarkan teori optimasi.")

    # Input dari pengguna untuk persentase pembagian data
    st.sidebar.header("Pengaturan Pembagian Data")
    test_size = st.sidebar.slider('Persentase Data Testing', 0.1, 1.0, 0.2)
    val_size = st.sidebar.slider('Persentase Data Validasi dari Data Training', 0.1, 1.0, 0.2)

    # Input dari pengguna untuk memilih kernel SVM
    st.sidebar.header("Pengaturan Kernel SVM")
    kernel = st.sidebar.selectbox('Pilih Kernel untuk SVM',
        ('rbf', 'sigmoid', 'poly')
    )

    # Fungsi untuk melatih model dan menampilkan peta
    def train_and_display_map():
        # Baca dan gabungkan file shapefile atau pickle
        df = gpd.read_file("input/points_data_new.shp")

        # Gabungan shapefile digunakan sebagai area studi
        df_SA = load_and_merge_files(file_paths)
    
        # Definisikan variabel dependen yang perlu diprediksi (label)
        Y = df["ID"].values
    
        # Definisikan variabel independen. Juga hapus geometri dan label
        X = df.drop(labels=["ID", "geometry"], axis=1)
        features_list = list(X.columns)  # Daftar fitur untuk merangking kepentingannya nanti
    
        # Bagi data menjadi pelatihan (training), validasi (validation), dan pengujian (testing)
        X_train_val, X_test, y_train_val, y_test = train_test_split(X, Y, test_size=test_size, shuffle=True, random_state=42)
        val_size_adjusted = val_size / (1 - test_size)  # Adjust validation size relative to the training set
        X_train, X_val, y_train, y_val = train_test_split(X_train_val, y_train_val, test_size=val_size_adjusted, shuffle=True, random_state=42)
    
        # SVM
        model = SVC(kernel=kernel, probability=True)  # Menggunakan nilai default dari parameter.
    
        # Latih model pada data pelatihan
        model.fit(X_train, y_train)
    
        # Persiapkan data untuk prediksi
        X_SA = df_SA.drop(labels=["ID", "geometry"], axis=1)
    
        # Prediksi kerentanan banjir
        prediction_SA = model.predict(X_SA)
        prediction_prob = model.predict_proba(X_SA)
    
        # Tambahkan probabilitas prediksi ke GeoDataFrame
        df_SA['FSM'] = prediction_prob[:, 1]
    
        # Konversi shapefile titik menjadi grid (raster dalam memori)
        out_grid = make_geocube(vector_data=df_SA, measurements=["FSM"], resolution=(-0.0001, 0.0001))
    
        # Konversi xarray DataArray menjadi array NumPy untuk plotting
        flood_susceptibility = out_grid["FSM"].data
    
        # Tampilkan hasil langsung tanpa menyimpan ke file
        st.subheader('Peta Kerentanan Banjir (FSM)')
        st.write("Peta Kerentanan Banjir (FSM) menunjukkan area dengan berbagai tingkat kerentanan terhadap banjir. "
             "Peta ini dihasilkan berdasarkan probabilitas prediksi dari model SVM. Area dengan nilai lebih tinggi "
             "(berwarna merah) lebih rentan terhadap banjir.")
    
        cmap = plt.get_cmap('RdYlGn_r')

        fig, ax = plt.subplots(figsize=(10, 10))
        cax = ax.imshow(flood_susceptibility, cmap=cmap, origin='upper')
        ax.set_title('Peta Kerentanan Banjir')
        ax.set_xlabel('Longitude')
        ax.set_ylabel('Latitude')
        fig.colorbar(cax, ax=ax, label='Kerentanan Banjir')
        st.pyplot(fig)

        # Tampilkan matriks korelasi untuk dataset
        numeric_df = df.select_dtypes(include=['number'])
        corrMatrix = numeric_df.corr()
        st.subheader('Matriks Korelasi')
        st.write("Matriks korelasi menunjukkan koefisien korelasi antara variabel-variabel dalam dataset. "
                "Setiap sel dalam matriks menunjukkan korelasi antara dua variabel. Ini membantu memahami "
                "bagaimana perubahan dalam satu variabel berhubungan dengan perubahan dalam variabel lain.")
        fig_corr, ax_corr = plt.subplots(figsize=(10, 10))
        sns.heatmap(corrMatrix, annot=True, linewidths=.5, ax=ax_corr)
        st.pyplot(fig_corr)

        # Plot Kurva ROC
        st.subheader('Kurva ROC')
        st.write("Kurva ROC (Receiver Operating Characteristic) adalah plot grafis yang mengilustrasikan kemampuan diagnostik "
                "dari sistem klasifikasi biner saat ambang batas diskriminasi bervariasi. Plot ini menunjukkan trade-off antara "
                "sensitivitas (atau TPR) dan spesifisitas (1 - FPR). Model dengan kurva ROC yang lebih dekat ke sudut kiri atas "
                "menunjukkan performa yang lebih baik.")
        fig_roc, ax_roc = plt.subplots()
        model_disp = RocCurveDisplay.from_estimator(model, X_test, y_test, ax=ax_roc, alpha=0.8)
        st.pyplot(fig_roc)
    

    # Tombol untuk melatih model dan menampilkan peta
    if st.sidebar.button('Latih Model dan Tampilkan Peta'):
        train_and_display_map()


if __name__ == '__main__':
    main()
