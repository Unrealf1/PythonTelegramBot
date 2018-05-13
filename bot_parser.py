import requests
from bs4 import BeautifulSoup
import re


def get_rbkstyle_themes(url, class_name):
    page = requests.get(url)
    soup = BeautifulSoup(page.text, 'html.parser')
    return soup.find_all(class_= class_name)


print("here start:\n")
themes = get_rbkstyle_themes('https://www.rbc.ru/story/', 'item_story')

for theme in themes:
    theme_name = theme.contents[1].contents[1].contents[0]
    print("name: " + theme_name)
    theme_description = str(theme.contents[1].contents[3].contents[0]).strip()
    print("description: ", theme_description)
    theme_link = re.findall(r"\"https\S*\"", str(theme))[0][1:-1]
    print("link: " + theme_link)
    print()
    docs = get_rbkstyle_themes(theme_link, 'item_story-single')
    for doc in docs:
        doc_name = doc.contents[1].contents[1].contents[0]
        print("  name: " + doc_name)
        doc_description = doc.contents[1].contents[3].contents[0].strip()
        print("  description: ", doc_description)
        doc_link = re.findall(r"\"https\S*\"", str(doc))[0][1:-1]
        print("  link: " + doc_link)
        print()
        doc_page = requests.get(doc_link)
        doc_soup = BeautifulSoup(doc_page.text, 'html.parser')
        # print(doc_soup.findAll('p')[0])
        doc_text = ''
        for paragraph in doc_soup.findAll('p'):
            doc_text += str(paragraph)[3:-4] + '\n'
        print("TEXT:")
        f = open("TEXT", 'w')
        f.write(str(doc_text))
        f.close()
        print(doc_text)
        exit()
