import requests
from Logger import logger
import time
from bs4 import BeautifulSoup
import json


_HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.'
                          '0.3497.100 Safari/537.36'}

proxyHost = "http-proxy-sg2.dobel.cn"
proxyPort = "9180"
proxyUser = "ZYYTHTT1"
proxyPass = "6tEQ26bA9"

# proxyHost = "http-dyn.abuyun.com"
# proxyPort = "9020"
# proxyUser = "HE67H8188DLDT85D"
# proxyPass = "4145553046D4B3BB"
# proxyUser = "H8461Q488M583V1D"
# proxyPass = "D90F780427E4D69E"
# proxyUser = "HX55696WE9Q2XJ4D"
# proxyPass = "21F210078BAEA359"

proxyHost = "proxy.crawlera.com"
proxyPort = "8010"
proxyAuth = "78d4b6f49900465f881f63b4b1de4029:"
proxyMeta = {"https": "https://{}@{}:{}/".format(proxyAuth, proxyHost, proxyPort),
             "http": "http://{}@{}:{}/".format(proxyAuth, proxyHost, proxyPort)}


proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
    "host": proxyHost,
    "port": proxyPort,
    "user": proxyUser,
    "pass": proxyPass,
}
_PROXIES = {
    "http": proxyMeta,
    "https": proxyMeta,
}


def page_parser(resp):
    result_list = list()
    try:
        soup = BeautifulSoup(resp.text, 'lxml')
    except AttributeError:
        logger.error('resp is None!')
        return
    repo_list = soup.find('ul', 'repo-list').contents
    daily_num = soup.find_all('h3')[1].string.strip('\n repository results').replace(',', '')
    daily_num = int(daily_num)
    result_dict = dict(daily_num=daily_num)
    for i in range(1, len(repo_list), 2):
        result_list.append(repo_parser(repo_list[i]))
    result_dict["repo"] = result_list
    return result_dict


def repo_parser(raw_repo):
    t1 = raw_repo.contents[1]
    repo_item = t1.h3.a
    description = t1.p.contents[0].string.strip()
    repo_json = repo_item['data-hydro-click']
    repo_dict = json.loads(repo_json)
    repo_url = repo_dict['payload']['result']['url']
    repo_title = repo_item.string
    repo_titles = repo_title.split('/')
    repo_owner = repo_titles[0]
    repo_name = repo_titles[1]
    topics = t1.find('div', 'topics-row-container col-12 col-md-9 d-inline-flex flex-wrap flex-items-center f6 my-1')
    topic_list = list()
    if topics and len(topics) > 0:
        for i in range(1, len(topics), 2):
            topic_list.append(topics.contents[i].string.strip())
    t3 = raw_repo.contents[3]
    # 语言和star
    language = None
    try:
        language = t3.contents[1].contents[2].strip()
    except IndexError:
        pass
    star = t3.contents[3].contents[1].contents[2].strip()
    repo = {'name': repo_name,
            'owner': repo_owner,
            'path': repo_url,
            'description': description,
            'topics': topic_list,
            'language': language,
            'star': star
            }
    return repo


def get_response(url, param=None):
    max_try = 0
    r = None
    while max_try <= 5:
        max_try += 1
        try:
            r = requests.get(url=url,
                             params=param,
                             proxies=_PROXIES,
                             headers=_HEADERS)
            r.raise_for_status()
            r.encoding = r.apparent_encoding
            break
        except Exception as e:
            if max_try < 5:
                logger.info("Try: %d | Error : %s" % (max_try, str(e)))
            else:
                logger.error("Try: %d | Error : %s" % (max_try, str(e)))
            time.sleep(max_try)
    if not r:
        return None
    return r


if __name__ == '__main__':
    SEARCH_URL = 'https://github.com/search'
    page = 1
    date_str = '2009-01-03'
    p = {'p': page,
         'q': 'created:' + date_str,
         'type': 'Repositories',
         's': 'stars',
         'o': 'desc'}
    r = get_response(SEARCH_URL, p)
    d = page_parser(r)
    repo = d['repo']
    for i in d['repo']:
        print(i['language'])
