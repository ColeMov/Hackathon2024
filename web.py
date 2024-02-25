import pandas as pd
from flask import Flask, request, jsonify, Response, render_template
from markupsafe import escape
import zipfile
from collections import deque
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium import webdriver
import os
import time
import requests
from bs4 import BeautifulSoup

cars = pd.read_excel("vehicle_data.xlsx")
car_dict = {}

for index, row in cars.iterrows():
    make = row['make']
    year = str(row['year'])
    model = row['model']

    if make not in car_dict:
        car_dict[make] = {}
    if year not in car_dict[make]:
        car_dict[make][year] = set()
    car_dict[make][year].add(model)


car_dict = {make: {year: list(models) for year, models in make_years.items()} for make, make_years in car_dict.items()}

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/process', methods=['POST'])
def process():
    global car_brand, state
    selected_values = {key: value for key, value in request.form.items()}
    car_brand = selected_values.get('Car Make')
    state = selected_values.get('State')
    available_years = car_dict.get(car_brand, {}).keys()
    # Generating options for the years dropdown
    year_options = ""
    for year in available_years:
        year_options += f'<option value="{escape(year)}">{escape(year)}</option>'
    return render_template('home2.html', state=state, car_brand=car_brand, year_options=year_options)

@app.route('/next', methods=['POST'])
def nowwhat():
    global car_brand, state, year
    selected_values = {key: value for key, value in request.form.items()}
    year = selected_values.get('Year')  # Assuming 'Year' is the name of the year dropdown
    models = car_dict.get(car_brand, {}).get(year, [])
    options = ""
    for model in models:
        options += f'<option value="{escape(model)}">{escape(model)}</option>'
    return render_template('home3.html', options=options, year=year, car_brand=car_brand, state=state)
    #
@app.route('/final', methods=['POST'])
def final():
    return render_template('home4.html', year=year, car_brand=car_brand, state=state)

#ill have a list of models which can go into the html and will become the drop down models


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, threaded=False)