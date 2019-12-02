#!/usr/bin/env python3
import os
import slack
import sqlite3
import random
from flask import Flask, render_template

app = Flask(__name__)

sqlite_connection = sqlite3.connect("SQLite_Python.db")
cursor = sqlite_connection.cursor()

posts = [
	{
		"author": "Oscar Gonzalez",
		"title": "Blog post 1",
		"content": "First post content",
		"date_posted": "November 19, 2019"
	},
	{
		"author": "Jan Doe",
		"title": "Blog post 2",
		"content": "Second post content",
		"date_posted": "November 20, 2019"
	}
]

@app.route("/")
@app.route("/home")
def home():
	return render_template('home.html', posts=posts)


@app.route("/about")
def about():
	return render_template('about.html', title="About")

@app.route("/api/v1/")
@app.route("/api/v1/random")
def random_quote():
    random_index = random.randint(1,100)
    quote_query = f"select michael_quotes from mscott_quotes where indicator = {random_index};"
    record = cursor.execute(quote_query).fetchone()
    return record

@app.route("/api/v1/michael")
def michael_quote():
    random_index = random.randint(1,100)
    quote_query = f"select michael_quotes from mscott_quotes where indicator = {random_index};"
    record = cursor.execute(quote_query).fetchone()
    return record


cursor.close
if __name__ == '__main__':
	app.run(debug=True)