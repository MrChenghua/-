# 抓取实验楼课程内容
在使用实验楼平台学习的过程中，有时需要查阅之前课程所讲的一些知识点。但是往往进入实验环境后，再查看之前课程文档需要再重新开一个或多个页面而且每个文档字体过大导致页面所呈现内容较少，查找较为耗时。于是便有了将所学的课程都下载为markdown形式的txt的想法。

## 1. 用户登陆
由于是要查看用户自身的课程内容，所以需要先行登陆，才能查看到课程列表。因为本人用的weibo的auth2登陆shiyanlou，本身比较复杂，所以最后我选择现在浏览器登陆保存下来登陆的Cookie，之后再将Cookie加入到header中，完成用户登陆。下图为使用Firefox浏览器，截取的Cookie：
<img src="https://user-images.githubusercontent.com/31018275/30380240-14954726-9867-11e7-884a-403b064f67dd.png" width="700"/>

根据获得的Cookie设置header：

```
headers = {'Connection' : 'keep-alive',    
           'Cookie': Cookie #此插入所获得的Cookie
           "Referer":"www.shiyanlou.com",
           "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0",
           "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
           "Accept-Language":"en-US,en;q=0.5"}
```

随后用这个header访问User界面：
```
user_url = User account url # 用户的url
r = requests.get(user_url,headers=headers)
r.encoding = r.apparent_encoding #保证编码一致，输出正确中文格式
user_Soup = BeautifulSoup(r.text, "lxml") #抓取网址解码
```
## 2. 搜索课程
上一步已经完成了用户登陆以及用户页面抓取，通过web-developer发现课程名称和链接都在\<div class = 'course-img col-md-4'>中：

<img src = "https://user-images.githubusercontent.com/31018275/30387701-5fa44cbc-987b-11e7-9cec-725747144aa3.png" width="500">

课程链接在\<a href>中保存，而课程名称在\<img alt>里。于是通过以下代码可以遍历得到每个课程的链接以及名称：

```
courses_url = user_Soup.find_all('div',class_="course-img col-md-4")
for i in courses_url:
    course_name = i.img['alt'] # 课程名称
    course_url = "https://www.shiyanlou.com"+i.a['href'] # 课程链接
    os.makedirs(os.path.join("/Users/.../shiyanlou_doc", course_name)) # 创建课程文件夹
    os.chdir("/Users/.../shiyanlou_doc"+course_name) # 进入文件夹
    get_txt(course_url) # 抓取课程文本
```

同时为了保存课程内容到相应课程的文件中，上述代码加入os.makedirs以及os.chdir来创建课程文件夹和进入该文件夹，从而使课程文本能保存在与该课程名称对应的文件夹中。

## 3. 抓取课程文本

上面已经获得了课程的url，进入链接找到课程文档所在的链接并抓取内容文本及可。同样使用web-developer就可以找到相应内容所在的位置，这里就不赘述了。唯一需要注意的是，发现如果不人为的加入sleep函数，程序在运行过程中会报错。可能是因为网站有反爬虫机制，在加入sleep(5)后程序运行正常。最终将所有实验楼线上课程都保存成了markdown格式的txt文本。

<img src = "https://user-images.githubusercontent.com/31018275/30391324-f37f447c-9886-11e7-8620-21c2c7f6b980.png" width="500">

[完整代码](https://github.com/MrChenghua/-/blob/master/shiyanlou_doc_markdown.py)已经上传。





