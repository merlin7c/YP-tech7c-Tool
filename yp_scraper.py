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
import math


def yp_au_scrape(clue="", loc_clue="", direct_url=""):
    All_result_dict = {}
    try:
        # clue = "chirofactor"
        # loc_clue = "Brisbane"
        output_file = "Output_Files/yp_au.csv"

        if direct_url:
            main_url = direct_url
        else:
            main_url = f"https://www.yellowpages.com.au/search/listings?clue={clue}&locationClue={loc_clue}"

        st.write(f"Searching URL: {main_url}")
        progress_bar = st.progress(0)
        main_resp = requests.get(main_url, headers={"User-Agent": "Mozilla/5.0"})
        main_soup = Bs(main_resp.text, "html.parser")
        dom = etree.HTML(str(main_soup))

        item_count = int(
            main_soup.find(
                "h2",
                class_="MuiTypography-root jss310 MuiTypography-body2 MuiTypography-paragraph",
            )
            .text.strip()
            .split()[0]
        )
        cnt = 0
        max_page = math.ceil(item_count / 35)
        print(max_page)
        for page in range(1, max_page):
            main_resp = requests.get(
                f"{main_url}&pageNumber={page}", headers={"User-Agent": "Mozilla/5.0"}
            )
            print(f"{main_url}&pageNumber={page}")

            main_soup = Bs(main_resp.text, "html.parser")
            dom = etree.HTML(str(main_soup))

            card_list = main_soup.find_all("div", class_="Box__Div-sc-dws99b-0 dAyAhR")
            print(len(card_list))
            for card in card_list:
                try:
                    card_dom = etree.HTML(str(card.parent()))
                    title = "".join(
                        card_dom.xpath(
                            "//a[@class='MuiTypography-root MuiLink-root MuiLink-underlineNone MuiTypography-colorPrimary']//h3/text()"
                        )[:1]
                    )

                    phone_No = "".join(
                        card_dom.xpath(
                            "//button[@class='MuiButtonBase-root MuiButton-root MuiButton-text ButtonPhone MuiButton-textPrimary MuiButton-fullWidth']//span/text()"
                        )[:1]
                    )
                    website = "".join(card_dom.xpath("//a[.='View Website']/@href")[:1])
                    yp_url = "https://www.yellowpages.com.au" + "".join(
                        card_dom.xpath(
                            "//a[@class='MuiTypography-root MuiLink-root MuiLink-underlineNone MuiTypography-colorPrimary']/@href"
                        )[:1]
                    )
                    yp_resp = requests.get(
                        yp_url, headers={"User-Agent": "Mozilla/5.0"}
                    )
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
                        email_pattern = (
                            r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,4}"
                        )
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

                    cnt += 1
                except Exception as e:
                    print(e)

            progress_bar.progress((page / (max_page - 1)))

    except Exception as e:
        print(e)

    return All_result_dict
