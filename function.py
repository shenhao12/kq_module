import time #引入时间模块
import math #引入数学模块
import matplotlib.pyplot as plt #引入绘图模块matplotlib

def min_degree(dict):
    '''
    函数功能:寻找随机网络中度数最小的节点的度数
    dict:代表随机网络的字典，节点和边存储在里面
    '''
    new_list = [] #创建一个新列表用来接收每个节点的度
    min_degree = 0 #度最小的节点的度数默认设置为0
    for key in dict.keys():
        new_list.append(len(dict[key])) #将每个节点的度数存入新列表
        min_degree = min(new_list) #用min_degree来存储度最小的节点的度数
    return min_degree #返回度数最小的节点的度数

def max_degree(dict):
    '''
    函数功能:寻找随机网络中度数最大的节点的度数
    dict:代表随机网络的字典，节点和边存储在里面
    '''
    new_list = [] #创建一个新列表用来接收每个节点的度
    max_degree = 0 #度最大的节点的度数默认设置为0
    for key in dict.keys():
        new_list.append(len(dict[key])) #将每个节点的度数存入新列表
        max_degree = max(new_list) #用max_degree来存储度最大的节点的度数
    return max_degree #返回度数最大的节点的度数

def del_node(dict,current_key):
    '''
    函数功能:删除相关节点以及其所连的边
    dict:代表随机网络的字典，节点和边存储在里面
    current_key:代表当前传进来的节点的键值
    '''
    del dict[current_key] #先删除当前传来的节点和其所连接的边
    for key in dict.keys():
        if current_key in dict[key]:
            dict[key].remove(current_key) #删除节点后删除节点所连的边
    return dict #返回调整后的随机网络模型

def GetNowTime():
    '''
    函数功能:获取当前时间
    '''
    return time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))

def ER_sequence(node_num,average_degree,max_degree):
    '''
    函数功能:返回ER随机网络的度序列
    '''
    power = float(1)
    sum = float(0)
    e = 2.718282
    distribution = []#记录各个度值节点的个数
    degree_sequence = []#记录度序列
    sum_test = 0
    count = 0
    count_temp = 0 

    for i in range(node_num):
        degree_sequence.append(1)
    for i in range(max_degree):
        power = power * (i+1)
        sum = sum+pow(average_degree, i+1) * pow(e, -average_degree)/power * 100 #泊松分布公式
    amplify = node_num / sum
    #print(sum)
    #print(amplify)
    power = 1
    for i in range(max_degree):
        power = power * (i+1)
        distribution.append(int(pow(average_degree,i+1) * pow(e, -average_degree)/power * amplify * 100 + 0.5))
        #print(distribution[i])
        sum_test = sum_test + distribution[i]
    #print(sum_test)
    for i in range(max_degree):
        count = count_temp+count
        count_temp = 0
        for j in range(distribution[i]):
            degree_sequence[count+j] = i + 1#生成度序列
            count_temp = count_temp+1
    #for i in range(node_num):
    #    print(degree_sequence[i]) #打印测试度序列  
    return degree_sequence #返回度序列

def EXP_sequence(node_num,average_degree,max_degree):
    '''
    函数功能:返回EXP随机网络的度序列
    '''
    sum = float(0)
    e = 2.718282
    distribution = []#记录各个度值节点的个数
    degree_sequence = []#记录度序列
    sum_test = 0
    count = 0
    count_temp = 0 

    for i in range(node_num):
        degree_sequence.append(1)
    for i in range(max_degree):
        sum = sum + 1/average_degree * pow(e, -(i+1)/average_degree) * 100 #指数分布公式
    amplify = node_num / sum
    for i in range(max_degree):
        distribution.append(int(1/average_degree * pow(e, -(i+1)/average_degree) * amplify * 100 + 0.5))
        #print(distribution[i])
    for i in range(max_degree):
        count = count_temp+count
        count_temp = 0
        for j in range(distribution[i]):
            degree_sequence[count+j] = i + 1#生成度序列
            count_temp = count_temp+1
    #for i in range(node_num):
    #    print(degree_sequence[i]) #打印测试度序列  
    return degree_sequence #返回度序列

def SF_sequence(node_num,gamma,max_degree,min_degree):
    '''
    函数功能:返回SF随机网络的度序列
    '''
    sum = float(0)
    e = 2.718282
    distribution = []#记录各个度值节点的个数
    degree_sequence = []#记录度序列
    sum_test = 0
    count = 0
    count_temp = 0 

    for i in range(node_num):
        degree_sequence.append(1)
    for i in range(max_degree-min_degree):
        a = pow(i + min_degree, -gamma);
        sum = sum + pow(i + min_degree, -gamma) * 100 #幂率分布公式
    amplify = node_num / sum
    for i in range(max_degree-min_degree):
        distribution.append(int(amplify * pow(i + min_degree, -gamma) * 100 + 0.5))
        #print(distribution[i])
        sum_test = sum_test + distribution[i]
    for i in range(max_degree-min_degree):
        count = count_temp+count
        count_temp = 0
        for j in range(distribution[i]):
            degree_sequence[count+j] = i + min_degree#生成度序列
            count_temp = count_temp+1
    for i in range(node_num):
        if degree_sequence[i] == 1:
            degree_sequence[i] = 5
        #print(degree_sequence[i]) #打印测试度序列  
    return degree_sequence #返回度序列

def max_delete(dict):
    '''
    函数功能:删除1%度数最大的节点，返回修改后的字典
    '''
    remove_nodes = len(dict)*0.01 #当前网络的总结点数的1%用来删除
    for i in range(int(remove_nodes)):
        node_degree = max_degree(dict) #需要删除的节点的度数
        my_key = get_onenode(dict,node_degree) #找到需要删除的节点的键
        del_node(dict,my_key) #删除节点
        #print(len(dict))
    return dict #返回修改后的字典

def get_onenode(dict,degree):
    '''
    函数功能:根据度数找到一个节点的键
    '''
    now_key = 0 #默认需要删除的节点的键是0
    for key in dict.keys():
        if len(dict[key]) == degree:
            now_key = key
    return now_key #返回节点的键值


    