import pdfplumber
import os
import pandas as pd

path1 = R"C:\Users\jjdet\Desktop\PL_Data_Collection\Vanguard\PDF_Holder\\"
pdf_list = os.listdir(path1)


def reformat_text(text):
    text = text.replace("\\n", "\n")
    text = text.replace("\\t", "\t")
    text = text.replace("\\xe2", "\xe2")
    text = text.replace("\\x80", "\x80")
    text = text.replace("\\x93", "\x93")
    text = text.replace("\\x99", "\x99")
    text = text.replace("\\x94", "\x94")
    text = text.replace("\\x0c", "\x0c")

    for i in range(50):
        dots = ""
        for x in range(51 - i):
            dots += "."
        text = text.replace(dots, "")
    for i in range(len(text) - 1):
        if text[i].islower() and (text[i+1].isupper() or text[i+1].isnumeric()):
            text = text[:i+1] + " " + text[i+1:]
    for i in range(len(text) - 1):
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
    fund_name = fund_name.replace(".pdf", "")
    fund_name = fund_name.strip()

    with pdfplumber.open(path1 + path) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            page_list.append(page_text)
        page_list.append(pdf.pages[0].extract_text())

    fund_name_list = []
    page_list[0] = reformat_text(page_list[0])
    last_ind = 0
    while page_list[0].find(")") != -1:
        print('a')
        par1_ind = page_list[0].find("(")
        par2_ind = page_list[0].find(")")
        page_list[0] = page_list[0][:par1_ind] + page_list[0][par2_ind + 1:]
    for i in range(page_list[0].count("fund")):
        print("a")
        fund_ind = page_list[0].find("fund", last_ind + 1)
        last_ind = fund_ind + 1
        nl_ind = page_list[0].rfind("\n", 0, fund_ind)
        if page_list[0][fund_ind+4] != "s":
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
    for i in range(len(statements_page_list)):
        statements_page_list[i] = reformat_text(statements_page_list[i])
        data_list = []
        block_string = statements_page_list[i]
        while block_string.count("\n") != 0:
            data_list.append(block_string[:block_string.find("\n")])
            block_string = block_string[block_string.find("\n") + 1:]
        for i in range(len(data_list)):
            data_list[i] = data_list[i].strip()
            if data_list[i].count("class") != 0:
                ind = data_list[i].find("class")
                if data_list[i][:ind].count("  ") != 0:
                    double_space_ind = data_list[i].rfind("  ", 0, ind)
                    string1 = data_list[i][:double_space_ind]
                    data_list[i] = data_list[i][double_space_ind + 2:]
                    data_list.insert(i, string1)
                    i += 1
            data_list[i] = data_list[i].replace("  ", " ")
            if data_list[i].count("(") != 0:
                start_ind = data_list[i].rfind("(")
                end_ind = data_list[i].rfind(")")
                data_list[i] = data_list[i][:start_ind] + data_list[i][end_ind + 1:]

            if data_list[i].count("(") != 0:
                start_ind = data_list[i].rfind("(")
                end_ind = data_list[i].rfind(")")
                data_list[i] = data_list[i][:start_ind] + data_list[i][end_ind + 1:]
            data_list_dict = {}
            for string in data_list:
                hasnum = False
                for char in string:
                    if char.isnumeric():
                        hasnum = True

                if hasnum:
                    space_index = string.rfind(" ")
                    data_list_dict[string[:space_index].strip(" $")] = string[space_index + 1:].replace(",", "")
                else:
                    data_list_dict[string] = ""

            df = pd.DataFrame(list(data_list_dict.items()), columns=['Statement of Operations', fund_name.title()])
            print(df)
            return df





extract_data("Cash_Reserves_Federal_Money_Market_Fund_Admiral__annualReport.pdf")