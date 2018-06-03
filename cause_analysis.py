# -*- coding: utf-8 -*-
"""
Created on Fri Jun  1 11:08:24 2018

@author: liuxinying
"""


# index_key = effect_price
# platform = app
# drill_filter_1 = {"category_1":"13765"} level = 1
# drill_filter_2 = {"category_2":"13767","category_1":"13765"}
# drill_filter_3 = {"category_2":"5019","category_1":"1320"}
# drill_filter_4 = {"department_1":"1726","category_1":"13765"}

class Level1(object):
    def __init__(self, features={}, children=[]):
        self.features = {
            'category_1': '',
            'province': '',
            'department_1': '',  # bu_id
            'owner-pop': False,
            'channel_1': ''
        }
        self.children = children

    def add_features(self, feature_name, feature_value):
        self.features[feature_name] = feature_value

    def verify_level2(self, level2_bean):
        for key, value in self.features.items():
            # 只比较level有的属性
            if not value:
                continue

            # 如果level2 该属性为空, 直接通过
            if not level2_bean.features[key]:
                continue

            if level2_bean.features[key] == value:
                return True
            else:
                return False

    def add_child(self, level2_bean):
        if self.verify_level2(level2_bean):
            self.children.append(level2_bean)

    def fusion(self):
        # for i in range(len(self.children)):
        #     if self.verify_level2(self.children[i]):
        #         self.features['bu_id'] = self.children[i].features['bu_id']
        return

    def print_result(self):
        print (self.features)


class Level2(object):
    def __init__(self):
        self.features = {
            'category_1': '',
            'province': [],
            'department_1': '',
            'owner-pop': [],
            'category_2': [],
            'channel_1': '',
            'channel_2': '',
            'city': []}

    def add_features(self, feature_name, feature_value):
        self.features[feature_name] = feature_value


# constuct drill_filter_1        
drill_filter_1 = Level1()
drill_filter_1.add_features('category_1', '13765')
# drill_filter_1.print_alter()

# construct drill_filter_2  
drill_filter_2 = Level2()
drill_filter_2.add_features('category_2', '13767')
drill_filter_2.add_features('category_1', '13765')
# drill_filter_2.print_alter()


# construct drill_filter_3    
drill_filter_3 = Level2()
drill_filter_3.add_features('category_2', '5019')
drill_filter_3.add_features('category_1', '1320')
# drill_filter_3.print_alter()

# construct drill_filter_4    
drill_filter_4 = Level2()
drill_filter_4.add_features('category_1', '13765')
drill_filter_4.add_features('department_1', '1726')
# drill_filter_4.print_alter()

# classify the alters which have the same features
level_2_filters = [drill_filter_2, drill_filter_3, drill_filter_4]

for filters in level_2_filters:
    drill_filter_1.add_child(filters)
print(drill_filter_1.children)
