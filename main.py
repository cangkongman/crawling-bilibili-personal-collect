import json
import os
import time
import requests
from concurrent import futures


# 处理原始数据，获取up头像和视频封面
def ProcessRawData(RawData):
    NewData = {}
    for i in RawData.values():
        media = {
            "id": i['id'],
            "BV": i['bv_id'],
            "是否失效": False,
            "up主": {
                "ID": i['upper']['mid'],
                "昵称": i['upper']['name'],
                "头像": i['upper']['face']
            },
            "视频信息": {
                "标题": i['title'],
                "封面": i['cover'],
                "简介": i['intro'],
                "时长": time.strftime("%H:%M:%S", time.gmtime(i['duration']))
            },
            "观众数据": {
                "播放量": i['cnt_info']['play'],
                "收藏量": i['cnt_info']['collect'],
                "弹幕数量": i['cnt_info']['danmaku']
            },
            "三个时间": {
                "上传时间": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(i['ctime'])),
                "发布时间": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(i['pubtime'])),
                "收藏时间": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(i['fav_time']))
            }
        }
        NewData[media['id']] = media
    return NewData


# 与上一次爬取对比，目前是标记上次没失效，但是这次失效的视频
def CompareLastTime(ReadPath, NewData):
    with open(ReadPath, 'r', encoding='utf-8') as f:
        OldData = json.load(f)
    for i in list(NewData.values()):
        if i['视频信息']['标题'] == "已失效视频" and str(i['id']) in OldData.keys():
            print('失效了')
            OldData[str(i['id'])]['是否失效'] = True
            NewData[str(i['id'])] = OldData[str(i['id'])]
    return NewData


# 爬取收藏夹的ID
def GetFavoriteID(WritePath):
    # 请求头
    headers = {
        'authority': 'api.bilibili.com',
        'method': 'GET',
        'path': '/x/v3/fav/resource/list?media_id=309076131&pn=1&ps=20&keyword=&order=mtime&type=0&tid=0&platform=web&jsonp=jsonp',
        'scheme': 'https',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        # 'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'max-age=0',
        'cookie': "_uuid=F500E27C-018D-CC3F-17E8-C64812E174DA08613infoc; buvid3=475B7DAC-0579-421B-85B7-07A4076090B734771infoc; buvid_fp=475B7DAC-0579-421B-85B7-07A4076090B734771infoc; CURRENT_FNVAL=80; blackside_state=1; rpdid=|(k|k)~~RkkJ0J'uYk|YumRkm; fingerprint3=c1d980f375c848a729ebdd130960a847; CURRENT_QUALITY=112; LIVE_BUVID=AUTO9716210898194009; fingerprint_s=be57440a1cba44ed342ad526646463d4; bp_t_offset_51541144=529073781132033226; bp_video_offset_51541144=529330083309673464; bp_t_offset_289920431=529693188424888145; fingerprint=a43248e91a776fba5e92af41d1a900e0; buvid_fp_plain=95AEE299-5E58-4AA1-92EF-CFE2BE6C6243184999infoc; SESSDATA=41ff3c64%2C1637735786%2Cff017%2A51; bili_jct=c0a63b68e972a8d1acc44a3718075b58; DedeUserID=289920431; DedeUserID__ckMd5=c43d13bc962635fe; sid=bvgle9dv; PVID=3; bp_video_offset_289920431=529757320878990660; bfe_id=5db70a86bd1cbe8a88817507134f7bb5",
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
        'sec-ch-ua-mobile': '?0',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
    }
    url = 'https://api.bilibili.com/x/v3/fav/folder/created/list-all'
    params = {
        'up_mid': 289920431,  # 自己账号的UID
        'jsonp': 'jsonp',
    }
    response = requests.get(url=url, params=params, headers=headers)
    assign = response.json()

    with open(WritePath + '收藏夹id.json', 'w', encoding='utf-8') as fp:
        json.dump(assign, fp, ensure_ascii=False)
    print('收藏夹id爬取成功')


