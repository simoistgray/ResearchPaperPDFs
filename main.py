import random
import re
import time
from datetime import datetime as dt

import keyboard
import pyautogui
import pyperclip
from selenium.webdriver.common.by import By

from Paper import *
from finishedPaper import *
import pickle
from scrapingbee import ScrapingBeeClient
import requests
from bs4 import BeautifulSoup
from selenium import webdriver


def getTitlesAndLinks(url, usedTitles):
    user_agents = [
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
    ]

    linksForEachIssue = []

    selected_user_agent = random.choice(user_agents)

    driver = webdriver.Chrome()

    # url = "https://www.jstor.org/journal/polipsyc"
    # url = "https://www.jstor.org/stable/25655426"
    # url = "https://www.jstor.org/stable/10.2307/i292640"
    headers = {"User-Agent": selected_user_agent}

    driver.get(url)

    page_source = driver.page_source

    soup = BeautifulSoup(page_source, "html.parser")

    driver.quit()

    volume_match = re.search(r"Vol\. (\d+)", soup.prettify())
    issue_match = re.search(r"No\. (\d+)", soup.prettify())
    year_match = re.search(r"(\d{4})", soup.prettify())

    issue = issue_match.group(1)
    volume = volume_match.group(1)
    year = year_match.group(1)

    papers = []
    titles = []
    check = True
    for li_tag in soup.find_all('li'):
        try:
            title = li_tag.a.get_text().strip()
        except:
            check = False
        if check and title not in titles and title != "Download" and title != "XML" and title != "Untitled"\
                and title not in usedTitles:
            link = "https://www.jstor.org" + li_tag.a['href']
            titles.append(title)
            papers.append(Paper(title, link, year, issue, volume))
            print(f"{title}, {link}")
        check = True

    return papers


def getAbstract(url, client):

    # response = client.get(url)

    current_time = dt.now()
    minutes = current_time.minute
    choice = minutes % 2
    if choice == 0:
        driver = webdriver.Chrome()
    else:
        driver = webdriver.Edge()

    driver.get(url)

    time.sleep(5)

    page_response = driver.page_source

    # soup = BeautifulSoup(response.content, "html.parser")
    soup = BeautifulSoup(page_response, "html.parser")

    title_tag = soup.find('title')

    if title_tag:
        title_text = title_tag.text.strip()
        if 'JSTOR: Access Check' in title_text:
            print("Caught!!!!")
            print("Caught!!!!")
            print("Caught!!!!")
            print("Caught!!!!")
            print("Caught!!!!")
            driver.quit()
            time.sleep(90)
            return False

    abstract_tag = soup.find("div", class_="abstract")

    toSleep = random.randint(0, 10)

    try:
        abstract_text = abstract_tag.get_text()
        # print(abstract_text)
    except:
        try:
            soup = str(soup)
            start_index = soup.find('<div data-v-6f3e0b52="">')
            end_index = soup.find('</div>', start_index)
            start_index + len('<div data-v-6f3e0b52> =')
            abstract_text = soup[start_index + len('<div data-v-6f3e0b52="">'):end_index]
            if "<" in abstract_text or ">" in abstract_text:
                abstract_text = None
        except:
            abstract_text = None
    if abstract_text is not None:
        print("Abstract found!\n")
        print(abstract_text.strip()[:20] + "\n")
        time.sleep(3)
        driver.quit()
        time.sleep(60+toSleep)
        return abstract_text.strip()
    else:
        print("Abstract not found\n")
        time.sleep(3)
        driver.quit()
        time.sleep(60+toSleep)
        return "no abstract available"


def createPaperObjects(url):
    with open("researchPapers.pickle", "rb") as f:
        try: papers = pickle.load(f)
        except: papers = []

    superTitles = []
    if papers:
        for paper in papers:
            superTitles.append(paper.getTitle())

    papers = papers + getTitlesAndLinks(url, superTitles)

    with open("researchPapers.pickle", "wb") as f:
        pickle.dump(papers, f)


def addAbstracts():
    with open("finishedSortedResearchPapers.pickle", "rb") as f:
        papers = pickle.load(f)
    client = ScrapingBeeClient(
        api_key='U6SWC1OLRV6NPVLC5PR31S94XIZLZAEOEYV0GSNCRJD7A5WCUZRZHFWU8BQL4HYZFAM6Z2EWS83SFEJN')
    for paper in papers:
        print("Checking " + str(paper.getLink()) + "  " + str(paper.getVolume()) + "  " + str(paper.getIssue()) + "\n")
        # if paper.getAbstract() == "abstract not set" or paper.getAbstract() == "no abstract available":
        if paper.getAbstract() == "abstract not set" or paper.getAbstract() == "no abstract available":
            abstract = getAbstract(paper.getLink(), client)
            if abstract:
                paper.setAbstract(abstract)
        with open("finishedSortedResearchPapers.pickle", "wb") as f:
            pickle.dump(papers, f)

    with open("finishedSortedResearchPapers.pickle", "wb") as f:
        pickle.dump(papers, f)


def downloadPDFHelper(link, volume, issue, abstract):
    end = ".pdf?refreqid=fastly-default%3Aced7de61c0e0d96a30edce1795b978a3&ab_segments=&origin=&initiator=&acceptTC=1"
    start = "https://www.jstor.org/stable/pdf/"
    newLink = start + link.split("/")[-1] + end
    driver = webdriver.Firefox()
    driver.get(newLink)

    # Wait for PDF to load
    time.sleep(3)

    try:
        download_button = driver.find_element(By.ID, "download")
        download_button.click()

        # Wait for download
        time.sleep(2)

        keyboard.press_and_release("left")
        toWrite = "V" + str(volume) + "_I" + str(issue) + "_"
        keyboard.write(toWrite)
        pyautogui.hotkey('command', 'a')
        pyautogui.hotkey('command', 'c')
        keyboard.press_and_release("enter")
        time.sleep(2)
        driver.close()
        print("PDF downloaded!\n")
        toReturn = pyperclip.paste() + ".pdf"
        print(toReturn + "\n")
        return toReturn
    except:
        print("FAILED")
        print("FAILED")
        print("FAILED")
        print("FAILED")
        print("FAILED\n")
        time.sleep(90)
        return None


def downloadPDFs():
    with open("finishedSortedResearchPapers.pickle", "rb") as f:
        papers = pickle.load(f)
    for p in papers:
        print("Checking " + str(p.getLink()) + "  " + str(p.getVolume()) + "  " + str(p.getIssue()) + "\n")
        if p.getPDF() is None and len(p.getAbstract()) > 50:
            pdfPath = downloadPDFHelper(p.getLink(), p.getVolume(), p.getIssue(), p.getAbstract())
            p.setPDF(pdfPath)
            with open("finishedSortedResearchPapers.pickle", "wb") as f:
                pickle.dump(papers, f)
            # toSleep = random.randint(0, 10)
            # time.sleep(60 + toSleep)
        else:
            if p.getPDF() is not None:
                print("Skipped, already gathered\n")
            else:
                print("Skipped, no abstract\n")


with open("finishedSortedResearchPapers.pickle", "rb") as f:
    papers = pickle.load(f)
i = 0
for p in papers:
    if p.getPDF() is not None:
        print(p.getPDF())
        i += 1
print(i)
