import streamlit as st
import requests
from bs4 import BeautifulSoup

st.header('Budget Food Hub!')

url = "http://quotes.toscrape.com"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
# print(soup.prettify())
quotes = soup.find('span', class_='text').text
# print(quotes)
# print(response.text)
st.write(quotes)
# st.write(response.text)