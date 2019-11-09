import random #引入随机数模块
import function as fc #引入功能函数模块
import time #引入时间模块
import network_model as nm #引入网络模型模块
import pymysql #引入mysql数据库
import os #引入文件系统模块

#打开mysql数据库链接
db = pymysql.connect("localhost","root","root","kq_model" )
# 使用cursor()方法获取操作游标 
cursor = db.cursor()

#这个模块记录不同的攻击方式和实验方法
#记录一些全局变量
degree_dict = { }#degree_dict用来记录每个节点的初始度
remain_node_rate =1 #remain_node_rate代表剩余节点比例,初始值为1
start_time = fc.GetNowTime() #获取当前时间作为起始时间
crash_time = 0 #crash_time代表系统崩溃的时间
timestamp = time.time() #获取当前时间戳用于文件命名
my_model = 'er' #记录每次实验选择的模型
#实验一 从度数小的节点开始攻击
def experiment(ex_num):
    '''
    函数功能:从节点的度小于ks的节点开始攻击,即传统的k核模型，同时考虑q的影响
    node_num:代表初始网络的节点总数
    model:代表ER随机网络的类
    '''
    mkdir_name = str(timestamp) #创建的文件夹名
    paper_file = "E:\\project\\kq\\kq_cascade\\ex_data\\%s" %mkdir_name #文件夹创建路径
    os.makedirs(paper_file) #在ex_data文件夹下创建本次试验的文件夹
    for i in range(ex_num):
        step = 0 #步长代表横坐标，从0开始
        is_crash = 0 #is_crash记录是否发生崩溃，0代表未崩溃，1代表崩溃
        #每次实验选择实验中的模型,1代表er，2代表exp，3代表sf,4代表facebook真实网络,5代表epa真实网络
        model_select = int(input("please input the select of model:")) #选择实验中使用的模型
        if model_select == 1:
            model = nm.ER_network_model()
            my_model = "er"
        elif model_select == 2:
            model = nm.EXP_network_model()
            my_model = "exp"
        elif model_select == 3:
            model = nm.SF_network_model()
            my_model = "sf"
        elif model_select == 4:
            model = nm.facebook_network_model()
            my_model = "facebook"
        elif model_select == 5:
            model = nm.epa_network_model()
            my_model = "epa"
        initial_nodes = len(model.dict_G) #记录初始节点总度数
        len_dict = len(model.dict_G) #记录剩余节点个数，初始值为未攻击前总节点数
        k_max = fc.max_degree(model.dict_G) #当前网络所有节点中度的最大值
        k_min = fc.min_degree(model.dict_G) #当前网络所有节点中度的最小值
        for key in model.dict_G.keys():
            degree_dict[key] = len(model.dict_G[key])
        ex_select = int(input("please input the type of attack:")) #选择进行的实验,1代表传统kq模型,2代表从大节点开始攻击，3代表q与节点的初始度值成正比,4代表q与节点的初始度值成反比,5代表先删除10%的大节点
        if ex_select == 1:
            data_file = open(paper_file + "\\" + str(i) + ".txt",'a') #在ex_data文件夹下的本次试验的文件夹下创建记录实验数据的txt文件
            data_file.write('step_size,residual_node_ratio\n') #文件里写入抬头
            k = int(input("please input k:")) #输入每次实验的k值
            q = float(input("please input q:")) #输入每次实验的q值
            f = float(input("please input f:")) #输入每次实验的f值
            insert_sql = "insert into experimental_data(model,k,q,f,paper_file)values('%s',%f,%f,%f,'%s')"%(str(my_model),k,q,f,str(mkdir_name))
            #print(insert_sql)
            cursor.execute(insert_sql)
            er_threshold = initial_nodes*0.05 #er_threshold代表临界阈值，即损失超过原始节点的5%视为崩溃
            while step < 100000 :
                if len_dict < 100:
                    break
                step +=1 #步长每次加1
                if step % 5 == 0:
                        data_file.write(str(step))
                        data_file.write(',')
                        data_file.write(str(len_dict / initial_nodes))
                        data_file.write('\n')
                for key in list(model.dict_G.keys()): #遍历节点,item代表节点的键,由于遍历过程中不能修改字典元素，所以将字典转为列表后处理
                    if len_dict < int(er_threshold): #达到崩溃阈值时，认定崩溃
                        is_crash = 1
                        crash_time = fc.GetNowTime() #获取系统奔溃时的时间
                    if len(model.dict_G[key]) <= k or (degree_dict[key] - len(model.dict_G[key])) / degree_dict[key] > q: #满足条件k<=ks或者损失邻居节点比例超过q
                        probability = random.random() #取一个0-1之间的随机数
                        if probability < f: #按照概率f删除节点
                            model.dict_G = fc.del_node(model.dict_G,key) #删除k<ks的节点和其所连接的边
                            del degree_dict[key] #删除存储初始度节点的字典中的相关项
                            len_dict = len(model.dict_G) #更新剩余节点个数
                            remain_node_rate = len_dict / initial_nodes #计算剩余节点比例
                        else:
                            continue
                else:
                    continue
        elif ex_select == 2:
             data_file = open(paper_file + "\\" + str(i) + ".txt",'a') #在ex_data文件夹下的本次试验的文件夹下创建记录实验数据的txt文件
             data_file.write('step_size,residual_node_ratio\n') #文件里写入抬头
             k = int(input("please input k:")) #输入每次实验的k值
             q = float(input("please input q:")) #输入每次实验的q值
             f = float(input("please input f:")) #输入每次实验的f值
             insert_sql = "insert into experimental_data(model,k,q,f)values('%s',%f,%f,%f)"%(str(my_model),k,q,f)
             #print(insert_sql)
             cursor.execute(insert_sql)
             er_threshold = initial_nodes*0.05 #er_threshold代表临界阈值，即损失超过原始节点的5%视为崩溃
             while step < 100000 :
                if len_dict < 100:
                    break
                step +=1 #步长每次加1
                if step % 1 == 0:
                        data_file.write(str(step))
                        data_file.write(',')
                        data_file.write(str(len_dict / initial_nodes))
                        data_file.write('\n')
                for key in list(model.dict_G.keys()): #遍历节点,item代表节点的键,由于遍历过程中不能修改字典元素，所以将字典转为列表后处理
                    if len_dict < int(er_threshold): #达到崩溃阈值时，认定崩溃
                        is_crash = 1
                        crash_time = fc.GetNowTime() #获取系统奔溃时的时间
                    if len(model.dict_G[key]) > k or (degree_dict[key] - len(model.dict_G[key])) / degree_dict[key] > q: #满足条件k>ks或者损失邻居节点比例超过q
                        probability = random.random() #取一个0-1之间的随机数
                        if probability < f: #按照概率f删除节点
                            model.dict_G = fc.del_node(model.dict_G,key) #删除k>ks的节点和其所连接的边
                            del degree_dict[key] #删除存储初始度节点的字典中的相关项
                            len_dict = len(model.dict_G) #更新剩余节点个数
                            remain_node_rate = len_dict / initial_nodes #计算剩余节点比例
                        else:
                            continue
                else:
                    continue
        elif ex_select == 3:
            data_file = open(paper_file + "\\" + str(i) + ".txt",'a') #在ex_data文件夹下的本次试验的文件夹下创建记录实验数据的txt文件
            data_file.write('step_size,residual_node_ratio\n') #文件里写入抬头
            while step < 100000 :
                if len_dict < 100:
                    break
                step +=1 #步长每次加1
                if step % 1 == 0:
                        data_file.write(str(step))
                        data_file.write(',')
                        data_file.write(str(len_dict / 10000))
                        data_file.write('\n')
                for key in list(model.dict_G.keys()): #遍历节点,item代表节点的键,由于遍历过程中不能修改字典元素，所以将字典转为列表后处理
                    k_now = len(model.dict_G[key]) #k_now代表当前节点的度数
                    var_q = (k_now-k_min)/(k_max-k_min) #变量q的公式
                    if len_dict < int(er_threshold): #达到崩溃阈值时，认定崩溃
                        is_crash = 1
                        crash_time = fc.GetNowTime() #获取系统奔溃时的时间
                    if len(model.dict_G[key]) > k or (degree_dict[key] - len(model.dict_G[key])) / degree_dict[key] > var_q: #满足条件k>ks或者损失邻居节点比例超过var_q
                        probability = random.random() #取一个0-1之间的随机数
                        if probability < f: #按照概率f删除节点
                            model.dict_G = fc.del_node(model.dict_G,key) #删除k>ks的节点和其所连接的边
                            del degree_dict[key] #删除存储初始度节点的字典中的相关项
                            len_dict = len(model.dict_G) #更新剩余节点个数
                            remain_node_rate = len_dict / 10000 #计算剩余节点比例
                        else:
                            continue
                else:
                    continue
        elif ex_select == 4:
             data_file = open(paper_file + "\\" + str(i) + ".txt",'a') #在ex_data文件夹下的本次试验的文件夹下创建记录实验数据的txt文件
             data_file.write('step_size,residual_node_ratio\n') #文件里写入抬头
             while step < 100000 :
                if len_dict < 100:
                    break
                step +=1 #步长每次加1
                if step % 1 == 0:
                        data_file.write(str(step))
                        data_file.write(',')
                        data_file.write(str(len_dict / 10000))
                        data_file.write('\n')
                for key in list(model.dict_G.keys()): #遍历节点,item代表节点的键,由于遍历过程中不能修改字典元素，所以将字典转为列表后处理
                    k_now = len(model.dict_G[key]) #k_now代表当前节点的度数
                    var_q = (k_max-k_now)/(k_max-k_min) #变量q的公式
                    if len_dict < int(er_threshold): #达到崩溃阈值时，认定崩溃
                        is_crash = 1
                        crash_time = fc.GetNowTime() #获取系统奔溃时的时间
                    if len(model.dict_G[key]) > k or (degree_dict[key] - len(model.dict_G[key])) / degree_dict[key] > var_q: #满足条件k>ks或者损失邻居节点比例超过var_q
                        probability = random.random() #取一个0-1之间的随机数
                        if probability < f: #按照概率f删除节点
                            model.dict_G = fc.del_node(model.dict_G,key) #删除k>ks的节点和其所连接的边
                            del degree_dict[key] #删除存储初始度节点的字典中的相关项
                            len_dict = len(model.dict_G) #更新剩余节点个数
                            remain_node_rate = len_dict / 10000 #计算剩余节点比例
                        else:
                            continue
                else:
                    continue
        elif ex_select == 5:
            data_file = open(paper_file + "\\" + str(i) + ".txt",'a') #在ex_data文件夹下的本次试验的文件夹下创建记录实验数据的txt文件
            data_file.write('step_size,residual_node_ratio\n') #文件里写入抬头
            k = int(input("please input k:")) #输入每次实验的k值
            q = float(input("please input q:")) #输入每次实验的q值
            f = float(input("please input f:")) #输入每次实验的f值
            insert_sql = "insert into experimental_data(model,k,q,f,paper_file)values('%s',%f,%f,%f,'%s')"%(str(my_model),k,q,f,str(mkdir_name))
            #print(insert_sql)
            cursor.execute(insert_sql)
            er_threshold = initial_nodes*0.05 #er_threshold代表临界阈值，即损失超过原始节点的5%视为崩溃
            fc.max_delete(model.dict_G) #调用函数删除1%的最大节点
            while step < 100000 :
                if len_dict < 100:
                    break
                step +=1 #步长每次加1
                if step % 5 == 0:
                        data_file.write(str(step))
                        data_file.write(',')
                        data_file.write(str(len_dict / initial_nodes))
                        data_file.write('\n')
                for key in list(model.dict_G.keys()): #遍历节点,item代表节点的键,由于遍历过程中不能修改字典元素，所以将字典转为列表后处理
                    if len_dict < int(er_threshold): #达到崩溃阈值时，认定崩溃
                        is_crash = 1
                        crash_time = fc.GetNowTime() #获取系统奔溃时的时间
                    if len(model.dict_G[key]) <= k or (degree_dict[key] - len(model.dict_G[key])) / degree_dict[key] > q: #满足条件k<=ks或者损失邻居节点比例超过q
                        probability = random.random() #取一个0-1之间的随机数
                        if probability < f: #按照概率f删除节点
                            model.dict_G = fc.del_node(model.dict_G,key) #删除k<ks的节点和其所连接的边
                            del degree_dict[key] #删除存储初始度节点的字典中的相关项
                            len_dict = len(model.dict_G) #更新剩余节点个数
                            remain_node_rate = len_dict / initial_nodes #计算剩余节点比例
                        else:
                            continue
                else:
                    continue

        data_file.close() #关闭记录实验数据的文件
        end_time = fc.GetNowTime() #获取实验结束的时间
  
