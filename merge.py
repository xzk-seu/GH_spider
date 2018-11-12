import os
import json
from datetime import date


def get_page_num(date_str):
    # r_list = list()
    y, m, d = date_str.split('-')
    path = os.path.join(os.getcwd(), 'result', y, '%s-1.json' % date_str)
    with open(path, 'r') as fr:
        daily_num = json.load(fr)['daily_num']
        p_num = daily_num // 10
        if daily_num % 10 != 0:
            p_num += 1
        if p_num > 100:
            p_num = 100
        print(date_str, daily_num, p_num)
        # for p in range(p_num):
        #     # f_path = os.path.join(path, '%s-%s-%s-%d.json' % (y, f[1], f[2], p + 1))
        #     r_list.append('%s-%d.json' % (date_str, p+1))
    return p_num


def daily_merge(date_str):
    r_list = list()
    page_num = get_page_num(date_str)
    path = os.path.join(os.getcwd(), 'result', date_str.split('-')[0])
    for p in range(page_num):
        file_path = os.path.join(path, '%s-%d.json' % (date_str, p+1))
        with open(file_path, 'r') as fr:
            js = json.load(fr)
        js['page'] = p+1
        r_list.append(js)
    merge_path = os.path.join(path, 'merge')
    if not os.path.exists(merge_path):
        os.makedirs(merge_path)
    merge_path = os.path.join(merge_path, '%s.json' % date_str)
    with open(merge_path, 'w') as fw:
        json.dump(r_list, fw)


if __name__ == '__main__':
    y = input('input year: ')
    path = os.path.join(os.getcwd(), 'result', y)
    # file_list = os.listdir(path)
    # for file in file_list:
    #     print(file[:10])
        # y, m, d, r = file.split('-')
        # p = r.split('.')[0]
        # print(y, m, d, p)
    begin = date(int(y), 1, 1)
    end = date(int(y), 12, 31)
    day = begin
    for d in range((end - begin).days + 1):
        d_str = day.isoformat()
        day += day.resolution
        print(d_str)
        daily_merge(d_str)
