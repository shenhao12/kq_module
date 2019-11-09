import networkx as nx #引入复杂网络networkx模块
import pymongo #引入相关模块操控mongodb模块
import pandas as pd #引入pandas模块用来读取数据
import re #正则表达式

#facebook真实网络
mongodb_link = pymongo.MongoClient(host='localhost', port=27017) #创建mogondb连接
db = mongodb_link.model #创建一个名为model的数据库
collection = db.facebook_model #在model数据库下创建一个名为facebook_model的集合，类似于关系型数据库中的表
data = pd.read_table(r'E:\project\kq\kq_cascade\network\Facebook_net.txt',sep = ',',skip_blank_lines = True)  #读取facebook真实网络的数据
rows = data.shape[0] #获取数据行数
my_list = [] #空列表
change_list = []
lists = [[]for i in range(rows)] #二维列表存储
my_data = { }
dict_G = { } #空字典用来存储数据
for i in range(rows):
    my_list.append(data.ix[i,0])
for i in range(len(my_list)):
    change_list.append(re.findall(r"\d+\.?\d*",my_list[i]))
for i in range(len(change_list)):
   del change_list[i][0]
for i in range(len(change_list)):
   del change_list[i][0]
for i in range(len(change_list)):
    for j in range(len(change_list[i])):
        if change_list[i][j] != "1.00":
           lists[i].append(change_list[i][j])
        else:
            continue
for i in range(len(lists)):
    my_data[i] = lists[i]
#将网络转换成字典
G = nx.from_dict_of_lists(my_data)
mydict = { } #空字典用来改变dict_G键的类型把数据存入mongodb
for key in my_data:
    mydict[str(key+1)] = my_data[key]
result = collection.insert_one(mydict) #插入mongodb数据库




