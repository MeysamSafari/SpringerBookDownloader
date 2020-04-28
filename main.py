import os
import re
import threading
from concurrent.futures import as_completed
from concurrent.futures import ThreadPoolExecutor
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup as bs
from time import gmtime, strftime
from pathlib import Path

lock = threading.Lock()


def downloader(url: str, folder_name: Path) -> Path:
    with lock:
        print("downloading:", url, "\n\n")
    r = requests.get(url)
    book_id = r.url.rsplit('/', 1)[1]
    soup = bs(r.content, 'lxml')
    page_title = soup.title.text
    page_title_file_name = page_title.rsplit(' |', 1)[0].replace(' ', '_').replace('/', '_') + '.pdf'
    result_file = os.path.join(folder_name, page_title_file_name)
    download_url = urljoin("https://link.springer.com/content/pdf/", book_id)
    with open(result_file, 'wb') as f:
        f.write(requests.get(download_url + '.pdf').content)

    return result_file


def main():
    file_name = Path(input("Enter file name with list of book names and their URLs ..."))
    if not file_name.exists():
        raise FileNotFoundError(f"{str(file_name)} does't exist")
    folder_name = Path(input('Enter the folder name to be created to store all pdf files ...'))
    folder_name.mkdir(parents = True, exist_ok = True)

    print('Start time:', strftime("%Y-%m-%d %H:%M:%S", gmtime()))

    url_pattern = re.compile('http://[^\s]+')
    urls = url_pattern.findall(file_name.read_text(encoding = 'UTF8'))

    with ThreadPoolExecutor(max_workers = 10) as pool:
        jobs = {pool.submit(downloader, url, folder_name) for url in urls}
        for job in as_completed(jobs):
            result_file = job.result()
            with lock:
                print(f"Enjoy reading the {result_file.name}. It is downloaded successfully!!!")
                print("File available at:", str(result_file.absolute()), "\n\n")

    print(strftime("%Y-%m-%d %H:%M:%S", gmtime()))


if __name__ == '__main__':
    main()