import streamlit as st
from predictor import predict


st.set_page_config(
    page_title = "Kia Rio Price Prediction",
    page_icon = "🚙" ,
    layout='centered'
)

st.title("Kia Rio Price Prediction")
st.write('enter car details & click **predict**')
st.subheader("car details")

col1 , col2 = st.columns(2)

with col1:
    mileage = st.number_input("Mileage", 0, 520000, 135000)
    date = st.number_input('Date', 2006, 2017, 2014)
with col2:
    color = st.radio('Color of Your Car', ["Dark", "Light"])
    insurance = st.number_input("Insurance", 1, 12)

if st.button("Predict the price"):
    input_data = {
        "mileage": mileage,
        "date": date,
        "insurance": insurance,
        "color_2_cat": color
    }
    prediction = predict(input_data=input_data)
    st.divider()
    st.success(prediction)
