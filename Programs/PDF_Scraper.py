import requests
import validators
import sys
from bs4 import BeautifulSoup as bs
from urllib.parse import urlparse
import wget
from urllib.request import urlopen
import urllib.request 


def check_validity(url):
    try:
        urlopen(url)
        print("Valid URL")
    except IOError:
        print("Invalid URL")
        sys.exit()


def get_pdfs(url):
    links = []
    html = urlopen(url).read()
    html_page = bs(html, features="html.parser")
    og_url = html_page.find("meta")
    print(og_url)
    base = urlparse(url)
    print("base", base)
    print(html_page)
    print(type(html_page))
    for link in html_page.find_all('a'):
        current_link = link.get('href')
        if current_link.endswith('pdf'):
            if og_url:
                print("currentLink", current_link)
                links.append(og_url["content"] + current_link)
            else:
                links.append(base.scheme + "://" + base.netloc + current_link)

    for link in links:
        try:
            print(type(link))
            wget.download(link)
        except:
            print(" \n \n Unable to Download A File \n")
    print('\n')


my_url = "https://www.wellsfargoassetmanagement.com/literature#tab=products&documentTypes=Annual%20Report"
check_validity(my_url)
get_pdfs(my_url)
