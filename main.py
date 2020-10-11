import os
import re
import csv
import json
import urllib.request
from bs4 import BeautifulSoup

user_agent = os.getenv('USER_AGENT', (
  'Mozilla/5.0 (compatible; VNDBQuoteBot/1.0; '
  '+https://github.com/vndb-quote-service/vndb-quotes)'
))

def get_quote(txt):
  soup = BeautifulSoup(txt, 'html.parser')
  el = soup                                \
    .find('div', id='footer')              \
    .find('a', href=re.compile(r'^/v\d+'))
  return el and el.get_text(), f'https://vndb.org{el["href"]}'

def get_title(txt):
  soup = BeautifulSoup(txt, 'html.parser')
  el = soup.find('div', class_='mainbox')
  title, alt_title = el.find('h1'), el.find('h2', class_='alttitle')
  return title and title.get_text(), alt_title and alt_title.get_text()

def vndb_req(url):
  headers = { 'User-Agent': user_agent }
  req = urllib.request.Request(url, headers=headers)
  return urllib.request.urlopen(req).read().decode()

def main():
  mainpage = vndb_req('https://vndb.org')
  quote, link = get_quote(mainpage)
  detailspage = vndb_req(link)
  title, alttitle = get_title(detailspage)

  data = {
    'quote': quote,
    'link': link,
    'title': title,
    'alt_title': alttitle
  }
  fieldnames = list(data.keys())

  with open('vndb.csv_excel', 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames, dialect='excel')
    writer.writeheader()
    writer.writerow(data)

  with open('vndb.csv', 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames, dialect='unix')
    writer.writeheader()
    writer.writerow(data)

  with open('vndb.tsv', 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=fieldnames, dialect='excel-tab')
    writer.writeheader()
    writer.writerow(data)

  with open('vndb.json', 'w', newline='') as file:
    json.dump(data, file)


if __name__ == '__main__':
  main()

