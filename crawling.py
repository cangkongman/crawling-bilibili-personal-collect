import requests
import json
import os


def crawling(path_collect_data):
    # 请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    # 第一次爬取: 获取所有收藏夹的id
    url = 'https://api.bilibili.com/x/v3/fav/folder/created/list-all'
    params = {
        'up_mid': ,  # 写入自己账号的UID
        'jsonp': 'jsonp',
    }
    response = requests.get(url=url, params=params, headers=headers)
    assign = response.json()
    with open('收藏夹id.json', 'w', encoding='utf-8')as fp:
        json.dump(assign, fp, ensure_ascii=False)
    print('收藏夹id爬取成功')

    # 第二次爬取: 获取收藏夹的json数据
    url = 'https://api.bilibili.com/x/v3/fav/resource/list'
    # 参数，还需要添加 pn 和 media_id 两个参数
    params = {
        'ps': 20,
        'keyword': '',
        'order': 'mtime',
        'type': 0,
        'tid': 0,
        'platform': 'web',
        'jsonp': 'jsonp'
    }
    with open('收藏夹id.json', 'r', encoding='utf-8')as fp:
        file = json.load(fp)
        data = file['data']
        list = data['list']
        # 遍历所有的收藏夹
        for i in list:
            os.chdir(path_collect_data)
            path = i['title']

            if not os.path.exists(path):
                os.makedirs(path)

            os.chdir(path)

            # 开始第二次爬取
            params['pn'] = 1
            while (params['pn'] < (i['media_count'] / 20 + 1)):
                with open(i['title'] + str(params['pn']) + '.json', 'w', encoding='utf-8')as f:
                    print('爬取中: 当前爬取'+os.getcwd()+str(params['pn']))
                    params['media_id'] = i['id']
                    result = requests.get(url=url, params=params, headers=headers)
                    assign = result.json()
                    json.dump(assign, f, ensure_ascii=False)
                    params['pn'] += 1
            print('收藏夹'+i['title']+'信息爬取完毕!')
        print('所有收藏夹爬取完毕！！！')
