import re
import requests
import os
import time
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
    "Connection": "keep-alive",
    "Accept": "text/html,application/json,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.8"}

# 知乎问题id
question_id = 319709102
#爬取的回答数
answers_num = 10
#爬取起点
answer_startnum = 0
#排序方式
sorted_choi = 'default' #按时间排序则修改为updated

# 结果存放根目录
result_path = "./result"

#问题title
title = "穿 JK 制服上街是什么体验？"

#爬取头像存放根目录
save_path = os.path.join(result_path,title)

pattern = re.compile('''<img\s.*?\s?data-original\s*=\s*['|"]?([^\s'"]+).*?>''')
while answer_startnum<answers_num:
    try:
        url = url = f'https://www.zhihu.com/api/v4/questions/{question_id}/answers?include=content&limit={answers_num}&offset={answer_startnum}&sort_by=default'
        html = requests.get(url,headers=headers)
        print(html)
        answers = html.json()['data']
        for answer in answers:
            author = answer['author']['name']
            content = answer['content']
            results = re.findall(pattern,content)
            results = results[::2]
            imgpath = os.path.join(save_path,author)
            if not os.path.isdir(imgpath):
                os.makedirs(imgpath)
            for i,imgurl in enumerate(results):
                res = requests.get(imgurl)
                with open(imgpath+'/{}.jpg'.format(i),'wb') as f:
                    f.write(res.content)
                print(i)
        answer_startnum += answers_num
    except requests.ConnectionError:
        print('Failed to connect')