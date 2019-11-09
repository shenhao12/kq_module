import random #引入随机数模块
import function as fc #引入功能函数模块
import time #引入时间模块
#这个模块实现不同顺序的攻击，一是传统的k-shell分解，从度数小的节点开始攻击，二是从度数大的节点开始攻击，三是先从度数小的节点开始攻击，然后交替攻击
#记录一些全局变量
degree_dict = { }#degree_dict用来记录每个节点的初始度
is_crash = 0 #is_crash记录是否发生崩溃，0代表未崩溃，1代表崩溃
remain_node_rate =1 #remain_node_rate代表剩余节点比例,初始值为1
start_time = fc.GetNowTime() #获取当前时间作为起始时间
crash_time = 0 #crash_time代表系统崩溃的时间
timestamp = time.time() #获取当前时间戳用于文件命名
#实验一 从度数小的节点开始攻击
def experiment_one(node_num,model):
    '''
    函数功能:从节点的度小于ks的节点开始攻击,即传统的k核模型，同时考虑q的影响
    node_num:代表初始网络的节点总数
    model:代表ER随机网络的类
    '''
    step = 0 #步长代表横坐标，从0开始
    step_threshold = 1000000 #设定实验总步长的阈值,达到阈值停止迭代
    len_dict = len(model.dict_G) #记录剩余节点个数，初始值为未攻击前总节点数
    min_node_degree = fc.min_degree(model.dict_G) #将随机网络的字典传入函数，获得度最小节点的度,min_node_degree表示度数最小的节点的度
    for key in model.dict_G.keys():
        degree_dict[key] = len(model.dict_G[key])
    data_file = open("ex_data1/datafile"+ str(timestamp) +".txt",'a') #在ex_data1文件夹下创建记录实验数据的txt文件
    data_file.write('step_size,residual_node_ratio\n')
    while step < step_threshold: #小于一定步数进行迭代
        for key in list(model.dict_G.keys()): #遍历节点,item代表节点的键,由于遍历过程中不能修改字典元素，所以将字典转为列表后处理
            if min_node_degree <= model.er_ks or (degree_dict[key]-len(model.dict_G[key]))/degree_dict[key] > model.er_q: #满足条件k<=ks或者损失邻居节点比例超过q
                if step % 2000 == 0:
                    data_file.write(str(step))
                    data_file.write(',')
                    data_file.write(str(len_dict/node_num))
                    data_file.write('\n')
                if len(model.dict_G[key]) == min_node_degree: #如果满足k<=ks，从度数最小的节点开始删除
                    probability = random.random() #取一个0-1之间的随机数
                    if probability < model.er_f: #按照概率f删除节点
                        model.dict_G = fc.del_node(model.dict_G,key) #删除k<ks的节点和其所连接的边
                        del degree_dict[key] #删除存储初始度节点的字典中的相关项
                        step +=1 #步长每次加1
                    else:
                        continue
                else:
                    continue
            else:
                break
        len_dict = len(model.dict_G) #更新剩余节点个数
        min_node_degree = fc.min_degree(model.dict_G) #更新度数最小的节点的度
        remain_node_rate = len_dict/node_num #计算剩余节点比例
        if len_dict < int(model.er_threshold): #达到崩溃阈值时，认定崩溃
            is_crash = 1
            crash_time = fc.GetNowTime() #获取系统奔溃时的时间
        if len_dict < int(model.er_threshold)*0.1: #剩余节点数过少时，跳出循环
            break
    end_time = fc.GetNowTime() #获取实验结束时的时间
    data_file.close() #关闭记录实验数据的文件

