import requests
import pandas as pd
import random
import jieba
from stylecloud import gen_stylecloud
from wordcloud import WordCloud
import cv2
import jieba.analyse
from PIL import Image
import numpy as np
import collections
import json
# 这样我们就可以完成列表页前十页链接的爬取了
# 但是我们还是需要每个详情页的具体链接
# 在列表页中提取出数据

def pa():

    pro = ['122.152.196.126', '114.215.174.227', '119.185.30.75']
    index_url = "https://m.douban.com/rexxar/api/v2/gallery/topic/325990/items?"
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36 SLBrowser/7.0.0.12151 SLBChan/25",
        "Referer": "https://www.douban.com/gallery/topic/325990/"
    }
    commit = []
    loc=[]
    for i in range(0, 150):
        paras = {
            'start': i * 20,
            'count': 20
        }
        rp = random.choice(pro)
        resp = requests.get(url=index_url, params=paras, headers=header, proxies={'http': rp})
        data = resp.json()

        items = data['items']

        for values in items:
            # print(values['abstract'])
            try:
                commit.append(values['target']['status']['text'])
            #print(commit)
            except:
                continue
            try:
                loc.append(values['target']['status']['author']['loc']['name'])
            except:
                continue

        # print(item)
        # print(commit)

    resp.close()
    df = pd.DataFrame({'评论': commit})
    df1= pd.DataFrame({'地址':loc})
    df.to_excel('反诈骗评论.xlsx')
    df1.to_excel('地区.xlsx')
    print(df)

def ciyun():
    # 读取文件
    pd_data = pd.read_excel('反诈骗评论.xlsx')
    with open('fixes-zh.txt', 'r', encoding='UTF-8') as meaninglessFile:
        stop_words = set(meaninglessFile.read().split('\n'))
    stop_words.add('n')
    stop_words.add('r')
    # 读取内容
    text = pd_data['评论'].tolist()

    # 切割分词
    result=''
    jieba.load_userdict("safe.txt")
    wordlist = jieba.cut_for_search(''.join(str(text)))
    for word in wordlist:
        if len(word)>1:
            result += word
            result += ' '
    #result = ' '.join(wordlist)
    #print(result)
    # 设置停用词
    #stop_words = set(['你', '我', '的', '了', '们', '...', '就', '和', '也', '是', '都', '吃', '在', '还', '但', '有', '没有','感觉','没','n','r'])
    ciyun_words = ''
    # 过滤后的词
    for word in result:
        if word not in stop_words:
            ciyun_words += word

    print(ciyun_words)

    mask = np.array(Image.open("1.png"))
    # print(ciyun_words)
    tag = jieba.analyse.extract_tags(sentence=ciyun_words, topK=10, withWeight=True,allowPOS=('ns','n'))
    # im = cv2.imread('1.jpg')
    # 设置参数，创建WordCloud对象
    wc = WordCloud(
        font_path='msyh.ttc',  # 中文
        background_color='white',  # 设置背景颜色为白色
        stopwords=stop_words,  # 设置禁用词，在生成的词云中不会出现set集合中的词
        # max_font_size=100,           # 设置最大的字体大小，所有词都不会超过100px
        # min_font_size=10,            # 设置最小的字体大小，所有词都不会超过10px
        max_words=100,                # 设置最大的单词个数
        scale=2,
        mask=mask,
        collocations = False
    )
    # 根据文本数据生成词云
    wc.generate(ciyun_words)
    # 保存词云文件
    wc.to_file('词云图1.jpg')
    # print(ciyun_words)
    word_counts = collections.Counter(ciyun_words)  # 词频统计
    word_counts_top8 = word_counts.most_common(50)  # 词云取前50的词
    print(word_counts_top8)  # 打印出来top50的词云 及对应数量
    print(tag)

if __name__ =='__main__':
    while 1:
        i = int(input("请选择 爬取数据（1） 生成词云（2） 退出（3）："))
        if i == 1:
            pa()
        elif i == 2:
            ciyun()
        else:
            break



#resp.close()
# 储存所爬取的数据

