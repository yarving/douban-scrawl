#-*- coding: UTF-8 -*-


import requests
from bs4 import BeautifulSoup
import urllib
import re
import time 
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


s = requests.Session()
url =  'https://accounts.douban.com/login'
data={
    'redir': 'https://www.douban.com/',
    'form_email':'-----',
    'form_password':'----',
    'login':'登录'
}

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6'}
r = s.post(url, data, headers=headers )
page = r.text

soup = BeautifulSoup(page,"html.parser")
captcha_url = soup.find('img',id='captcha_image')['src']
pattern = re.compile('<input type="hidden" name="captcha-id" value="(.*?)"/')
captcha_id = re.findall(pattern, page)

urllib.urlretrieve(captcha_url,"captcha.jpg")
captcha = raw_input('please input the captcha:')
data['captcha-solution'] = captcha
data['captcha-id'] = captcha_id

r = s.post(url, data=data, headers=headers )


# soup = BeautifulSoup(r.text,"html.parser")
# movie_link = soup.select('#db-global-nav > div > div.global-nav-items > ul > li > a')[2].get('href')
# print(movie_link)

'''
具体解析评论页面的函数
'''

def scrawl_movie_comments(i,url):
    r = s.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    #f=open('/users/xuye/desktop/test1.txt','a')
    for item in soup.findAll('div', {'class': 'comment-item'}):
        f=open('/users/xuye/desktop/test1.txt','a')
        for comment in item.findAll('p'):
            global desc
            desc = comment.text 
            # print(desc)
             # get comment

        for rating in item.findAll('span', {'class': 'rating'}):
            global score
            score = str(int(rating['class'][0][7:]) / 10)
            # print(score)

        print(score + desc)
        f.write(score + ' ' + desc + '\n')

    print(str(i) + '---------------------')
    print r.status_code
    f.close()
	


# for i in range(200,1001,20):
# 	url=movie_link + 'subject/25980443/comments?start={}&limit=20&sort=new_score&status=P'.format(i)
# 	scrawl_movie_info(url)

def scrawl_movie_info(url):
    #comment_url = url + 'comments?start={}&limit=20&sort=new_score&status=P'.format(i)
    '''
    r = requests.get(url)
    soup = BeautifulSoup(r.text,"html.parser")
    link = soup.select('#comments-section > div.mod-hd > h2 > span > a')[0].get('href')
    #comments-section > div.mod-hd > h2 > span > a
    #print link
    '''
    r = s.get(url)
    soup = BeautifulSoup(r.text, "html.parser")
    num = str(soup.select('#comments-section > div.mod-hd > h2 > span > a')[0]).split('>')[1][6:12]
    # print(num)
    num = num[1:]
    
    num = int(str(num)[0:1]) * (10 ** (len(str(num)) - 1))
    #print num
    for i in range(0,num+1,20):
        comment_url = url + 'comments?start={}&limit=20&sort=new_score&status=P'.format(i)
        scrawl_movie_comments(i,comment_url)
        print(str(i) + '------------------------------')

def main():
    r = s.get('https://movie.douban.com/tag/2016')
    soup = BeautifulSoup(r.text,"html.parser")
    #print(soup)
    article = soup.findAll('div', {'class': 'article'})[0]
    #print(article)
      # div for movies
    for table in article.findAll("table", {'class': 'infobox'}):
        table.extract()

    for div in article.findAll("div", {'class': ['clearfix', 'paginator']}):
        div.extract()

    # get all movie links
    for link in article.find_all('a', {'class': 'nbg'}):
        #print(link.get('href'))
		scrawl_movie_info(link.get('href'))

main()




'''
page = r.text
soup = BeautifulSoup(page,"html.parser")
result = soup.findAll('div',attrs={'class':'title'})
# print result
for item in result:
    print item.find('a').get_text()
'''