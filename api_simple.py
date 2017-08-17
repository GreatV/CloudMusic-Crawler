# -*- coding: utf-8 -*-
# @Author: GreatV
# @Date: 2017-04-16
# 参考 https://github.com/darknessomi/musicbox

import requests

headers = {
	'Accept': '*/*',
    'Accept-Encoding': 'gzip,deflate,sdch',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Host': 'music.163.com',
    'Referer': 'http://music.163.com/search/',
    'User-Agent':
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36'
}

cookies = {'appver': '1.5.2'}


def get_playlist_detail(playlist_id):
	url = 'http://music.163.com/api/playlist/detail?id={}'.format(playlist_id)

	try:
		r = requests.get(url, headers = headers, cookies = cookies)
		return r.json()['result']['tracks']
	except requests.exceptions.RequestException as e:
		print(e)
		return []


def get_artist_music(artist_id):
	url = 'http://music.163.com/api/artist/{}'.format(artist_id)

	try:
		r = requests.get(url, headers = headers, cookies = cookies)
		return r.json()['hotSongs']
	except requests.exceptions.RequestException as e:
		print(e)
		return []


def get_music_lyric(song_id):
	url = 'http://music.163.com/api/song/lyric?os=pc&id={}&lv=-1&kv=-1&tv=-1'.format(song_id)

	try:
		r = requests.get(url, headers = headers, cookies = cookies)
		if 'lrc' in r.json() and 'lyric' in r.json()['lrc'] and r.json()['lrc']['lyric'] is not None:
			return r.json()['lrc']['lyric']
		else:
			return []
	except requests.exceptions.RequestException as e:
		print(e)
		return []


def get_music_comments(song_id, offset=0, total='fasle', limit=100):
	url = 'http://music.163.com/api/v1/resource/comments/R_SO_4_{}/'.format(song_id)
	payload = {
		'rid': 'R_SO_4_{}'.format(song_id),
		'offset': offset,
		'total': total,
		'limit': limit
	}

	try:
		r = requests.get(url, headers = headers, cookies = cookies, params = payload)
		return r.json()
	except requests.exceptions.RequestException as e:
		print(e)
		return []


if __name__ == '__main__':
	pass