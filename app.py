#######################################################################################################
# Filename    : app.py
# Description : 1 . Main Flask application file
#               2. Initiates data model based on the input data files companies.json and people.json
#               3. Handles the different requests based on the customer requirements
# Developer   : Suresh Kumar
# Date        : 26th Feb 2019
#######################################################################################################
import os
import json
from datetime import datetime
from flask import Flask, jsonify, redirect, url_for, Blueprint, request
from flask_restplus import Api, Resource
from datamodel import Company, People


app = Flask(__name__)

companies=Company('companies.json')
people=People('people.json')
people.load_favourite_food_data('fruits_vegetables.json')

@app.route('/employees/<int:company_index>', methods = ['GET'])
def get_employees(company_index):
    """ Method to fetch all Employees data for a given company index.
        Considered 'index' value in companies.json as a value rather
        than the index in the list.
        The code here considers  index : 0 as value 0 but not as index 1.
        Since people.json doesn't have any company_id == 0 or
        index in companies.json doesn't have index == 100, these two values 0 and 100
        would return empty list.
        If expectation has to be index as in list, then we would need minor code change to
        up the index by 1.
        """
    try:
        if company_index < 0:
            raise ValueError

        employees_list = people.get_employee_data_for_company(company_index)

        response = {
            'status': 204 if  len(employees_list) is 0 else 200,
            'message': 'Request has been processed successfully',
            'content': employees_list
        }
        return jsonify(response)

    except Exception as excp_msg:
        return jsonify({'status': 500,
                        'message': 'Request Couldn\'t be processed',
                        'content': None
                        })


@app.route('/people/friends/<int:person1_index>/<int:person2_index>', methods = ['GET'])
def get_friends(person1_index, person2_index):
    """ Method to fetch given people info and the info of their common friends.
        Common friends who are still alive and having Brown eyes are to be retrieved
        Considered common friends list will exclude the given people here as input .
        for example, if person1 has friends - person1, person2 and person3 and
        if person2 has friends - person1, person2, person3 , then only person3 is considered
        for common friend """
    try:
        if person1_index < 0 or person2_index < 0:
            raise ValueError

        # retrieve person_info objects for given person indices
        person1_info = people.get_person_info_by_index(person1_index)
        person2_info = people.get_person_info_by_index(person2_index)

        # retrieving common friends list only if both the 2 persons have info in datamodel
        common_friends_list = []
        if person1_info is not None and person2_info is not None:
            common_friends_list = people.get_common_friends(person1_info,person2_info)

        # return given people info and their common friends info
        persons_info = []
        persons_info.append({'index': person1_index,
                             'info' : people.get_person_basic_info(person1_info) if person1_info is not None else None
                             })
        persons_info.append({'index': person2_index,
                             'info': people.get_person_basic_info(person2_info) if person1_info is not None else None
                             })

        response = {  'status': 200,
                    'message': 'Request has been processed successfully',
                    'content' : {
                                'personsInfo': persons_info,
                                'friendsInfo' : common_friends_list if len(common_friends_list) > 0 else None
                                }}
        return jsonify(response)

    except Exception as excp_msg:
        return jsonify({'status': 500,
                        'message': 'Request Couldn\'t be processed',
                        'content': None
                        })


@app.route('/people/fav_food/<int:person_index>', methods = ['GET'])
def get_favourite_food(person_index):
    """ Static data defined for classification of fruit and vegetable in file fruits_vegetables.json since
        there is no classification criteria/data provided to determine if food is fruit or vegetable.
        If any new fruit or vegetable outside the static data is present in 'favouriteFood', the
        assumption is that by default, it would be added as vegetable. Also the fact that almost all fruits
        can be used as vegetable until it ripes !!!!
    """
    try:
        if person_index < 0 :
            raise ValueError

        user_fav_food = people.get_person_favourite_food(person_index)
        response = {
            'status': 204 if len(user_fav_food) is 0 else 200,
            'message': 'Request has been processed successfully',
            'content': user_fav_food
        }
        #return the expected output as requested by customer.
        #ideally would be better to return response with status value,etc
        return jsonify(user_fav_food)

    except Exception as excp_msg:
        return jsonify({'status': 500,
                        'message': 'Request Couldn\'t be processed',
                        'content': None
                        })


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=False, port = 5000)
