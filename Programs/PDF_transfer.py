from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.pdfpage import PDFPage
from io import BytesIO
import os


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
        text = str(retstr.getvalue())
        retstr.close()
    file_name = path[13:-4]
    print(file_name)
    file_name_txt = file_name + ".txt"
    file1 = open(R"C:\Users\jjdet\Desktop\PL_Data_Collection\TXT_Holder\\" + file_name_txt, "a")
    text = text.replace("\\n", "\n")
    file1.writelines(text)
    file1.close()


pdf_list = ["cb-large-cap-value-ar.pdf", "classic-value-ar.pdf", "large-company-value-ar.pdf",
            "small-company-value-ar.pdf", "special-mid-cap-value-ar.pdf", "special-small-cap-value-ar.pdf"]

path = R"C:\Users\jjdet\Desktop\PL_Data_Collection\\"

pdf_list = os.listdir(path + R"PDF_Holder_2")

txt_list = os.listdir(path + R"TXT_Holder")

for name in pdf_list:
    if txt_list.count(name[:-3] + 'txt') == 0:
        pdf2xt(R"PDF_Holder_2\\" + name)
        print(name)
