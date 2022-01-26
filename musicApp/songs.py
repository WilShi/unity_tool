import os
from sys import argv
import time
from lxml import etree
import requests
import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

class Songs:

    def __init__(self) -> None:

        self.pool = ThreadPoolExecutor(max_workers=10)

        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3741.400 QQBrowser/10.5.3863.400"
        }

        self.path = '{}/Downloads/music'.format(str(Path.home()))
        if not os.path.exists(self.path): os.makedirs(self.path)

    def download(self, id, name):

        url = f'http://music.163.com/song/media/outer/url?id={id}'
        response = requests.get(url=url, headers=self.headers, timeout=5).content

        path = '{}/{}.mp3'.format(self.path, name)
        with open(path,'wb') as f:
            f.write(response)

        print(name,'下载完成')


    def get_id(self, url):

        response = requests.get(url=url, headers=self.headers).text

        # with open("test222.txt", 'w', encoding='utf-8') as f:
        #     f.write(response)

        page_html = etree.HTML(response)
        id_list = page_html.xpath('//textarea[@id="song-list-pre-data"]/text()')[0]
        

        songinfo = {}
        for i in json.loads(id_list):
            name = i['name']
            id = i['id']
            author = i['artists'][0]['name']
            songinfo[id] = name+'-'+author
        return songinfo


    def start(self, url):

        link = "https://music.163.com/discover/toplist?id="
        url = f"{link}{url[url.find('=')+1:]}"
        print(url)

        ids = self.get_id(url)
        
        for id in ids:
            # print(id, ids[id])
            self.pool.submit(self.download, id, ids[id])
        self.pool.shutdown()

        print("爬取完毕")



if __name__ == '__main__':
    # url = 'https://music.163.com/discover/toplist?id=3778678'#id可以自行更改

    # get_id(url)

    # Songs().download('1336856777', '我曾-隔壁老樊')

    Songs().start(argv[1])