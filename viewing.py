import json
import os
import xlwt


def organize(path_collect_data):
    """ 将同一收藏夹的数据整合到同一个json文件中
    :param path_collect_data: 文件输出路径
    :return:
    """
    print('正在将同一收藏夹的数据整合到同一个json文件中')
    # 获取文件夹下所有文件/文件夹的名称集合，这个文件夹是存放所有收藏夹的总文件夹
    dir_names = os.listdir(path_collect_data)

    # 遍历所有收藏夹
    for i in dir_names:
        os.chdir(path_collect_data)

        if os.path.isdir(i):
            file_names = os.listdir(i)
        else:
            continue

        os.chdir(i)
        medias = []
        with open(i + '.json', 'w', encoding='utf-8')as fp:
            for j in file_names:
                if os.path.getsize(j):
                    with open(j, 'r', encoding='utf-8')as f:
                        file = json.load(f)
                    data = file['data']
                    media = data['medias']
                    print('正在整合:'+j)
                    for k in media:
                        medias.append(k)
            json.dump(medias, fp, ensure_ascii=False)
        print('收藏夹'+i+'整合完毕')
    print('所有收藏夹整合完毕！！！')



alignment = xlwt.Alignment()
borders = xlwt.Borders()

alignment.wrap = 1
alignment.horz = 2
alignment.vert = 1

borders.left = xlwt.Borders.MEDIUM  # 添加边框-虚线边框
borders.right = xlwt.Borders.MEDIUM  # 添加边框-虚线边框
borders.top = xlwt.Borders.MEDIUM  # 添加边框-虚线边框
borders.bottom = xlwt.Borders.MEDIUM  # 添加边框-虚线边框

def headStyle():
    style = xlwt.XFStyle()
    font = xlwt.Font()
    font.colour_index = xlwt.Style.colour_map['red']
    font.bold = True

    style.borders = borders
    style.alignment = alignment
    style.font = font
    return style

def TitleStyle():
    style = xlwt.XFStyle()
    style.borders = borders
    style.alignment = alignment
    return style

def introStyle():
    style = xlwt.XFStyle()
    style.borders = borders
    style.alignment = alignment
    return style

def nalStyle():
    style = xlwt.XFStyle()
    style.borders = borders
    style.alignment = alignment
    return style

def viewing(path_collect_data):
    """
    将json文件汇总为xls表格文件
    :param path_collect_data:
    :return:
    """
    # path_collect_data = 'C:\\Users\\86135\\Desktop\\python\\B站个人资料\\收藏夹\\collect-data'  # 存放收藏夹数据的目录
    work = xlwt.Workbook(encoding='utf-8', style_compression=2)
    dir_names = os.listdir(path_collect_data)
    print('将json转为exce')
    for i in dir_names:
        print('正在录入: '+i)
        os.chdir(path_collect_data)
        if os.path.isdir(i):
            os.chdir(i)
        else:
            continue
        sht = work.add_sheet(i)

        # sht.set_panes_frozen('1')
        # # 水平冻结
        # sht.set_horz_split_pos(1)

        with open(i+'.json', 'r', encoding='utf-8') as fp:
            file = json.load(fp)
        num = 1
        sht.write_merge(0, 0, 0, 1, '标题', headStyle())
        sht.write(0, 2, 'UP主', headStyle())
        sht.write(0, 3, 'UP主UID', headStyle())
        sht.write(0, 4, '播放量', headStyle())
        sht.write(0, 5, '收藏', headStyle())
        sht.write(0, 6, '弹幕', headStyle())
        sht.write(0, 7, 'avId', headStyle())
        sht.write(0, 8, 'bvId', headStyle())
        sht.write(0, 9, '简介', headStyle())

        sht.col(0).width = 6666
        sht.col(1).width = 6666
        sht.col(2).width = 3333
        sht.col(3).width = 3333
        sht.col(4).width = 3333
        sht.col(5).width = 3333
        sht.col(6).width = 3333
        sht.col(7).width = 3333
        sht.col(8).width = 5000
        sht.col(9).width = 30000

        sum = 0
        for j in file:
            sum += 1
            sht.row(num).height = 1500
            sht.write_merge(num, num, 0, 1, j['title'], TitleStyle())
            sht.write(num, 2, j['upper']['name'], nalStyle())
            sht.write(num, 3, j['upper']['mid'], nalStyle())
            sht.write(num, 4, j['cnt_info']['play'], nalStyle())
            sht.write(num, 5, j['cnt_info']['collect'], nalStyle())
            sht.write(num, 6, j['cnt_info']['danmaku'], nalStyle())
            sht.write(num, 7, j['id'], nalStyle())
            sht.write(num, 8, j['bv_id'], nalStyle())
            sht.write(num, 9, j['intro'], introStyle())
            # if(sum < len(file)):
            #     sht.write_merge(num+3, num+3, 0, 6, '')
            num += 1
    os.chdir(path_collect_data)
    work.save('收藏夹.xls')
    print('录入完毕！！！')
