import json
from urllib.request import urlopen
import time
from urllib import request
import pandas as pd
import xlwt
from geopy.distance import geodesic


# 将对应参数接入圆形区域搜索接口
def urls(itemy, loc):
    urls = []
    radius = 800     # 圆形区域搜索半径
    for page in range(0, 20):    # 由于百度地图数据保护目的，只允许访问20页POI数据，每页有20个信息，共计400个POI数据
        url = "http://api.map.baidu.com/place/v2/search?query=" + request.quote(itemy) + "&location=" + str(loc)
        url = url + "&page_size=20&page_num=" + str(
            page) + "&output=json&ak=百度开发者申请的ak" + "&radius=" + str(radius)
        urls.append(url)
    return urls


# 获取每一个POI的名称与经纬度信息
def baidu_search(urls):
    try:
        json_sel_1 = []
        json_sel_2 = []
        for url in urls:
            req = request.Request(url)
            json_obj = urlopen(req)
            data = json.load(json_obj)

            for item in data['results']:
                jname = item["name"]
                jlat = item["location"]["lat"]
                jlng = item["location"]["lng"]
                js_sel = str(jlat) + ',' + str(jlng)
                json_sel_2.append(js_sel)
                json_sel_1.append(jname)
    except:
        pass

    return json_sel_1, json_sel_2


if __name__ == '__main__':
    print("开始爬取数据，请稍等...")
    start_time = time.time()
    filepath_1 = r'关键词.txt'
    filepath = r'地铁站.xlsx'
    df = pd.read_excel(filepath)
    datas = df.iloc[:, 1].values
    print("读取指定行的数据：\n{0}".format(datas))
    words = ['关键词']
    f = open(filepath_1, 'a', encoding='utf-8')
    results = []
    error_datas = []
    error_words = []
    flag = 0
    t = 1
    for word in words:
        result = []
        for data in datas:
            url = []
            url = urls(word, data)
            names, locations = baidu_search(url)
            b = len(names)
            result.append(b)
            # 如果一个区域内POI数据少于400个则将所有数据写入txt文件中
            if b < 400:
                count = 0
                for i in range(len(names)):
                    con = (geodesic(locations[i], data)).km
                    # 为确保数据准确性此处再进行一次距离筛选，并记录POI数据对应的类型、名称、经纬度、对应的地铁站和距离
                    if con < 0.8:
                      count += 1
                      item = word + ',' + str(names[i]) + ',' + str(locations[i]) + ',' + str(t) + ',' + str(con)
                      f.write(item)
                      f.write("\n")
                print("录入%d个数据" % count)
            # 否则记录多于400个数据的地铁站信息
            else:
                error_datas.append(data)
                error_words.append(word)
            t += 1
        results.append((result))
        flag = flag + 1
    print(results)
    # 将多于400个数据的地铁站信息导出
    file = xlwt.Workbook()  # 创建工作薄
    sheet1 = file.add_sheet(u'统计', cell_overwrite_ok=True)  # 创建sheet
    i = 0
    for data in error_datas:
        sheet1.write(0, 0, label='地铁站经纬度')
        sheet1.write(i + 1, 0, str(error_datas[i]))
        i = i + 1
    j = 0
    for word in error_words:
        sheet1.write(0, 1, label='关键词')
        sheet1.write(j + 1, 1, str(error_words[j]))
        j = j + 1
    file.save(r'统计超过400的地铁站及相应关键词.xls')

    end_time = time.time()
    print("爬取完毕，用时%.2f秒" % (end_time - start_time))