#实验二 从度数大的节点开始攻击
def experiment_two(node_num,model):
    '''
    函数功能:从节点的度大于ks的节点开始攻击,同时考虑q的影响
    node_num:代表初始网络的节点总数
    model:代表ER随机网络的类
    '''
    step = 0 #步长代表横坐标，从0开始
    len_dict = len(model.dict_G) #记录剩余节点个数，初始值为未攻击前总节点数
    max_node_degree = fc.max_degree(model.dict_G) #将随机网络的字典传入函数，获得度最大节点的度,max_node_degree表示度数最大的节点的度
    degree_dict = { }#degree_dict用来记录每个节点的初始度
    for key in model.dict_G.keys():
        degree_dict[key] = len(model.dict_G[key])
    remain_node_rate =1 #remain_node_rate代表剩余节点比例,初始值为1
    is_crash = 0 #is_crash记录是否发生崩溃，0代表未崩溃，1代表崩溃
    start_time = fc.GetNowTime() #获取当前时间作为起始时间
    crash_time = 0 #crash_time代表系统崩溃的时间
    data_file = open("ex_data2/datafile"+ str(timestamp) +".txt",'a') #在ex_data2文件夹下创建记录实验数据的txt文件
    data_file.write('step_size,residual_node_ratio\n')
    while step < 1000000: #小于一定步数进行迭代
        for key in list(model.dict_G.keys()): #遍历节点,item代表节点的键,由于遍历过程中不能修改字典元素，所以将字典转为列表后处理
            if max_node_degree > model.er_ks or (degree_dict[key]-len(model.dict_G[key]))/degree_dict[key] > model.er_q: #满足条件k>ks或者损失邻居节点比例超过q
                step +=1 #步长每次加1
                if step % 20000 ==0:
                    data_file.write(str(step))
                    data_file.write(',')
                    data_file.write(str(len_dict/node_num))
                    data_file.write('\n')
                if len(model.dict_G[key]) == max_node_degree: #如果满足k>ks，从度数最大的节点开始删除
                    probability = random.random() #取一个0-1之间的随机数
                    if probability < model.er_f: #按照概率f删除节点
                        model.dict_G = fc.del_node(model.dict_G,key) #删除k>ks的节点和其所连接的边
                        del degree_dict[key] #删除存储初始度节点的字典中的相关项
                    else:
                        continue
                else:
                    continue
            else:
                break
        len_dict = len(model.dict_G) #更新剩余节点个数
        max_node_degree = fc.max_degree(model.dict_G) #更新度数最大的节点的度
        remain_node_rate = len_dict/node_num #计算剩余节点比例
        if len_dict < int(model.er_threshold): #达到崩溃阈值时，认定崩溃
            is_crash = 1
            crash_time = fc.GetNowTime() #获取系统奔溃时的时间
        if len_dict < int(model.er_threshold)*0.1: #剩余节点数过少时，跳出循环
            break
    end_time = fc.GetNowTime() #获取实验结束时的时间
    data_file.close() #关闭记录实验数据的文件

#实验三 从度数小的节点开始，交替攻击
def experiment_three(node_num,model):
    '''
    函数功能:从节点的度最小的节点开始攻击,然后交替攻击,同时考虑q的影响
    node_num:代表初始网络的节点总数
    model:代表ER随机网络的类
    '''
    step = 0 #步长代表横坐标，从0开始
    len_dict = len(model.dict_G) #记录剩余节点个数，初始值为未攻击前总节点数
    min_node_degree = fc.min_degree(model.dict_G) #将随机网络的字典传入函数，获得度最小节点的度,min_node_degree表示度数最小的节点的度
    max_node_degree = fc.max_degree(model.dict_G) #将随机网络的字典传入函数，获得度最大节点的度,max_node_degree表示度数最大的节点的度
    degree_dict = { }#degree_dict用来记录每个节点的初始度
    for key in model.dict_G.keys():
        degree_dict[key] = len(model.dict_G[key])
    remain_node_rate =1 #remain_node_rate代表剩余节点比例,初始值为1
    is_crash = 0 #is_crash记录是否发生崩溃，0代表未崩溃，1代表崩溃
    start_time = fc.GetNowTime() #获取当前时间作为起始时间
    crash_time = 0 #crash_time代表系统崩溃的时间
    data_file = open("ex_data3/datafile"+ str(timestamp) +".txt",'a') #在ex_data2文件夹下创建记录实验数据的txt文件
    data_file.write('step_size,residual_node_ratio\n')
    while step < 1000000: #小于一定步数进行迭代
        for key in list(model.dict_G.keys()): #遍历节点,item代表节点的键,由于遍历过程中不能修改字典元素，所以将字典转为列表后处理
            if step % 2 == 0:
                if min_node_degree <= model.er_ks or (degree_dict[key]-len(model.dict_G[key]))/degree_dict[key] > model.er_q: #满足条件k<ks或者损失邻居节点比例超过q
                    step +=1 #步长每次加1
                    if step % 20000 ==0:
                        data_file.write(str(step))
                        data_file.write(',')
                        data_file.write(str(len_dict/node_num))
                        data_file.write('\n')
                    if len(model.dict_G[key]) == min_node_degree: #如果满足k<ks，从度数最小的节点开始删除
                        probability = random.random() #取一个0-1之间的随机数
                        if probability < model.er_f: #按照概率f删除节点
                            model.dict_G = fc.del_node(model.dict_G,key) #删除k>ks的节点和其所连接的边
                            del degree_dict[key] #删除存储初始度节点的字典中的相关项
                        else:
                            continue
                    else:
                        continue
                else:
                    break
            else:
                if max_node_degree > model.er_ks or (degree_dict[key]-len(model.dict_G[key]))/degree_dict[key] > model.er_q: #满足条件k>ks或者损失邻居节点比例超过q
                    step +=1 #步长每次加1
                    if step % 20000 ==0:
                        data_file.write(str(step))
                        data_file.write(',')
                        data_file.write(str(len_dict/node_num))
                        data_file.write('\n')
                    if len(model.dict_G[key]) == max_node_degree: #如果满足k>ks，从度数最大的节点开始删除
                        probability = random.random() #取一个0-1之间的随机数
                        if probability < model.er_f: #按照概率f删除节点
                            model.dict_G = fc.del_node(model.dict_G,key) #删除k>ks的节点和其所连接的边
                            del degree_dict[key] #删除存储初始度节点的字典中的相关项
                        else:
                            continue
                    else:
                        continue
                else:
                    break
        len_dict = len(model.dict_G) #更新剩余节点个数
        min_node_degree = fc.min_degree(model.dict_G) #更新度数最小的节点的度
        max_node_degree = fc.max_degree(model.dict_G) #更新度数最大的节点的度
        remain_node_rate = len_dict/node_num #计算剩余节点比例
        if len_dict < int(model.er_threshold): #达到崩溃阈值时，认定崩溃
            is_crash = 1
            crash_time = fc.GetNowTime() #获取系统奔溃时的时间
        if len_dict < int(model.er_threshold)*0.1: #剩余节点数过少时，跳出循环
            break
    end_time = fc.GetNowTime() #获取实验结束时的时间
    data_file.close() #关闭记录实验数据的文件

