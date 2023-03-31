# Crawler-and-Word-cloud
##爬取豆瓣社区关于反诈骗的评论并制作词云
爬取网站链接：https://m.douban.com/rexxar/api/v2/gallery/topic/325990/items?

使用requests发送请求

jieba库用来分词，分词器导入了中文常用语，用来对评论进行划分

爬取的文件存储在excel中，采用pandas保存读取文件

导入WorldCloud库用来制作词云
