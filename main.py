import streamlit as st
from yp_scraper import yp_au_scrape

st.header("YP Tech7c Tool")

st.write("Enter the Searching Data")

# Country dropdown options
countries = ["Austrailia", "USA", "Canada", "New Zealand"]

# Form inputs
country = st.selectbox("Select Country", countries)
name = st.text_input("Search Name")
city = st.text_input("City")

# Submit button
if st.button("Collect Data"):
    # Validation check
    if country and name and city:
        st.write(f"Collected Data for : {name}, {city}, {country}")
    else:
        st.warning("Please fill in all the inputs before collecting data.")
