# -*- coding: utf-8 -*-
# encoding=utf-8
# @Author: GreatV
# @Date: 2017-04-16

import jieba
import pandas as pd
from pandas import Series, DataFrame
import numpy as np
from PIL import Image
from collections import Counter
import matplotlib.pyplot as plt
from wordcloud import WordCloud

# configure font
plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来在 matplotlib 中正常显示中文

# 获取分词结果


def get_word_list(path):
    raw_word_list = []

    with open(path, 'r') as f:
        for line in f:
            #line = line.replace(' ','')
            line = line.strip()
            # return formation ['a', 'b', 'a']
            seg_list = jieba.cut(line, cut_all=False)
            raw_word_list += seg_list  # return formation ['xx', 'a', 'b', 'a']
        print 'Write word list done!'
    return raw_word_list

# 词频统计


def words_frequency(word_list, top):  # top: 所需高频词位数
    # world_dic = Counter(word_list) # return formation Counter({'aa': 2, 'c':
    # 5, 'd':89})
    sorted_list = sorted(
        Counter(word_list).iteritems(),
        key=lambda t: t[1],
        reverse=True)  # return formation [('xx',100),('aa',97)]
    # print sorted_list
    # for word, freq in sorted_list[:top]:
    # 	print word+' : '+str(freq)

    return sorted_list[:top]

# 分词过滤


def word_list_filter(raw_word_list, top=25):
    stopwords = [u' ', u'说', u'里', u'嘞', u'做', u'噢', u'话']  # 预定义停用词
    word_list = []

    # 停用词表来自：
    # https://github.com/XuJin1992/ChineseTextClassifier/blob/master/src/main/resources/text/stop_word.txt
    with open('stop_words.txt', 'r') as f:
        for word in f:
            word = word.strip().decode('utf-8')
            stopwords.append(word)

    # 过滤停用词
    for word in raw_word_list:
        if word not in stopwords:
            word_list.append(word)

    return words_frequency(word_list, top=top)


# 可视化
# 可传入 kind 的参数
# ‘bar’ or ‘barh’ 柱状图
# ‘pie’ 饼状图
# 其它参见 http://pandas.pydata.org/pandas-docs/stable/visualization.html
def visualization(word_list, kind='bar'):
    # data = {'word': word_list.keys(), 'frequency': word_list.values()}
    frame = DataFrame(word_list, columns=['word', 'frequency'])
    frame.set_index('word', inplace=True)

    if kind == 'pie':
        frame.plot(subplots=True, kind=kind, legend=False)
    else:
        frame.plot(kind=kind)
    plt.show()


# 创建词云
def generate_wordcloud(word_list, mask_name):
    text = ' '.join(word_list)
    mask = np.array(Image.open(mask_name))

    wc = WordCloud(
        font_path='SourceHanSerifCN-Regular.otf',
        background_color='white',
        max_words=100,
        mask=mask)
    # generate word cloud
    wc.generate(text)

    # store to file
    # wc.to_file('haha.png')

    # show
    plt.imshow(wc, interpolation='bilinear')
    plt.axis("off")
    plt.figure()
    plt.imshow(mask, cmap=plt.cm.gray, interpolation='bilinear')
    plt.axis("off")
    plt.show()

# 情感分析


def sentiment_analysis():
    pass


if __name__ == '__main__':
    path = '4903.txt'  # 读取文件路径
    word_list = get_word_list(path)
    wlf = word_list_filter(word_list, top=50)
    visualization(wlf, 'pie')
    # words_frequency(word_list, 100)

    # mask_name = '4903.png'
    # generate_wordcloud(word_list, mask_name)
