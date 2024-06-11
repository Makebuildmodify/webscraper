#!/usr/bin/env python3


################################################################################
# RRRRRRR  EEEEEEEE    AAAAA    DDDDDDD   MMMMM   MMMMM   EEEEEEEE  !!!!!!!!!! #
# RRR   RR EE         AA   AA   DD    DD  MM MM MM MM MM  EE        !!!!!!!!!! #
# RRRRRRR  EEEEE     AAAAAAAAA  DD    DD  MM  MM  MM  MM  EEEEE     !!!!!!!!!! #
# RRR   RR EE       AA       AA DD    DD  MM      MM      EE                  #
# RRR   RR EEEEEEEE AA       AA DDDDDDD   MM      MM      EEEEEEEE  !!!!!!!!!! #
################################################################################

# Blakely,

# Be sure to read all of the comments to get a better idea of what is happening.

# This script fetches business card information from a specified URL and writes
# the details (Name, Address, Phone, and Website) to a CSV file.

# Key Points:
# 1. Sends an HTTP GET request to fetch the HTML content of the specified URL.
# 2. Parses the HTML content using BeautifulSoup to find business card elements.
# 3. Extracts relevant details from each card and stores them in a list.
# 4. Writes the structured data to a CSV file using csvwriter.writerow.
# 5. Using a list for card details ensures that each piece of information is
#    correctly aligned with the corresponding column in the CSV file.

# If you need any further assistance, feel free to reach out.

# Justin

################################################################################

import requests
from bs4 import BeautifulSoup
import csv


# Define the URL to fetch
url = "https://business.medfordchamber.com/directory/FindStartsWith?term=%23%21"

# Send an HTTP GET request to the URL with a timeout of 10 seconds
response = requests.get(url, timeout=10)

# Check if the request was successful
# The "response" object has a bunch of cool stuff available including the server's returned status codes.
# In this case, we are checking for a 200 status code,
# which means that the server was happy with the request and returned something other than an error.
# If it had been an error, the script would stop and print a message (see the last print statement).
if response.status_code == 200:
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all elements with the specified class in the HTML content
    cards = soup.findAll("div", class_="card-body gz-directory-card-body")

    # Open a CSV file to write the output
    with open("cards_info.csv", "w", newline="", encoding="utf-8") as csvfile:
        csvwriter = csv.writer(csvfile)

        # Write the header row to the CSV file
        csvwriter.writerow(["Name", "Address", "Phone", "Website"])

        # Iterate over each card found in the HTML content
        for card in cards:
            # Initialize a list to hold card details for writing to the CSV;
            # using a list ensures structured data and is required by csvwriter.writerow.
            # Remember this list is reinitialized for every card.
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
