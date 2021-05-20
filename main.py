from crawling import crawling
from viewing import organize
from viewing import viewing

if __name__ == "__main__":
    path_collect_data = ''  # 写入存放收藏夹数据的目录
    crawling(path_collect_data)
    organize(path_collect_data)
    viewing(path_collect_data)
