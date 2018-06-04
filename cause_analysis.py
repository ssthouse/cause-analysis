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
        self.level2_feature = {
            'category_1': [],
            'province': [],
            'department_1': [],
            'owner-pop': [],
            'category_2': [],
            'channel_1': [],
            'channel_2': [],
            'city': []}
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
        return True

    def isSameLevel1(self, level1_bean):
        for key, value in self.features.items():
            # 只比较level有的属性
            if not value:
                continue
            if level1_bean.features[key] == value:
                return True
            else:
                return False

    def isConfictLevel1(self, level1_bean):
        # 判断两个level1 的feature2 可不可以融合
        for key, value in self.level2_feature.items():
            if bool(value) is False or bool(level1_bean.level2_feature[key]) is False:
                continue
            # 当两个level的feature的value都有值时 , 判断是不是包含关系
            if set(value) >= set(level1_bean.level2_feature[key]) or set(value) <= set(level1_bean.level2_feature[key]):
                return False
            else:
                return True

    def add_child(self, level2_bean):
        if self.verify_level2(level2_bean):
            self.children.append(level2_bean)
        return

    def fusion(self):
        for level2_bean in self.children:
            for key, value in level2_bean.features.items():
                if level2_bean.features[key] and level2_bean.features[key] not in self.level2_feature[key]:
                    self.level2_feature[key].append(level2_bean.features[key])

    def print_result(self):
        print (self.features)
        print (self.level2_feature)


class Level2(object):
    def __init__(self):
        self.features = {
            'category_1': '',
            'province': '',
            'department_1': '',
            'owner-pop': '',
            'category_2': '',
            'channel_1': '',
            'channel_2': '',
            'city': ''}

    def add_features(self, feature_name, feature_value):
        self.features[feature_name] = feature_value


class TimeSlot(object):
    def __init__(self):
        self.level1_list = []

    def add_child(self, new_level1_bean):
        if len(self.level1_list) == 0:
            self.level1_list.append(new_level1_bean)
            return

        # 判断同样level1是否已经存在
        for level1 in self.level1_list:
            # 如果是一样的
            if level1.isSameLevel1(new_level1_bean):
                return

        isMerged = False
        for level1_bean in self.level1_list:
            if level1_bean.isConfictLevel1(new_level1_bean):
                continue
            else:
                # merge
                self.merge_level1(level1_bean, new_level1_bean)

        # 如果和每一个之前的level1_bean都没有merge(也就是都冲突), 放到list最后
        if isMerged:
            return
        else:
            self.level1_list.append(new_level1_bean)

    def print_result(self):
        print('timeSlot result begin: ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        for level1_bean in self.level1_list:
            print(level1_bean.features)
            print(level1_bean.level2_feature)
            print('------')
        print('timeSlot result end: ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')

    @staticmethod
    def merge_level1(old_level1_bean, new_level1_bean):
        for key, value in old_level1_bean.level2_feature.items():
            old_level1_bean.level2_feature[key] = [x for x in
                                                   iter(set(value) | set(new_level1_bean.level2_feature[key]))]


# construct drill_filter_1
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


# another test case
# level one
drill_filter_5 = Level1()
drill_filter_5.add_features('category_1', '1319')

drill_filter_6 = Level1()
drill_filter_6.add_features('department_1', '1727')

drill_filter_7 = Level1()
drill_filter_7.add_features('owner-pop', 'OWNER')

drill_filter_8 = Level1()
drill_filter_8.add_features('province', '5')

# level two
drill_filter_9 = Level2()
drill_filter_9.add_features('category_2', '1523')
drill_filter_9.add_features('category_1', '1319')

drill_filter_10 = Level2()
drill_filter_10.add_features('department_1', '1727')
drill_filter_10.add_features('category_1', '1319')

drill_filter_11 = Level2()
drill_filter_11.add_features('owner-pop', 'OWNER')
drill_filter_11.add_features('category_1', '1319')

drill_filter_12 = Level2()
drill_filter_12.add_features('department_1', '1727')
drill_filter_12.add_features('owner-pop', 'OWNER')

drill_filter_13 = Level2()
drill_filter_13.add_features('province', '5')
drill_filter_13.add_features('category_1', '1319')

drill_filter_14 = Level2()
drill_filter_14.add_features('province', '5')
drill_filter_14.add_features('department_1', '1727')

drill_filter_15 = Level2()
drill_filter_15.add_features('province', '5')
drill_filter_15.add_features('owner-pop', 'OWNER')

# classify the alters which have the same features
# level_2_filters = [drill_filter_2, drill_filter_3, drill_filter_4]
#
# for filters in level_2_filters:
#     drill_filter_1.add_child(filters)
# drill_filter_1.fusion()
# drill_filter_1.print_result()

#
level_1_filters = [drill_filter_5, drill_filter_6, drill_filter_7, drill_filter_8]
level_2_filters = [drill_filter_9, drill_filter_10, drill_filter_11,
                   drill_filter_12, drill_filter_13, drill_filter_14, drill_filter_15]
for level_1_filter in level_1_filters:
    for filters in level_2_filters:
        level_1_filter.add_child(filters)
    level_1_filter.fusion()
    level_1_filter.print_result()

timeSlot = TimeSlot()
for level1 in level_1_filters:
    timeSlot.add_child(level1)
timeSlot.print_result()
