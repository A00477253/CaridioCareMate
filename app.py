# app.py
import streamlit as st
from home_page import show_home_page
from prediction import show_prediction_page

# Define a function to control the page rendering
def main():
    st.sidebar.title("Navigation")
    menu = ["Home", "Prediction"]
    choice = st.sidebar.selectbox("Menu", menu)

    if choice == "Home":
        show_home_page()
    elif choice == "Prediction":
        show_prediction_page()

if __name__ == "__main__":
    main()
