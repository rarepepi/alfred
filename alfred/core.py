from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import json
import requests
from bs4 import BeautifulSoup
from binance.client import Client

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
					level=logging.INFO)

logger = logging.getLogger(__name__)

#Load config
with open('config.json') as file:
		config = json.load(file)

binance = Client(config['binance']['apikey'], config['binance']['apisecret'])


# Genesis grades
def genesis_get_grades():

	#Create session
	session_requests = requests.session()

	#Get login page
	result = session_requests.get(config['genesis']['login_url'])

	# Create payload
	payload = {
		"j_username": config['genesis']['username'],
		"j_password": config['genesis']['password'],
	}

	# Perform login
	result = session_requests.post(config['genesis']['login_url'], data = payload, headers = dict(referer = config['genesis']['login_url']))

	# Scrape url
	result = session_requests.get(config['genesis']['grade_url'], headers = dict(referer = config['genesis']['grade_url']))
	soup = BeautifulSoup(result.content, 'lxml')

	#Get rows of classes
	courses = soup.find_all('tr', 'listrowodd') + soup.find_all('tr', 'listroweven')

	classes = []
	grades = []
	percents = []

	# Add soups into lists
	for x in range(0, len(courses)):
		if "No Grades" not in courses[x].find('td', {'class':'cellCenter'}).text:
			classes.append(courses[x].find('span', {'class':'categorytab'}).text.strip())
			grades.append(courses[x].find('td', {'width':'70%'}).text.strip())
			percents.append(courses[x].find('td', {'width': '30%'}).text.strip())

	final_grades = ""
	for x in range(0, len(classes)):
		final_grades += classes[x] + " | " + grades[x] + " | " + percents[x] + "\n------------------------------------\n"

	return(final_grades)


# Binance info
def get_btc_value(ticker, amount):
	pass


def binance_get_balance():
	balances = []
	info = binance.get_account()
	assets = info['balances']
	for asset in assets:
		if float(asset['free']) > 0.001:
			balances.append((asset['asset'], asset['free']))
	return(balances)


# Telegram commands
def start(bot, update):
	update.message.reply_text("Hello! I am Alfred, your customized personal butler.")


def grades(bot, update):
	update.message.reply_text(genesis_get_grades())


def balance(bot, update):
	update.message.reply_text(binance_get_balance())


def echo(bot, update):
	update.message.reply_text(update.message.text)


def error(bot, update, error):
	logger.warning('Update "%s" caused error "%s"', update, error)


def main():

	updater = Updater(config['telegram']['token'])

	dp = updater.dispatcher

	dp.add_handler(CommandHandler("start", start))
	dp.add_handler(CommandHandler("grades", grades))
	dp.add_handler(CommandHandler("balance", balance))

	dp.add_error_handler(error)

	dp.add_handler(MessageHandler(Filters.text, echo))

	updater.start_polling()

	updater.idle()


if __name__ == '__main__':
	main()
