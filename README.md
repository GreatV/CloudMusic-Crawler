# 网易云音乐爬虫
---

## Introduction

看见有人写了一篇[我用Python分析了42万字的歌词，为了搞清楚民谣歌手们在唱些什么](https://ask.hellobi.com/blog/spuerwdk/6336)，觉得挺好玩的，于是就想自己也实现一下。于是本作品就诞生了。

## 爬虫

爬虫部分主要是调用已有的 API。这部分的工作可以参考[NetEase-MusicBox](https://github.com/darknessomi/musicbox)，该作品作者实现了网易云音乐的命令行版，我用了一下还不错。主要参考了该作者的[api.py](https://github.com/darknessomi/musicbox/blob/master/NEMbox/api.py)部分。

![Screenshot3.png](http://bucket0zero-1253582002.file.myqcloud.com/mdimg/Screenshot3.png)

## 文件处理

该部分主要的工作是将所有歌词写入一个文件，同时每个作者的所有歌词也放入一个文件，以备后面的分析只用。

![Screenshot4.png](http://bucket0zero-1253582002.file.myqcloud.com/mdimg/Screenshot4.png)

本次获取的歌词大概 26000 行。

## 文本分析

分词用的是[“结巴”中文分词](https://github.com/fxsjy/jieba)。

我首先选取了一位歌手作为代表分析了一下词频，如下所示：

![shisanfigure_2.png](http://bucket0zero-1253582002.file.myqcloud.com/mdimg/shisanfigure_2.png)

![figure_bar01.png](http://bucket0zero-1253582002.file.myqcloud.com/mdimg/figure_bar01.png)

![figure_pie01.png](http://bucket0zero-1253582002.file.myqcloud.com/mdimg/figure_pie01.png)

做了一个词云：

![shisanfigure_1.png](http://bucket0zero-1253582002.file.myqcloud.com/mdimg/shisanfigure_1.png)

然后。把所有的歌词都分析了一下，得到了如下饼状图：

![fm3.png](http://bucket0zero-1253582002.file.myqcloud.com/mdimg/fm3.png)

还做了一个词云，如下所示：

![fm0.png](http://bucket0zero-1253582002.file.myqcloud.com/mdimg/fm0.png)

## 接下来的工作

- 情绪分析
- 云音乐的评论很精彩，可以做一下评论，看看有什么发现
- 饼状图太丑，想换一个



