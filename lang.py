#! -*- coding: utf-8 -*-

from datetime import datetime
import html
import random
import re
import time
from click import argument
import requests
from fake_useragent import UserAgent
from lxml import etree

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup



class lang():
    def __init__(self, dic={}, tag='', translateFrom='google') -> None:
        self.dic = dic if dic else {}
        self.tag = tag
        self.translateFrom = translateFrom

    def transReactChinese(self, ses, to_='en'):
        ans = []
        nocomm = re.findall("(.*?)//", ses)
        
        if nocomm:
            new_ses = str().join(nocomm)
        else:
            new_ses = ses

        nocomm = re.findall("(.*?)\*", new_ses)
        if nocomm:
            new_ses = str().join(nocomm)


        xx = u"([(（\-]*\w*[\u4e00-\u9fff]+[.。，,;；)）>=\/\、\-(（\d:：？?\u4e00-\u9fff\w]*[\u4e00-\u9fff]+[.。，,;；(（+=\-)）~？?\w\d]*)"
        pattern = re.compile(xx)
        results = pattern.findall(new_ses)

        if results:
            for word in results:
                wd = self.translate(word, to_=to_)
                key = "{}_".format(self.tag) + wd[to_].replace(' ', '_')
                key = key.replace("'", '')
                wd["key"] = key
                ans.append(wd)
                key = "$t(/*{}*/'{}')".format(word, wd.get("key"))
                f = ses.find(word[0])
                if ses[f-1] == "'" or ses[f-1] == '"' or ses[f-1] == "`":
                    ses = ses.replace(ses[f-1], '', 1)
                e = ses.rfind(word[-1])
                if ses[e+1] == "'" or ses[e+1] == '"' or ses[e+1] == "`":
                    ses = ses.replace(ses[e+1], '', 1)
                ses = ses.replace(word, key, 1)
        return ses, ans


    def translate(self, word, from_='zh', to_='en'):

        if word in self.dic:
            wd = {from_: word, to_: self.dic[word][2], "key": "{}_".format(self.tag) + self.dic[word][2].replace(' ', '_')}
            return wd
        
        if self.translateFrom == "google":
            gfrom_ = 'zh-CN' if from_ == 'zh' else from_
            # 使用Google翻译翻译单词
            translateApi = "http://translate.google.cn/m?q=%s&tl=%s&sl=%s" % (word, to_, gfrom_)
            try:
                info = requests.get(translateApi)
            except Exception as error:
                time.sleep(1)
                info = requests.get(translateApi)
            data = info.text
            expr = r'(?s)class="(?:t0|result-container)">(.*?)<'
            result = re.findall(expr, data)

            print("成功翻译‘{}’至‘{}’".format(word, html.unescape(result[0])))
            res = html.unescape(result[0])
            wd = {from_: word, to_: res}

            
        elif self.translateFrom == "deepl":
            # translateApi = "https://www.deepl.com/translator#%s/%s/%s" % (from_, to_, word)

            # # 不显示页面
            # option=webdriver.ChromeOptions()
            # option.add_argument('headless')

            # # browser = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=option)
            # browser = webdriver.Chrome(ChromeDriverManager().install()) # 显示页面
            # browser.get(translateApi)
            # time.sleep(5) # 等待加载翻译结果

            # pagehtml = browser.page_source
            # bs = BeautifulSoup(pagehtml, "html.parser")
            # res = bs.find('div', id='target-dummydiv').get_text().strip()

            # print("成功翻译‘{}’至‘{}’".format(word, res))
            # wd = {from_: word, to_: res}

            proxies = {
                'https': 'http://127.0.0.1:41091'
            }

            word = '"' + word + '"'
            u_sentence = word.encode("unicode_escape").decode()
            data = '{"\
                jsonrpc":"2.0",\
                "method": "LMT_handle_jobs",\
                "params":\
                    {"jobs":[\
                        {"kind":"default",\
                        "raw_en_sentence":' + word + ',\
                        "raw_en_context_before":[],\
                        "raw_en_context_after":[],\
                        "preferred_num_beams":4,\
                        "quality":"fast"}\
                        ],\
                    "lang":{"user_preferred_langs":["EN","ZH"],\
                            "source_lang_computed":"ZH",\
                            "target_lang":"EN"\
                            },\
                    "priority": 1,\
                    "commonJobParams":{},\
                    "timestamp":' + str(int(time.time() * 10000)) + \
                    '},\
                "id":' + str(random.randint(1, 100000000)) + '}'

            r = requests.post('https://www2.deepl.com/jsonrpc',
                            headers={'content-type': 'application/json'},
                            data=data.encode(),
                            proxies=proxies)

            print(r.status_code)
            if r.status_code != 200:
                print(r.text)
            else:
                res =  r.json()['result']['translations'][0]['beams'][0]['postprocessed_sentence']
                print("成功翻译‘{}’至‘{}’".format(word, res))
                wd = {from_: word, to_: res}

        return wd


    
    def ip_proxy(self):
        ip_pool = [
            '119.98.44.192:8118',
            '111.198.219.151:8118',
            '101.86.86.101:8118',
            '111.155.124.78:8123'
        ]

        ip = ip_pool[random.randrange(0,4)]
        proxy_ip = 'http://'+ip
        proxies = {'http':proxy_ip}
        return proxies
    

if __name__ == "__main__":

    f = open('chinese.txt', encoding='utf-8')
    msg = f.read().split('\n')

    # res = lang(translateFrom='deepl').translate("风萧萧兮易水寒，壮士一去兮不复还")
    # for i in res:
    #     print(i)

    for i in msg:
        res = lang(translateFrom='google').translate(i)


    # print(lang().ip_proxy())


    # print(int(round(time.time() * 1000)))
