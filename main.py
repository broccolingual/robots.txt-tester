import re
import urllib.robotparser

class Robots:
    def __init__(self, url, user_agent):
        self.raw_url = url
        if user_agent == '':
            self.user_agent = '*'
        else:
            self.user_agent = user_agent
        self.root_url = self._get_root_url()
        self.robots_url = self._get_robots_txt_path()
        self.rp = self._get_robots_txt()

    def _get_root_url(self):
        pattern = r'(?P<root>https?://.*?)\/.*'
        result = re.match(pattern, self.raw_url)
        if result is not None:
            return result.group('root')

    def _get_robots_txt_path(self):
        return self.root_url + '/robots.txt'

    def _get_robots_txt(self):
        rp = urllib.robotparser.RobotFileParser()
        rp.set_url(self.robots_url)
        rp.read()
        return rp

    def url_can_fetch(self) -> str:
        if self.rp.can_fetch(self.user_agent, self.raw_url) is True:
            return 'Allow'
        else:
            return 'Disallow'

    def url_crawl_delay(self) -> str:
        if self.rp.crawl_delay(self.user_agent) is not None:
            return str(self.rp.crawl_delay(self.user_agent)) + 's'
        else:
            return 'None (1s wait recommended)'

def main():
    url = input('URL Here >>> ')
    user_agent = input('User-Agent Here >>> ')
    robots = Robots(url, user_agent)

    print(f"""
    root URL -> {robots.root_url}
    robots.txt URL -> {robots.robots_url}
    -------------------------------------
    Can fetch 
        user-agent: {robots.user_agent} -> {robots.url_can_fetch()}
    -------------------------------------
    Crawl delay
        user-agent: {robots.user_agent} -> {robots.url_crawl_delay()}
    """)

if __name__ == '__main__':
    main()
