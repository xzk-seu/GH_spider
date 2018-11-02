from get_response import get_response, page_parser, proxy_cfg
import json
import os
from datetime import date
from multiprocessing import Pool
from Logger import logger

SEARCH_URL = 'https://github.com/search'


def get_date_list(y):
    # 条件2：year.json中不存在
    # 根据条件获取一个日期list
    csv_path = os.path.join(os.getcwd(), 'Statistic', '%d.csv' % y)
    json_path = os.path.join(os.getcwd(), 'Result', '%d.json' % y)
    content = get_csv_content(csv_path)
    csv_list = list()
    for i in content:
        if 0 < int(i['count']) < 1000:
            csv_list.append(i['date'])
    with open(json_path, 'r') as fr:
        j = json.load(fr)
    result_list = [i for i in csv_list if i not in j.keys()]
    return result_list


def page_spider(date_str, page, proxy):
    res_path = os.path.join(os.getcwd(), 'result', date_str.split('-')[0], '%s-%d.json' % (date_str, page))
    if os.path.exists(res_path):
        with open(res_path, 'r') as fr:
            logger.info('%s-%d.json is existing!' % (date_str, page))
            return json.load(fr)['daily_num']
    p = {'p': page,
         'q': 'created:'+date_str,
         'type': 'Repositories',
         's': 'stars',
         'o': 'desc'}
    # p['p'] = page
    # p['q'] = 'created:'+date_str
    # p['type'] = 'Repositories'
    # p['s'] = 'stars'
    # p['o'] = 'desc'
    r = get_response(SEARCH_URL, p, proxy)
    page_dict = dict()
    try:
        page_dict = page_parser(r)
    except AttributeError as e:
        logger.error('invalid page: %s' % r.url)
        logger.error('reason: %s' % str(e))
        with open('invalid_page', 'a') as fa:
            fa.write(r.url + '\n')
    if not page_dict:
        return
    path = os.path.join(os.getcwd(), 'result', date_str.split('-')[0])
    if not os.path.exists(path):
        os.makedirs(path)
    file_name = os.path.join(path, '%s-%d.json' % (date_str, page))
    with open(file_name, 'w') as fw:
        json.dump(page_dict, fw, indent=4)
        logger.info('%s:%d is done!!!!!!!!!!!!' % (date_str, page))
        return page_dict['daily_num']


def daily_spider(date_str, pool, proxy):
    daily_num = page_spider(date_str, 1, proxy)
    if not isinstance(daily_num, int):
        return
    if daily_num > 990:
        remain_page = 99
    else:
        remain_page = daily_num//10
        if daily_num % 10 == 0:
            remain_page -= 1
    for i in range(remain_page):
        page = i+2
        pool.apply_async(page_spider, args=(date_str, page, proxy))


def zero_day():
    r = ['2008-01-01',
         '2008-01-02',
         '2008-01-03',
         '2008-01-04',
         '2008-01-05',
         '2008-01-06',
         '2008-01-07',
         '2008-01-08',
         '2008-01-09',
         '2008-01-10',
         '2008-01-11',
         '2008-01-16',
         '2008-01-24',
         '2008-01-26',
         '2008-01-20']
    return r


if __name__ == '__main__':
    proxy_id = int(input('please input proxy id: '))
    proxy = proxy_cfg(proxy_id)
    y = int(input('input year: '))
    p = Pool(1)
    begin = date(y, 1, 1)
    end = date(y, 12, 31)
    day = begin
    for d in range((end-begin).days+1):
        d_str = day.isoformat()
        day += day.resolution
        if d_str in zero_day():
            continue
        daily_spider(d_str, p, proxy)
        # res = pool.apply_async(search_page_parse.get_daily_reponum, args=(d_str,))
        # result_list.append([d_str, res])
        logger.info('%s task begin!' % d_str)
    p.close()
    p.join()


