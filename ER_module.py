import networkx as nx #引入复杂网络networkx模块
import matplotlib.pyplot as plt #引入绘图模块matplotlib
import function as fc #引入功能函数模块
import pymongo #引入相关模块操控mongodb模块

#ER随机网络
mongodb_link = pymongo.MongoClient(host='localhost', port=27017) #创建mogondb连接
db = mongodb_link.model #创建一个名为model的数据库
collection = db.er_model #在model数据库下创建一个名为er_model的集合，类似于关系型数据库中的表
degree_sequence = fc.ER_sequence(10000,20,50) #获取度分布的列表
G = nx.configuration_model(degree_sequence) #将度分布转换成图
dict_G = nx.to_dict_of_lists(G) #图G的字典表示形式，存储在dict_G中，形式为{0: [2], 1: [2], 2: [0, 1]}
mydict = { } #空字典用来改变dict_G键的类型把数据存入mongodb
for key in dict_G:
    mydict[str(key)] = dict_G[key]
result = collection.insert_one(mydict) #插入mongodb数据库
#print(result)#打印测试
'''
#测试生成的图是否正确
degree = nx.degree_histogram(G)#返回图中所有节点的度分布序列
x = range(len(degree))#生成X轴序列，从1到最大度
y = [z/float(sum(degree))for z in degree]#将频次转化为频率，利用列表内涵
plt.plot(x,
         y,
         linestyle = '-')
plt.show()
'''

db.close() #关闭mongodb数据库连接
    