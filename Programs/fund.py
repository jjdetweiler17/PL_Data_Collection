import pandas as pd
import PyPDF2
import os

columns = ['Statement of Operations']

# !/usr/bin/python3
# coding: utf-8


from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.pdfpage import PDFPage
from io import BytesIO


def pdf2xt(path):
    """
    Extract text from PDF file, and return
    the string contained inside
    :param path (str) path to the .pdf file
    :return: text (str) string extracted
    """

    rsrcmgr = PDFResourceManager()
    retstr = BytesIO()
    device = TextConverter(rsrcmgr, retstr)
    with open(path, "rb") as fp:  # open in 'rb' mode to read PDF bytes
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        for page in PDFPage.get_pages(fp, check_extractable=True):
            interpreter.process_page(page)
        device.close()
        text = retstr.getvalue()
        retstr.close()
    file_name = path[:-3]
    file_name_txt = file_name + ".txt"
    file1 = open(file_name_txt, "a")
    file1.writelines(text)
    file1.close()


def pdf_save_txt(file_name_pdf):
    text = ""
    file_name = file_name_pdf[:-3]
    file_name_txt = file_name + ".txt"
    # From AskPython, "Convert PDF to TXT file using Python",
    # https://www.askpython.com/python/examples/convert-pdf-to-txt
    # create file object variable
    # opening method will be rb
    pdffileobj = open(file_name_pdf, 'rb')

    # create reader variable that will read the pdffileobj
    pdfreader = PyPDF2.PdfFileReader(pdffileobj)

    for page_num in range(pdfreader.numPages + 1):
        # This will store the number of pages of this pdf file
        # create a variable that will select the selected number of pages
        pageobj = pdfreader.getPage(page_num)

        # (x+1) because python indentation starts with 0.
        # create text variable which will store all text data from pdf file
        text += pageobj.extractText()

    # save the extracted data from pdf to a txt file
    # we will use file handling here
    # dont forget to put r before you put the file path
    # go to the file location copy the path by right clicking on the file
    # click properties and copy the location path and paste it here.
    # put "\\your_txtfilename"
    file1 = open(file_name_txt, "a")
    file1.writelines(text)

    # End of borrowed code


def get_data(file_name_txt):
    print("------------------------------------------------------------")
    df = pd.read_csv("Fund_Data_Base.csv")
    wanted_stats = df["Statement of Operations"].tolist()

    for i in range(len(wanted_stats)):
        wanted_stats[i] = wanted_stats[i].lower()

    report = open(file_name_txt, encoding="utf8").read().lower()
    report = report.replace("\\n", "\n")

    # Find fund name
    """
    newline_index = report.find("\n")
    newline_index = report.find("\n", newline_index + 1)
    newline_index = report.find("\n", newline_index + 1) + 1
    current_char = report[newline_index]
    last_char = newline_index
    while current_char != "\n":
        last_char += 1
        current_char = report[last_char]
    fund_name = report[newline_index:last_char]
    """
    date_index = report.find("202") + 4

    beg_index = report.find("beginning")

    fund_name = report[date_index:beg_index]

    fund_name = fund_name.strip()
    print(fund_name)
    print("---------------------------------------------------------------")
    # Find statement of assets and liabilities of contents and find page num of data
    contents_index = report.find('contents')
    contents_statement_index = report.find('statement of assets and liabilities', contents_index)
    data_page_num_ind = contents_statement_index + len('statement of assets and liabilities')
    page_num = ""
    for char in report[data_page_num_ind:data_page_num_ind + 100]:
        if char.isnumeric():
            page_num += char
    page_num = str(int(page_num[0:2]) - 1)
    print(page_num)

    contents_final_index = report.find('statement of changes in net assets', contents_index)
    final_page_num_ind = contents_final_index + len('statement of changes in net assets')
    final_page_num = ""
    for char in report[final_page_num_ind:final_page_num_ind + 100]:
        if char.isnumeric():
            final_page_num += char
    final_page_num = str(int(final_page_num[0:2]) - 1)
    print(final_page_num)

    # go to page index so that data can be searched first from that index
    if int(page_num) % 2 == 0:
        page_index = report.find(page_num + " | " + fund_name) + 6 + len(fund_name)
    else:
        page_index = report.find(fund_name + " | " + page_num) + 6 + len(fund_name)

    if int(final_page_num) % 2 == 0:
        final_page_index = report.find(final_page_num + " | " + fund_name) + 1
    else:
        final_page_index = report.find(fund_name + " | " + final_page_num) + 1

    # This code will block out the statement of assets and liabilities and the statement of operations
    # and then convert whatever stats can be found in there into a dictionary
    block_string = report[page_index:final_page_index]

    dot_index = block_string.find(".....")
    while dot_index != -1:
        dollar_index = block_string.find("$", dot_index)
        block_string = block_string[:dot_index] + block_string[dollar_index:]
        dot_index = block_string.find(".....")
    data_list = []
    while block_string.count(" ") != 0:
        item_ind = block_string.find(" ")
        data_list.append(block_string[:block_string.find(" ", item_ind)])
        block_string = block_string[block_string.find(" ", item_ind) + 1:]
    data_list_dict = {}
    for string in data_list:
        space_index = string.rfind(" ")
        data_list_dict[string[:space_index].strip(" $")] = string[space_index + 1:].replace(",", "")

    df = pd.DataFrame(list(data_list_dict.items()), columns=['Statement of Operations', fund_name.title()])
    df = df.loc[df[fund_name.title()].str.isnumeric()]

    return df


