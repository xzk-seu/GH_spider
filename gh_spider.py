from get_response import get_response, page_parser
import json
from Logger import logger

SEARCH_URL = 'https://github.com/search'


if __name__ == '__main__':
    page = 1
    p = dict()
    p['p'] = page
    p['q'] = 'created:2010-10-19'
    p['type'] = 'Repositories'
    p['s'] = 'stars'
    p['o'] = 'desc'
    r = get_response(SEARCH_URL, p)
    page_dict = dict()
    try:
        page_dict = page_parser(r)
    except AttributeError as e:
        logger.error('invalid page: %s' % r.url)
        logger.error('reason: %s' % str(e))

    print(len(page_dict['repo']))
    with open('test.json', 'w') as fw:
        json.dump(page_dict, fw, indent=4)
    print(page_dict)




