# -*- coding: utf-8 -*-
# @Author: GreatV
# @Date: 2017-04-16

import api_simple as api
import codecs

artistslist = {
    '李志': 3681,
    '周云蓬': 6461,
    '赵雷': 6731,
    '马頔': 4592,
    '房东的猫': 1050282,
    '陈粒': 1007170,
    '贰佰': 896894,
    '丢火车': 11370,
    '布衣乐队': 2092,
    '张玮玮和郭龙': 173002,
    '张悬': 10557,
    '万晓利': 5345,
    '张过年': 6488,
    '宋冬野': 5073,
    'Jam': 1071031,
    '低苦艾': 11365,
    '不可撤销': 900084,
    '陈鸿宇': 1058228,
    '尧十三': 4903,
    '鹿先森乐队': 1195028,
    '大乔小乔': 11358,
    '晓月老板': 1138004,
    '程璧': 973004,
    '胡德夫': 3056,
    '谢春花': 1039895,
    '赵照': 6729,
    '花粥': 8103,
    '阿肆': 7122,
    '好妹妹乐队': 711683
}

# 参考 https://zhuanlan.zhihu.com/p/25710477
# 去除歌词中多余的信息


def prettify_lyric(lyric):
    lyric_text_list = []

    for idx, line in enumerate(lyric.split('\n')):
        if u'作曲' in line or u'作词' in line:  # 去除歌词中可能出现的作词、作曲行
            continue
        if line.strip() != '':
            if u']' in line:  # []内可能是时间信息，去除
                if line.rindex(u']') + 1 != len(line):
                    line = line[line.rindex(u']') + 1:].strip()
                else:
                    continue
            if u':' in line:  # 冒号前面可能是歌者，应去除。e.g.: "女:"、"老狼:"
                line = line[line.rindex(u':') + 1:]
            if u'：' in line:  # 冒号前面可能是歌者，应去除。e.g.: "女："、"老狼："
                line = line[line.rindex(u'：') + 1:]
            lyric_text_list.append(line.strip())

    lyric_text = '\n'.join(lyric_text_list)
    return lyric_text

# 获取歌手热门歌曲的歌词


def artist_lyric_text(artist_id):
    artists_songs = api.get_artist_music(artist_id)

    song_list = []

    for song in artists_songs:
            # print '-'*32

        song_id = song['id']
        lyric = api.get_music_lyric(song_id)
        if lyric:
            song_list.append('{}'.format(song_id))
            text = prettify_lyric(lyric)

            with codecs.open('{}.txt'.format(song_id), 'w', 'utf-8') as f:
                f.write(text)
        print 'Write ' + song['name'] + ' lyric......DONE!'

    songs = '\n'.join(song_list)
    with open('{}.txt'.format(artist_id), 'w') as f:
        f.write(songs)

# 根据歌手列表获取歌词


def get_lyric_text_from_artistslist(artistslist):
    for artist_id in artistslist.values():
        artist_lyric_text(artist_id)

#  获取指定歌曲的评论


def get_music_comments_text(song_id, hc=True):

    if hc:
        hot_comments_text = []
        hot_comments_list = api.get_music_comments(song_id)['hotComments']
        for hot_comment in hot_comments_list:
            hot_comments_text.append(hot_comment['content'])
        text = '\n'.join(hot_comments_text)
    else:
        comments_text = []
        comments_list = api.get_music_comments(song_id)['comments']
        for comment in comments_list:
            comments_text.append(comment['content'])
        text = '\n'.join(comments_text)

    with codecs.open('{}_comments.txt'.format(song_id), 'w', 'utf-8') as f:
        f.write(text)


# artist_lyric_text(4903)
# song_id = 418603077
# get_music_comments_text(song_id, 0)

# get_lyric_text_from_artistslist(artistslist)
