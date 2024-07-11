#import Library yang dibutuhkan
import streamlit as st

sidebar_logo="images/logo_umm_saja.png"
main_body_logo="images/logo_umm_saja.png"

st.logo(sidebar_logo, icon_image=main_body_logo)

#mengatur tampilan halaman
st.set_page_config(
    page_title="Prediksi Daerah Dampak Banjir",
    page_icon=":earth_asia:",
    layout="wide",
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

st.markdown("<h2 style='text-align: center; color: black;'>Hasil Peta Prediksi</h2>", unsafe_allow_html=True)
st.image('./images/hasil peta machine learning.png')

st.write("<h3> Interpretasi Peta:</h3>",unsafe_allow_html=True)

st.write('Random Forest: Peta dari Random Forest menunjukkan variasi warna yang lebih jelas antara daerah yang berisiko tinggi dan rendah. Ini menunjukkan bahwa model ini bisa mengidentifikasi area dengan risiko banjir tinggi (merah) dan rendah (hijau) dengan cukup baik.')
st.write('SVM: Peta dari SVM terlihat lebih "berbintik" dan kurang tersegregasi. Daerah merah dan hijau tampak bercampur lebih banyak, yang mungkin menunjukkan bahwa model ini memiliki lebih banyak kesalahan dalam memprediksi kerentanan banjir.')

st.markdown("<h2 style='text-align: center; color: black;'>Kurva ROC dari Machine Learning</h2>", unsafe_allow_html=True)
st.image('./images/kurva ROC machine learning.png')

st.markdown("<h3>Interpretasi Kurva ROC:</h3>",unsafe_allow_html=True)

st.write("Random Forest:")
st.write("AUC = 0.82: Ini menunjukkan bahwa model Random Forest memiliki kinerja yang baik dalam memprediksi kerentanan banjir. Dengan nilai AUC yang mendekati 1, model ini mampu membedakan antara area yang berisiko dan tidak berisiko dengan cukup baik.")
st.write("SVM:")
st.write("AUC = 0.69: Nilai ini lebih rendah dibandingkan dengan Random Forest, menunjukkan bahwa kinerja SVM dalam memprediksi kerentanan banjir tidak sebaik Random Forest. Model ini kurang mampu membedakan dengan jelas antara area yang berisiko tinggi dan rendah.")

st.markdown("<h3> Kesimpulan </h3>",unsafe_allow_html=True)
st.write('Random Forest lebih baik dalam memprediksi kerentanan banjir dibandingkan dengan SVM, baik dari hasil peta kerentanan maupun dari nilai AUC pada kurva ROC.')
st.write('Random Forest memberikan peta yang lebih tersegregasi dengan jelas, menunjukkan daerah yang berisiko tinggi dan rendah dengan baik.')
st.write('SVM menunjukkan hasil yang lebih bercampur dan kurang akurat dalam memprediksi kerentanan banjir.')