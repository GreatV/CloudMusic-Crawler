# -*- coding: utf-8 -*-
# @Author: GreatV
# @Date: 2017-04-16

import api_simple as api
import json
# import re


def get_artists_from_file(file_path):
	artists_list = {}
	
	with open(file_path, 'r') as f:
		for line in f.readlines():
			artist_name, artist_id = line.split()
			artists_list[artist_name] = int(artist_id)

	return artists_list


def get_artists_from_playlist(playlist_id):
	artists_list = {}
	artist_details = []

	tracks = api.get_playlist_detail(playlist_id)
	for track in tracks:
		for artist in track['artists']:
			artist_details.append((artist['name'], artist['id']))

	artist_details = set(artist_details)
	# print(artist_details)
	for detail in artist_details:
		artist_name, artist_id = detail
		artists_list[artist_name] = int(artist_id)

	return artists_list


def purify_lyric_text(lyric_text, allow_duplicate = True):
	purify_text = []

	lyric_text_list = lyric_text.split('\n')
	for line in lyric_text_list:
		
		if ('作曲' in line) or ('作词' in line):
			continue
		
		if ']' in line:
			line = line.split(']')[1]

		if line.strip() == '':
			continue

		line = line.strip()
		if ':' in line:
			line = line.split(':')[1]

		if '：' in line:
			line = line.split('：')[1]

		purify_text.append(line)

	if not allow_duplicate:
		purify_text = list(set(purify_text))

	return purify_text


def get_lyrics_from_artist_id(artist_id):
	lyrics_list = []
	
	songs = api.get_artist_music(artist_id)
	
	for song in songs:		
		song_details = {}
		print('====> Getting lyric of {}'.format(song['name']))
		
		song_lyric = api.get_music_lyric(song['id'])
		
		if song_lyric:
			song_details['name'] = song['name']
			song_details['id'] = song['id']
			song_lyric = purify_lyric_text(song_lyric)
			song_details['lyric'] = song_lyric
		
			lyrics_list.append(song_details)
		else:
			print('+++ Oops... no lyric +++')

	return lyrics_list


def get_lyrics_from_artists_list(artists_list):
	lyrics = {}
	artists = []
	artist = {}
	
	with open('./data/lyrics.json', 'w') as f:
		
		for artist_name, artist_id in artists_list.items():
			
			print("'----Handling {}'s hot-song list-----".format(artist_name))
			artist['name'] = artist_name
			artist['id'] = artist_id
			artist['songs'] = get_lyrics_from_artist_id(artist_id)

			artists.append(artist)

		lyrics['lyrics'] = artists
		json.dump(lyrics, f)
		
	print('-----Write Done-----')



def comments_handler(song_id): # in test
	comments_list = []
	comment_list = {}

	more_comments = True
	offset = 0
	counter = 1

	while more_comments:
		results = api.get_music_comments(song_id, offset = offset)
		for comment in results['comments']:
			print('----Geting No. {} comment'.format(counter))
			counter += 1
			comment_list['content'] = comment['content']
			comment_list['username'] = comment['user']['nickname']
			comment_list['likedCount'] = comment['likedCount']

			comments_list.append(comment_list)

		more_comments = results['more']
		offset += 1

	print('-----Got {} comments'.format(results['total']))
	return comments_list


def get_comments_from_aritist_id(artist_id):
	# song_details = {}
	# songs = api.get_artist_music(artist_id)

	# for song in songs:
	# 	song_details['name'] = song['name']
	# 	song_details['id'] = song['id']
	pass


if __name__ == '__main__':
	pass
