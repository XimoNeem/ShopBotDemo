from typing import List
from scripts.bot_db_handler import *
from scripts.bot_types import ProductType
from telebot import types, TeleBot
from scripts.bot_messages import *

class Product:
    '''
    Description of the product unit
    '''
    def __init__(self, item_id:int, item_name:str, item_type:ProductType, item_description:str, item_price:float, item_image_url:str):
        self.id = item_id
        self.name = item_name
        self.type = item_type
        self.description = item_description
        self.price = item_price
        self.image_URL = item_image_url

    '''
    Debug log of product info
    '''
    def get_text(self):
        out_text = 'Товар {} с id {} имеет описание {}'.format(self.name, self.id, self.description)
        print(out_text)

class User:
    '''
    Shop user
    '''
    def __init__(self, user_id:int,  user_current_type:ProductType, user_list:List[Product], chat_id:int):
        self.id = user_id
        self.products_list: List[Product] = user_list
        self.current_product = Product(000, 'Default', ProductType.cases, 'This is default product', 0, 'http://default.png')
        self.current_type:ProductType = user_current_type
        self.chat_id = chat_id

    def get_products_list(self):
        '''
        Returns a list of products (Product instances)
        '''
        return self.products_list

    def get_products_ids(self):
        '''
        Returns a list of product id's as a string
        '''
        print(self.products_list)
        ids: List[str] = []
        if self.products_list is not None:
            for item in self.products_list:
                ids.append(str(item.id))
        return ', '.join(ids)

    def get_checkout_price(self):
        result:float = 0
        for item in self.products_list:
            result += item.price
        return result
    
    def add_product(self, new_product:Product):
        self.products_list.append(new_product)
        add_product_to_user_list(self.id, new_product.id)

    def clear_product_list(self):
        self.products_list = []
        update_user_list(self.id, '')
    
    def get_messages(self):
        return get_user_messages(self.id)
    
    def add_message(self, message_id:int):
        add_message_to_user_list(self.id, message_id)


class BotPage:
    '''
    The bot's page may contain a picture or text and buttons
    '''
    def __init__(self, page_text: str, page_image: str=None, page_markup=None):
        self.text= page_text
        self.imageURL = page_image
        self.reply_markup = page_markup

def get_main_menu():
    '''
    Main menu buttons
    '''
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton(text=button_toShop))
    markup.add(types.KeyboardButton(text=button_itemsList))
    markup.add(types.KeyboardButton(text=button_about))
    return markup

def get_products_types():
    '''
    Types of products buttons
    '''

    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton(text=button_allItems, callback_data=callback_all))
    markup.add(types.InlineKeyboardButton(text=button_casesItems, callback_data=callback_cases))
    markup.add(types.InlineKeyboardButton(text=button_headphonesItems, callback_data=callback_headphones))
    return markup

def get_list_cleared():
    '''
    Buttons for empty shopping list
    '''
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton(button_toMenu))
    markup.add(types.KeyboardButton(button_toShop))
    return markup

def get_shop_menu():
    '''
    Shop menu buttons
    '''
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton(button_toMenu))
    markup.add(types.KeyboardButton(button_itemsList))
    return markup

def get_checkout():
    '''
    Checkout buttons
    '''
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.InlineKeyboardButton(text=button_pay, callback_data=callback_pay))
    markup.add(types.InlineKeyboardButton(text=button_clearList, callback_data=callback_clearList), types.InlineKeyboardButton(text=button_toShop, callback_data=callback_toShop))
    return markup

# def get_checkout_empty_list():
#     markup = types.InlineKeyboardMarkup(row_width=2)
#     markup.add(types.InlineKeyboardButton(text=button_toShop, callback_data=callback_toShop))
#     return markup

def get_shop_item_menu(product: Product):
    '''
    Inline button for adding an item to the cart
    '''
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(types.InlineKeyboardButton(text=button_addToList, callback_data= 'shop_item:' + str(product.id)))
    return markup

def get_bill_menu():
    '''
    Bill menu
    '''
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.InlineKeyboardButton(text=button_cancelBill))
    markup.add(types.InlineKeyboardButton(text=button_applyBill))
    return markup