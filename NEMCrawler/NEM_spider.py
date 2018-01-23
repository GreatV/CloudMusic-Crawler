#/usr/bin/env python3
# @Author: GreatV
# @Date: 2017-04-16
# @Update: 2018-01-21

'''
本项目需要用到的网易云音乐 api
参考 https://github.com/darknessomi/musicbox/blob/master/NEMbox/api.py
'''

import requests
import json
from pprint import pprint


class NEM_spider(object):


    def __init__(self):
        self.headers = {
        'host': 'music.163.com',
        'Referer': 'http://music.163.com/search/',
        'User-Agent': 
        ('Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        ' (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36')
        }
        self.cookies = {'appver': '1.5.2'}


    # Getting playlist (歌单)
    def get_playlist_detail(self, playlist_id):
        url = 'http://music.163.com/api/playlist/detail'
        payload = {'id': playlist_id}

        r = requests.get(url, params = payload, headers = self.headers, 
            cookies=self.cookies)

        playlist_detail = r.json()['result']['tracks']

        return playlist_detail


    def from_playlist_get_song_list(self, playlist_id):
        playlist_detail = self.get_playlist_detail(playlist_id)
        songlist = []
        for song_detail in playlist_detail:
            song = {}
            song['id'] = song_detail['id']
            song['name'] = song_detail['name']
            artists_detail = []
            for artist in song_detail['artists']:
                artist_detail = {}
                artist_detail['name'] = artist['name']
                artist_detail['id'] = artist['id']
                artists_detail.append(artist_detail)
            song['artists'] = artists_detail
            songlist.append(song)

        return songlist


    def get_artists_songlist(self, artist_id):
        url = 'http://music.163.com/api/artist/{}'.format(artist_id)

        r = requests.get(url, headers=self.headers, cookies=self.cookies)
        hotSongs = r.json()['hotSongs']

        songlist = []
        for hotSong in hotSongs:
            song = {}
            song['id'] = hotSong['id']
            song['name'] = hotSong['name']
            songlist.append(song)

        return songlist


    def get_song_lyric(self, song_id):
        url = 'http://music.163.com/api/song/lyric'
        payload = {
        'os': 'pc', # osx
        'id': song_id,
        'lv': -1,
        'kv': -1,
        'tv': -1
        }

        r = requests.get(url, params=payload, headers=self.headers, 
            cookies=self.cookies)

        result = r.json()
        # print(result)
        if ('nolyric' in result) or ('uncollected' in result):
            return None
        elif 'lyric' not in result['lrc']:
            return None
        else:
            return result['lrc']['lyric']


    def get_song_comments(self, song_id, offset=0, total='false', limit=100):
        url = ('http://music.163.com/api/v1/resource/comments/R_SO_4_{}/'
            ''.format(song_id))
        payload = {
        'rid': 'R_SO_4_{}'.format(song_id),
        'offset': offset,
        'total': total,
        'limit': limit
        }

        r = requests.get(url, params=payload, headers=self.headers, 
            cookies=self.cookies)


        return r.json()


    def get_total_comments(self, song_id):
        comments = self.get_song_comments(song_id)['comments']
        comments_list = []
        offset = 0
        while comments:
            for comment in comments:
                comment_detail = {}
                comment_detail['user_name'] = comment['user']['nickname']
                comment_detail['user_id'] = comment['user']['userId']
                comment_detail['content'] = comment['content']
                comment_detail['time'] = comment['time']
                comments_list.append(comment_detail)

            offset = offset + 100
            comments = self.get_song_comments(song_id, 
                offset=offset)['comments']

        return comments_list


    def from_playlist_get_artist_id(self, *playlists):
        artist_id_list = []
        for playlist_id in playlists:
            song_list = self.from_playlist_get_song_list(playlist_id)
            for song in song_list:
                for artist in song['artists']:
                    print("Got {}'s id ==> {}".format(artist['name'], 
                        artist['id']))
                    # artist_id_dict = {}
                    # artist_id_dict['name'] = artist['name']
                    # artist_id_dict['id'] = artist['id']
                    # artist_id_list.append(artist_id_dict)
                    artist_id_list.append(artist['id'])

        artist_id_list=list(set(artist_id_list))
        return artist_id_list


    def from_playlist_get_full_lyric_text(self, *playlists):
        artist_id_list = self.from_playlist_get_artist_id(playlists)
        song_id_list = []
        lyric_list = []

        for artist_id in artist_id_list:

            print('Processing the work of the artist with id: {}'
                ''.format(artist_id))

            songlist = self.get_artists_songlist(artist_id)
            artist_song_id_list = [song['id'] for song in songlist]
            song_id_list.extend(artist_song_id_list)

        song_id_list = list(set(song_id_list))

        for song_id in song_id_list:

            print('Processing the lyric of the song with id: {}'
                ''.format(song_id))

            lyric = self.get_song_lyric(song_id)
            # print(lyric)
            if lyric is not None:
                # pprint(lyric)
                lyric_list.append(lyric)

        return lyric_list




if __name__ == '__main__':
    spider = NEM_spider()
    # playlist = spider.get_playlist_detail(605415618)
    # with open('test_playlist.json', 'w') as f:
    #     pprint(playlist, f)

    # songlist = spider.from_playlist_get_song_list(605415618)
    # with open('test_songlist.json', 'w') as f:
    #     pprint(songlist, f)

    # songlist = spider.get_artists_songlist(1007170)
    # with open('test_artist_songlist1.json', 'w') as f:
    #     pprint(songlist, f)

    # songlyric = spider.get_song_lyric(31838188)
    # with open('test_songlyric1.json', 'w') as f:
    #     pprint(songlyric, f)

    # songcomments = spider.get_song_comments(31838188)
    # with open('test_songcomments.json', 'w') as f:
    #     pprint(songcomments, f)

    # songcomments = spider.get_song_comments(31838188, offset=4400)
    # with open('test_songcomments_total1.json', 'w') as f:
    #     pprint(songcomments, f)

    # commentslist = spider.get_total_comments(31838188)
    # with open('test_commentslist.json', 'w') as f:
    #     pprint(commentslist, f)

    # artist_id_list = spider.from_playlist_get_artist_id(605415618, 2051837289)
    # with open('test_artist_id_list.json', 'w') as f:
    #     pprint(artist_id_list, f)

    lyriclist = spider.from_playlist_get_full_lyric_text(605415618,2051837289)
    with open('data/lyric_list.json', 'w') as f:
        json.dump(lyriclist, f)
    print('Done!')
