from bs4 import BeautifulSoup
import requests
import re


def get_items(link):
    page = requests.get(link)
    soup = BeautifulSoup(page.content, 'html.parser')

    scraped_data = soup.findAll(['th', 'a'])
    cleaned_data = clean_data(scraped_data)
    cleaned_data = remove_unnecessary_data(cleaned_data)
    cleaned_data = replace_roman_numerals(cleaned_data)

    return remove_redundancies(cleaned_data)


def clean_data(scraped_data):
    cleaned_data = []

    for item in scraped_data:
        if '<a href="/fipu/predmet/' in str(item) or 'predmetispis_seme' in str(item):
            cleaned_data.append(remove_html_tags(str(item)))

    return cleaned_data


def remove_unnecessary_data(items):
    clean_items = []

    for item in items:
        item = re.sub(''' \(\d+\)''', '', item)
        clean_items.append(item)

    return clean_items


def replace_roman_numerals(items):
    clean_items = []

    for item in items:
        item = item.replace(" I ", " 1 ").replace(" II ", " 2 ")
        clean_items.append(item)

    return clean_items


def remove_redundancies(subjects):
    indices = [i for i, x in enumerate(subjects) if x == subjects[0]]

    if len(indices) > 1:
        return subjects[0:indices[1]]
    else:
        return subjects


def remove_html_tags(text):
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text).strip()

