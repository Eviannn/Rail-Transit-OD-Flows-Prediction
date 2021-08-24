from bs4 import BeautifulSoup
import re
import requests
from parsel import Selector
import pandas as pd
import time
import sys
import io

# 进行网络请求的浏览器头部
headers={
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
    }


# 获取链家网小区信息
def l_par_html(url):
    wr=requests.get(url,headers=headers,stream=True)
    sel=Selector(wr.text)
    print(wr.text)

    xiaoquID=sel.xpath('//div[@class="agentInfo"]/div[@class="agent_chat im-talk LOGCLICKDATA"]/@data-lj_action_resblock_id').extract()
    print(xiaoquID)
    # hou_code用来获取房源的编号
    hou_code=sel.xpath('//div[@class="priceInfo"]/div[@class="unitPrice"]/@data-rid').extract()
    print(hou_code)
    # 将信息形成表格全部写到一起
    pages_info=pd.DataFrame(list(zip(xiaoquID)),columns=['ID'])
    return pages_info


# pages是不同页码的网址列表
pages=['https://nj.lianjia.com/xiaoqu/pg{}/?from=rec'.format(x) for x in range(1,2)]
lj_xiaoqu = pd.DataFrame(columns=['ID'])

count=0
# 为了避免反爬虫策略，设定每5秒钟抓取一页信息
for page in pages:
    a=l_par_html(page)
    count=count+1
    print('the '+str(count)+' page is sucessful')
    time.sleep(5)
    lj_xiaoqu=pd.concat([lj_xiaoqu,a],ignore_index=True)
# 将表格数据输出到excel文件
lj_xiaoqu.to_excel('输入保存路径')
print(1)