import sqlite3
import emoji
import re
import os, re, configparser, requests, time
from aiogram import Bot, types
from aiogram.dispatcher import dispatcher, FSMContext
from aiogram.utils import executor
from aiogram.utils.helper import Helper, HelperMode, ListItem
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import BoundFilter
import db
import keyboard as kb
import data

config = configparser.ConfigParser()
config.read("settings.ini")
cfg_token = config["bot"]["token"]
cfg_group_link = config["bot"]["open_link"]
cfg_admin_group = int(config["bot"]["admin_group"])
sber = config["bot"]["sber"]
qiwi = config["bot"]["qiwi"]
umoney = config["bot"]["umoney"]
admin = int(config["bot"]["admin"])
discount = float(config["bot"]["discount"])
min_to_buy = float(config["bot"]["min"])
max_to_buy = float(config["bot"]["max"])

bot = Bot(token=cfg_token)

dp = Dispatcher(bot, storage=MemoryStorage())

async def check_sub(id):
	user = await bot.get_chat_member(chat_id = cfg_group_link, user_id = id)
	if (db.settings_check_sub() == 0):
		return True
	if (user):
		if (user['status'] != 'left'):
			return True
	return False

class States(StatesGroup):
	menu = State()
	buy = State()
	buy_coin = State()
	buy_sum = State()
	buy_wallet = State()
	buy_type = State()
	buy_accept = State()
	admin_menu = State()
	admin_change_price = State()
	admin_rassilka = State()

#------------------------------

# Меню
@dp.message_handler(text="Вернуться в меню", state=[States.buy_accept, States.admin_menu])
@dp.message_handler(text="Назад", state=States.buy)
@dp.message_handler(commands=["start", "menu"], state="*")
async def cmd_menu(message: types.Message, state: FSMContext):
	if not (db.get_users_exist(message.chat.id)):
		try:
			await bot.send_message(chat_id = cfg_admin_group, text = f"Новый пользователь: {message.chat.id} (@{message.chat.username})")
		except:
			await bot.send_message(chat_id = cfg_admin_group, text = f"Новый пользователь: {message.chat.id}")
	db.add_user_to_db(message.chat.id)
	if not (await check_sub(message.chat.id)):
		await message.answer(f"Для начала подпишитесь на канал: \n{cfg_group_link}")
	else:
		try:
			await message.answer(data.hello(message.chat.first_name), reply_markup = kb.menu(), parse_mode="Markdown")
		except:
			await message.answer(data.hello(message.chat.id), reply_markup = kb.menu(), parse_mode="Markdown")
	await States.menu.set()

# Выбор крипты
@dp.message_handler(text="Назад", state=States.buy_coin)
@dp.message_handler(text=["📈 Купить монеты"], state=States.menu)
async def cmd_buy(message: types.Message, state: FSMContext):
	if not (await check_sub(message.chat.id)):
		await message.answer(f"Для начала подпишитесь на канал: \n{cfg_group_link}")
	else:
		await message.answer("Выберите монету", reply_markup = kb.coins_list(), parse_mode="Markdown")
		await States.buy.set()

# Купить TON
@dp.message_handler(text="Назад", state=States.buy_sum)
@dp.message_handler(state=States.buy)
async def cmd_buy(message: types.Message, state: FSMContext):
	if not (await check_sub(message.chat.id)):
		await message.answer(f"Для начала подпишитесь на канал: \n{cfg_group_link}")
	else:
		if (message.text == "Назад"):
			_data = await state.get_data()
			coin = _data['coin']
			price = db.coins_get_price(coin)
			await state.update_data(price=price)
			await message.answer(data.buy(coin, price), reply_markup = kb.buy(), parse_mode="Markdown")
			await States.buy_coin.set()
		elif (message.text in [i[0] for i in db.get_all_coins()]):
			coin = message.text
			await state.update_data(coin=coin)
			price = db.coins_get_price(coin)
			await state.update_data(price=price)
			await message.answer(data.buy(coin, price), reply_markup = kb.buy(), parse_mode="Markdown")
			await States.buy_coin.set()
		else:
			await message.answer("Неверная монета")

