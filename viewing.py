import xlwings as xw
import json
import os

def viewing(path_collect_data):

    app = xw.App(visible=False, add_book=False)
    wb = app.books.add()
    dir_name = os.listdir(path_collect_data)
    for i in dir_name:
        os.chdir(path_collect_data)
        print(i)
        if os.path.isdir(i):
            os.chdir(path_collect_data + '\\' + i)
        else:
            continue
        sht = wb.sheets.add(i)
        sht.range("a1:d1").value = ['Title', 'UP name', 'UP UID', 'Link']
        with open(i+'.json', 'r', encoding='utf-8') as fp:
            medias = json.load(fp)
            num = 2
            for j in medias:
                sht.range('a'+str(num)).value = j['title']
                sht.range('b'+str(num)).value = j['upper']['name']
                sht.range('c'+str(num)).value = j['upper']['mid']
                sht.range('d'+str(num)).value = 'www.bilibili.com/'+j['bv_id']
                sht.range('a'+str(num)).columns.autofit()
                sht.range('b'+str(num)).columns.autofit()
                sht.range('c'+str(num)).columns.autofit()
                sht.range('d'+str(num)).columns.autofit()
                num+=1

    os.chdir(path_collect_data)
    print(os.getcwd())
    wb.save("./收藏夹.xlsx")
    wb.close()
    app.quit()
