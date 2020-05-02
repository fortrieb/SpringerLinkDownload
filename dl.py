#!/usr/local/bin/python3
'''
Author: Ajani Stewart

This code is liscenced under the MIT license
'''
from sys import argv
from csv import DictReader, QUOTE_ALL
from os import mkdir, chdir, path
from argparse import ArgumentParser, Namespace
import logging
import glob
import concurrent.futures
from threading import Lock
import requests

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger("Downloader")

BASE_PDF_URL = "https://link.springer.com/content/pdf/"
BASE_EPUB_URL = "https://link.springer.com/download/epub/"


def dl_arg_parser() -> Namespace:
    """Parse cli argument for download program
  
  :return: parsed argument namespace
  """
    parse = ArgumentParser()
    parse.add_argument("folder", type=str, help="Path folder with CSV files")
    parse.add_argument("--epub",
                       default=False,
                       help="Trying to download ePub file",
                       dest="epub",
                       action="store_true")
    return parse.parse_args()


def download_book(csv, folder: str, epub: bool):
    e = concurrent.futures.ThreadPoolExecutor(max_workers=4)
    with open(csv, "r") as csv_file:
        reader = DictReader(csv_file, quotechar='"', skipinitialspace=True)
        for row in reader:
          e.submit(process_row, row, folder, epub)
    e.shutdown(wait=True)

def process_row(row: str, folder: str, epub: bool):
    """ Row processesing 
    :param row: current row from CSV file
    :param folder: folder to store file
    :param epub: EPUB file should downloaded
    """
    row_title = row['Item Title'].strip('\"')
    log.debug("Start downloading: %s", row_title)
    item_doi = row['Item DOI'].split('/')
    cur_url_pdf = BASE_PDF_URL + item_doi[0] + "%2f" + item_doi[1] + ".pdf"
    cur_url_epub = BASE_EPUB_URL + item_doi[0] + "%2f" + item_doi[
        1] + ".epub"
    response = requests.get(cur_url_pdf)
    response_epub = None
    if epub:
        response_epub = requests.get(cur_url_epub)
    year = row['Publication Year']
    content_type = row['Content Type']
    item_title = ''.join(row_title.split(sep=' '))

    book_pdf_title = f"{year + '_' + content_type + '_' + item_title}.pdf"
    book_epub_title = f"{year + '_' + content_type + '_' + item_title}.epub"

    # Epub
    if epub and response_epub:
        if response_epub.status_code == 200:
            log.debug("Epub: %s", path.join(folder, book_epub_title))
            with open(path.join(folder, book_epub_title), 'wb') as book:
                if response.status_code == 200:
                    log.info("Finished %s", book_epub_title)
                book.write(response_epub.content)
        else:
            log.error("EPUB not found for %s", item_doi)
    # PDF
    log.debug("PDF: %s", path.join(folder, book_pdf_title))
    with open(path.join(folder, book_pdf_title), 'wb') as book:
        if response.status_code == 200:
            log.info("Finished %s", book_pdf_title)
        book.write(response.content)


if __name__ == "__main__":
    args = dl_arg_parser()
    log.debug("CSV files in folder %s", args.folder)
    # read CSV files
    csvs = [f for f in glob.glob(path.join(args.folder, "*.csv"))]
    log.debug("Files found: %s", csvs)
    executor = concurrent.futures.ThreadPoolExecutor(max_workers=2)
    futures = []
    for csv in csvs:
        log.debug("Process file: %s", csv)
        base_name = path.basename(csv)
        out_dir = path.join(args.folder, path.splitext(base_name)[0])
        # check file is present
        if not path.exists(out_dir):
            log.debug("Output directory not exists. Create %s", out_dir)
            mkdir(out_dir)
        log.debug("Output dir: %s", out_dir)
        futures.append(executor.submit(download_book, csv, out_dir, args.epub))
    executor.shutdown(wait=True)
