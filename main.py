import config
import os
import requests
import bs4
# import lxml
# import pprint
from selenium import webdriver
# from selenium.webdriver.remote import webelement
import time

# ------------------------------------------------ bs4 ------------------------------------------------ #
response = requests.get(os.environ.get('TRULIA_TARGET_URL'))
response.raise_for_status()
website_html = response.text

soup = bs4.BeautifulSoup(website_html, 'lxml')

property_listings_link_tags = soup.find_all('a', 'PropertyCard__StyledLink-m1ur0x-3')

property_listings_links = [
    'https://www.trulia.com/' + property_listings_link_tag.get('href')
    for property_listings_link_tag
    in property_listings_link_tags
]

property_listings_price_divs = soup.select(
    '.Text__TextBase-sc-1cait9d-0-div.Text__TextContainerBase-sc-1cait9d-1.keMYfJ'
)

property_listings_prices = [
    property_listings_price_div.string
    for property_listings_price_div
    in property_listings_price_divs
]

property_listings_address_divs = soup.select(
    'a .Text__TextBase-sc-1cait9d-0-div.Text__TextContainerBase-sc-1cait9d-1.dZyoXR'
)

property_listings_addresses = [
    property_listings_address.get_text()
    for property_listings_address
    in property_listings_address_divs
]

property_listings_full_addresses = []

for property_listings_address_index in range(0, len(property_listings_addresses) - 1, 2):
    property_listing_full_address = ''.join(
        property_listings_addresses[property_listings_address_index] +
        ', ' +
        property_listings_addresses[property_listings_address_index + 1]
    )
    property_listings_full_addresses.append(property_listing_full_address)

# ------------------------------------------------ selenium ------------------------------------------------ #


def wait(secs):
    time.sleep(secs)


def get_all_fields():
    global address_input_field, price_input_field, link_input_field, submit_form_button
    address_input_field = driver.find_element_by_xpath(
        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input'
    )
    price_input_field = driver.find_element_by_xpath(
        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input'
    )
    link_input_field = driver.find_element_by_xpath(
        '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input'
    )
    submit_form_button = driver.find_element_by_class_name('quantumWizButtonPaperbuttonLabel')


driver = webdriver.Chrome(os.environ.get('CHROME_DRIVER_PATH'))
driver.get(os.environ.get('GOOGLE_FORM_URL'))
driver.maximize_window()

wait(1)

address_input_field = driver.find_element_by_xpath(
    '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input'
)

price_input_field = driver.find_element_by_xpath(
    '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input'
)

link_input_field = driver.find_element_by_xpath(
    '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input'
)

submit_form_button = driver.find_element_by_class_name('quantumWizButtonPaperbuttonLabel')

for property_listing_full_address_index in range(len(property_listings_full_addresses)):
    get_all_fields()

    address_input_field.send_keys(property_listings_full_addresses[property_listing_full_address_index])
    price_input_field.send_keys(property_listings_prices[property_listing_full_address_index])
    link_input_field.send_keys(property_listings_links[property_listing_full_address_index])

    submit_form_button.click()

    wait(1)

    submit_another_response_anchor_tag = driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[1]/div/div[4]/a')
    submit_another_response_anchor_tag.click()

    wait(3)
