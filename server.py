from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy
from scraper import *
from database_setup import app, db, Food
@app.route("/")
def display():
	food = Food.query.all()
	return render_template('index.html', food = food)

if __name__ == "__main__":
    app.run(debug=True)