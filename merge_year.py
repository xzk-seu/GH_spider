import os
import json
from datetime import date


if __name__ == '__main__':
    y = input('year: ')
    r_dict = dict()
    path = os.path.join(os.getcwd(), 'result', y, 'merge')
    # file_list = os.listdir(path)
    # for file in file_list:
    #     d = file.split('.')[0]

    begin = date(int(y), 1, 1)
    end = date(int(y), 12, 31)
    day = begin
    for d in range((end - begin).days + 1):
        d_str = day.isoformat()
        day += day.resolution
        file_path = os.path.join(path, '%s.json' % d_str)
        print(d_str)
        if os.path.exists(file_path):
            with open(file_path) as fr:
                js = json.load(fr)
            r_dict[d_str] = js
        else:
            r_dict[d_str] = None
    result_path = os.path.join(os.getcwd(), 'result', '%s.json' % y)
    with open(result_path, 'w') as fw:
        json.dump(r_dict, fw)
