import time

import requests


def get_ip(ip_url):
    respond = requests.get(ip_url)
    print(respond.text)
    with open('proxy.txt', 'w', encoding='UTF-8') as f:
        for ip in str(respond.text).strip().split('\r\n'):
            f.writelines(ip+'\n')
    # return str(respond.text).strip().split('\r\n')


if __name__ == '__main__':
    while True:
        get_ip('http://ip.16yun.cn:817/myip/pl/ceafb464-46b5-4803-b154-3f1ec44e5ef8/?s=wkexsvkhrf&u=zhubo')
        time.sleep(61)




