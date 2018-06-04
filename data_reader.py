import pandas as pd
from . import cause_analysis_lxy as analyzer

csv_data = pd.read_csv('0531_real-time_tags.csv')
# print(csv_data[csv_data.time_slot == 0])

test_data = csv_data[
    csv_data['platform'] == 'app' and csv_data['index_key'] == 'effect_price' and csv_data['time_slot'] == 50]

level1_df = test_data[csv_data['drill_level'] == 1]
level2_df = test_data[csv_data['drill_level'] == 2]

level1_bean_list = []
for index, row in level1_df.iterrows():
    temp_level1 = analyzer.Level1()
    print(row['drill_filters'])
    temp_level1.add_features()
    level1_bean_list.append()