import sys
import requests
import json
import os.path
from datetime import timedelta, datetime


class WeatherForecast:
	def __init__(self, api_key, file_name):
		self.api_key = api_key
		self.file_name = file_name
		self.file_empty = False
		self.input_date = ''
		self.full_weather_history = {}
		self.today = str(datetime.today().date()).strip()
		self.tomorrow = str(datetime.today().date() + timedelta(days=1)).strip()

	def check_if_date_provided(self):
		if len(sys.argv) == 2:
			print('No date provided, checking tomorrows weather')
			return False
		else:
			self.input_date = sys.argv[2]
			return True

	def print_key(self):
		print(self.api_key)

	def check_for_file(self):
		if os.path.exists(self.file_name):
			print('File found')
		else:
			with open(self.file_name, 'w'):
				print('Empty file created')
				self.file_empty = True

	def read_from_file(self):
		print('Loading file...')
		if os.path.getsize(self.file_name) != 0:
			with open(self.file_name, 'r', encoding='utf-8') as openfile:
				json_object = json.load(openfile)
				self.full_weather_history = json_object['data']
				self.file_empty = False
		else:
			print('File is empty')
			self.file_empty = True
			return False

	# def items(self):
	# 	print('')
	# 	print('***Generator tupli***')
	# 	for daily_history in self.full_weather_history:
	# 		dane = daily_history['valid_date'], daily_history['precip']
	# 		print(tuple(dane))
	# 	print('***Generator tupli***')
	# 	print('')

	def check_for_date(self):
		if not self.file_empty:
			for daily_history in self.full_weather_history:
				if not self.input_date:
					if self.tomorrow == daily_history['valid_date'] and daily_history['precip'] > 0:
						print(f'On {self.tomorrow} it will be raining!')
						quit()
					elif self.tomorrow == daily_history['valid_date'] and daily_history['precip'] == 0:
						print(f'On {self.tomorrow} it wont be raining!')
						quit()
				else:
					if self.input_date == daily_history['valid_date'] and daily_history['precip'] > 0:
						print(f'On {self.input_date} it will be raining!')
						quit()
					elif self.input_date == daily_history['valid_date'] and daily_history['precip'] == 0:
						print(f'On {self.input_date} it wont be raining!')
						quit()
			else:
				return False

	def api_data_download(self):
		if self.file_empty or not self.check_for_date():
			print('Downloading from API...')
			url = "https://weatherbit-v1-mashape.p.rapidapi.com/forecast/daily"
			querystring = {"lat":"38.5","lon":"-78.5"}
			headers = {
				"X-RapidAPI-Key": self.api_key,
				"X-RapidAPI-Host": "weatherbit-v1-mashape.p.rapidapi.com"
			}
			api_output = requests.request("GET", url, headers=headers, params=querystring).json()
			with open(self.file_name, "w", encoding='utf-8') as outfile:
				json.dump(api_output, outfile)
			self.read_from_file()
			self.check_for_date()

	def if_found(self):
		if not self.check_for_date():
			print(f'Please check your input')
			print(f'I only store weather info for the next 16 days')


	# def __getitem__(self, item):
	# 	return
	#
	# def __setitem__(self, key, value):
	# 	return


wf = WeatherForecast(sys.argv[1], 'out.json')
wf.check_if_date_provided()
wf.check_for_file()
wf.read_from_file()
# wf.items()
wf.check_for_date()
wf.api_data_download()
wf.if_found()
