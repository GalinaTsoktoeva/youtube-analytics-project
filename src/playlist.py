from datetime import timedelta
from src.channel import Channel
from src.video import Video

import isodate

class PlayList():
    """
    Класс для представления PlayLista из Youtube.
    """
    def __init__(self, id_playlist):
        """
        :param id_playlist: id playlist
        :param url: ссылка видео
        """
        self.id_playlist = id_playlist
        self.url = f"https://www.youtube.com/playlist?list={self.id_playlist}"
        playlist_videos = Channel.get_service().playlistItems().list(playlistId=id_playlist,
                                                        part='contentDetails,snippet',
                                                        maxResults=50,
                                                        ).execute()
        if playlist_videos:
            self.title = playlist_videos['items'][0]['snippet']['title']
            self.id_video = [video['contentDetails']['videoId'] for video in playlist_videos['items']]


    @property
    def total_duration(self):
        """
        :return:возвращает объект класса datetime.timedelta
        с суммарной длительность плейлиста
        """
        video_response = Channel.get_service().videos().list(part='contentDetails,statistics',
                                               id=','.join(self.id_video)
                                               ).execute()
        res = timedelta()

        for video in video_response['items']:
            # YouTube video duration is in ISO 8601 format
            print(video)
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            res += duration
        return res

    def show_best_video(self):
        """
        :return: возвращает ссылку на самое популярное видео из плейлиста
        """
        max_count = 0

        for id_video in self.id_video:
            new_video = Video(id_video)

            if max_count < int(new_video.count_likes):
                max_count = max(int(new_video.count_likes), max_count)
                url = new_video.url
        return url


