import json
import jieba
import re
from collections import Counter
from pyecharts.charts import Bar, Pie
import pyecharts.options as opts
from pprint import pprint


# 格式化文本，去除无关信息
def format_content(content):
    content = content.replace(u'\xa0', u' ')
    content = re.sub(r'\[.*?\]','',content)
    content = re.sub(r'\s*作曲.*\n','',content)
    content = re.sub(r'\s*作词.*\n','',content)
    content = re.sub(r'.*:','',content)
    content = re.sub(r'.*：','',content)
    content = content.replace('\n', ' ')
    return content


# 分词
def word_segmentation(content, stop_words):

    # 使用 jieba 分词对文本进行分词处理
    jieba.enable_parallel()
    seg_list = jieba.cut(content, cut_all=False)

    seg_list = list(seg_list)

    # 去除停用词
    word_list = []
    for word in seg_list:
        if word not in stop_words:
            word_list.append(word)

    # 过滤遗漏词、空格
    user_dict = [' ', '哒']
    filter_space = lambda w: w not in user_dict
    word_list = list(filter(filter_space, word_list))

    return word_list

# 词频统计
# 返回前 top_N 个值，如果不指定则返回所有值
def word_frequency(word_list, *top_N):
    if top_N:
        counter = Counter(word_list).most_common(top_N[0])
    else:
        counter = Counter(word_list).most_common()

    return counter


def plot_chart(counter, chart_type='Bar'):

    items = [item[0] for item in counter]
    values = [item[1] for item in counter]

    if chart_type == 'Bar':
        # chart = Bar('词频统计')
        # chart.add('词频', items, values, is_more_utils=True)
        chart = (
            Bar()
            .add_xaxis(items)
            .add_yaxis('词频', values)
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(title_opts=opts.TitleOpts(title='词频统计'))
            )
    else:
        # chart = Pie('词频统计')
        # chart.add('词频', items, values, is_label_show=True, is_more_utils=True)
        chart = (
            Pie()
            .add_xaxis(items)
            .add_yaxis('词频', values)
            .set_series_opts(label_opts=opts.LabelOpts(is_show=True))
            .set_global_opts(title_opts=opts.TitleOpts(title='词频统计'))
            )
    
    chart.render()



def main():
    with open('data/lyric_list.json') as f:
        data = json.load(f)

    # 停用词表来自：
    # https://github.com/XuJin1992/ChineseTextClassifier
    with open('data/stop_words.txt') as f:
        stop_words = f.read().split('\n')

    # 此处仅选择一首歌
    lyric = data[1]
    lyric = format_content(lyric)

    seg_list = word_segmentation(lyric, stop_words)

    counter = word_frequency(seg_list, 10)

    # plot_chart(counter, 'Pie')
    plot_chart(counter)
    
    # pprint(counter)
    # pprint(type(stop_words))


if __name__ == '__main__':
    main()