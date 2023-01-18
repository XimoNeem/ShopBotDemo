from telebot import types

from scripts.bot_items import *
from scripts.bot_messages import *

page_welcome = BotPage(message_welcome, image_welcome, get_main_menu())
page_about = BotPage(message_about, page_markup= get_list_cleared())
page_shop = BotPage(message_shopMain, page_markup= get_shop_menu())
page_listHeader = BotPage(message_listHeader, page_markup= get_checkout())
page_paid = BotPage(message_billPaid, page_markup=get_shop_menu())
page_billCanceled = BotPage(message_clearBill, page_markup=get_shop_menu())