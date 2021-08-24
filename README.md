# Rail-Transit-OD-Flows-Prediction
Student Research and Training Programme, National Level, 2018.12-2020.08

### Abstract
The spatial-temporal big data such as rail transit AFC data and electronic map data are used to mine the multi-dimensional characteristics of rail transit passenger flow OD distribution, and the relationship between urban built environment characteristics and rail passenger flow characteristics is deeply studied; By analyzing the land use around the station, this paper explores the relationship between the boarding and landing passenger flow of rail transit stations and the surrounding built environment, excavates the influencing factors including land use characteristics, bus connection characteristics and station attributes, and constructs a deep neural network model to quantify the impact of urban land development on rail transit passenger flow and predict the OD passenger flow of urban rail transit.

### Data Source
1. Rail transit AFC data in Nanjing, 2017(Strictly confidential)
2. Electronic map data from Baidu and Lianjia

### Files Including
1. poi crawler 1.py
2. poi crawler 2.py
3. lianjia crawler.py
4. NN Prediction Model.py

### Detailed Description in Chinese
#### 百度地图POI数据获取
1. 数据来源及依据
百度地图API提供地点检索服务。该服务提供多种场景的地点（POI）检索功能，包括城市检索、圆形区域检索和矩形区域检索。百度地图开发者可通过接口获取地点（POI）基础或详细地理信息。
根据项目具体要求，需要获取轨道交通站点周边POI数据信息，故采用圆形区域搜索方式。圆形区域搜索接口格式如下：http://api.map.baidu.com/place/v2/search?query=关键词&location=地铁站纬度,地铁站经度&radius=半径&output=xml&ak=百度地图开发者申请的密钥 //GET请求。圆心设定为轨道交通站点经纬度，半径为轨道交通影响范围，设定为800米。关键词即为需要获取的POI数据名称，此处检索的名称参考百度地图提供的POI行业分类标准，共检索15类POI数据，分别为公司企业、生活服务、景点、金融、美食、教育培训、购物、公交车站、酒店、文化传媒、休闲娱乐、医疗、运动健身、政府机构和自行车租赁点。
将每一个地铁站经纬度和搜索的POI关键词输入接口中，即可得到对应地铁站周边的POI数据。由于工作量庞大，故采用Python语言编写爬虫代码爬取POI信息。
2. 爬取过程中的注意事项
项目指导老师提供2017年1月的轨道交通客流刷卡数据；百度公司出于数据保护的目的，百度地图API中提供的地点检索服务最近的更新时间是2017年1月10日。因此两类数据正好可以相互匹配。与现在相比，当时的南京地铁有一部分线路尚未开通，因此在该项目中使用的地铁站总量为113个。
百度公司出于数据保护的目的，每日给开发者使用的地点检索服务有配额限制，因此Python代码中不能一次性爬取所有站点所有POI信息的数据。
百度公司出于数据保护的目的，圆形区域搜索中，每一个区域搜索上限为400个POI数据，因此若区域内POI数据超过400个，需要记录下对应的站点，之后对这些站点使用矩形区域检索方法，在站点附近取一个大矩形，包含但不仅含800米范围内的POI数据，再把大矩形分割成若干小矩形，使得每一个小矩形内包含的POI数据不超过400个，最终汇总得到大矩形内的POI数据，之后通过距离筛选语句，把地铁站周边800米POI数据筛选出来，即可得到每一个地铁站周边准确的POI数据，而不是最多只能获得400个数据。
3. 爬取代码实现
在注意事项中提及，开发者每日使用的配额受限，为保证数据的准确性，每一次只爬取所有轨道交通站点的一类POI数据。当收到配额使用接近上限的提示短信时，当日停止爬取数据工作。
分两个代码共同实现爬取POI数据的功能，第一个代码（圆形区域检索代码）获取同一类POI数据在所有地铁站附近的具体信息，同时，若地铁站附近的POI数据超过400个，将对应的地铁站记录下来，在另一个代码（矩形区域检索及距离筛选代码）中，对这些站点进行矩形区域检索并筛选距离，保留距地铁站800米以内的POI数据，具体原因、方式及原理在注意事项中已做解释。
圆形区域搜索代码需要每一个地铁站的经纬度数据，通过百度地图API提供的接口爬取需要的POI数据，记录在生成的txt格式文件中，并导出周边POI数据超过400个的地铁站经纬度信息。
矩形区域检索及距离筛选代码可直接读取圆形区域搜索代码中生成的地铁站经纬度信息，将对应的地铁站周边分割成若干小矩形，获取每一个小矩形内包含的POI数据，并进行距离筛选。已有研究成果表明，轨道交通车站的直接影响半径为500m—800m左右,考虑到外围区轨道交通具有更广的吸引范围，取影响半径的最大值800m对轨道交通车站周围的土地利用数据进行统计分析。因此，保留距地铁站800米范围之内的POI数据，记录在生成的txt格式文件中。

#### OD客流预测
对于每一条轨道交通OD数据，都有与之对应的两条O、D点周边建成环境数据。因此，本项目欲通过每一条OD周边的建成环境数据，来预测对应OD的客流量。
为重点关注早晚高峰时段客流量情况，区分早晚高峰时段OD客流预测模型，早高峰时段一小时取7点至8点，晚高峰时段一小时取17点至18点，利用AFC刷卡数据统计对应时段客流OD情况，并匹配对应OD周边的建成环境数据。基于神经网络模型，对南京市轨道交通113个站点共计112*113条OD数据及对应建成环境数据进行训练，最终得到最优化模型结果，输出权重文件，实现利用O、D点周边建成环境数据预测OD客流量。