# Введена сумма
@dp.message_handler(text="Назад", state=States.buy_wallet)
@dp.message_handler(state=States.buy_coin)
async def cmd_buy(message: types.Message, state: FSMContext):
	if not (await check_sub(message.chat.id)):
		await message.answer(f"Для начала подпишитесь на канал: \n{cfg_group_link}")
	else:
		_data = await state.get_data()
		coin = _data['coin']
		if (message.text == "Назад"):
			await message.answer(data.buy_sum(coin), reply_markup = kb.buy_sum(message.chat.id), parse_mode="Markdown")
			await States.buy_sum.set()
		else:
			try:
				if (float(message.text) >= min_to_buy and float(message.text) <= max_to_buy):
					float(message.text)
					await message.answer(data.buy_sum(coin), reply_markup = kb.buy_sum(message.chat.id), parse_mode="Markdown")
					await States.buy_sum.set()
					await state.update_data(count=message.text)
				else:
					await message.answer(f"*Неверная сумма!*\n\n*Минимум:* {int(min_to_buy)} TON\n*Максимум:* {int(max_to_buy)} TON", reply_markup = kb.buy(), parse_mode="Markdown")
			except:
				await message.answer("Неверное количество", reply_markup = kb.buy(), parse_mode="Markdown")

# Введен кошелек
@dp.message_handler(text="Назад", state=States.buy_type)
@dp.message_handler(state=States.buy_sum)
async def cmd_buy_wallet(message: types.Message, state: FSMContext):
	if not (await check_sub(message.chat.id)):
		await message.answer(f"Для начала подпишитесь на канал: \n{cfg_group_link}")
	else:
		if (message.text == "Назад"):
			await message.answer(data.buy_wallet(message.chat.id), reply_markup = kb.buy_wallet(), parse_mode="Markdown")
			await States.buy_wallet.set()
		else:
			if (len(message.text) >= 10):
				db.set_last_wallet(message.chat.id, message.text)
				await message.answer(data.buy_wallet(message.chat.id), reply_markup = kb.buy_wallet(), parse_mode="Markdown")
				await States.buy_wallet.set()
			else:
				await message.answer("Неверный формат кошелька", reply_markup = kb.buy_sum(message.chat.id), parse_mode="Markdown")

# Выбран способ оплаты
@dp.message_handler(state=States.buy_wallet)
async def cmd_buy_type(message: types.Message, state: FSMContext):
	if not (await check_sub(message.chat.id)):
		await message.answer(f"Для начала подпишитесь на канал: \n{cfg_group_link}")
	else:
		tondata = await state.get_data()
		topay = round(float(tondata['price']) * float(tondata['count']), 2)
		if (message.text == "Qiwi"):
			await message.answer(data.buy_type(qiwi, topay), reply_markup = kb.buy_type(), parse_mode="Markdown")
			await States.buy_type.set()
		elif (message.text == "Сбербанк"):
			await message.answer(data.buy_type(sber, topay), reply_markup = kb.buy_type(), parse_mode="Markdown")
			await States.buy_type.set()
		elif (message.text == "Юмани"):
			await message.answer(data.buy_type(umoney, topay), reply_markup = kb.buy_type(), parse_mode="Markdown")
			await States.buy_type.set()
		else:
			await message.answer("Неверный способ оплаты", reply_markup = kb.buy_wallet(), parse_mode="Markdown")

# Проверить оплату
@dp.message_handler(text="✅ Проверить оплату", state=States.buy_type)
async def cmd_buy_accept(message: types.Message, state: FSMContext):
	if not (await check_sub(message.chat.id)):
		await message.answer(f"Для начала подпишитесь на канал: \n{cfg_group_link}")
	else:
		await message.answer(data.buy_accept(), reply_markup = kb.buy_accept(), parse_mode="Markdown")
		await States.buy_accept.set()
		try:
			await bot.send_message(chat_id = cfg_admin_group, text = f"{message.chat.id} (@{message.chat.username})\nпытается проверить оплату")
		except:
			await bot.send_message(chat_id = cfg_admin_group, text = f"{message.chat.id}\nпытается проверить оплату")

# Профиль
@dp.message_handler(text=["💼 Профиль"], state=States.menu)
async def cmd_profile(message: types.Message, state: FSMContext):
	if not (await check_sub(message.chat.id)):
		await message.answer(f"Для начала подпишитесь на канал: \n{cfg_group_link}")
	else:
		await message.answer(data.profile(message.chat.id), reply_markup = kb.menu(), parse_mode="Markdown")

