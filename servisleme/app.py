import streamlit as st
import pandas as pd
import joblib
import os


def main():
    
    st.sidebar.title('Streamlit ile ML Uygulaması')
    selected_page = st.sidebar.selectbox('Sayfa Seçiniz..',["-","Tahmin Yap","Hakkında"])

    if selected_page == "-":
        st.title('Kiralık ev sorgulama uygulamasına Hoşgeldiniz 👋')

        st.markdown(
            """
            Bu proje makine öğrenmesi uygulamalarının web ortamında streamlit
            kullanılarak yayınlanmasına örnek olarak geliştirilmiştir.HepsiEmlak sitesi üzerinden Ankara ilindeki kiralık evlerin verileri çekilmiştir
            ve incelenmiştir. Bu veriler kullanılarak makine öğrenmesi modelleri eğitilmiş ve projeye dahil edilmiştir.
            
            """)
        st.info("Sol taraftaki Tahmin Yap kısmı çalışmıyorsa cmd kısmında streamlit run yazdığınız dizinin servisleme dosyası olması gerekiyor.")
        


    if selected_page == "Tahmin Yap":
        predict()
    
    if selected_page == "Hakkında":
        about() 
    

def about():
    st.title('Geliştirici Bilgileri')
    st.subheader('Github Adresi : [Ronay Öktem](https://github.com/Poeron/)')
    st.subheader('Linkedin Adresi : [Ronay Öktem](https://www.linkedin.com/in/ronayoktem)')
    st.subheader('Mail Adresi : ronay_oktem1@hotmail.com')



# Mevcut çalışma dizinini al
current_directory = os.getcwd()

def predict():
    # Load the pre-trained Gradient Boosting model
    gb_model = joblib.load(f"{current_directory}\\gradient_boosting_regressor.joblib")

    # Load the data
    data = pd.read_excel(f"{current_directory}\\veri.xlsx")

    # Streamlit App
    st.title('Gradient Boosting Model App')
    konumlar = pd.read_csv(f"{current_directory}\\one_hot_column_names.csv")

    # Get Konum bilgisi interactively from the user
    user_location = st.selectbox('Konum Seçiniz..', konumlar)


    # Example manual input values for prediction
    manual_input = pd.DataFrame({
        'Oda Sayısı': [st.slider("Select Oda Sayısı", min_value=1, max_value=10, value=5)],
        'm²': [st.slider("Select m²", min_value=50, max_value=300, value=100)],
        'Bina Yaşı': [st.slider("Select Bina Yaşı", min_value=1, max_value=20, value=3)],
        'Bulunduğu Kat': [st.slider("Select Bulunduğu Kat", min_value=1, max_value=21, value=5)],
        # Set the user-provided location to True and others to False
        **{f'{location}': [True] if location.lower() == user_location.lower() else [False] for location in data.columns[5:]}
    })

    # Make predictions with manual input
    manual_prediction = gb_model.predict(manual_input)

    # Display the predicted value
    st.subheader('Manual Prediction:')
    st.write(f'Manual Prediction: {manual_prediction[0]}')


if __name__ == "__main__":
    main()