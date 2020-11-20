import requests
from bs4 import BeautifulSoup
from os import getenv, system
from bot_logger import info as log_info, error as log_error


class BlogDownloader():
    def __init__(self) -> None:
        self.url = getenv('BLOG_URL')
        self.next = None
        self.audio = getenv('AUDIO_PATH')
        # these html elements are hardcoded since the blog is specific to me. in the future, would be cool to abstract this to allow for more blogs
        self.post = 'post'
        self.post_link = 'post-link'
        self.post_content = 'post-content'
        self.pagination_next = 'pagination-next'
        self.post_title = 'post-title'

    def download_content(self, q: list) -> None:
        for url in q:
            page = requests.get(url)
            if page.status_code != 200:
                log_error("request failed for url: {} with response: {}".format(self.url, page.text))
            else:
                soup = BeautifulSoup(page.text, 'lxml')
                title = soup.find('h1', class_=self.post_title).get_text()
                title = "".join(x for x in title if x.isalnum()).strip()
                content = soup.find('div', class_=self.post_content)
                content = content.get_text()
                system('espeak \"{}\" -s 145  --stdout > {}'.format(content, '{}/{}.mp3'.format(self.audio, title)))
                log_info('saved {}/{}'.format(self.audio, title))

    def download_blog(self) -> None:
        blog_post_q = []  # for the actual posts
        
        self.next = self.url

        while self.next is not None:
            req = requests.get(self.next)
            if req.status_code != 200:
                log_error("request failed for url: {} with response: {}".format(self.url, req.text))
                self.url = None
            else:
                soup = BeautifulSoup(req.text, 'lxml')
                next_href = soup.find('a', class_=self.pagination_next)
                self.next = self.url + next_href.get('href') if next_href is not None else None
                posts_on_page = soup.find_all('a', class_=self.post_link)
                posts_on_page = [p.get('href') for p in posts_on_page]
                for p in posts_on_page:
                    blog_post_q.append(p)

        self.download_content(blog_post_q)

