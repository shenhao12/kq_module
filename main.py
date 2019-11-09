import network_model as nm #引入网络模型模块
import attack as ao #引入攻击模块
import pandas as pd #引入pandas模块用来读取数据
import matplotlib.pyplot as plt #引入绘图模块matplotlib
import pymysql #引入mysql数据库
import os #引入文件系统模块


#打开mysql数据库链接
db = pymysql.connect("localhost","root","root","kq_model" )
# 使用cursor()方法获取操作游标 
cursor = db.cursor()

#ER网络模型实验
experiment_num = int(input("please input the number of experiment:")) #控制实验次数
ao.experiment(experiment_num) #将参数传入实验进行攻击
pic_name = str(ao.timestamp) + ".png" #将时间戳用于图片命名
#读取txt文件中的实验数据
file_name = [] #定义一个空列表用来存储文件名
file_sql = "select paper_file from experimental_data order by id desc limit 1" #查询文件名的sql语句
cursor.execute(file_sql) #执行查找语句
ex_file = str(cursor.fetchone())# 获取一条记录，即文件夹的名字
ex_file = ex_file[2:-3]
ex_data = []
for i in range(experiment_num):
    now_file = str(i) + ".txt" #记录当前文件名称
    file_name.append(now_file) #将文件添加进列表
    data = pd.read_table(r'E:\project\kq\kq_cascade\ex_data\%s\%s'  %(ex_file,file_name[i]),sep = ',',skip_blank_lines = True)
    ex_data.append(data)

#从mysql数据库中读取数据
find_sql = "select * from experimental_data order by id desc limit %s" %experiment_num
cursor.execute(find_sql) #执行查找语句
results = cursor.fetchall()# 获取所有记录列表

my_model = []
my_k = []
my_q = []
my_f = []

for row in results:
    my_model.append(row[1])
    my_k.append(row[2])
    my_q.append(row[3])
    my_f.append(row[4])

#print(my_model)
#print(my_k)
#print(my_q)
#print(my_f)

#用matplotlib作图
for i in range(experiment_num):
    plt.plot(ex_data[i].step_size,
             ex_data[i].residual_node_ratio,
             linestyle = '-',
             marker = 'o',
             markersize = 6,
             label = "model=%s,k=%d,q=%f,f=%f"%(my_model[i],my_k[i],my_q[i],my_f[i]))
    #添加x轴标签
    plt.xlabel('step')
    #添加y轴标签
    plt.ylabel("remain_rate")

plt.legend()
#将数据图保存
plt.savefig('ex_picture\%s' %pic_name)

#显示图片
plt.show()




