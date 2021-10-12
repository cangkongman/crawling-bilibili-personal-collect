import os

from crawling import crawling
from viewing import organize
from viewing import viewing

"""
    使用方法：python3 main.py [uid 必填] [output_path 可选]
    
"""
import sys

if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print('参数个数不正确\n使用方法：python3 main.py [uid 必填] [output_path 可选]')
    print(f'当前文件路径： {sys.path[0]}')
    uid = sys.argv[1]
    print(sys.argv)

    if len(sys.argv) < 3:
        # 未指定output_path 使用默认路径
        path_collect_data = os.path.join(sys.path[0], 'output')
    else:
        path_collect_data = sys.argv[2]  # 写入存放收藏夹数据的目录

    crawling(uid, path_collect_data)
    organize(path_collect_data)
    viewing(path_collect_data)
