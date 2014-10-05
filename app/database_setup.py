from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from .scraper import *
from app import app
db = SQLAlchemy(app)
class Food(db.Model):
	__tablename__ = "food"
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.Text)
	calories = db.Column(db.Integer())
	frequency = db.Column(db.Integer())
	timeOfDay = db.Column(db.Integer())
	lastServed = db.Column(db.Date)
	location = db.Column(db.Text)
	def __init__(self, name, calories, lastServed, location, timeOfDay):
		self.name = name
		self.calories = calories
		self.frequency = 1
		if lastServed is None:
			lastServed = date.min()
		self.lastServed = lastServed
		if location == 0:
			location = "Crossroads"
		elif location == 1:
			location = "Cafe 3"
		elif location == 2:
			location = "Foothill"
		elif location == 3:
			location = "Clark Kerr"
		else:
			location = "Nowhere"
		self.location = location
		if timeOfDay is None:
			timeOfDay = "-1"
		self.timeOfDay = timeOfDay
		print(self.name)
		print(self.calories)
		print(self.location)
		print(self.timeOfDay) 
	def __repr__(self):
		return '<name %r>' % self.name
db.create_all()
#db.drop_all()
def add_food(base, link):
	soup = make_soup(base + link)
	date = serve_day(soup)
	foods = find_food(soup)
	n = []
	t = []
	l = []
	for food in foods:
		n.append(food[0])
		t.append(food[1])
		l.append(food[2])
	food_links = find_food_links(soup)
	for x in range(0, len(n)):
		if Food.query.filter_by(name=n[x]).first() != None:
			Name = Food.query.filter_by(name=n[x]).first()
			update_food(Name, date, l[x], t[x])
			db.session.commit()
		else:
			food_url = re.sub(r'web/\*/', '', food_links[x])
			new_soup = make_soup(base + food_url)
			food_info = find_food_info(new_soup)
			if food_info['calories'] != 0:
				new_food = Food(n[x], food_info['calories'], date, l[x], t[x])
				db.session.add(new_food)
				db.session.commit()
#Create database from archive
def create_archive():
	date_links = get_food()
	for day in date_links:
		add_food(base_url, day)
def get_menu_today():
	dining_root = 'http://services.housing.berkeley.edu/FoodPro/dining/static/'
	dining_menu = 'todaysentrees.asp'
	add_food(dining_root, dining_menu)
def update_food(food, date, location, time):
	if date > food.lastServed:
		food.frequency += 1
	food.lastServed = date
	food.location = location
	food.timeOfDay = time
#RUN ONCE
#create_archive()
#run daily
get_menu_today()