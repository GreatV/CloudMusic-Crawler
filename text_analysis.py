# -*- coding: utf-8 -*-
# @Author: GreatV
# @data: 2017-05-17

import jieba
from collections import Counter
import pandas as pd
from matplotlib import pyplot as plt
from PIL import Image
import numpy as np
from wordcloud import WordCloud

#用来在 matplotlib 中正常显示中文
# 参考 http://blog.csdn.net/and_w/article/details/70288479
plt.rcParams['font.sans-serif']=['SimHei']


# 分词
def words_split(corpus_path):

	with open(corpus_path, 'r') as f:
		content = f.read()

	jieba.load_userdict('data/userdict.txt') # 设置用户自定义词典
	jieba.enable_parallel(4) # 启用并行


	seg_list = jieba.cut(content, cut_all = False) # 分词

	return seg_list


# 过滤停用词
def stop_words_filter(raw_words_list):
	# 停用词表来自：
	# https://github.com/XuJin1992/ChineseTextClassifier
	stop_words_path = 'data/stop_words.txt' # 在此设置停用词路径
	stop_words_list = [u' ', u'\n'] # 在此预定义停用词
	filtered_words_list = [] # 过滤后的结果

	with open(stop_words_path, 'r') as f: # 从文件中读取停用词
		for word in f:
			word = word.strip().decode('utf-8')
			stop_words_list.append(word)

	for word in raw_words_list: # 过滤停用词
		if word not in stop_words_list:
			filtered_words_list.append(word)

	return filtered_words_list


# 词频统计
def words_frequency(words_list, top = 25):
	sorted_words_list = sorted(Counter(words_list).iteritems(), key = lambda t:t[1], reverse = True)

	return sorted_words_list[:top] # [('xx',100),('aa',97)]


# 画图
# 参见 http://pandas.pydata.org/pandas-docs/stable/visualization.html
def plot_figure(words_list, kind = 'bar'):
	# print words_list
	frame = pd.DataFrame(words_list, columns = ['item', 'frequency'])
	frame.set_index('item',inplace = True)

	if kind == 'pie':
		frame.plot(subplots = True, kind = kind, legend = False)
	else:
		frame.plot(kind = kind)
	
	plt.show()


# 生成词云
def generate_wordcloud(words_list, mask_path):
	text = ' '.join(words_list)
	# print text
	mask = np.array(Image.open(mask_path))
	# stopwords = set(STOPWORDS)
	# stopwords.add(u'')

	wc = WordCloud(font_path = 'data/SourceHanSerifCN-Regular.otf', background_color = 'white', 
		max_words = 2000, mask = mask) # 请使用支持中文的字体

	wc.generate(text)

	# wc.to_file('data/path/to/file')

	plt.imshow(wc, interpolation='bilinear')
	plt.axis("off")
	plt.show()


if __name__ == '__main__':
	text_path = 'data/alltext.txt'
	text_path_test = 'data/3681_alltext.txt'

	raw_words_list = words_split(text_path_test)
	# print('/'.join(words_split(text_path_test)))

	filtered_words_list = stop_words_filter(raw_words_list)
	# print('/'.join(stop_words_filter(raw_words_list)))

	# TF = words_frequency(filtered_words_list)
	# print(words_frequency())

	# plot_figure(TF, 'pie')

	mask_path = 'data/yaoshisan0.png'
	generate_wordcloud(filtered_words_list, mask_path)
