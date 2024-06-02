import configparser
import db
import random
import string

config = configparser.ConfigParser()
config.read("settings.ini")
cfg_group_link = config["bot"]["open_link"]

def hello(id):
	return f'''
*Приветствую, {id}!*

Этот телеграм бот предназначен для покупки криптовалют. А также быстрый и бесплатный кошелек!
'''

def profile(id):
	return f'''
*💼 Кошелек*

*Сумма покупок:* 0 RUB
*Холд:* 0 RUB

Вами было проведено 0 сделок на общую сумму 0 RUB.
'''

def info():
	return f'''
🙋 Благодарим за использование нашего Телеграм-бота для покупки криптовалют.

*Телеграм канал:* {cfg_group_link}
'''

def buy(coin, price):
	return f'''
*🎾 Курс: {price}₽*
Введите сумму покупки в {coin}
'''

def buy_sum(coin):
	return f'''
Введите адрес своего {coin} кошелька
'''

def buy_wallet(id):
	return f'''
Выберите способ оплаты
'''

def buy_type(num, topay):
	r = f"{random.randint(44,77)}{random.choice(string.ascii_letters)}{random.choice(string.ascii_letters)}{random.randint(371,984)}{random.choice(string.ascii_letters)}{random.randint(11,24)}"
	return f'''
*📈 Сделка ID{r}*

*К оплате: {topay}₽*

*Реквизиты для перевода:*
{num}

*Комментарий:*
{r}
'''

def buy_accept():
	return f'''
⏳ Ожидается поступление средств...

Как только мы получим оплату, TON автоматически поступят на ваш кошелек, а вы получите от нас уведомление
'''