import streamlit as st
import time
import csv
import requests
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as Bs
from lxml import etree
from tqdm import tqdm
import json
import os
import re
import pandas as pd
import sqlite3
from io import BytesIO


def yp_au_scrape(clue="", loc_clue="", direct_url=""):
    try:
        # clue = "chirofactor"
        # loc_clue = "Brisbane"
        output_file = "Output_Files/yp_au.csv"

        if direct_url:
            main_url = direct_url
        else:
            main_url = f"https://www.yellowpages.com.au/search/listings?clue={clue}&locationClue={loc_clue}"

        st.write(f"Searching URL: {main_url}")
        main_resp = requests.get(main_url, headers={"User-Agent": "Mozilla/5.0"})
        main_soup = Bs(main_resp.text, "html.parser")
        dom = etree.HTML(str(main_soup))

        card_list = main_soup.find_all(
            "div",
            class_="Box__Div-sc-dws99b-0 iOfhmk MuiPaper-root MuiCard-root PaidListing MuiPaper-elevation1 MuiPaper-rounded",
        )
        st.write(len(card_list))

        All_result_dict = {}
        for cnt, card in enumerate(card_list):
            try:
                card_dom = etree.HTML(str(card))
                title = "".join(
                    card_dom.xpath(
                        "//div[@class='Box__Div-sc-dws99b-0 iOfhmk MuiPaper-root MuiCard-root PaidListing MuiPaper-elevation1 MuiPaper-rounded']//a[@class='MuiTypography-root MuiLink-root MuiLink-underlineNone MuiTypography-colorPrimary']//h3/text()"
                    )
                )
                phone_No = "".join(
                    card_dom.xpath(
                        "//button[@class='MuiButtonBase-root MuiButton-root MuiButton-text ButtonPhone MuiButton-textPrimary MuiButton-fullWidth']//span/text()"
                    )
                )
                website = "".join(
                    card_dom.xpath(
                        "//a[@class='MuiButtonBase-root MuiButton-root MuiButton-text ButtonWebsite MuiButton-textSecondary MuiButton-fullWidth']/@href"
                    )
                )
                yp_url = "https://www.yellowpages.com.au" + "".join(
                    card_dom.xpath(
                        "//div[@class='Box__Div-sc-dws99b-0 iOfhmk MuiPaper-root MuiCard-root PaidListing MuiPaper-elevation1 MuiPaper-rounded']//a[@class='MuiTypography-root MuiLink-root MuiLink-underlineNone MuiTypography-colorPrimary']/@href"
                    )
                )
                yp_resp = requests.get(yp_url, headers={"User-Agent": "Mozilla/5.0"})
                yp_soup = Bs(yp_resp.text, "html.parser")
                yp_dom = etree.HTML(str(yp_soup))
                email = "".join(
                    yp_dom.xpath(
                        "//a[@class='contact contact-main contact-email']/@data-email"
                    )
                )

                if not email:
                    Google_Search_url = (
                        f"https://www.google.com/search?q={title}+email+address"
                    )
                    search_resp = requests.get(
                        Google_Search_url, headers={"User-Agent": "Mozilla/5.0"}
                    )
                    email_pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,4}"
                    email = ", ".join(re.findall(email_pattern, search_resp.text))

                address = "".join(
                    yp_dom.xpath(
                        "//div[@class='listing-address mappable-address mappable-address-with-poi']/text()"
                    )
                )

                result_dict = {
                    "YP URL": yp_url,
                    "Business Name": title,
                    "Website URL": website,
                    "Phone Number": phone_No,
                    "Physical Address": address,
                    "Email": email,
                }
                All_result_dict[result_dict["Business Name"]] = result_dict

                headers = result_dict.keys()

                df = pd.DataFrame([result_dict.values()], columns=headers)

                if cnt == 0:
                    st_df = st.dataframe(df)
                else:
                    st_df.add_rows(df)

            except Exception as e:
                print(e)
                pass

        result_df = pd.DataFrame(All_result_dict.values())
        json_format = json.dumps(All_result_dict)
        print(All_result_dict)

        csv_col, json_col = st.columns(2)

        if csv_col.download_button(
            "Download CSV",
            result_df.to_csv(index=False).encode("utf-8"),
            file_name="output.csv",
        ):
            st.success("CSV file downloaded successfully!")

        if json_col.download_button(
            "Download JSON",
            json_format.encode("utf-8"),
            file_name="output.json",
        ):
            st.success("JSON file downloaded successfully!")

        # Create a temporary file for SQLite database
        # with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as temp_file:
        #     temp_file_name = temp_file.name

        #     # Convert DataFrame to SQLite database
        #     with sqlite3.connect(temp_file_name) as conn:
        #         result_df.to_sql(
        #             "your_table_name", conn, index=False, if_exists="replace"
        #         )

        # # Create download button
        # if st.button("Download SQLite"):
        #     st.download_button(
        #         label="Download SQLite", data=temp_file_name, key="download_sqlite"
        #     )
        #     st.success("SQLite database file downloaded successfully!")

    except Exception as e:
        st.write("Can't Find Data")
        print(yp_url, e)