# 爬取一个收藏夹信息，Media_Id代表收藏夹，MaxPage代表收藏夹的页数
def GetOneFavorite(Media_Id, MaxPage):
    # 爬虫的参数，其中params里的pn（页数）会随着遍历的改变而改变
    url = 'https://api.bilibili.com/x/v3/fav/resource/list'
    params = {
        'ps': 20,
        'keyword': '',
        'order': 'mtime',
        'type': 0,
        'tid': 0,
        'platform': 'web',
        'jsonp': 'jsonp',
        'pn': 1,
        'media_id': Media_Id
    }
    headers = {
        'authority': 'api.bilibili.com',
        'method': 'GET',
        'path': '/x/v3/fav/resource/list?media_id=309076131&pn=1&ps=20&keyword=&order=mtime&type=0&tid=0&platform=web&jsonp=jsonp',
        'scheme': 'https',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        # 'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'zh-CN,zh;q=0.9',
        'cache-control': 'max-age=0',
        'cookie': "_uuid=F500E27C-018D-CC3F-17E8-C64812E174DA08613infoc; buvid3=475B7DAC-0579-421B-85B7-07A4076090B734771infoc; buvid_fp=475B7DAC-0579-421B-85B7-07A4076090B734771infoc; CURRENT_FNVAL=80; blackside_state=1; rpdid=|(k|k)~~RkkJ0J'uYk|YumRkm; fingerprint3=c1d980f375c848a729ebdd130960a847; CURRENT_QUALITY=112; LIVE_BUVID=AUTO9716210898194009; fingerprint_s=be57440a1cba44ed342ad526646463d4; bp_t_offset_51541144=529073781132033226; bp_video_offset_51541144=529330083309673464; bp_t_offset_289920431=529693188424888145; fingerprint=a43248e91a776fba5e92af41d1a900e0; buvid_fp_plain=95AEE299-5E58-4AA1-92EF-CFE2BE6C6243184999infoc; SESSDATA=41ff3c64%2C1637735786%2Cff017%2A51; bili_jct=c0a63b68e972a8d1acc44a3718075b58; DedeUserID=289920431; DedeUserID__ckMd5=c43d13bc962635fe; sid=bvgle9dv; PVID=3; bp_video_offset_289920431=529757320878990660; bfe_id=5db70a86bd1cbe8a88817507134f7bb5",
        'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
        'sec-ch-ua-mobile': '?0',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36'
    }

    data = {}
    # 遍历爬取一个收藏夹的不同页数，然后合并到一个字典里
    for params['pn'] in range(MaxPage)[1::]:
        print('第' + str(params['pn']) + '页')

        response = requests.get(url=url, params=params, headers=headers).json()
        medias_list = response['data']['medias']
        # 将不同页数合并到字典里
        for i in medias_list:
            data[i['id']] = i
    return data


# 爬取全部收藏夹信息
def GetALLFavorite(WritePath):
    # 打开文件，获取之前爬取到的收藏夹id和收藏夹页数
    with open(WritePath + '收藏夹id.json', 'r', encoding='utf-8') as fp:
        file = json.load(fp)
    ID_list = file['data']['list']

    # 遍历所有收藏夹，爬取所有收藏夹
    for i in ID_list:
        print('爬取中...当前正在爬取' + i['title'])
        filename = WritePath + i['title'] + '.json'
        data = GetOneFavorite(i['id'], int(i['media_count'] / 20 + 1) + 1)
        # 再次处理数据，并且写入json文件
        finally_data = CompareLastTime(filename, ProcessRawData(data))
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(finally_data, f, ensure_ascii=False)
    print('所有收藏夹爬取完毕！！！')


# 爬取图片，包括视频封面和up主头像
def GetPhoto(ReadPath):
    file_name_list = os.listdir(ReadPath)
    file_name_list.remove('收藏夹id.json')
    UP_dict = {}
    Video_dict = {}
    for i in file_name_list:
        with open(ReadPath + i, 'r', encoding='utf-8') as f1:
            data = json.load(f1)
        # 因为时间较长，想要显示当前进度，所以先获取全部要爬取的图片信息,顺便给up主去重
        for j in data.values():
            # 如果视频已经失效了，就不操作
            if j['是否失效']:
                continue
            Video_dict[j['id']] = j['视频信息']['封面']
            UP_dict[j['up主']['ID']] = j['up主']['头像']

    CrawlPhoto(Video_dict, '视频封面/')
    CrawlPhoto(UP_dict, 'up头像/')


def CrawlPhoto(data_dict, WritePath):
    ss = '视频'
    if WritePath == 'up头像/':
        ss = 'up'
    keys = list(data_dict.keys())
    for i in range(len(keys))[::15]:
        executor = futures.ThreadPoolExecutor(max_workers=15)
        fs = []
        for j in range(15):
            if (i + j) < len(keys):
                f = executor.submit(requests.get, data_dict[keys[i + j]])
                print('[' + str(i + +j + 1) + '/' + str(len(keys)) + ']:' + ss + str(keys[i + j]))
                fs.append(f)
        futures.wait(fs)
        result = [f.result().content for f in fs]
        for c, k in zip(result, keys):
            with open(WritePath + str(k) + '.jpg', 'wb') as fp:
                fp.write(c)


if __name__ == "__main__":
    path = '收藏夹信息/'  # 存放信息的文件夹
    GetFavoriteID(path)
    GetALLFavorite(path)
    STime = time.perf_counter()
    GetPhoto(path)
    ETime = time.perf_counter()
    print(time.strftime("%M:%S", time.gmtime(ETime - STime)))
