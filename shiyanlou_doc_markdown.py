import requests
from bs4 import BeautifulSoup
import os
import time # 加时间delay


user_url = User account url

# 绕过Weibo的Auth2验证，直接用Cookies登陆
headers = {'Connection' : 'keep-alive',    
           'Cookie': Cookie
           "Referer":"www.shiyanlou.com",
           "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0",
           "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
           "Accept-Language":"en-US,en;q=0.5"}

r = requests.get(user_url,headers=headers)

r.encoding = r.apparent_encoding #编码一致

user_Soup = BeautifulSoup(r.text, "lxml") #抓取网址解码

courses_url = user_Soup.find_all('div',class_="course-img col-md-4")
  

def get_txt(url):
    course_url =url
    r = requests.get(course_url,headers=headers)
    r.encoding = r.apparent_encoding #编码一致
    Soup = BeautifulSoup(r.text, "lxml") #抓取网址解码
    
    #Get all files name
    docu_content = Soup.find_all('div',class_="lab-item-header")
    docu_url = [i.a['href'] for i in docu_content if i.a is not None]
    docu_name = [i.find('div',class_="lab-item-title").text for i in docu_content]
    
    
    tmp_index = 1
    for u, n in zip(docu_url, docu_name[:len(docu_url)]):
        if u!= '#':
            tmp_url = 'https://www.shiyanlou.com'+u
            tmp_r = requests.get(tmp_url,headers=headers)
            tmp_r.encoding = tmp_r.apparent_encoding #编码一致
            tmp_Soup = BeautifulSoup(tmp_r.text, "lxml")
            textarea = tmp_Soup.find("textarea")
            f = open(str(tmp_index) +'. '+ n +'.txt', 'a')
            f.writelines(textarea)
            f.close()
            tmp_index = tmp_index+1
            time.sleep(5)

for i in courses_url:
    course_name = i.img['alt']
    course_url = "https://www.shiyanlou.com"+i.a['href']
    os.makedirs(os.path.join("/Users/.../shiyanlou_doc", course_name))
    os.chdir("/Users/.../shiyanlou_doc"+course_name)
    get_txt(course_url)