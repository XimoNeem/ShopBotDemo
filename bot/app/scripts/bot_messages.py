import os

message_welcome = '''Добро пожаловать, это пример чат-бота для интернет магазина.
\nБот написан на Python(Telebot) + SQLite. С кодом проекта можно ознакомиться тут: 
'''
message_about = 'https://t.me/xeemoneem'
message_listHeader = 'Вот ваша корзина: '
message_listEmpty = 'Ваша корзина пуста('
message_checkout = 'Вот ваша корзина.\nИтого '
message_shopMenu = 'Какие товары показать?'
message_addedToList = '✅ Товар добавлен в корзину'
message_shopMain = 'Это главная страница магизина. Товары хранятся в базе данных SQLite и разбиты по категориям'
message_billCaption = 'Вот ссылка на оплату:\n'
message_clearBill = 'Счет отменен'
message_billPaid = 'Ваша корзина олачена'

button_allItems = '📝 Все'
button_casesItems = '📱 Чехлы'
button_headphonesItems = '🎧 Наушники'
button_itemsList = '🛒 Корзина'
button_toMenu = '📃 В меню'
button_about = '👨‍💻 Связаться со мной'
button_pay = '💳 К оплате'
button_clearList = '🆑 Очистить корзину'
button_toShop = '🛍 В магазин'
button_cancelBill = 'Отменить оплату 🆑'
button_applyBill = 'Подтвердить оплату ✅'


button_addToList = 'Добавить в корзину'
button_removeFromList = 'Удалить из корзины'

image_welcome = os.getcwd() + '/assets/welcome_image.jpg'

callback_show = 'sh'
callback_list = 'lt'
callback_about = 'ab'

callback_all = 'items_All'
callback_cases = 'items_Cases'
callback_headphones = 'items_Headphones'
callback_pay = 'pa'
callback_clearList = 'cll'
callback_toShop = 'bts'