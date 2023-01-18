from typing import List
from scripts.bot_types import ProductType
from scripts.bot_config import * 

import scripts.bot_items
import pymysql

connection = pymysql.connect(
        host=config_mysqlhost,
        user = config_mysquser,
        password=config_mysqpassword,
        database=config_databaseName,
        cursorclass=pymysql.cursors.DictCursor
    )

cursor = connection.cursor()

def get_products_from_db(type: ProductType):
    '''
    Getting a list of all products from the database
    '''
    results:List[scripts.bot_items.Product] = []
    try:
        if type != ProductType.all:
            cursor.execute(f'''SELECT * FROM itemsData WHERE item_type = "{type.value}"''')
        else:
            cursor.execute('''SELECT * FROM itemsData''')
        for row in cursor.fetchall():
            results.append(scripts.bot_items.Product(row['item_id'], row['item_name'], ProductType.get_type_by_value(row['item_type']), row['item_description'], row['item_price'], row['item_imageURL'] ))
    except pymysql.Error as error:
        print('[ERROR] Error when getting list of products from sqlite: ', error)
    finally:
        return(results)

def get_products_by_ids(ids: List[str]):
    '''
    Retrieving products from the database by list of IDs
    '''
    results:List[scripts.bot_items.Product] = []
    try:
        for id in ids:
            cursor.execute(f'''SELECT * FROM itemsData WHERE item_id = {id}''')
            item_data = cursor.fetchone()
            if item_data is None:
                print(f'[ERROR] No product with id {id}')
                continue
            results.append(get_product_from_row(item_data))
    except pymysql.Error as error:
        print('[ERROR] Error when getting list of products from sqlite: ', error)
    finally:
        return results

def get_user(user_id: int):
    '''
    Getting a user from the database
    '''
    print(f'[LOG] Checking ID {user_id}')
    cursor.execute(f'''SELECT * FROM userData WHERE user_id = {user_id}''')
    user_data = cursor.fetchone()
    if user_data is None:
        print('[WARNING] No such user found')
        return None
    else:
        user_list: List[scripts.bot_items.Product] = []
        if user_data['user_itemsList'] is None or user_data['user_itemsList'] == '':
            print('[WARNING] Users items list is empty')
        else:
            user_list = get_products_by_ids(str(user_data['user_itemsList']).split(', '))
        user = scripts.bot_items.User(
                user_id= user_data['user_id'],
                user_current_type= ProductType.get_type_by_value(user_data['user_currentItemsType']),
                user_list= user_list,
                chat_id= user_data['chat_id']
            )    
        return user

def create_user(user_id: int, chat_it:int):
    '''
    Adding a new user to the database
    '''
    try:
        user_data = cursor.execute('SELECT * FROM userData WHERE user_id = ?', (user_id, ))
        if user_data.fetchone() is None:
            cursor.execute('''INSERT INTO userData (user_id, chat_id) VALUES (?, ?)''', (user_id, chat_it,))
            connection.commit()
            print(f'[LOG] User with ID {user_id} added to database')
        else:
            print(f'[WARNING] User with ID {user_id} is already in the database')
    except pymysql.Error as error:
        print('[ERROR] Cant add new user to database > ' + error)
    finally:
        return get_user(user_id)

def add_product_to_user_list(user_id: int, product_id: int):
    '''
    Add product to user list
    '''
    user = get_user(user_id)
    current_list:str = user.get_products_ids()
    if current_list is None or current_list == '':
        current_list = str(product_id)
    else:
        current_list += ', ' + str(product_id)
    cursor.execute(f"""UPDATE userData SET user_itemsList = "{current_list}" where user_id = {user_id}""")
    connection.commit()

def update_user_list(user_id: int, new_list:str):
    '''
    Overwrite row in user table
    '''
    cursor.execute(f"""UPDATE userData SET user_itemsList = "{new_list}" where user_id = {user_id}""")
    connection.commit()

def clear_messages(user_id:int):
    cursor.execute(f"""UPDATE userData SET user_massages = "" where user_id = {user_id}""")
    connection.commit()

def add_message_to_user_list(user_id: int, message_id: int):
    '''
    Add a message to the user's list
    '''
    try:
        current_list:List[str] = get_user_messages(user_id)
        result:str = ''
        if len(current_list) == 0:
            result = str(message_id)
        else:
            result = ','.join(current_list)
            result += ',' + str(message_id)
        cursor.execute(f"""UPDATE userData SET user_massages = "{result}" where user_id = {user_id}""")
        connection.commit()
    except pymysql.Error as error:
        print('[ERROR] Error while getting message list from sqlite: ', error)

def get_user_messages(user_id:int):
    '''
    Returns a list of id messages sent to the user
    '''
    result: List[int] = []
    try:
        cursor.execute(f'''SELECT user_massages FROM userData WHERE user_id = {user_id}''')
        messages_data = str(cursor.fetchone()['user_massages'])
        if messages_data is not None and messages_data != '':
            splitter = ','
            if splitter in messages_data:
                result = messages_data.split(',')
            else:
                result = [messages_data]
    except pymysql.Error as error:
        print('[ERROR] Error while getting message list from sqlite: ', error)
    finally:
        return result

def get_product_from_row(row: dict):
    '''
    Getting a product instance from a single database row
    '''
    result = scripts.bot_items.Product(
                item_id= row['item_id'],
                item_name= row['item_name'],
                item_description= row['item_description'],
                item_price= row['item_price'],
                item_image_url= row['item_imageURL'],
                item_type= ProductType.get_type_by_value(row['item_type']) 
                )
    return result