from crawling import crawling
from viewing import organize
from viewing import viewing

if __name__ == "__main__":
    path_collect_data = 'C:\\Users\\86135\\Desktop\\python\\B站个人资料\\收藏夹\\collect-data'  # 存放收藏夹数据的目录
    crawling(path_collect_data)
    organize(path_collect_data)
    viewing(path_collect_data)
