import json


# proxyHost = "http-proxy-sg2.dobel.cn"
# proxyPort = "9180"
# proxyUser = "ZYYTHTT1"
# proxyPass = "6tEQ26bA9"

if __name__ == '__main__':
    proxy = dict(proxyHost = "http-proxy-sg2.dobel.cn",
                 proxyPort = "9180",
                 proxyUser = "ZYYTHTT1",
                 proxyPass = "6tEQ26bA9")
    r_list = [proxy,]
    with open('proxy.json', 'w') as fw:
        json.dump(r_list, fw, indent=4)

