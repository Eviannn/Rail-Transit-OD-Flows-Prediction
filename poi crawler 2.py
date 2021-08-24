import json
from urllib.request import urlopen
import time
from urllib import request
import pandas as pd
from geopy.distance import geodesic

# 将对应参数接入矩形区域搜索接口
def urls(itemy, loc):
    urls=[]
    for page in range(0,20):      # 由于百度地图数据保护目的，只允许访问20页POI数据，每页有20个信息，共计400个POI数据
        url = "http://api.map.baidu.com/place/v2/search?query=" + request.quote(itemy) + "&bounds=" + loc
        url = url + "&page_size=20&page_num=" + str(page) + "&output=json&ak=百度开发者申请的ak"
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

    return json_sel_1,json_sel_2


# 大矩形的纬度分割
def lat_all(loc_all):
    lat_sw = float(loc_all.split(',')[0])
    lat_ne = float(loc_all.split(',')[2])
    lat_list = []

    for i in range(0, int((lat_ne - lat_sw ) / 0.01)):  # 网格大小，可根据区域内POI数目修改
        lat_list.append(lat_sw + 0.01 * i)
    lat_list.append(lat_ne)

    return lat_list


# 大矩形的经度分割
def lng_all(loc_all):
    lng_sw = float(loc_all.split(',')[1])
    lng_ne = float(loc_all.split(',')[3])
    lng_list = []
    for i in range(0, int((lng_ne - lng_sw ) / 0.01)):
        lng_list.append(lng_sw + 0.01 * i)
    lng_list.append(lng_ne)

    return lng_list


# 小矩形处理
def ls_com(loc_all):
    l1 = lat_all(loc_all)
    l2 = lng_all(loc_all)
    ab_list = []
    for i1 in range(0, len(l1)):
        a = str(l1[i1])
        for i2 in range(0, len(l2)):
            b = str(l2[i2])
            ab = a + ',' + b
            ab_list.append(ab)
    return ab_list


# 小矩形处理
def ls_row(loc_all):
    l1 = lat_all(loc_all)
    l2 = lng_all(loc_all)
    ls_com_v = ls_com(loc_all)
    ls = []
    for n in range(0, len(l1) - 1):
        for i in range(0 + len(l2) * n, len(l2) + (len(l2)) * n - 1):
            a = ls_com_v[i]
            b = ls_com_v[i + len(l2) + 1]
            ab = a + ',' + b
            ab_list = ab.split(',')
            if (ab_list[0] < ab_list[2] and ab_list[1] < ab_list[3]):
                ls.append(ab)
    return ls


if __name__ == '__main__':
    print("开始爬取数据，请稍等...")
    start_time = time.time()
    filepath = r'统计超过400的地铁站及相应关键词.xls'
    df = pd.read_excel(filepath)
    datas = df.iloc[:, 0].values
    words = df.iloc[:, 1].values
    print(words)
    filepath_1 = '筛选后信息.txt'
    f = open(filepath_1, 'a', encoding='utf-8')
    locs_to_use = []
    i = 0
    flag = 1
    for data in datas:
        x = data.split(',',1)
        print("筛选第%d个地铁站" % flag)
        flag += 1
        # 划分大矩形的范围
        lat_1 = str(float(x[0]) - 0.02)
        lng_1 = str(float(x[1]) - 0.02)
        lat_2 = str(float(x[0]) + 0.02)
        lng_2 = str(float(x[1]) + 0.02)
        loc_to_use = lat_1 + ',' + lng_1 + ',' + lat_2 + ',' + lng_2
        locs_to_use = ls_row(loc_to_use)
        count = 0
        for loc_to_use in locs_to_use:
            url = []
            url = urls(words[i], loc_to_use)
            names,locations = baidu_search(url)
            b = len(names)
            c = len(locations)
            if b > 0 :
                for j in range(len(names)):
                    con = (geodesic(locations[j],data)).km
                    # 距离筛选
                    if con < 0.8:
                        count += 1
                        # 记录每一个POI数据类型、名称、经纬度和距地铁站的距离
                        item = words[i] + ',' + names[j]+ ',' + locations[j] + ',' + str(con)
                        f.write(item)
                        f.write("\n")
        print("录入%d个数据" % count)
        i += 1
    end_time = time.time()
    print("爬取完毕，用时%.2f秒" % (end_time - start_time))
