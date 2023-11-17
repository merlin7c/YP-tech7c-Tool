import streamlit as st
from yp_scraper import yp_au_scrape

st.header("YP Tech7c Tool")

st.write("Enter the Searching Data")

# Country dropdown options
countries = ["Australia", "USA", "Canada", "New Zealand"]

# Form inputs
country = st.selectbox("Select Country", countries)
name = st.text_input("Search Name")
city = st.text_input("City")
# st.write("OR")
# Center and change font color of "OR"
st.markdown(
    "<h3 style='text-align:center; color:blue;'>OR</h3>",
    unsafe_allow_html=True,
)
direct_url = st.text_input("Direct URL")

# Submit button
if st.button("Collect Data"):
    # Validation check
    if country and name and city or direct_url:
        if direct_url:
            # st.write(f"Collecting Data for : {name}, {city}, {country}")
            yp_au_scrape(name, city, direct_url)
            
        else:
            st.write(f"Collecting Data for : {name}, {city}, {country}")
            yp_au_scrape(name, city)

    else:
        st.warning("Please fill in all the inputs before collecting data.")
