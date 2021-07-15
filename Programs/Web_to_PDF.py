import urllib.request

web_path = "https://www.wellsfargoassetmanagement.com/assets/edocs/regulatory/annual-report/"

comp_path = r'C:\Users\jjdet\Desktop\PL_Data_Collection\PDF_Holder\\'

fund_list_text = open("WF Fund Name List.txt", encoding="utf8").read().lower()
fund_list = fund_list_text.split("\n")
new_fund_list = []
for i in range(len(fund_list)):
    if i % 3 == 1:
        new_fund_list.append(fund_list[i])

fund_list = new_fund_list

for i in range(len(fund_list)):
    if fund_list[i].count("(") != 0:
        fund_list[i] = fund_list[i][:fund_list[i].find("(")]
    fund_list[i] = fund_list[i].strip()
    fund_list[i] = fund_list[i].replace("fund", "")
    fund_list[i] = fund_list[i].replace(" ", "-")
    fund_list[i] = fund_list[i] + "-ar"
    fund_list[i] = fund_list[i].replace("--ar", "-ar")

    word = ""
    for char in fund_list[i]:
        if char.isalnum() or char == "-":
            word += char
    fund_list[i] = word

print(fund_list)

from pathlib import Path
import requests


def download_file(download_url, filename):
    response = requests.get(web_path + download_url)
    file = Path(comp_path + filename + ".pdf")
    file.write_bytes(response.content)


for fund in fund_list[:5]:
    download_file(web_path + fund, fund)