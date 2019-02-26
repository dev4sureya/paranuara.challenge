#######################################################################################################
# Filename    : datamodel.py
# Description : Load all data models for given json data files
# Developer   : Suresh Kumar
# Date        : 26th Feb 2019
#######################################################################################################

import json

class Company(object):
    def __init__(self,data_source):
        with open(data_source, 'r') as fp:
            self.company_list = json.load(fp)

    def get_company_id(self,company_name):
        return next((elem for elem in self.company_list if elem['company'] == company_name), None)


class People(object):
    def __init__(self,data_source):
        with open(data_source, 'r') as fp:
            self.people_list = json.load(fp)

    def load_favourite_food_data(self, data_source):
        with open(data_source, 'r') as fp:
            self.fav_food_list = json.load(fp)

    def get_employee_data_for_company(self, company_id):
        return [elem for elem in self.people_list if elem['company_id'] == company_id ]

    def get_person_info(self, person_name):
        return next((elem for elem in self.people_list if elem['name'] == person_name), None)

    def get_person_info_by_index(self,person_index):
        return next((elem for elem in self.people_list if elem['index'] == person_index), None)

    def get_common_friends(self,person1_info, person2_info):
        # Exclude self index of person1 and person2
        common_friends_ids = [friend for friend in person1_info['friends']
                                            if ( friend in person2_info['friends'] and
                                                        (friend.get('index') != person1_info['index'] and
                                                             friend.get('index') != person2_info['index']))]

        common_friends = [{'name':friend['name'],
                           'age': friend['age'],
                           'address':friend['address'],
                           'phone': friend['phone']} for friend_id in common_friends_ids for friend in self.people_list
                                                                        if friend['index'] == friend_id['index'] and
                                                                           friend['eyeColor'] == 'brown' and
                                                                           not friend['has_died']]
        return common_friends

    def get_person_basic_info(self,person_info):
        return {'name': person_info['name'],
                'age': person_info['age'],
                'address': person_info['address'],
                'phone': person_info['phone']}

    def get_person_favourite_food(self, person_index):
        person_info = self.get_person_info_by_index(person_index)
        if person_info is not None:
            fruits = []
            vegetables = []
            for food in person_info['favouriteFood']:
                elem = next((elem for elem in self.fav_food_list if elem['food'] == food), None)
                if elem is not None:
                    if elem['type'] == 'fruit':
                        fruits.append(elem['food'])
                    else:
                        vegetables.append(elem['food'])

            return ({'username': person_info['name'],
                     'age':person_info['age'],
                     'fruits': fruits,
                     'vegetables':vegetables})
        return None
