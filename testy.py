import joblib
import numpy as np
import streamlit as st
from PIL import Image
from db import ConnectDB

# import the model
model = joblib.load('model.pkl')
st.title("Petroleum Price Prediction")

# Flag to control the state of the login and signup buttons
login_button_disabled = False
signup_button_disabled = False

def sel_callback():
    st.session_state.agree = st.session_state.sel

# side bar menu creations 
menu = ['Home', 'Login', 'SignUp']
side_choice = st.sidebar.selectbox("Menu", menu)

if side_choice == "Home":
    st.subheader("Home")

elif side_choice == "Login":
    st.sidebar.subheader("Login")
    # form fields defintion
    username = st.sidebar.text_input("Username")
    password = st.sidebar.text_input("Password", type="password")

    if st.sidebar.checkbox("Login", key='login_button'):
        result = ConnectDB.login_user(
            username=username,
            password=password
        )

        if result:
            st.sidebar.success(f"Logged-In as {username}")
            side_choice = None

            menu = ['Prediction', 'Logout']
            side_choice = st.sidebar.selectbox("Menu", menu)

            if side_choice == "Prediction":
                st.subheader("Crude Oil Price Prediction")
                st.write("enter the features for that corresponds to the dataset except the closing price and date column")

                # defining the input field
                input_vol = st.text_input('volume')
                input_open = st.text_input('open')
                input_high = st.text_input('high')
                input_low = st.text_input('low')

                # Create a button to submit input and get a prediction
                predict = st.button("Submit")
                if predict:
                    if not input_vol:
                        st.warning("volume field is required")
                    elif not input_open:
                        st.warning("open field is required") 
                    elif not input_low:
                        st.warning("low field is required") 
                    elif not input_low:
                        st.input_high("high field is required")      
                    else:
                        # Volume	Open	High	Low
                        features = np.array([input_vol, input_open, input_high, input_low], dtype=np.float64)
                        # Make prediction
                        prediction = model.predict(features.reshape(1, -1))
                        st.write("Closing Price Result")
                        st.write(prediction)

                # Disable the login button after clicking
                login_button_disabled = True

elif side_choice == "SignUp":
    st.subheader("SignUp")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("SignUp", key='signup_button'):
        ConnectDB.create_user_table()
        ConnectDB.create_user(
            username=username,
            password=password
        )
        st.success("Account created")
        st.info("Goto Login")

        # Disable the signup button after clicking
        signup_button_disabled = True
