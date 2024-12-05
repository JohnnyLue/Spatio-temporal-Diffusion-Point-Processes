import pandas as pd
import pickle
import argparse
import random

seed = 123
random.seed(seed)

# 设定文件路径
input_file = 'atlantic_new.csv'

# 读取 CSV 文件
data = pd.read_csv(input_file)

# 将 Date 列转换为 datetime 格式
data['datetime'] = pd.to_datetime(data['Date'], format='%Y%m%d')  # 按 YYYYMMDD 格式解析日期

# 按时间分组：设定时间区间
time_interval_days = 21  # 例如按 3 周（21 天）分组
data['time_group'] = data['datetime'].dt.floor(f'{time_interval_days}D')

# 选择需要的列
filtered_data = data[['time_group', 'Maximum Wind', 'Longitude', 'Latitude']]

# 分组并生成三层列表
grouped_list = [
    sorted(group[['Maximum Wind', 'Longitude', 'Latitude']].values.tolist())
    for _, group in filtered_data.groupby('time_group')
]

# 随机化数据
random.shuffle(grouped_list)

# 分割训练、测试和验证集
test_val_len = int(len(grouped_list) * 0.05)
test_data = [grouped_list.pop() for _ in range(test_val_len)]
val_data = [grouped_list.pop() for _ in range(test_val_len)]

test = test_data
train = grouped_list
val = val_data
strip_list = ['N', 'E', 'S', 'W']

new_test = []
for i in range(len(test)):
    if test[i][0][0] < 0:
        continue
    new_time_group = []
    for m in range(len(test[i])):
        new_list = [test[i][m][0], ]
        new = test[i][m][1]
        for j in strip_list:
            new = new.strip(j)
        new_list.append(float(new))
        new = test[i][m][2]
        for j in strip_list:
            new = new.strip(j)
        new_list.append(float(new))
        new_time_group.append(new_list)
    new_test.append(new_time_group)
    
new_train = []
for i in range(len(train)):
    if train[i][0][0] < 0:
        continue
    new_time_group = []
    for m in range(len(train[i])):
        new_list = [train[i][m][0], ]
        new = train[i][m][1]
        for j in strip_list:
            new = new.strip(j)
        new_list.append(float(new))
        new = train[i][m][2]
        for j in strip_list:
            new = new.strip(j)
        new_list.append(float(new))
        new_time_group.append(new_list)
    new_train.append(new_time_group)
    
new_val = []
for i in range(len(val)):
    if val[i][0][0] < 0:
        continue
    new_time_group = []
    for m in range(len(val[i])):
        new_list = [val[i][m][0], ]
        new = val[i][m][1]
        for j in strip_list:
            new = new.strip(j)
        new_list.append(float(new))
        new = val[i][m][2]
        for j in strip_list:
            new = new.strip(j)
        new_list.append(float(new))
        new_time_group.append(new_list)
    new_val.append(new_time_group)
    
f = open("data_test.pkl", "wb")
pickle.dump(new_test, f)
f = open("data_train.pkl", "wb")
pickle.dump(new_train, f)
f = open("data_val.pkl", "wb")
pickle.dump(new_val, f)

print(f"数据转换完成：训练集 {len(new_train)}，测试集 {len(new_test)}，验证集 {len(new_val)}")
