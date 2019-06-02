**新版即将到来。。。**

![](https://i.loli.net/2018/01/23/5a672e59bbfab.png)

![](https://i.loli.net/2018/01/23/5a672e63457b7.png)

## Introduction

看见有人写了一篇[我用Python分析了42万字的歌词，为了搞清楚民谣歌手们在唱些什么](https://ask.hellobi.com/blog/spuerwdk/6336)，觉得挺好玩的，于是就想自己也实现一下。于是本作品就诞生了。

## 爬虫

爬虫部分主要是调用已有的 API。这部分的工作可以参考[NetEase-MusicBox](https://github.com/darknessomi/musicbox)，该作品作者实现了网易云音乐的命令行版，我用了一下还不错。主要参考了该作者的[api.py](https://github.com/darknessomi/musicbox/blob/master/NEMbox/api.py)部分。

![Screenshot3.png](https://i.loli.net/2017/12/28/5a44fdcfc0ba9.png)

## 文件处理

该部分主要的工作是将所有歌词写入一个文件，同时每个作者的所有歌词也放入一个文件，以备后面的分析之用。

![Screenshot4.png](https://i.loli.net/2017/12/28/5a44fdcfdffae.png)

本次获取的歌词大概 26000 行。

## 文本分析

分词用的是[“结巴”中文分词](https://github.com/fxsjy/jieba)。

我首先选取了一位歌手作为代表分析了一下词频，如下所示：

![shisanfigure_2.png](https://i.loli.net/2017/12/28/5a44fdcf52893.png)

![figure_bar01.png](https://i.loli.net/2017/12/28/5a44fdcf44e0e.png)

![figure_pie01.png](https://i.loli.net/2017/12/28/5a44fdcf85627.png)

做了一个词云：

![shisanfigure_1.png](https://i.loli.net/2017/12/28/5a44fdcf7d383.png)

然后。把所有的歌词都分析了一下，得到了如下饼状图：

![fm3.png](https://i.loli.net/2017/12/28/5a44fdcf7efac.png)

还做了一个词云，如下所示：

![fm0.png](https://i.loli.net/2017/12/28/5a44fdcf7cca2.png)

## 接下来的工作

- 情绪分析
- 云音乐的评论很精彩，可以做一下评论，看看有什么发现

## 如何使用

```
git clone https://github.com/GreatV/CloudMusic-Crawler.git

cd CloudMusic-Crawler

python3 -m venv venv

source venv/bin/activate

pip install -r requirements.txt

cd NEMCrawler

python NEM_spider.py

python text_mining.py

firefox render.html
```
