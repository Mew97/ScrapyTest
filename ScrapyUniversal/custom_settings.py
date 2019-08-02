SPIDER = 'spider'

START_URS = ['https://wuhan.8684.cn/list1',
             'https://wuhan.8684.cn/list2',
             'https://wuhan.8684.cn/list3',
             'https://wuhan.8684.cn/list4',
             'https://wuhan.8684.cn/list5',
             'https://wuhan.8684.cn/list6',
             'https://wuhan.8684.cn/list7',
             'https://wuhan.8684.cn/list8',
             'https://wuhan.8684.cn/list9']

ALLOWED_DOMAINS = ['8684.cn']

COLLECTION = 'bus'

ITEM = {

    'bus_num': {
      'method': 'xpath',
      'args': '/html/body/div[2]/div[1]/h2[2]'
    },

    'bus_list': {
      'method': 'xpath',
      'args': '//*[@id="scrollTr"]'
    },

}



