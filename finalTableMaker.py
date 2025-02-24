import csv
import pickle
import re
import pdfplumber
from unidecode import unidecode


def extract_authors_from_text(text):
    try:
        text = text[
               text.find("Author(s):") + 11:text.find("Author(s):") + (text[text.find("Author(s):"):].find("Source"))]
        # print(text)
    except:
        return None
    try:
        text = text.replace("\n", " ")
        authors = re.split(r', | and | and\n | ,\n', text.strip())
        # if authors[0] == 'doi: 10.1111/j. 1467-9221.2010.00771 .x':
        #     print(authors)
        newAuthors = []
        for a in authors:
            a = a.replace("£", "E")
            newAuthors.append(unidecode(a.replace("\n", " ")))
        return newAuthors
    except:
        return None


with open("finishedSortedResearchPapers.pickle", "rb") as f:
    papers = pickle.load(f)

rows = []

for p in papers:
    if p.getPDF() is not None and len(p.getAbstract()) > 25:
        pdf_path = "/Users/simongray/Desktop/tomasiProject/pdfFolder/Volume " + str(p.getVolume()) + "/Issue " + str(
            p.getIssue()) + "/" + p.getPDF()
        with pdfplumber.open(pdf_path) as pdf:
            first_page = pdf.pages[0]
            text = first_page.extract_text()
        authors = extract_authors_from_text(text)
        newAuthors = []
        for a in authors:
            if authors.index(a) == 0:
                parts = a.split()
                newAuthors.append(f"{parts[-1]}, {' '.join(parts[:-1])}")
            else:
                newAuthors.append(a)
        # print(newAuthors)
        citation = ""
        for a in newAuthors:
            if newAuthors.index(a) != 0:
                citation += ", " + a
            else:
                citation += a
        year = 1979 + int(p.getVolume())
        citation += ". "
        citation += "\"" + str(p.getTitle()) + "\". Political Psychology " + str(p.getVolume()) + ", no. " + str(p.getIssue()) + " (" + str(year) + ")"
        abstract = p.getAbstract()
        colleges = p.getColleges()
        toAdd = [citation, abstract, colleges[0], colleges[1:]]
        rows.append(toAdd)
        # print(toAdd)

header = ['Chicago Citation', 'Abstract', 'First Author Institution', "Other Author Institutions"]

filename = 'final.csv'

with open(filename, 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(header)
    csvwriter.writerows(rows)

print(f"CSV file '{filename}' created successfully.")
