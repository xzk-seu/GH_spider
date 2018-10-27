import requests
from Logger import logger
import time
from bs4 import BeautifulSoup
import json


_HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.'
                          '0.3497.100 Safari/537.36'}

proxyHost = "http-proxy-sg2.dobel.cn"
proxyPort = "9180"
proxyUser = "ZYYTHTTTEST1"
proxyPass = "Y63b1qDf"
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


def page_parser(page):
    result_list = list()
    soup = BeautifulSoup(page.text, 'lxml')
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
    description = t1.p.string.strip()
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
    t3 = raw_repo.contents[3] # 语言和star
    language = t3.contents[1].contents[2].strip()
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
                             # proxies=_PROXIES,
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