# Информация
@dp.message_handler(text=["ℹ Информация"], state=States.menu)
async def cmd_info(message: types.Message, state: FSMContext):
	if not (await check_sub(message.chat.id)):
		await message.answer(f"Для начала подпишитесь на канал: \n{cfg_group_link}")
	else:
		await message.answer(data.info(), reply_markup = kb.menu(), parse_mode="Markdown")

@dp.message_handler(text="Назад", state=[States.admin_change_price, States.admin_rassilka])
@dp.message_handler(commands="admin", state="*")
async def admin_menu(message: types.Message, state: FSMContext):
	if (message.chat.id == admin):
		await States.admin_menu.set()
		await message.answer(f"*Меню администратора*\n\nПользователей всего: {len(db.get_all_users())} \nЗа неделю: {len(db.get_week_users())}", reply_markup = kb.admin_menu(), parse_mode="Markdown")

@dp.message_handler(text=["👤 Нужно подписаться: Нет", "👤 Нужно подписаться: Да"], state=States.admin_menu)
async def admin_check_sub(message: types.Message, state: FSMContext):
	if (message.chat.id == admin):
		await States.admin_menu.set()
		if (db.settings_check_sub() == 0):
			db.settings_set_check_sub(1)
			await message.answer(f"*Теперь для работы бота нужно подписаться на канал*", reply_markup = kb.admin_menu(), parse_mode="Markdown")
		else:
			db.settings_set_check_sub(0)
			await message.answer(f"*Теперь для работы бота НЕ нужно подписываться на канал*", reply_markup = kb.admin_menu(), parse_mode="Markdown")

@dp.message_handler(text="💰 Установить цену", state=States.admin_menu)
async def admin_set_price(message: types.Message, state: FSMContext):
	if (message.chat.id == admin):
		await States.admin_change_price.set()
		await message.answer(f"Введите новую *ФИКСИРОВАННУЮ* цену за 1 монету в формате:*\nМонета цена\n\nНапример: BTC 100*", reply_markup = kb.just_back(), parse_mode="Markdown")

@dp.message_handler(state=States.admin_change_price)
async def admin_set_price_2(message: types.Message, state: FSMContext):
	if (message.chat.id == admin):
		data = message.text.strip().split(" ")
		if (len(data) > 1):
			try:
				float(data[1])
				db.coins_set_price(data[0], data[1])
				await States.admin_menu.set()
				await message.answer(f"Для {data[0]} установлен новый курс: {data[1]}", reply_markup = kb.admin_menu(), parse_mode="Markdown")
			except:
				await message.answer("Неверный формат", parse_mode="Markdown")
		else:
			await message.answer("Неверный формат", parse_mode="Markdown")

@dp.message_handler(text="📬 Рассылка", state=States.admin_menu)
async def admin_set_price(message: types.Message, state: FSMContext):
	if (message.chat.id == admin):
		await States.admin_rassilka.set()
		await message.answer(f"Введите текст рассылки", reply_markup = kb.just_back(), parse_mode="Markdown")

@dp.message_handler(state=States.admin_menu)
async def admin_add_delete_coin(message: types.Message, state: FSMContext):
	if (message.chat.id == admin):
		if (" " in message.text):
			data = message.text.split(" ")
			name = data[1]
			if (data[0] == "/add"):
				db.coins_create_coin(name)
				await message.answer(f"Монета {name} добавлена")
			elif (data[0] == "/del"):
				if (name in [i[0] for i in db.get_all_coins()]):
					db.coins_delete_coin(name)
					await message.answer(f"Монета {name} удалена")
				else:
					await message.answer(f"Монета {name} не найдена в базе")

@dp.message_handler(state=States.admin_rassilka)
async def rassilka2(message: types.Message, state: FSMContext):
	if (message.chat.id == admin):
		if message.text != 'Назад':
			text = message.text
			users = db.get_all_users()
			for user in users:
				try:
					await bot.send_message(chat_id=user[0], text=text)
					time.sleep(0.1)
				except:
					pass
			await bot.send_message(message.from_user.id, f"✅ Рассылка успешно завершена", reply_markup=kb.admin_menu())
			await States.admin_menu.set()

#------------------------------

if __name__ == "__main__":
	db.check_db()
	executor.start_polling(dp, skip_updates=True)
