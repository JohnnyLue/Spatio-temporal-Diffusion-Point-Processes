import pandas as pd
import pickle
import argparse
import random

seed = 123
random.seed(seed)

argparser = argparse.ArgumentParser()
argparser.add_argument("time_interval")
args = argparser.parse_args()

# 設定檔案路徑
input_file = 'storms.csv' 

# 設定時間區間
time_interval_days = args.time_interval  # 3 週
time_interval = f'{time_interval_days}D'  # 轉為 pandas 的時間頻率格式

# 讀取 CSV 檔案
data = pd.read_csv(input_file)

# 將資料中的時間轉換為 pandas 的 datetime 物件
data['datetime'] = pd.to_datetime(
    dict(year=data['year'], month=data['month'], day=data['day'], hour=data['hour'])
)

# 按照時間區間分組（例如每3週）
data['time_group'] = data['datetime'].dt.floor(time_interval)

# 選取需要的欄位
filtered_data = data[['time_group', 'wind', 'long', 'lat']]

# 按時間區間整理資料，轉換為三層 list 結構
grouped_list = [
    sorted(group[['wind', 'long', 'lat']].values.tolist())
    for _, group in filtered_data.groupby('time_group')
]

# 隨機排序
random.shuffle(grouped_list)

test_val_len = int(len(grouped_list)*0.05)

test_data = []
for i in range(test_val_len):
    test_data.append(grouped_list.pop())

val_data = []
for i in range(test_val_len):
    val_data.append(grouped_list.pop())

# 儲存結果
f = open("Storms/data_train.pkl", "wb")
pickle.dump(grouped_list, f)
f = open("Storms/data_test.pkl", "wb")
pickle.dump(test_data, f)
f = open("Storms/data_val.pkl", "wb")
pickle.dump(val_data, f)

print(f"資料完成轉換，長度:訓練 {len(grouped_list)}, 測試 {len(test_data)}, 驗證 {len(val_data)}")

