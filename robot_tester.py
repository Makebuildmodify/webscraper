#!/usr/bin/env python3


import requests
from bs4 import BeautifulSoup
import csv



# Define the URL to fetch
url = "https://business.medfordchamber.com/directory/FindStartsWith?term=%23%21"

# Send an HTTP GET request to the URL with a timeout of 10 seconds
response = requests.get(url, timeout=10)

# Check if the request was successful
if response.status_code == 200:
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all elements with the specified class in the HTML content
    cards = soup.findAll("div", class_="card-body gz-directory-card-body")

    # Open a CSV file to write the output
    with open("cards_info.csv", "w", newline='', encoding='utf-8') as csvfile:
        csvwriter = csv.writer(csvfile)
        
        # Write the header row to the CSV file
        csvwriter.writerow(["Name", "Address", "Phone", "Website"])

        # Iterate over each card found in the HTML content
        for card in cards:
            # Initialize an empty list to hold the card details
            card_details = []

            # Extract and append the name (text inside the first h5 element)
            h5_tag = card.find("h5")
            if h5_tag:
                card_details.append(h5_tag.text.strip())
            else:
                card_details.append("")

            # Extract and append the address (text inside the li element with class "gz-card-address")
            address_li = card.find("li", class_="gz-card-address")
            if address_li:
                address = address_li.get_text(separator=" ", strip=True)
                card_details.append(address)
            else:
                card_details.append("")

            # Extract and append the phone number (text inside the li element with class "gz-card-phone")
            phone_li = card.find("li", class_="gz-card-phone")
            if phone_li:
                phone = phone_li.get_text(separator=" ", strip=True)
                card_details.append(phone)
            else:
                card_details.append("")

            # Extract and append the website URL (href attribute of the a tag inside the li element with class "gz-card-website")
            website_li = card.find("li", class_="gz-card-website")
            if website_li:
                website = website_li.find("a")["href"]
                card_details.append(website)
            else:
                card_details.append("")

            # Write the card details to the CSV file
            csvwriter.writerow(card_details)

        print("Data successfully written to cards_info.csv")

else:
    print(f"Failed to retrieve the page. Status code: {response.status_code}")


