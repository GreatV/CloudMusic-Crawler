import json
import jieba
import re
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

    # 过滤空格
    filter_space = lambda w: w != ' '
    word_list = list(filter(filter_space, word_list))

    return word_list


def main():
    with open('data/lyric_list.json') as f:
        data = json.load(f)

    # 停用词表来自：
    # https://github.com/XuJin1992/ChineseTextClassifier
    with open('data/stop_words.txt') as f:
        stop_words = f.read().split('\n')

    lyric = data[0]
    lyric = format_content(lyric)

    seg_list = word_segmentation(lyric, stop_words)
    
    pprint(seg_list)
    # pprint(type(stop_words))


if __name__ == '__main__':
    main()