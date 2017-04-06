#!/usr/bin/env python
# encoding: utf-8


import random
import requests
from bs4 import BeautifulSoup
from multiprocessing import Pool

user_agent_list = [
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
]


def scrawl_list(url='https://movie.douban.com/tag/2016'):
    UA = random.choice(user_agent_list)
    headers = {'User-Agent': UA}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")
    article = soup.findAll('div', {'class': 'article'})[0]  # div for movies
    next_link = article.select('div.paginator > span.next > a')

    for table in article.findAll("table", {'class': 'infobox'}):
        table.extract()

    for div in article.findAll("div", {'class': ['clearfix', 'paginator']}):
        div.extract()

    # get all movie links
    p = Pool(20)
    for link in article.find_all('a', {'class': 'nbg'}):
        url = link.get('href')
        print(url)
        p.apply_async(scrawl_movie_info, args=(url, ))

    p.close()
    p.join()

    # get next page links
    print(next_link)
    if next_link:
        url = next_link[0].get('href')
        print(url)
        scrawl_list(url)


def scrawl_movie_info(url='https://movie.douban.com/subject/25980443/'):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    link = soup.select('#comments-section > div.mod-hd > h2 > span > a')[0].get('href')
    # print(link.get('href'))
    scrawl_movie_comments(link)


def scrawl_movie_comments(url):
    r = requests.get(url)
    # print(r.text)
    soup = BeautifulSoup(r.text, "html.parser")
    for item in soup.findAll('div', {'class': 'comment-item'}):
        for comment in item.findAll('p'):
            desc = comment.text  # get comment

        for rating in item.findAll('span', {'class': 'rating'}):
            score = rating['class'][0][7:]
            # print(score)

        print(score, desc)



scrawl_list()
# scrawl_movie_comments('https://movie.douban.com/subject/25980443/comments?status=P')

