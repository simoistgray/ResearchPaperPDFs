import csv
import pickle
from unidecode import unidecode
import pdfplumber
import re


def extract_colleges_from_csv(csv_file_path):
    colleges = []
    with open(csv_file_path, 'r', newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            college_name = row[0].strip()
            colleges.append(college_name)
    return colleges


def extract_authors_from_text(text):
    try:
        text = text[text.find("Author(s):") + 11:text.find("Author(s):") + (text[text.find("Author(s):"):].find("Source"))]
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

def extract_affiliation(pdf_path, universities, abstract, vol):
    with pdfplumber.open(pdf_path) as pdf:
        first_page = pdf.pages[0]
        second_page = pdf.pages[1]
        text1 = first_page.extract_text()
        text = second_page.extract_text()
        text = text.replace(" '", "'")
        text = text.replace(" ,", ",")
        text = text.replace("  ", " ")
        text = unidecode(text)
        # print(text)
        authors = extract_authors_from_text(text1)
        # print(authors)
        if int(vol) > 14:
            if authors:
                found_affiliations = []
                if text.find(authors[0]) == -1:
                    authors[0] = authors[0].replace(".", "")
                offset = 30
                while text.find(abstract[:offset]) == -1:
                    offset -= 1
                authorsAndColleges = text[text.find(authors[0]):text.find(abstract[:offset])]
                for line in authorsAndColleges.split('\n')[1:]:
                    uni = line.strip()
                    if uni not in found_affiliations and uni not in authors and len(uni) < 70:
                        found_affiliations.append(uni)
                if found_affiliations != []:
                    newF = []
                    for f in found_affiliations:
                        if len(f) > 3:
                            newF.append(f)
                    return newF if newF else ["Affiliation not found"]
                else:
                    for university in universities:
                        if re.search(r'\b' + re.escape(university) + r'\b', text):
                            found_affiliations.append(university)

                    return found_affiliations if found_affiliations else ["Affiliation not found"]

        else:
            if authors:
                found_affiliations = []
                authorsAndColleges = text[text.find(authors[0]):text.find(abstract[:15])]
                # print(authors)
                for line in authorsAndColleges.split('\n')[1:]:
                    uni = unidecode(line.strip())
                    # print(uni)
                    if uni not in found_affiliations and uni not in authors and len(uni) < 70:
                        found_affiliations.append(uni)
                if found_affiliations != []:
                    newF = []
                    for f in found_affiliations:
                        if len(f) > 3:
                            newF.append(f)
                    if newF:
                        return newF
                    else:
                        # print("second")
                        found_affiliations = []
                        authorsAndColleges = text[text.find("This content downloaded from") - 200:text.find(
                            "This content downloaded from")]
                        for university in universities:
                            if re.search(r'\b' + re.escape(university) + r'\b', authorsAndColleges):
                                found_affiliations.append(university)
                        if found_affiliations:
                            return found_affiliations
                        else:
                            # print("first")
                            for university in universities:
                                if re.search(r'\b' + re.escape(university) + r'\b',
                                             text[:text.find(abstract[:15])]):
                                    found_affiliations.append(university)
                            if found_affiliations:
                                return found_affiliations
                            else:
                                return ["Affiliation not found"]

    return ["Affiliation not found"]

with open("finishedSortedResearchPapers.pickle", "rb") as f:
    papers = pickle.load(f)

for p in papers:
    print(p.getColleges())

universities = extract_colleges_from_csv('world-universities.csv')

for p in papers:
    if p.getPDF() is not None:
        pdf_path = "/pdfFolder/Volume " + str(p.getVolume()) + "/Issue " + str(p.getIssue()) + "/" + p.getPDF()
        affiliations = extract_affiliation(pdf_path, universities, str(p.getAbstract()), p.getVolume())
        # if affiliations == ["Affiliation not found"]:
        #     print(p.getVolume(), p.getIssue(), pdf_path[67:73], affiliations)
        for x in affiliations:
            p.appendColleges(x)
        if papers.index(p) % 10 == 0:
            print(papers.index(p))
with open("finishedSortedResearchPapers.pickle", "wb") as f:
    pickle.dump(papers, f)
