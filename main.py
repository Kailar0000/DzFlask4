import multiprocessing
import threading
import asyncio
import aiohttp
import requests

from urllib.parse import urlparse
from posixpath import basename

import os
import sys
import time

# urls = ['https://gas-kvas.com/uploads/posts/2023-02/1675446644_gas-kvas-com-p-kartinki-na-fonovii-risunok-rabochego-11.jpg',
#         'https://gas-kvas.com/grafic/uploads/posts/2023-10/1696581493_gas-kvas-com-p-kartinki-vsyakie-9.jpg',
#         'https://w.forfun.com/fetch/f1/f1288f09927aafd68470ea0b626645fd.jpeg',
#         'https://mykaleidoscope.ru/x/uploads/posts/2022-10/1666206281_64-mykaleidoscope-ru-p-kartinka-na-zastavku-oboi-65.jpg',
#         'https://w.forfun.com/fetch/25/25b9ef112453bb3c4ae59da72c1f33d7.jpeg'
#         ]

def get_name(urls):
    urls_name = {}
    for index, url in enumerate(urls):
        parse_object = urlparse(url)
        name = basename(parse_object.path)
        urls_name[name] = url
    return urls_name



def checkUrls(urls):
    folder = 'data_task_1'
    if not os.path.exists(folder):
        os.mkdir(folder)
    for index, url in urls.items():
        name = os.path.join(folder, f'{index}.jpg')
        download_data(url, name)


def download_data(url, filename):
    with open(filename, 'wb') as handle:
        response = requests.get(url, stream=True)
        handle.write(response.content)


def threads(urls):
    threads = []
    start_time = time.time()
    folder = 'data_task_1'
    if not os.path.exists(folder):
        os.mkdir(folder)

    for index, url in urls.items():
        name = os.path.join(folder, f'{index}.jpg')
        thread = threading.Thread(target=download_data, args=[url, name])
        threads.append(thread)

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
    print(f"Многопоточный: {time.time() - start_time}")
    # checkUrls()


def multiproces(urls):
    processes = []
    start_time = time.time()
    folder = 'data_task_1'
    if not os.path.exists(folder):
        os.mkdir(folder)

    for index, url in urls.items():
        name = os.path.join(folder, f'{index}.jpg')
        p = multiprocessing.Process(target=download_data, args=[url, name])
        processes.append(p)

    for p in processes:
        p.start()

    for p in processes:
        p.join()
    print(f"Многопроцессорный: {time.time() - start_time}")


def async_task(urls):
    tasks = []
    processes = []
    start_time = time.time()
    folder = 'data_task_1'
    if not os.path.exists(folder):
        os.mkdir(folder)

    for index, url in enumerate(urls):
        name = os.path.join(folder, f'{index}.jpg')
        task = asyncio.ensure_future(async_download(url, name))
        tasks.append(task)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(asyncio.wait(tasks))
    print(f"Асинхронный метод: {time.time() - start_time}")


async def async_download(url, failname):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as respons:
            img = respons.read()
            with open(failname, 'wb') as f:
                f.write(img)

if __name__ == '__main__':
    urls = sys.argv
    urls.pop(0)
    urls_name = get_name(urls)
    print(urls_name)
    threads(urls_name)
    multiproces(urls_name)
    # async_task(urls)
