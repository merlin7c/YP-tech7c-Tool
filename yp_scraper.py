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


def yp_au_scrape(clue, loc_clue, country):
    clue = "chirofactor"
    loc_clue = "Brisbane"
    output_file = "/content/drive/MyDrive/Upwork_data/YP AU/yp_au.csv"
    headers = [
        "YP URL",
        "Business Name",
        "Website URL",
        "Phone Number",
        "Physical Address",
        "Email",
    ]
    with open(output_file, "w", newline="", encoding="utf-8") as output_csv:
        csvwriter = csv.writer(output_csv)
        csvwriter.writerow(headers)

    main_url = f"https://www.yellowpages.com.au/search/listings?clue={clue}&locationClue={loc_clue}"
    main_resp = requests.get(main_url, headers={"User-Agent": "Mozilla/5.0"})
    main_soup = Bs(main_resp.text, "html.parser")
    dom = etree.HTML(str(main_soup))

    result_list = []
    for card in main_soup.find_all(
        "div",
        class_="Box__Div-sc-dws99b-0 iOfhmk MuiPaper-root MuiCard-root PaidListing MuiPaper-elevation1 MuiPaper-rounded",
    ):
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
        email = yp_soup.find("a", class_="contact contact-main contact-email")[
            "data-email"
        ]
        address = "".join(
            yp_dom.xpath(
                "//div[@class='listing-address mappable-address mappable-address-with-poi']/text()"
            )
        )
        result = [yp_url, title, website, phone_No, address, email]
        print(result)
        result_list.append(result)

    with open(output_file, "a", newline="", encoding="utf-8") as output_csv:
        csvwriter = csv.writer(output_csv)
        csvwriter.writerows(result_list)
