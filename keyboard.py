from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
import db

def menu():
	button1 = KeyboardButton('📈 Купить монеты')
	button3 = KeyboardButton('💼 Профиль')
	button4 = KeyboardButton('ℹ Информация')
	keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
	keyboard.add(button1)
	keyboard.add(button3, button4)
	return keyboard

def buy():
	button1 = KeyboardButton('Назад')
	keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
	keyboard.add(button1)
	return keyboard

def buy_sum(user_id):
	if (db.get_last_wallet(user_id)):
		button1 = KeyboardButton(db.get_last_wallet(user_id))
		button2 = KeyboardButton('Назад')
		keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
		keyboard.add(button1)
		keyboard.add(button2)
	else:
		button1 = KeyboardButton('Назад')
		keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
		keyboard.add(button1)
	return keyboard

def buy_wallet():
	button1 = KeyboardButton('Сбербанк')
	button2 = KeyboardButton('Qiwi')
	button3 = KeyboardButton('Юмани')
	button4 = KeyboardButton('Назад')
	keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
	keyboard.add(button1, button2, button3)
	keyboard.add(button4)
	return keyboard

def buy_type():
	button1 = KeyboardButton('✅ Проверить оплату')
	button2 = KeyboardButton('Назад')
	keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
	keyboard.add(button1)
	keyboard.add(button2)
	return keyboard

def buy_accept():
	button1 = KeyboardButton('Вернуться в меню')
	keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
	keyboard.add(button1)
	return keyboard

def admin_menu():
	if (db.settings_check_sub() == 0):
		button2 = KeyboardButton('👤 Нужно подписаться: Нет')
	else:
		button2 = KeyboardButton('👤 Нужно подписаться: Да')
	button1 = KeyboardButton('📬 Рассылка')
	button3 = KeyboardButton('💰 Установить цену')
	button4 = KeyboardButton('Вернуться в меню')
	keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
	keyboard.add(button1)
	keyboard.add(button2)
	keyboard.add(button3)
	keyboard.add(button4)
	return keyboard

def just_back():
	button1 = KeyboardButton('Назад')
	keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
	keyboard.add(button1)
	return keyboard

def coins_list():
	keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
	coins = db.get_all_coins()
	for item in coins:
		keyboard.add(KeyboardButton(item[0]))
	keyboard.add(KeyboardButton("Назад"))
	return keyboard