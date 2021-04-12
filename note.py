#%%
from PyPDF2 import PdfFileReader, PdfFileWriter
import re
import numpy as np
import pathlib


def read_pdf(input_path):
    file_path = str(pathlib.Path(input_path).resolve())
    pdf_name = file_path.split('.')[0].split('\\')[-1]
    return PdfFileReader(file_path), pdf_name


# Extract text and do the search for pages
def extract_pdf(input_path, r_pattern):
    reader, _ = read_pdf(input_path)
    target_pages = []
    for i in range(0, reader.getNumPages()):
        page_obj = reader.getPage(i)
        text = page_obj.extractText()
        str_bucket = r_ecl.findall(text)
        if len(np.unique(str_bucket)):
            target_pages.append(i)
            print("Pattern Found on Page: " + str(i))
    return target_pages


def export_pdf(input_path, target_pages):
    reader, pdf_name = read_pdf(input_path)
    output = PdfFileWriter()
    for i in target_pages:
        output.addPage(reader.getPage(i))
    with open(f"Filtered_{pdf_name}.pdf", "wb") as outputStream:
        output.write(outputStream)


# %%

# ECL regex pattern
r_ecl = re.compile(r'stage\s*1|stage\s*2|stage\s*3')
reader, pdf_name = read_pdf(r'C:\Users\jhkang\Downloads\TSB_2020Q4.pdf')