def get_data2(file_name_txt):
    report = open(file_name_txt, encoding="utf8").read().lower()
    # Replace escape sequences
    report = report.replace("\\n", "\n")
    report = report.replace("\\t", "\t")

    # Find the fund name
    date_index = report.find("202") + 4
    beg_index = report.find("beginning")
    fund_name = report[date_index:beg_index]
    fund_name = fund_name.strip()
    print(fund_name)

    # Find page nums in table of contents
    contents_index = report.find('contents')
    contents_statement_index = report.find('statement of assets and liabilities', contents_index)
    data_page_num_ind = contents_statement_index + len('statement of assets and liabilities')
    page_num = ""
    for char in report[data_page_num_ind:data_page_num_ind + 100]:
        if char.isnumeric():
            page_num += char
    page_num = str(int(page_num[0:2]) - 1)

    # Find end block page num
    contents_final_index = report.find('statement of changes in net assets', contents_index)
    final_page_num_ind = contents_final_index + len('statement of changes in net assets')
    final_page_num = ""
    for char in report[final_page_num_ind:final_page_num_ind + 100]:
        if char.isnumeric():
            final_page_num += char
    final_page_num = str(int(final_page_num[0:2]) - 1)
    print(final_page_num)

    # go to page index so that data can be searched first from that index
    if int(page_num) % 2 == 0:
        page_index = report.find(page_num + " | " + fund_name) + 6 + len(fund_name)
    else:
        page_index = report.find(fund_name + " | " + page_num) + 6 + len(fund_name)

    if int(final_page_num) % 2 == 0:
        final_page_index = report.find(final_page_num + " | " + fund_name) + 1
    else:
        final_page_index = report.find(fund_name + " | " + final_page_num) + 1

    block_string = report[page_index:final_page_index]
    dot_index = block_string.find(".....")
    while dot_index != -1:
        dollar_index = block_string.find("$", dot_index)
        block_string = block_string[:dot_index] + block_string[dollar_index:]
        dot_index = block_string.find(".....")
    block_string = block_string.replace(",", "")
    for i in range(len(block_string)):
        if len(block_string) > i + 1 and block_string[i].isnumeric() and block_string[i + 1] == " " and not (
                block_string[i - 1].isalpha() or block_string[i - 2].isalpha()):
            block_string = block_string[:i + 1] + "\n" + block_string[i + 2:]
    assets_index = block_string.find("assets") + len("assets") + 1
    assets_index = block_string.find("assets", assets_index) + len("assets") + 1
    block_string = block_string[assets_index:]
    block_string = block_string.replace("$", "")
    block_string = block_string.replace("\\xe2", "\xe2")
    block_string = block_string.replace("\\x80", "\x80")
    block_string = block_string.replace("\\x93", "\x93")
    block_string = block_string.replace("\\x99", "\x99")
    block_string = block_string.replace("\\x94", "\x94")
    block_string = block_string.replace("\\x0c", "\x0c")

    print(block_string)

    data_list = []
    while block_string.count("\n") != 0:
        data_list.append(block_string[:block_string.find("\n")])
        block_string = block_string[block_string.find("\n") + 1:]
    for i in range(len(data_list)):
        data_list[i] = data_list[i].strip()
    print(data_list)

    for i in range(len(data_list)):
        if data_list[i].count("class") != 0:
            ind = data_list[i].find("class")
            if data_list[i][:ind].count("  ") != 0:
                double_space_ind = data_list[i].rfind("  ", 0, ind)
                string1 = data_list[i][:double_space_ind]
                data_list[i] = data_list[i][double_space_ind + 2:]
                data_list.insert(i, string1)
                i += 1
        data_list[i] = data_list[i].replace("  ", " ")

    print(data_list)

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
    print(data_list_dict)
    fund_name = fund_name.replace("wells fargo ", "")
    df = pd.DataFrame(list(data_list_dict.items()), columns=['Statement of Operations', fund_name.title()])
    return df


"""
large_cap_df = get_data("WF_Practice_File.txt")
# mid_cap_df = get_data("WF Mid Cap Fund.txt")
large_cap_df_new = get_data2(r"TXT_Holder\cb-large-cap-value-ar.txt")
# print(large_cap_df_new)

full_df = pd.merge(large_cap_df, large_cap_df_new, how='outer', indicator=True)
print(full_df)
"""

path = R"C:\Users\jjdet\Desktop\PL_Data_Collection\\"
txt_list = os.listdir(path + R"TXT_Holder")
path = path + R"TXT_Holder\\"


full_df = pd.merge(get_data2(path + txt_list[0]), get_data2(path + txt_list[1]), how='outer')
for i in range(len(txt_list) - 3):
    full_df = pd.merge(full_df, get_data2(path + txt_list[i+2]), how='outer')
print(full_df)
full_df.to_csv(r'C:\Users\jjdet\Desktop\PL_Data_Collection\value_fund_practice.csv')





