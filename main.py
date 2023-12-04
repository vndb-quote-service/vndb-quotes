# The MIT License (MIT)
# Copyright © 2020 Takase
# Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the “Software”), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
# The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

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
    .find('footer')                        \
    .find('a', href=re.compile(r'^/v\d+'))
  print(f"quote: {el and el.get_text()}, id: {el['href']}")
  return el and el.get_text(), f'https://vndb.org{el["href"]}'

def get_title(txt):
  soup = BeautifulSoup(txt, 'html.parser')
  el = soup.select_one('main article:first-child')
  title, alt_title = el.find('h1'), el.find('h2', class_='alttitle')
  print(f"title: {title and title.get_text()}, alt title: {alt_title and alt_title.get_text()}")
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

