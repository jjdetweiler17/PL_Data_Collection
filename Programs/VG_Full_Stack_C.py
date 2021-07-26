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


def extract_data_sub(page, fund_name):
    page = reformat_text(page)
    data_list = []
    block_string = page
    while block_string.count("\n") != 0:
        data_list.append(block_string[:block_string.find("\n")])
        block_string = block_string[block_string.find("\n") + 1:]
    for x in range(len(data_list)):
        data_list[x] = data_list[x].strip()
        if data_list[x].count("class") != 0:
            ind = data_list[x].find("class")
            if data_list[x][:ind].count("  ") != 0:
                double_space_ind = data_list[x].rfind("  ", 0, ind)
                string1 = data_list[x][:double_space_ind]
                data_list[x] = data_list[x][double_space_ind + 2:]
                data_list.insert(x, string1)
                x += 1
        data_list[x] = data_list[x].replace("  ", " ")
        if data_list[x].count("(") != 0:
            start_ind = data_list[x].rfind("(")
            end_ind = data_list[x].rfind(")")
            data_list[x] = data_list[x][:start_ind] + data_list[x][end_ind + 1:]

        if data_list[x].count("(") != 0:
            start_ind = data_list[x].rfind("(")
            end_ind = data_list[x].rfind(")")
            data_list[x] = data_list[x][:start_ind] + data_list[x][end_ind + 1:]
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
    return df


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
    for a in range(page_list[0].count("fund")):
        print("a")
        fund_ind = page_list[0].find("fund", last_ind + 1)
        last_ind = fund_ind + 1
        nl_ind = page_list[0].rfind("\n", 0, fund_ind)
        if fund_ind + 4 < len(page_list[0]) and page_list[0][fund_ind+4] != "s":
            fund_name_list.append(page_list[0][nl_ind+1:fund_ind+4])
    if fund_name_list.count("toyourfund") != 0:
        fund_name_list.remove("toyourfund")
    if fund_name_list.count("to your fund") != 0:
        fund_name_list.remove("to your fund")
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
    print(type(fund_name_list))
    if fund_name_list is None or len(fund_name_list) < 2:
        df = extract_data_sub(statements_page_list[0], fund_name)
    else:
        df = extract_data_sub(statements_page_list[0], fund_name_list[0])
    if len(statements_page_list) >= 2:
        for a in range(len(statements_page_list) - 2):
            if fund_name_list is None or len(fund_name_list) < 2:
                df = pd.merge(df, extract_data_sub(statements_page_list[a+2], fund_name), how="outer")
            else:
                df = pd.merge(df, extract_data_sub(statements_page_list[a+2],
                                                   fund_name_list[a // 2]), how="outer")
    return df


count = 0
extract_data(pdf_list[25])
pdf_list = os.listdir(path1)
pdf_list = pdf_list[20:30]
print(len(pdf_list))
full_df = pd.merge(extract_data(pdf_list[0]), extract_data(pdf_list[1]), how='outer')
for i in range(len(pdf_list) - 2):
    full_df = pd.merge(full_df, extract_data(pdf_list[i+2]), how='outer')
    print(count)
    count += 1

full_df.to_csv(r'C:\Users\jjdet\Desktop\PL_Data_Collection\full_VG_spreadsheet.csv')
