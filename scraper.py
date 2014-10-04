import requests, bs4
base_url = 'https://web.archive.org'
start_url = base_url + '/web/*/http://services.housing.berkeley.edu/FoodPro/dining/static/todaysentrees.asp'
def get_food ():
	response = requests.get(archive)
	soup = bs4.BeautifulSoup(response.text)
	return [a.attrs.get('href') for a in soup.select('.day a')]
