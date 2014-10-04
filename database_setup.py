from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from scraper import *
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'
db = SQLAlchemy(app)
class Food(db.Model):
	id = db.Column(db.Integer(), primary_key = True)
	name = db.Column(db.Text)
	calories = db.Column(db.Integer())
	frequency = db.Column(db.Integer())
	lastServed = db.Column(db.Date)
	def __init__(self, name, calories, lastServed = None):
		self.name = name
		self.calories = calories
		self.frequency = 1
		if lastServed is None:
			lastServed = date.today()
		self.lastServed = lastServed
	def __repr__(self):
		return '<name %r>' % self.name
db.create_all()
#Create database from archive
def create_archive():
	date_links = get_food()
	for day in date_links:
		soup = make_soup(base_url + day)
		served = serve_day(soup)
		n = find_food(soup)
		food_links = find_food_links(soup)
		print(len(n))
		for x in range(0, len(n)):
			if Food.query.filter_by(name=n[x]).first() != None:
				Name = Food.query.filter_by(name=n[x]).first()
				update_food(Name, served)
				db.session.commit()
			else:
				print(x)
				print(n[x])
				food_info = find_food_info(food_links[x])
				if food_info['calories'] != 0:
					new_food = Food(n[x], food_info['calories'], served)
					db.session.add(new_food)
					db.session.commit()
#def get_menu_today():
#	dining_root = 'http://services.housing.berkeley.edu/FoodPro/dining/static/'
#	dining_menu = 'todaysentrees.asp'
#	soup = make_soup(dining_root + dining_menu)
#	served = serve_day(soup)
#	n = find_food(soup)
#	food_links = find_food_links(soup)
#	print(len(n))
#	for x in range(0, len(n)):
#		if Food.query.filter_by(name=n[x]).first() != None:
#			Name = Food.query.filter_by(name=n[x]).first()
#			update_food(Name, served)
#			db.session.commit()
#		else:
#			print(x)
#			print(n[x])
#			print(dining_root + food_links[x])
#			food_info = find_food_info(dining_root + food_links[x])
#			if food_info['calories'] != 0:
#				new_food = Food(n[x], food_info['calories'], served)
#				db.session.add(new_food)
#				db.session.commit()
def update_food(food, time):
	food.lastServed = time
	food.frequency += 1
#get_menu_today()
#create_archive() RUN ONCE