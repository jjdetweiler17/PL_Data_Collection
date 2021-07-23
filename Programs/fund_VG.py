import pandas as pd
import PyPDF2
import os


def get_data2(file_name_txt):
    report = open(file_name_txt, encoding="utf8").read().lower()
    # Replace escape sequences
    report = report.replace("\\n", "\n")
    report = report.replace("\\t", "\t")

    # Find the fund name
    date_index = report.find("202") + 4
    beg_index = report.find("fund")
    if report[beg_index + 5].isalpha():
        fund_name = report[date_index:beg_index + 4]
    else:
        fund_name = report[date_index:beg_index + 5]
    fund_name = fund_name.strip()

    for i in range(1000):
        if (report[i].isnumeric() and report[i+1].isalpha()) or (report[i].isalpha() and report[i+1].isnumeric()):
            report = report[:i+1] + '\n' + report[i+1:]

    # Find page nums in table of contents
    contents_index = report.find('financial statement')
    contents_statement_index = report.find('statement of assets and liabilities', contents_index)
    data_page_num_ind = contents_statement_index + len('statement of assets and liabilities')
    page_num = ""
    for char in report[data_page_num_ind:data_page_num_ind + 200]:
        if char.isnumeric():
            page_num += char
    page_num = str(int(page_num[0:2]) - 1)

    # Find end block page num
    contents_final_index = report.find('statement of changes in net assets', contents_index)
    final_page_num_ind = contents_final_index + len('statement of changes in net assets')
    final_page_num = ""
    for char in report[final_page_num_ind:final_page_num_ind + 200]:
        if char.isnumeric():
            final_page_num += char
    final_page_num = str(int(final_page_num[0:2]) - 1)

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

    for i in range(len(block_string)):
        if block_string[i].isnumeric() and block_string[i+1].isalpha():
            block_string = block_string[:i+1] + '\n' + block_string[i+1:]

    dot_index = block_string.find(".....")
    while dot_index != -1:
        dollar_index = block_string.find("$", dot_index)
        block_string = block_string[:dot_index] + block_string[dollar_index:]
        dot_index = block_string.find(".....")
    block_string = block_string.replace(",", "")

    assets_index = block_string.find("assets") + len("assets") + 1
    assets_index = block_string.find("assets", assets_index) + len("assets") + 1
    block_string = block_string[assets_index:]
    block_string = block_string.replace("\\xe2", "\xe2")
    block_string = block_string.replace("\\x80", "\x80")
    block_string = block_string.replace("\\x93", "\x93")
    block_string = block_string.replace("\\x99", "\x99")
    block_string = block_string.replace("\\x94", "\x94")
    block_string = block_string.replace("\\x0c", "\x0c")

    for i in range(len(block_string)):
        if len(block_string) > i + 1 and block_string[i].isnumeric() and block_string[i + 1] == " " and not (
                block_string[i - 1].isalpha() or block_string[i - 2].isalpha()):
            block_string = block_string[:i + 1] + "\n" + block_string[i + 2:]
        if len(block_string) > i + 1 and block_string[i].isalpha() and (block_string[i + 1].isnumeric() or block_string[i + 1] == "$"):
            block_string = block_string[:i + 1] + " " + block_string[i + 1:]

    block_string = block_string.replace("$", "")

    # print(block_string)
    last_ind = 0
    for i in range(block_string.count(")")):
        current_ind = block_string.find(")", last_ind + 1)
        if block_string[current_ind - 1].isnumeric():
            block_string = block_string[:current_ind + 1] + "\n" + block_string[current_ind + 1:]
        last_ind = current_ind
    block_string = block_string.replace("  ", "\n")
    data_list = []
    while block_string.count("\n") != 0:
        data_list.append(block_string[:block_string.find("\n")])
        block_string = block_string[block_string.find("\n") + 1:]
    for i in range(len(data_list)):
        data_list[i] = data_list[i].strip()

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

        if data_list[i].count("(") != 0:
            start_ind = data_list[i].rfind("(")
            end_ind = data_list[i].rfind(")")
            data_list[i] = data_list[i][:start_ind] + data_list[i][end_ind+1:]

        if data_list[i].count("(") != 0:
            start_ind = data_list[i].rfind("(")
            end_ind = data_list[i].rfind(")")
            data_list[i] = data_list[i][:start_ind] + data_list[i][end_ind+1:]
    # print(data_list)

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
    # print(data_list_dict)
    fund_name = fund_name.replace("wells fargo ", "")
    df = pd.DataFrame(list(data_list_dict.items()), columns=['Statement of Operations', fund_name.title()])
    return df