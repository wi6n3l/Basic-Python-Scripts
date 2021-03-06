#!/usr/bin/python3
# Created by Sam Ebison ( https://github.com/ebsa491 )
# If you have found any important bug or vulnerability,
# contact me pls, I love learning ( email: ebsa491@gmail.com )

"""
A script for extracting covid-19 virus online information from (https://www.worldometers.info/coronavirus/)
"""

import sys
import requests
from bs4 import BeautifulSoup

URL = "https://www.worldometers.info/coronavirus/"

# For coloring output
RED_COLOR = "\033[1;31m"
GREEN_COLOR = "\033[1;32m"
NO_COLOR = "\033[0m"

def main():
    """The main function of the script."""
    
    result = send_request(URL)

    if result == -1:
        print(f"[{RED_COLOR}-{NO_COLOR}] Connection error...")
        sys.exit(1)

    info_dict = parse_result(result)

    if "err" in info_dict:
        print(f"[{RED_COLOR}-{NO_COLOR}] Web scraping error...")
        sys.exit(1)

    print(f"========= {RED_COLOR}Covid-19 Info{NO_COLOR} =========\n")

    print(f" Coronavirus cases => {info_dict['cases']}")
    print(f" Death => {RED_COLOR}{info_dict['death']}{NO_COLOR}")
    print(f" Recovered => {GREEN_COLOR}{info_dict['recovered']}{NO_COLOR}\n")

    print("========= Top Ten Countries =========\n")

    for country in info_dict["top_ten_countries"]:
        print(f" #{info_dict['top_ten_countries'].index(country) + 1}: {country}")

    print("\n========= Hands | Face | Space =========")

def send_request(url):
    """
    Sends a GET request to the URL,
    and returns the result (returns -1 for any error).
    - url: The website URL.
    """

    try:
        return requests.get(url)
    except:
        return -1

def parse_result(result):
    """
    Parses the HTML result,
    and returns the info as a dictionary (returns {"err": some_err} for any error).
    - result: The HTML result (send_request function returns).   
    """
    
    # Coronavirus cases => <span style="color:#aaa">38,406,711</span>
    # Death => <span>1,091,593</span>
    # Recovered => <span>28,875,950</span>

    soup = BeautifulSoup(result.text, "html.parser")
    span_tags = soup.find_all("span")
    a_tags = soup.find_all("a", {"class": "mt_a"})
    # span_tags: index 4 => Coronavirus cases | index 5 => Death | index 6 => Recovered
    # a_tags: top ten [0...9]

    info = {
        "cases": "",
        "death": "",
        "recovered": "",
        "top_ten_countries": []
    }

    try:
        
        info["cases"] = span_tags[4].text
        info["death"] = span_tags[5].text
        info["recovered"] = span_tags[6].text

        for country in a_tags[:9]:
            info["top_ten_countries"].append(country.text)

        return info

    except Exception as err:
        return {"err": str(err)}

if __name__ == '__main__':
    main()
