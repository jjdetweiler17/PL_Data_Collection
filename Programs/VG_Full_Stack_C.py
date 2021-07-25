import pdfplumber
import os
import pandas as pd

path1 = R"C:\Users\jjdet\Desktop\PL_Data_Collection\Vanguard\PDF_Holder\\"
pdf_list = os.listdir(path1)


def reformat_text(text):
    text = text.replace("\\n", "\n")
    text = text.replace("\\t", "\t")
    for i in range(50):
        dots = ""
        for x in range(51 - i):
            dots += "."
        text = text.replace(dots, "")
    for i in range(len(text)):
        if text[i].islower() and (text[i+1].isupper() or text[i+1].isnumeric()):
            text = text[:i+1] + " " + text[i+1:]
    for i in range(len(text)):
        if text[i].islower() and (text[i+1].isupper() or text[i+1].isnumeric()):
            text = text[:i+1] + " " + text[i+1:]
    text = text.lower()
    return text


def extract_data(path):
    # put each page's string into a list
    page_list = []
    fund_name = path
    fund_name = fund_name.replace("annualReport", "")
    fund_name = fund_name.replace("ar", "")
    fund_name = fund_name.replace("-", " ")
    fund_name = fund_name.replace("_", " ")
    fund_name = fund_name.strip()

    with pdfplumber.open(path1 + path) as pdf:
        """
        for page in pdf.pages:
            page_text = page.extract_text()
            page_list.append(page_text)
        """
        page_list.append(pdf.pages[0].extract_text())

    fund_name_list = []
    page_list[0] = reformat_text(page_list[0])
    last_ind = 0
    while page_list[0].find(")") != -1:
        par1_ind = page_list[0].find("(")
        par2_ind = page_list[0].find(")")
        page_list[0] = page_list[0][:par1_ind] + page_list[0][par2_ind + 1:]
    print(page_list[0])
    while page_list[0].find("fund") != -1:
        fund_ind = page_list[0].find("fund", last_ind + 1)
        last_ind = fund_ind
        nl_ind = page_list[0].rfind("\n", 0, fund_ind)
        fund_name_list.append(page_list[0][nl_ind+1:fund_ind+4])
    print(fund_name_list)
    statements_page_list = []
    for page in page_list:
        page = reformat_text(page)
        nl_ind = page.find("\n")
        nl_ind = page.find("\n", nl_ind + 1)
        if page.find("statement of assets and liabilities", 0, nl_ind) != -1:
            statements_page_list.append(page)
        elif page.find("statement of operations", 0, nl_ind) != -1:
            statements_page_list.append(page)


pdf_list = os.listdir(path1)
extract_data(pdf_list[9])
