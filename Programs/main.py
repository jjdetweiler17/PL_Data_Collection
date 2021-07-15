import pandas as pd

# load csv file
df = pd.read_csv("Fund_Data_Base.csv")
wanted_stats = df["Statement of Operations"].tolist()

for i in range(len(wanted_stats)):
    wanted_stats[i] = wanted_stats[i].lower()


# upload annual report
"""" 
This code looks for keywords and then finds the adds the first numeric characters from the keywords to a string
report = open("WF_Practice_File.txt", encoding="utf8").read().lower()
wanted_stats_results = []
value = ""
stat_use_count = report.count('total net assets')
stat_index = report.find('total net assets') + 1
for i in range(stat_use_count - 1):
    stat_index = report.find('total net assets', stat_index) + 1
for i in range(stat_index, stat_index + 40):
    if(report[i].isnumeric()):
        value += report[i]
wanted_stats_results.append(value)

value = ""
stat_use_count = report.count('management fee')
stat_index = report.find('management fee') + 1
for i in range(stat_use_count - 1):
    stat_index = report.find('management fee', stat_index) + 1
for i in range(stat_index, stat_index + 40):
    if(report[i].isnumeric()):
        value += report[i]
wanted_stats_results.append(value)
"""

"""
This code similarly also is intended to find the keyword and add values as soon as it finds numbers
for stat in wanted_stats:
    stat_count = report.count(stat)
    index = report.find(stat)
    for i in range(stat_count - 1):
        index = report.find(stat, index)
    value = ""
    for i in range(30):
        print(report[index])
        if report[index].isnumeric():
            break
        index += 1
    for i in range(30):
        if ~(report[index].isnumeric()):
            break
        value += report[index]
        index += 1
    wanted_stats_results.append(value)
"""

report = open("WF_Practice_File.txt", encoding="utf8").read().lower()
wanted_stats_results = []

# Find fund name
annual_report_index = 0
newline_index = report.find("\n")
newline_index = report.find("\n", newline_index + 1)
newline_index = report.find("\n", newline_index + 1) + 1
current_char = report[newline_index]
last_char = newline_index
while current_char != "\n":
    last_char += 1
    current_char = report[last_char]
print(newline_index)
print(last_char)
fund_name = report[newline_index:last_char]
fund_name = fund_name.strip()
print(fund_name)

# Find statement of assets and liabilities of contents and find page num of data
contents_index = report.find('contents')
contents_statement_index = report.find('statement of assets and liabilities', contents_index)
data_page_num_ind = contents_statement_index + len('statement of assets and liabilities')
page_num = ""
for char in report[data_page_num_ind:data_page_num_ind + 50]:
    if char.isnumeric():
        page_num += char
page_num = str(int(page_num[0:2]) - 1)
print(page_num)

contents_final_index = report.find('statement of changes in net assets', contents_index)
final_page_num_ind = contents_final_index + len('statement of changes in net assets')
final_page_num = ""
for char in report[final_page_num_ind:final_page_num_ind + 50]:
    if char.isnumeric():
        final_page_num += char
final_page_num = str(int(final_page_num[0:2]) - 1)
print(final_page_num)

# go to page index so that data can be searched first from that index
if int(page_num) % 2 == 0:
    page_index = report.find(page_num + " | " + fund_name) + 1
else:
    page_index = report.find(fund_name + " | " + page_num) + 1
print(page_index)

if int(final_page_num) % 2 == 0:
    final_page_index = report.find(final_page_num + " | " + fund_name) + 1
else:
    final_page_index = report.find(fund_name + " | " + final_page_num) + 1
print(final_page_index)


"""
#This code takes the keyword and makes a string until the next \n and then strips all but the value
# search for each stat using find from the page index
for stat in wanted_stats:
    stat_index = report.find(stat, page_index) + len(stat)

    last_ind = report.find("\n", stat_index + 1)
    value = report[stat_index:last_ind]
    value = value.strip("() payable$.\nclass a")
    if value[0:2] == "6 ":
        value = value[2:]
    wanted_stats_results.append(value)
"""

# This code will block out the statement of assets and liabilities and the statement of operations
# and then convert whatever stats can be found in there into a dictionary
block_string = report[page_index:final_page_index]

dot_index = block_string.find(".....")
while dot_index != -1:
    dollar_index = block_string.find("$", dot_index)
    block_string = block_string[:dot_index] + block_string[dollar_index:]
    dot_index = block_string.find(".....")
data_list = block_string.split("\n")
data_list_dict = {}
for string in data_list:
    space_index = string.rfind(" ")
    data_list_dict[string[:space_index].strip(" $")] = string[space_index + 1:].replace(",", "")
df = pd.DataFrame(list(data_list_dict.items()), columns=['Statement of Operations', fund_name.title()])
df = df.loc[df[fund_name.title()].str.isnumeric()]
print(df)

for i in range(len(wanted_stats_results)):
    if wanted_stats_results[i].count("$") != 0:
        wanted_stats_results[i] = wanted_stats_results[i][wanted_stats_results[i].find("$") + 2:]
# df[fund_name.title()] = wanted_stats_results
# print(df)
df.to_csv(r'C:\Users\jjdet\Desktop\PL_Data_Collection\\' + fund_name + '.csv')
