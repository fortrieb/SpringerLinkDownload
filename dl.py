#!/usr/local/bin/python3
'''
Author: Ajani Stewart

This code is liscenced under the MIT license
'''
from sys import argv
from csv import DictReader
from os import  mkdir, chdir
import concurrent.futures
from threading import Lock
import requests

count = 0
def download_book(row):
  url = "https://link.springer.com/content/pdf/"
  print(f"Downloading '{row['Item Title']}' ...",end='')
  item_doi = row['Item DOI'].split('/')
  cur_url = url + item_doi[0] + "%2f" + item_doi[1] + ".pdf"
  response = requests.get(cur_url)
  year = row['Publication Year']
  content_type = row['Content Type']
  item_title = ''.join(row['Item Title'].split(sep=' '))
  item_title = '"' + item_title + '"'

  book_title = f"{year + '_' + content_type + '_' + item_title}.pdf"
  with open(book_title,'wb') as book:
    book.write(response.content)
  with lock:
    if response.status_code == 200:
      global count
      count += 1
      print("done")
    else:
      print("failed")
  

if __name__ == "__main__":
  lock = Lock()
  count = 0
  input_csvs = argv[1:]

  for csv in input_csvs:
    out_dir = csv[:-4]
    mkdir(out_dir)
    chdir(out_dir)
    with open('../'+csv, "r") as csv_file:
      reader = DictReader(csv_file)
      with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(download_book, reader)
    chdir('..')
  print(f"Downloaded {count} files")