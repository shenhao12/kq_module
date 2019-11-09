import networkx as nx #引入复杂网络networkx模块
import pymongo #引入相关模块操控mongodb模块

def mongodb_link_er():
    '''
    函数功能:从mongodb中读取er模型数据
    '''
    mongodb_link = pymongo.MongoClient(host='localhost', port=27017) #创建mogondb连接
    db = mongodb_link['model'] #选择要操作的数据库
    collection = db.er_model #选择要操作的集合
    md_dict_G = collection.find_one() #查找存储在图中的数据
    #print(md_dict_G)
    md_dict_G.pop('_id')
    return md_dict_G #返回字典

def mongodb_link_exp():
    '''
    函数功能:从mongodb中读取exp模型数据
    '''
    mongodb_link = pymongo.MongoClient(host='localhost', port=27017) #创建mogondb连接
    db = mongodb_link['model'] #选择要操作的数据库
    collection = db.exp_model #选择要操作的集合
    md_dict_G = collection.find_one() #查找存储在图中的数据
    md_dict_G.pop('_id')
    return md_dict_G #返回字典

def mongodb_link_sf():
    '''
    函数功能:从mongodb中读取sf模型数据
    '''
    mongodb_link = pymongo.MongoClient(host='localhost', port=27017) #创建mogondb连接
    db = mongodb_link['model'] #选择要操作的数据库
    collection = db.sf_model #选择要操作的集合
    md_dict_G = collection.find_one() #查找存储在图中的数据
    md_dict_G.pop('_id')
    return md_dict_G #返回字典

def mongodb_link_facebook():
    '''
    函数功能:从mongodb中读取facebook模型数据
    '''
    mongodb_link = pymongo.MongoClient(host='localhost', port=27017) #创建mogondb连接
    db = mongodb_link['model'] #选择要操作的数据库
    collection = db.facebook_model #选择要操作的集合
    md_dict_G = collection.find_one() #查找存储在图中的数据
    md_dict_G.pop('_id')
    return md_dict_G #返回字典

def mongodb_link_epa():
    '''
    函数功能:从mongodb中读取epa模型数据
    '''
    mongodb_link = pymongo.MongoClient(host='localhost', port=27017) #创建mogondb连接
    db = mongodb_link['model'] #选择要操作的数据库
    collection = db.epa_model #选择要操作的集合
    md_dict_G = collection.find_one() #查找存储在图中的数据
    md_dict_G.pop('_id')
    return md_dict_G #返回字典

#单层网络模型

#ER随机网络
class ER_network_model:
    '''ER网络模型'''
    def __init__(self):
        self.md_dict_G = mongodb_link_er() #调用函数,打开mongodb链接
        #将字典的键改为int类型
        self.dict_G = { } #空字典用来改变类型
        self.k =0 
        for key in self.md_dict_G.keys(): #遍历字典
            self.dict_G[self.k] = self.md_dict_G[key]
            self.k += 1
        self.G = nx.from_dict_of_lists(self.dict_G)#从列表字典中返回图形G
        #degree = nx.degree_histogram(self.G)
        #print(degree)

#EXP随机网络
class EXP_network_model:
    '''EXP网络模型'''
    def __init__(self):
        self.md_dict_G = mongodb_link_exp() #调用函数,打开mongodb链接
        #将字典的键改为int类型
        self.dict_G = { } #空字典用来改变类型
        self.k =0 
        for key in self.md_dict_G.keys(): #遍历字典
            self.dict_G[self.k] = self.md_dict_G[key]
            self.k += 1
        self.G = nx.from_dict_of_lists(self.dict_G)#从列表字典中返回图形G
        #degree = nx.degree_histogram(self.G)
        #print(degree)

#SF随机网络
class SF_network_model:
    '''SF网络模型'''
    def __init__(self):
        self.md_dict_G = mongodb_link_sf() #调用函数,打开mongodb链接
        #将字典的键改为int类型
        self.dict_G = { } #空字典用来改变类型
        self.k =0 
        for key in self.md_dict_G.keys(): #遍历字典
            self.dict_G[self.k] = self.md_dict_G[key]
            self.k += 1
        self.G = nx.from_dict_of_lists(self.dict_G)#从列表字典中返回图形G
        #degree = nx.degree_histogram(self.G)
        #print(degree)

#facebook真实网络
class facebook_network_model:
    '''facebook网络模型'''
    def __init__(self):
        self.md_dict_G = mongodb_link_facebook() #调用函数,打开mongodb链接
        #将字典的键改为int类型
        self.dict_G = { } #空字典用来改变类型
        self.k =0 
        for key in self.md_dict_G.keys(): #遍历字典
            self.dict_G[self.k] = self.md_dict_G[key]
            self.k += 1
        self.G = nx.from_dict_of_lists(self.dict_G)#从列表字典中返回图形G
        #degree = nx.degree_histogram(self.G)
        #print(degree)

#epa真实网络
class epa_network_model:
    '''epa网络模型'''
    def __init__(self):
        self.md_dict_G = mongodb_link_epa() #调用函数,打开mongodb链接
        #将字典的键改为int类型
        self.dict_G = { } #空字典用来改变类型
        self.k =0 
        for key in self.md_dict_G.keys(): #遍历字典
            self.dict_G[self.k] = self.md_dict_G[key]
            self.k += 1
        self.G = nx.from_dict_of_lists(self.dict_G)#从列表字典中返回图形G
        #degree = nx.degree_histogram(self.G)
        #print(degree)
