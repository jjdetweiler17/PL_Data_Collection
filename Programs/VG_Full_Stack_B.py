from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.pdfpage import PDFPage
from io import BytesIO
import os
import pandas as pd
import PyPDF2

path1 = R"C:\Users\jjdet\Desktop\PL_Data_Collection\Vanguard\\"


def pdf_to_df(path):
    reader = PyPDF2.PdfFileReader(path1 + R"PDF_Holder\\" + path)
    text = ""
    print(reader.numPages)
    for i in range(3):
        text += reader.getPage(i).extractText()
    file_name = path[12:-4]

    report = text
    # Replace escape sequences
    report = report.replace("\\n", "\n")
    report = report.replace("\\t", "\t")
    print(report)


pdf_list = os.listdir(path1 + "PDF_Holder")
pdf_to_df(pdf_list[3])
