import telebot
from scripts import bot_config
from scripts.bot_items import *
from scripts.bot_types import *
from scripts.bot_db_handler import *
from scripts.bot_pages import *
from scripts.bot_messages import *
from time import sleep
from pyqiwip2p import QiwiP2P


p2p = QiwiP2P(auth_key=scripts.bot_config.config_qiwiPrivate)
bot = telebot.TeleBot(bot_config.config_token)

@bot.message_handler(commands=['start'])
def start_message(message):
	check_user_id(message.from_user.id, message.chat.id)
	show_page(message.chat.id, page_welcome)
	bot.delete_message(message.chat.id, message.message_id)

@bot.message_handler(content_types=['text'])
def get_data(message):
	if message.text == button_itemsList:
		show_checkout(message.from_user.id)
	elif message.text == button_about:
		show_page(message.from_user.id, page_about)
	elif message.text == button_toMenu:
		show_page(message.chat.id, page_welcome)
	elif message.text == button_toShop:
		show_shop(message.from_user.id)
	elif message.text == button_clearList:
		get_user(message.from_user.id).clear_product_list()
		show_checkout(message.from_user.id)
	elif message.text == button_pay:
		show_bill(message.from_user.id)
	elif message.text == button_cancelBill:
		show_page(message.from_user.id, page_billCanceled)
	elif message.text == button_applyBill:
		show_page(message.from_user.id, page_paid)

	bot.delete_message(message.chat.id, message.message_id)

@bot.callback_query_handler(func=lambda call: True)
def check_callback(call):
	if str(call.data).startswith('items_'):
		show_items(call.from_user.id, ProductType.get_type_by_value(call.data))
	elif str(call.data).startswith('shop_item'):
		id = str(call.data).split(':')
		get_user(call.from_user.id).add_product(get_products_by_ids([id[1]])[0])
		bot.answer_callback_query(call.id, message_addedToList, show_alert=True)
		
def show_page(user_id:int, page: BotPage):
	clear_chat(user_id)
	if page.imageURL is None:
		send_message(user_id, page.text, reply_markup = page.reply_markup, parse_mode="Markdown")
	else:
		img = open(page.imageURL, 'rb')
		send_photo(user_id, img, caption = page.text, reply_markup = page.reply_markup, parse_mode="Markdown")

def show_product_card(user_id: int, product: Product, markup = None):
	dsc = f'*{product.name.upper()}*\n{product.description.lower()}\n\n_{str(product.price)} ₽_'
	imageURL = product.image_URL
	send_photo(user_id, imageURL, caption=dsc, parse_mode="Markdown", reply_markup=markup)

def check_user_id(user_id:int, chat_id:int):
	if get_user(user_id) is None:
		create_user(user_id, chat_id)

def show_checkout(user_id:int):
	clear_chat(user_id)
	user = get_user(user_id)
	items = user.get_products_list()
	if len(items) == 0:
		send_message(user_id, message_listEmpty, reply_markup= get_list_cleared())
	else:
		show_page(user_id, page_listHeader)
		for item in items:
			show_product_card(user_id, item)
		send_message(user_id, message_checkout + str(user.get_checkout_price()) + '₽', reply_markup= get_checkout())

def show_shop(user_id):
	show_page(user_id, page_shop)
	send_message(user_id, message_shopMenu, reply_markup=get_products_types())

def show_items(user_id: int, type: ProductType):
	items = get_products_from_db(type)
	for item in items:
		show_product_card(user_id, item, get_shop_item_menu(item))

def show_bill(user_id:int):
    comment = 'Демо платеж, не оплачивать!'
    # price = get_user(user_id).get_checkout_price()
    price = 1 # one ruble bill (for demo)
    bill = p2p.bill(amount=price, lifetime=bot_config.config_billLifetime, comment=comment)
    message = message_billCaption + bill.pay_url + f'\nСсылка будет работать {bot_config.config_billLifetime} минут'
    send_message(user_id, message, reply_markup=get_bill_menu(), parse_mode=None)

def send_message(user_id:int, message:str, reply_markup = None, parse_mode="Markdown"):
	current_message = bot.send_message(user_id, message, reply_markup=reply_markup, parse_mode=parse_mode)
	add_message_to_user_list(user_id, current_message.message_id)

def send_photo(user_id, img, caption = '', reply_markup = None, parse_mode="Markdown"):
	current_message = bot.send_photo(user_id, img, caption = caption, reply_markup = reply_markup, parse_mode=parse_mode)
	add_message_to_user_list(user_id, current_message.message_id)

def clear_chat(user_id:int):
	user = get_user(user_id)
	for message in user.get_messages():
		try:
			bot.delete_message(user.chat_id, message)
		except Exception as error:
			print('[ERROR] ', error)
	clear_messages(user_id)

if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except:
            sleep(5) 