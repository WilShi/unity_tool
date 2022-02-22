import base64
import os
import random
from sys import argv
import time
from lxml import etree
from matplotlib.artist import Artist
import requests
import json
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from Crypto.Cipher import AES
import binascii
from urllib import parse

class Songs:

    def __init__(self) -> None:

        self.pool = ThreadPoolExecutor(max_workers=10)

        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3741.400 QQBrowser/10.5.3863.400"
        }

        self.path = '{}/Downloads/music'.format(str(Path.home()))
        if not os.path.exists(self.path): os.makedirs(self.path)


    def download(self, id, name, outpath=''):
        url = f'http://music.163.com/song/media/outer/url?id={id}'
        response = requests.get(url=url, headers=self.headers, timeout=5).content

        outpath = self.path if not outpath else outpath
        path = '{}/{}.mp3'.format(outpath, name)
        with open(path,'wb') as f:
            f.write(response)

        print(f"{name} 下载完成 {'='*10} 路径为：{path}")


    def getmusic(self, id):
        url = f'http://music.163.com/song/media/outer/url?id={id}'
        response = requests.get(url=url, headers=self.headers, timeout=5).content
        # print(response)
        return response


    def get_id(self, url):
        response = requests.get(url=url, headers=self.headers).text

        # with open("test.txt", 'w', encoding='utf-8') as f:
        #     f.write(response)

        page_html = etree.HTML(response)
        id_list = page_html.xpath('//textarea[@id="song-list-pre-data"]/text()')[0]
        
        songinfo = {}
        for i in json.loads(id_list):
            name = i['name']
            id = i['id']
            author = i['artists'][0]['name']
            songinfo[id] = f"{name}-{author}"
        return songinfo


    def start(self, mode, arg1, arg2=''):

        if mode == "list":
            # link = "https://music.163.com/discover/toplist?id="
            # url = f"{link}{url[url.find('=')+1:]}"
            url = arg1.replace('#/', '') if "toplist" in arg1 else arg1
            print(url)
            ids = self.get_id(url)
            for id in ids:
                # print(id, ids[id])
                self.pool.submit(self.download, id, ids[id])
            self.pool.shutdown()
            print("爬取完毕")

        if mode == "search":
            print(f"开始搜索功能...... 开始搜索 {arg1}")

            result = Search().get_music_id(arg1)
            for i in result:
                print(f"歌曲ID：{i} {'='*10} 歌曲名：{result[i]} {'='*10} 下载用：{i} {result[i]}")

        if mode == "download":
            self.download(arg1, arg2)
            


