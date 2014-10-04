import requests, bs4
base_url = 'https://web.archive.org'
start_url = base_url + '/web/*/http://services.housing.berkeley.edu/FoodPro/dining/static/todaysentrees.asp'
def get_food ():
	response = requests.get(start_url)
	soup = bs4.BeautifulSoup(response.text)
	return [a.attrs.get('href') for a in soup.select('.day a')]
def find_food(food_url):
	response = requests.get(base_url + food_url)
	soup = bs4.BeautifulSoup(response.text)
	return [a.get_text() for a in soup.select('td#content tr[valign=top] td a')]
food_links = get_food()
for day in food_links:
	print (find_food(day))