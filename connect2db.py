import mysql.connector
from mysql.connector import Error
import json

def create_connection(host_name, user_name, user_password, db_name):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name
        )
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection

def execute_select_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")

def execute_select_query_fetchone(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchone()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")

def execute_update_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        connection.commit()
    except Error as e:
        print(f"The error '{e}' occurred")

# https://dotm.atu.kz/openserver/phpmyadmin/
# connection = create_connection("172.20.252.101", "root", "123456789",'laravel_messenger')
# connection = create_connection("37.228.66.93", "root", "Desant3205363",'laravel_messenger')


def send_to_db_contact(data):
    connection = create_connection("localhost", "root", "123456789",'laravel_messenger')

    sql = "UPDATE contacts_json SET " + data['messenger'] + "= '" + data['data']+"' WHERE id="+str(data['id'])
    execute_update_query(connection, sql)

def send_to_db_chat(data):
    connection = create_connection("localhost", "root", "123456789",'laravel_messenger')

    sql = "UPDATE send_links SET data= '" + data['data']+"' WHERE user_id="+str(data['id'])
    execute_update_query(connection, sql)

def get_link_db(id = 1):
    connection = create_connection("localhost", "root", "123456789",'laravel_messenger')

    sql = "select * from send_links where user_id = "+str(id)
    # sql = "select * from contacts_json"
    
    return execute_select_query_fetchone(connection, sql)


    
if __name__ == "__main__":
    ID = 1
    # chats_data = {
    #     "id" : 1,
    #     "func" : "contacts_json",
    #     "messenger" : "telegram",
    #     "data": '456',
    # }
    
    # response = send_to_db(chats_data)
    # print(response)
    # pass
    response = get_link_db(ID)
    # for x in response:
    #     print(x)
    print(response)
    if response[2]==None:
        
        data = {
            "id" : ID,
            # "func" : "chat_json",
            # "messenger" : "telegram",
            "data": json.dumps(123, ensure_ascii=False),
        }
        send_to_db_chat(data)
        # response = send_to_server.send_to_server(data)
    