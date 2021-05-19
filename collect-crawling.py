# -- encoding utf-8 --
import requests
import json
import os

path_collect_data = 'C:\\Users\\86135\\Desktop\\python\\B站个人资料\\收藏夹\\collect-data'  # 存放收藏夹数据的目录

def crawling():
    # 请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    # 第一次爬取: 获取所有收藏夹的id
    url = 'https://api.bilibili.com/x/v3/fav/folder/created/list-all?up_mid=289920431&jsonp=jsonp'  # up_mid修改成自己的UID
    response = requests.get(url, headers)
    assign = response.json()
    with open('收藏夹id.json', 'w', encoding='utf-8')as fp:
        json.dump(assign, fp, ensure_ascii=False)

    # 第二次爬取: 获取收藏夹的json数据
    url = 'https://api.bilibili.com/x/v3/fav/resource/list'
    # 参数，pn代表页数需要自增，另外还有media_id需要添加
    params = {
        'pn': 1,
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
            params['pn'] = 1
            os.chdir(path_collect_data)
            path = i['title']

            if not os.path.exists(path):
                os.makedirs(path)

            os.chdir(path)
            print(os.getcwd())

            # 开始第二次爬取
            while (params['pn'] < (i['media_count'] / 20 + 1)):
                with open(i['title'] + str(params['pn']) + '.json', 'w', encoding='utf-8')as f:
                    params['media_id'] = i['id']
                    result = requests.get(url, params)
                    assign = result.json()
                    json.dump(assign, f, ensure_ascii=False)
                    params['pn'] += 1

def organize():
    # 获取文件夹下所有文件/文件夹的名称集合，这个文件夹是存放所有收藏夹的总文件夹
    dir_names = os.listdir(path_collect_data)
    # 继续修改路径
    os.chdir(path_collect_data)
    print(dir_names)
    print(os.getcwd())

    # 遍历所有收藏夹
    for i in dir_names:
        os.chdir(path_collect_data)
        file_names = os.listdir(i)
        os.chdir(path_collect_data + '\\' + i)
        medias = []
        with open(i + '.json', 'w', encoding='utf-8')as fp:
            for j in file_names:

                filepath = path_collect_data + '\\' + i + '\\' + j

                if os.path.getsize(filepath):
                    with open(filepath, 'r', encoding='utf-8')as f:
                        file = json.load(f)
                        data = file['data']
                        media = data['medias']
                        for k in media:
                            medias.append(k)
            json.dump(medias, fp, ensure_ascii=False)

if __name__ == "__main__":
    crawling()
    organize()