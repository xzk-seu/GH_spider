import os
import json


if __name__ == '__main__':
    y = input('input year: ')
    path = os.path.join(os.getcwd(), 'result', y)
    file_list = os.listdir(path)
    page_num = 0
    for file in file_list:
        f = file.split('-')
        if f[-1] == '1.json':
            file_path = os.path.join(path, file)
            with open(file_path, 'r') as fr:
                daily_num = json.load(fr)['daily_num']
                p_num = daily_num//10
                if daily_num % 10 != 0:
                    p_num += 1
                if p_num > 100:
                    p_num = 100
                print('%s-%s-%s' % (f[0], f[1], f[2]), daily_num, p_num)
                page_num += p_num
                for p in range(p_num):
                    f_path = os.path.join(path, '%s-%s-%s-%d.json' % (y, f[1], f[2], p+1))
                    if not os.path.exists(f_path):
                        print(f_path)
    print('%d pages should be got' % page_num)
    print('the number of file is %d' % len(file_list))
    print('%d%%' % (100*len(file_list)/page_num))


