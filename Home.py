#import Library yang dibutuhkan
import streamlit as st

sidebar_logo="images/logo_umm_saja.png"
main_body_logo="images/logo_umm_saja.png"

st.logo(sidebar_logo, icon_image=main_body_logo)

#mengatur tampilan halaman
st.set_page_config(
    page_title="Prediksi Daerah Dampak Banjir",
    page_icon=":earth_asia:",
    layout="centered",
)

st.image('./images/logo umm berjejer.png', width=300)
#judul halaman
st.title("Prediksi Daerah Dampak Banjir di Malang")

st.subheader("Tentang Website")
st.write("Selamat datang di sistem prediksi banjir kami! "
         "Kami mempersembahkan solusi inovatif untuk membantu Anda memahami "
         "dan mengelola potensi risiko banjir di wilayah Anda. Melalui "
         "penggunaan Geographic Information System (GIS), "
         "kami mengembangkan sistem yang memanfaatkan data spasial dan "
         "data histori banjir untuk memprediksi daerah dampak banjir dengan menggunakan Machine Learning.")

st.write("Terima kasih telah mengunjungi website kami. Kami sangat menghargai umpan balik dari Anda untuk membantu kami meningkatkan layanan dan konten. "
         "Mohon luangkan waktu sejenak untuk memberikan penilaian pada kelompok kami.")
if st.button('Beri Penilaian'):
    st.markdown(
    """
    <style>
    .button {
        display: inline-block;
        padding: 10px 20px;
        font-size: 16px;
        cursor: pointer;
        text-align: center;
        text-decoration: none;
        outline: none;
        color: #fff;
        background-color: #4CAF50;
        border: none;
        border-radius: 15px;
        box-shadow: 0 9px #999;
    }

    .button:hover {background-color: #3e8e41}

    .button:active {
        background-color: #3e8e41;
        box-shadow: 0 5px #666;
        transform: translateY(4px);
    }
    </style>
    <a href="https://forms.gle/AASv92LsXara6Rer7" target="_blank" class="button">Beri Penilaian</a>
    """,
    unsafe_allow_html=True
)
