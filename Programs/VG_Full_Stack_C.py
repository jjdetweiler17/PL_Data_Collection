import pdfplumber
import os

path1 = R"C:\Users\jjdet\Desktop\PL_Data_Collection\Vanguard\PDF_Holder\\"
pdf_list = os.listdir(path1)

with pdfplumber.open(path1 + pdf_list[0]) as pdf:
    text = ""
    for i in range(3):
        page = pdf.pages[i]
        text += page.extract_text()

print(text)
