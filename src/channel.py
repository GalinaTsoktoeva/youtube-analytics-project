import json
import os


# необходимо установить через: pip install google-api-python-client
from googleapiclient.discovery import build


def printj(dict_to_print: dict) -> None:
    """Выводит словарь в json-подобном удобном формате с отступами"""
    print(json.dumps(dict_to_print, indent=2, ensure_ascii=False))

class Channel:
    """Класс для ютуб-канала"""
    # YT_API_KEY скопирован из гугла и вставлен в переменные окружения
    #api_key: str = os.getenv('YT_API_KEY')
    api_key: str = 'AIzaSyDK25Zi9td3dOqUbsUM8kfEOkJPfDutEtk'
    #youtube = build('youtube', 'v3', developerKey=api_key)
    def __init__(self, channel_id: str) -> None:
        """название канала
            описание канала
            ссылка на канал
            количество подписчиков
            количество видео
            общее количество просмотров"""
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id

        channel = self.get_service().channels().list(id=channel_id, part='snippet,statistics').execute()
        print(channel)
        if channel:
            self.title = channel['items'][0]['snippet']['title']
            self.desc = channel['items'][0]['snippet']['description']
            self.url = channel['items'][0]['snippet']['thumbnails']['default']['url']
            self.subscribes_count = channel['items'][0]['statistics']['subscriberCount']
            self.video_count = channel['items'][0]['statistics']['videoCount']
            self.count_of_views = channel['items'][0]['statistics']['viewCount']


    @property
    def channel_id(self):
        return self.__channel_id


    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        channel_id = self.channel_id
        channel = self.get_service(self.api_key).channels().list(id=channel_id, part='snippet,statistics').execute()
        printj(channel)

    @classmethod
    def get_service(cls):
        # создать специальный объект для работы с API
        youtube = build('youtube', 'v3', developerKey=Channel.api_key)
        return youtube

    @staticmethod
    def to_json(filename):
        parameters = Channel('UCMCgOm8GZkHp8zJ6l7_hIuA')

        data = {
            "title": parameters.title,
            "description": parameters.desc,
            "url": parameters.url,
            "count_of_views": parameters.count_of_views,
            "subscribes_count": parameters.subscribes_count,
            "video_count": parameters.video_count,
                }

        with open(filename, 'w') as outfile:
            json.dump(data, outfile, indent=4, ensure_ascii=False)


