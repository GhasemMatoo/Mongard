import requests
import re
from bs4 import BeautifulSoup


class VideoDownloadException(Exception):
    pass


class QualityError(VideoDownloadException):
    pass


class Scraper:
    def __init__(self, url, quality):
        self.url = url
        self.quality = str(quality)
        self.qualities = {
            '144': 0,
            '240': 1,
            '360': 2,
            '480': 3,
            '720': 4,
            '1080': 5
        }

    def get_all_links(self):
        result = requests.get(self.url)
        content = BeautifulSoup(result.text, 'html.parser')
        video_links = content.find_all('a', href=re.compile('.mp4'))
        links = [link['href'] for link in video_links]
        links.reverse()
        return links

    def get_quality(self):
        link = self.get_all_links()
        quality_list = list(self.qualities.keys())
        available_quality = []
        for i in range(len(link)):
            available_quality.append(quality_list[i])
        return available_quality

    def get_link(self):
        links = self.get_all_links()
        available_quality = self.get_quality()
        if self.quality not in available_quality:
            raise QualityError(f'This quality is not available: {self.quality}')
        link = links[self.qualities[self.quality]]
        return link


class Main:
    def __init__(self, url, quality):
        self.url = url
        self.quality = str(quality)
        self.scraper = Scraper(self.url, self.quality)

    def download(self):
        video_link = self.scraper.get_link()
        with open('Video.mp4', 'wb') as file:
            print('Downloading...', end='')
            result = requests.get(video_link, stream=True)
            total = result.headers.get('content-length')
            if total is None:
                file.write(result.content)
            else:
                downloaded = 0
                total = int(total)
                for data in result.iter_content(chunk_size=4096):
                    file.write(data)
                    downloaded += len(data)
                    done = int(50 * downloaded / total)
                    print('\r[{}{}]'.format("=" * done, " " * (50 - done)), end='')
        print('\n Video downloaded')


s = Main('https://www.namasha.com/v/bAEyByUr', 144)
print(s.download())
