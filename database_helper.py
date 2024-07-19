import json
import pymysql
from dotenv import load_dotenv
import os

load_dotenv()

def get_connection():
    return pymysql.connect(
        host=os.getenv("MySQL_server"),
        port=3306,
        user=os.getenv("MySQL_user"),
        passwd=os.getenv("MySQL_password"),
        database=os.getenv("MySQL_table_visitors"),
        cursorclass=pymysql.cursors.DictCursor
    )

def students():
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM students;')
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return {"type": "getStudents", "args": result}

def single_student(condition):
    connection = get_connection()
    cursor = connection.cursor()
    conditions = [f"{column} = %s" for column in condition.keys()]
    query = f'SELECT * FROM students WHERE {" AND ".join(conditions)};'
    cursor.execute(query, tuple(condition.values()))
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return {"type": "getSingleVisitor", "args": result, "condition": condition}

def insert_student(firstname, lastname, email, number_of_tickets, number_of_hard_cards=0, neighbour_wish=None,
                   meat=0, vegetarian=0, vegan=0, allergens=None, place_number=None, money=0, payed=0):
    connection = get_connection()
    cursor = connection.cursor()
    
    cursor.execute('SELECT * FROM students WHERE firstname = %s AND lastname = %s;', [firstname, lastname])
    if cursor.fetchone() is None:
        cursor.execute(
            'INSERT INTO students (firstname, lastname, email, number_of_tickets, number_of_hard_cards, '
            'neighbour_wish, meat, vegetarian, vegan, allergens, place_number, money, payed) '
            'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);',
            (firstname, lastname, email, number_of_tickets, number_of_hard_cards, neighbour_wish, meat,
             vegetarian, vegan, allergens, place_number, money, payed)
        )
        connection.commit()
        cursor.execute('SELECT * FROM students WHERE firstname = %s AND lastname = %s;', [firstname, lastname])
        result = cursor.fetchall()
        answer = {"type": "insert", "args": result}
    else:
        answer = {
            "type": "error", "caused": "insert", "errorMessage": "The person already exists!", 
            "args": {
                "firstname": firstname, "lastname": lastname, "email": email, "number_of_tickets": number_of_tickets,
                "number_of_hard_cards": number_of_hard_cards, "neighbour_wish": neighbour_wish, "meat": meat,
                "vegetarian": vegetarian, "vegan": vegan, "allergens": allergens, "place_number": place_number,
                "money": money, "payed": payed
            }
        }
    cursor.close()
    connection.close()
    return answer

def update_student(update_data, condition):
    connection = get_connection()
    cursor = connection.cursor()
    set_values = [f"{column} = %s" for column in update_data.keys()]
    conditions = [f"{column} = %s" for column in condition.keys()]
    args = list(update_data.values()) + list(condition.values())
    
    query = f"UPDATE students SET {', '.join(set_values)} WHERE {' AND '.join(conditions)};"
    cursor.execute(query, tuple(args))
    connection.commit()
    
    where_condition = []
    where_condition_args = []
    if 'firstname' in update_data:
        where_condition.append('firstname = %s')
        where_condition_args.append(update_data.get('firstname'))
    if 'lastname' in update_data:
        where_condition.append('lastname = %s')
        where_condition_args.append(update_data.get('lastname'))
        
    if where_condition:
        cursor.execute(f'SELECT * FROM students WHERE {" AND ".join(where_condition)};', tuple(where_condition_args))
    else:
        cursor.execute(f'SELECT * FROM students WHERE {" AND ".join(conditions)};', tuple(condition.values()))
    
    result = cursor.fetchall()
    cursor.close()
    connection.close()
    return {"type": "update", "args": result, "condition": condition}

def delete_student(condition):
    connection = get_connection()
    cursor = connection.cursor()
    conditions = [f"{column} = %s" for column in condition.keys()]
    query = f'DELETE FROM students WHERE {" AND ".join(conditions)};'
    
    cursor.execute(f'SELECT * FROM students WHERE {" AND ".join(conditions)};', tuple(condition.values()))
    result = cursor.fetchall()
    
    cursor.execute(query, tuple(condition.values()))
    connection.commit()
    
    cursor.close()
    connection.close()
    return {"type": "delete", "args": result}
