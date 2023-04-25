from src.channel import Channel

class Video:
    """
    Класс для представления Video из Youtube.
    """
    def __init__(self, id_video):
        """
        :param id_video: id видео
        :param title: название видео
        :param url: ссылка на видео
        :param count_views: количество просмотров
        :param count_likes: количество лайков
        """
        self.id_video = id_video

        video_response = Channel.get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails', id=id_video).execute()

        if video_response:
            self.title = video_response['items'][0]['snippet']['title']
            self.url = f"https://youtu.be/{self.id_video}"
            self.count_views = video_response['items'][0]['statistics']['viewCount']
            self.count_likes = video_response['items'][0]['statistics']['likeCount']

    def __str__(self):
        return self.title


class PLVideo(Video):
    """
    Класс для представления плейлиста из Youtube.
    """
    def __init__(self, id_video, id_playlist):
        super().__init__(id_video)
        self.id_playlist = id_playlist

    def __str__(self):
        return self.title