#实验四 q随着实验减小
def experiment_four(node_num,model):
    '''
    函数功能:q随时间减小的情况下观察实验结果
    node_num:代表初始网络的节点总数
    model:代表ER随机网络的类
    '''
    step = 0 #步长代表横坐标，从0开始
    len_dict = len(model.dict_G) #记录剩余节点个数，初始值为未攻击前总节点数
    min_node_degree = fc.min_degree(model.dict_G) #将随机网络的字典传入函数，获得度最小节点的度,min_node_degree表示度数最小的节点的度
    degree_dict = { }#degree_dict用来记录每个节点的初始度
    for key in model.dict_G.keys():
        degree_dict[key] = len(model.dict_G[key])
    remain_node_rate =1 #remain_node_rate代表剩余节点比例,初始值为1
    is_crash = 0 #is_crash记录是否发生崩溃，0代表未崩溃，1代表崩溃
    start_time = fc.GetNowTime() #获取当前时间作为起始时间
    crash_time = 0 #crash_time代表系统崩溃的时间
    data_file = open("ex_data4/datafile"+ str(timestamp) +".txt",'a') #在ex_data1文件夹下创建记录实验数据的txt文件
    data_file.write('step_size,residual_node_ratio\n')
    while step < 1000000: #小于一定步数进行迭代
        for key in list(model.dict_G.keys()): #遍历节点,item代表节点的键,由于遍历过程中不能修改字典元素，所以将字典转为列表后处理
            if min_node_degree <= model.er_ks or (degree_dict[key]-len(model.dict_G[key]))/degree_dict[key] > model.er_q: #满足条件k<=ks或者损失邻居节点比例超过q
                step +=1 #步长每次加1
                if step % 20000 ==0:
                    model.er_q -= 0.01
                    data_file.write(str(step))
                    data_file.write(',')
                    data_file.write(str(len_dict/node_num))
                    data_file.write('\n')
                if len(model.dict_G[key]) == min_node_degree: #如果满足k<=ks，从度数最小的节点开始删除
                    probability = random.random() #取一个0-1之间的随机数
                    if probability < model.er_f: #按照概率f删除节点
                        model.dict_G = fc.del_node(model.dict_G,key) #删除k<ks的节点和其所连接的边
                        del degree_dict[key] #删除存储初始度节点的字典中的相关项
                    else:
                        continue
                else:
                    continue
            else:
                break
        len_dict = len(model.dict_G) #更新剩余节点个数
        min_node_degree = fc.min_degree(model.dict_G) #更新度数最小的节点的度
        remain_node_rate = len_dict/node_num #计算剩余节点比例
        if len_dict < int(model.er_threshold): #达到崩溃阈值时，认定崩溃
            is_crash = 1
            crash_time = fc.GetNowTime() #获取系统奔溃时的时间
        if len_dict < int(model.er_threshold)*0.1: #剩余节点数过少时，跳出循环
            break
    end_time = fc.GetNowTime() #获取实验结束时的时间
    data_file.close() #关闭记录实验数据的文件
  