class Search():

    # 设置从JS文件提取的RSA的模数、协商的AES对称密钥、RSA的公钥等重要信息
    def __init__(self):
        self.modulus = "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b3ece0462db0a22b8e7"
        self.nonce = '0CoJUm6Qyw8W8jud'
        self.pubKey = '010001'
        self.url = "https://music.163.com/weapi/cloudsearch/get/web?csrf_token="
        self.HEADER = {}
        self.setHeader()
        self.secKey = self.getRandom()
 
    # 生成16字节即256位的随机数
    def getRandom(self):
        string = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
        res = ""
        for i in range(16):
            res += string[int(random.random()*62)]
        return res
 
    # AES加密，用seckey对text加密
    def aesEncrypt(self, text, secKey):
        pad = 16 - len(text) % 16
        text = text + pad * chr(pad)
        encryptor = AES.new(secKey.encode('utf-8'), 2, '0102030405060708'.encode('utf-8'))
        ciphertext = encryptor.encrypt(text.encode('utf-8'))
        ciphertext = base64.b64encode(ciphertext).decode("utf-8")
        return ciphertext
 
    # 快速模幂运算，求 x^y mod mo 
    def quickpow(self, x, y, mo):
        res = 1
        while y:
            if y & 1:
                res = res * x % mo
            y = y // 2
            x = x * x % mo
        return res 
 
    # rsa加密
    def rsaEncrypt(self, text, pubKey, modulus):
        text = text[::-1]
        a = int(binascii.hexlify(str.encode(text)), 16)
        b = int(pubKey, 16)
        c = int(modulus, 16)
        rs = self.quickpow(a, b, c)
        return format(rs, 'x').zfill(256)
 
    # 设置请求头
    def setHeader(self):
        self.HEADER = {
            'Accept': '*/*',
            'Accept-Encoding': 'gzip,deflate,sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8,gl;q=0.6,zh-TW;q=0.4',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'music.163.com',
            'Referer': 'https://music.163.com/search/',
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/33.0.1750.152 Safari/537.36'
        }
 
    # 设置相应的请求参数，从而搜索列表
    # 总体的密码加密步骤为：
    # 首先用nonce对text加密生成密文1
    # 然后用随机数seckey加密密文1生成密文2
    # 随后，用公钥加密seckey生成密文3
    # 其中，密文2作为请求参数中的params，密文3作为encSeckey字段
    # 这样，接收方可以通过私钥解密密文3获得seckey(随机数)
    # 然后用seckey解密密文2获得密文1
    # 最终用统一协商的密钥nonce解密密文1最终获得text
    def search(self, s, offset, type="1"):
        text = {"hlpretag": "<span class=\"s-fc7\">",
            "hlposttag": "</span>",
            "#/discover": "",
            "s": s,
            "type": type,
            "offset": offset,
            "total": "true",
            "limit": "30",
            "csrf_token": ""}
        text = json.dumps(text)
        params = self.aesEncrypt(self.aesEncrypt(text, self.nonce), self.secKey)
        encSecKey = self.rsaEncrypt(self.secKey, self.pubKey, self.modulus)
        data = {
            'params': params,
            'encSecKey': encSecKey
        }
        result = requests.post(url=self.url,
                                data=data,
                                headers = self.HEADER).json()
        return result


 
    # 获取指定音乐列表
    def get_music_id(self, keywords):
        # music_list = []
        songinfo = {}
        for offset in range(1):
            result = self.search(keywords, str(offset))
            result = result['result']['songs']
            for music in result:
                # if music['copyright'] == 1 and music['fee'] == 8:
                if (music['privilege']['fee'] == 0 or music['privilege']['payed']) and music['privilege']['pl'] > 0 and music['privilege']['dl'] == 0:
                    continue
                if music['privilege']['dl'] == 0 and music['privilege']['pl'] == 0:
                    continue
                # if music['fee'] == 8:

                name = music['name']
                id = music['id']
                artist = music['ar'][0]['name']
                songinfo[id] = f"{name}-{artist}"
                # music_list.append(music)
                # print(music)

        return songinfo


    def get_music_link(self, id, name=''):
        text = {
            "ids": "[" + str(id) + "]", 
            "level": "standard", 
            "encodeType": "",
            "csrf_token": ""
            }
            
        text = json.dumps(text)
        params = self.aesEncrypt(self.aesEncrypt(text, self.nonce), self.secKey)
        encSecKey = self.rsaEncrypt(self.secKey, self.pubKey, self.modulus)

        url = "https://music.163.com/weapi/song/enhance/player/url/v1?csrf_token="

        payload = 'params=' + parse.quote(params) + '&encSecKey=' + parse.quote(encSecKey)

        headers = {
            'authority': 'music.163.com',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
            'content-type': 'application/x-www-form-urlencoded',
            'accept': '*/*',
            'origin': 'https://music.163.com',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://music.163.com/',
            'accept-language': 'zh-CN,zh;q=0.9'
        }
        
        response = requests.request("POST", url, headers=headers, data=payload, timeout=5)
        if response.status_code == 200:
            response = json.loads(response.text)
            url = response['data'][0]['url']
            level = response['data'][0]['level']
            return {"url": url, "level": level} if not name else {"url": url, "level": level, "name": name}
        else:
            return {"msg": "获取失败"}



if __name__ == '__main__':
    # url = 'https://music.163.com/discover/toplist?id=3778678'#id可以自行更改

    if argv[1] == "test":
        print(Search().get_music_link(argv[2]))
        
    elif len(argv) == 3:
        Songs().start(argv[1], argv[2])
    elif len(argv) == 4:
        Songs().start(argv[1], argv[2], argv[3])      
    else:
        print({"error": 1, "msg": "python songs.py [list|search|download] [url|songName|songID] [''|''|songName]"})