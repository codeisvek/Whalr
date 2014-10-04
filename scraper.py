import requests, bs4, re, datetime
base_url = 'https://web.archive.org'
start_url = base_url + '/web/*/http://services.housing.berkeley.edu/FoodPro/dining/static/todaysentrees.asp'
def make_soup(url):
	response = requests.get(url)
	return bs4.BeautifulSoup(response.text)
def get_food ():
	soup = make_soup(start_url)
	return [a.attrs.get('href') for a in soup.select('.day a')]
def serve_day(soup):
	months = {
		'January': 1,
		'February': 2,
		'March': 3,
		'April': 4,
		'May': 5,
		'June': 6,
		'July': 7,
		'August': 8,
		'September': 9,
		'October': 10,
		'November': 11,
		'December': 12
	}
	days = re.findall(r'\w+,\s(\w+)\s(\d+),\s(\d+)', soup.select('.title1 i')[0].get_text())
	return datetime.date(int(days[0][2]), months[days[0][0]], int(days[0][1]))
def find_food(soup):
	return [a.get_text() for a in soup.select('td#content tr[valign=top] td a')]
def find_food_links(soup):
	return [a.attrs.get('href') for a in soup.select('td#content tr[valign=top] td a')]
def find_food_info(food_url):
	food_info = {}
	new_url = re.sub(r'web/\*/', '', food_url)
	soup = make_soup(base_url + new_url)
	try:
		food_info['name'] = re.sub(r'[\r\n\xa0]+', '', soup.select('div[align=left]')[0].get_text().strip())
		food_info['calories'] = int(re.sub(r'\D+', '', soup.select('font[size="3"] b')[0].get_text()))
	except IndexError:
		food_info['calories'] = 0
	return food_info