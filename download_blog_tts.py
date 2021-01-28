import requests
from queue import Queue
from bs4 import BeautifulSoup
from os import getenv
from threading import Thread
from gtts import gTTS
from bot_logger import info as log_info, error as log_error

# a sequential class that downloads the text from a bunch of posts in a blog, and converts it to text to speech files.
# could be cool to make it concurrent to download multiple at once
class BlogDownloader():
    def __init__(self) -> None:
        self.url = getenv('BLOG_URL')
        self.next = None
        self.audio = getenv('AUDIO_PATH')
        self.thread_count = 4  # arbitrarily chosen
        # these html elements are hardcoded since the blog is specific to me. in the future, would be cool to abstract this to allow for more blogs
        self.post = 'post'
        self.post_link = 'post-link'
        self.post_content = 'post-content'
        self.pagination_next = 'pagination-next'
        self.post_title = 'post-title'

    def download_content(self, q: Queue, count: int) -> None:
        for _ in range(count):
            url = q.get()
            page = requests.get(url)
            if page.status_code != 200:
                log_error("request failed for url: {} with response: {}".format(self.url, page.text))
                q.task_done()
            else:
                soup = BeautifulSoup(page.text, 'lxml')
                title = soup.find('h1', class_=self.post_title).get_text()
                title = "".join(x for x in title if x.isalnum()).strip()
                content = soup.find('div', class_=self.post_content)
                content = content.get_text()
                # todo: gTTS is really slow on saving, see if there is a better alternative
                tts = gTTS('{}'.format(content))
                tts.save('{}/{}.mp3'.format(self.audio, title))
                log_info('saved {}/{}'.format(self.audio, title))
                q.task_done()
        print('here')

    def download_blog(self) -> None:
        blog_post_q = Queue()  # for the actual posts
        
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
                    blog_post_q.put(p)

        posts_per_thread = blog_post_q.qsize() // self.thread_count  # this is ok as the blog has an even amount of posts. however, not good for the long run

        # todo: look if this can be improved
        for _ in range(self.thread_count):
            Thread(target=self.download_content, daemon=True, args=(blog_post_q, posts_per_thread)).start()

        blog_post_q.join()

