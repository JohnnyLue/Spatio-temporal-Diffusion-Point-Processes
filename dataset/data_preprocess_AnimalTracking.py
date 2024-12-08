import os
import random
import pandas as pd
import numpy as np
from pathlib import Path
from datetime import timedelta
from typing import List, Dict

import pickle

def save_to_pkl(data: List, file_name: str):

    with open(file_name, 'wb') as file:
        pickle.dump(data, file)
    print(f"Data saved to {file_name}")

def modified_zscore(df: pd.DataFrame):
    """
    Modified Z-score（確保正值）：
    公式：exp((x - mean) / std)
    範圍：全部大於0
    特點：保持相對關係且全為正值
    適用：需要正值的場景
    """
    mean_val = df['tag-local-identifier'].mean()
    std_val = df['tag-local-identifier'].std()
    df['tag-local-identifier'] = (df['tag-local-identifier'] - mean_val) / std_val
    df['tag-local-identifier'] = np.exp(df['tag-local-identifier'])
    
    return df

def convert_to_list(sequences):
    result = []
    for sequence in sequences:
        sequence_list = list()
        sequence_list.append(sequence['tag-local-identifier'])
        sequence_list.append(sequence['location-lat'])
        sequence_list.append(sequence['location-long'])
        result.append(sequence_list)
    return result

def group_by_7days(df: pd.DataFrame):

    df['timestamp'] = pd.to_datetime(df['timestamp'])

    df = df.sort_values('timestamp')

    df = modified_zscore(df)
    
    start_date: pd.Timestamp = df['timestamp'].min()
    end_date: pd.Timestamp  = df['timestamp'].max()

    all_sequences: List[List[List]] = list()

    current_start: pd.Timestamp  = start_date
    while current_start <= end_date:
        current_end: pd.Timestamp = current_start + timedelta(days=7)

        mask = (df['timestamp'] >= current_start) & (df['timestamp'] < current_end)
       
        df_7days = df[mask]
        df_7days = df_7days.sort_values('tag-local-identifier')

        sequence_data = df_7days.to_dict('records')
        
        sequence_data = convert_to_list(sequence_data)

        if sequence_data:
            if len(sequence_data)<300:
                all_sequences.append(sequence_data)

        current_start = current_end
    random.shuffle(all_sequences)
    return all_sequences
def split_data(sequences: List[List[List]], train_ratio: float = 0.7, val_ratio: float = 0.15):
    total = len(sequences)
    train_end = int(total * train_ratio)
    val_end = train_end + int(total * val_ratio)

    train_data = sequences[:train_end]
    val_data = sequences[train_end:val_end]
    test_data = sequences[val_end:]

    return train_data, val_data, test_data

if __name__ == '__main__':
    root_dir = Path(__file__).parent
    file_name = 'Animal-Tracking'
    file_path = os.path.join(root_dir, "AnimalTracking", file_name + ".csv")
    df = pd.read_csv(file_path, encoding='utf-8')
    df = df[['timestamp', 'location-long', 'location-lat', 'tag-local-identifier']]
    all_sequences = group_by_7days(df)
    train_data, val_data, test_data = split_data(all_sequences)

    # Save datasets to .pkl files
    output_dir = os.path.join(root_dir, "AnimalTracking")
    os.makedirs(output_dir, exist_ok=True)

    save_to_pkl(train_data, os.path.join(output_dir, 'data_train.pkl'))
    save_to_pkl(val_data, os.path.join(output_dir, 'data_val.pkl'))
    save_to_pkl(test_data, os.path.join(output_dir, 'data_test.pkl'))