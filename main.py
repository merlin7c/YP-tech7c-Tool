import json
import streamlit as st
from yp_scraper import yp_au_scrape
import os
import sqlite3
import pandas as pd


if __name__ == "__main__":
    st.header("YP Tech7c Tool")

    st.write("Enter the Searching Data")

    # Country dropdown options
    countries = ["Australia", "USA", "Canada", "New Zealand"]
    # st.write(os.getcwd())
    # Form inputs
    country = st.selectbox("Select Country", countries)
    name = st.text_input("Search Name")
    city = st.text_input("City")

    st.markdown(
        "<h3 style='text-align:center; color:blue;'>OR</h3>",
        unsafe_allow_html=True,
    )
    direct_url = st.text_input("Direct URL")

    # Submit button
    if st.button("Collect Data"):
        # Validation check
        if country and name and city or direct_url:
            if not direct_url:
                st.write(f"Collecting Data for : {name}, {city}, {country}")
            All_result_dict = yp_au_scrape(name, city, direct_url)

            result_df = pd.DataFrame(All_result_dict.values())
            json_format = json.dumps(All_result_dict)
            # print(All_result_dict)

            csv_col, json_col, sqlite_col = st.columns(3)

            if csv_col.download_button(
                "Download CSV",
                result_df.to_csv(index=False).encode("utf-8"),
                file_name="CSV_output.csv",
            ):
                st.success("CSV file downloaded successfully!")

            if json_col.download_button(
                "Download JSON",
                json_format.encode("utf-8"),
                file_name="JSON_output.json",
            ):
                st.success("JSON file downloaded successfully!")

            # Create a temporary file for SQLite database
            temp_file_name = "yp_sqlite_output.db"
            with sqlite3.connect(temp_file_name) as conn:
                # Replace 'your_table_name' with the desired table name
                result_df.to_sql("yp_table", conn, index=False, if_exists="replace")

            # Create download button for SQLite

            with open(temp_file_name, "rb") as db_file:
                db_bytes = db_file.read()

            if sqlite_col.download_button(
                label="Download SQLite",
                data=db_bytes,
                key="download_sqlite",
                file_name=temp_file_name,
                mime="application/octet-stream",
            ):
                st.success("SQLite database file downloaded successfully!")

        else:
            st.warning("Please fill in all the inputs before collecting data.")
