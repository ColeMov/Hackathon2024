# app.py
from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from markupsafe import escape


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


def total_tons(emissions, miles):
    emissions_tons = (emissions * miles) / 907185
    return emissions_tons


def tons_per_mile(emissions):
    emissions_tons = emissions / 907185
    return emissions_tons


def ev_emissions_per_mile(data, state, yearly_mileage):
    kwh_per_year = yearly_mileage * .25
    dirty_kwh = data[data["State"] == state]["% Non Renewable"].iloc[0] * kwh_per_year
    g_co2_per_year = dirty_kwh * 388.7287
    return g_co2_per_year / 907185


def make_graph(gas_emissions, ev_emissions, mileage, state):
    x = np.array([])
    y1 = np.array([])
    y2 = np.array([])
    for i in range(0, mileage, 10):
        x = np.append(x, i)
        y1 = np.append(y1, gas_emissions * i)
        y2 = np.append(y2, (ev_emissions * i) + 8.8)

    plt.plot(x, y1, label="Gas Vehicle CO2 Emissions")
    plt.plot(x, y2, label="EV CO2 Emissions")

    plt.title("CO2 Emissions Comparison")
    plt.xlabel("Miles Traveled in " + state)
    plt.ylabel("CO2 Emissions (tons)")
    plt.legend()
    plt.grid()

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plot_data = base64.b64encode(buffer.getvalue()).decode()
    plt.close()

    return plot_data


@app.route('/')
def index():
    return render_template('home.html')


@app.route('/process', methods = ['POST'])
def process():
    global car_brand, state, year_options
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
def next():
    global car_brand, state, year
    models = car_dict.get(car_brand, {}).get(year, [])
    options = ""
    for model in models:
        options += f'<option value="{escape(model)}">{escape(model)}</option>'
    return render_template('home3.html',options=options, year=year, car_brand=car_brand, state=state)


@app.route('/result', methods=['POST'])
def result():

    selected_values = {key: value for key, value in request.form.items()}
    model=selected_values.get('Model')
    # return render_template('home4.html', year=year, car_brand=car_brand, state=state, model=model)
    make = request.form['make']
    model = request.form['model']
    year = int(request.form['year'])
    mileage = 160000
    state = request.form['state']

    file = pd.read_excel('vehicle_data.xlsx')
    vehicle_emissions = file[['co2', 'make', 'model', 'year']]
    vehicle_emissions_valid = vehicle_emissions[vehicle_emissions['co2'] != -1]
    cars_year = vehicle_emissions_valid[vehicle_emissions_valid['year'] == year]
    cars_make = cars_year[cars_year['make'] == make]
    cars_model = cars_make[cars_make['model'] == model]

    emissions_g = cars_model.iloc[0, 0]

    renewable = pd.read_csv("percent_renewable_state.csv")
    ev_per_mile = ev_emissions_per_mile(renewable, state, 1)
    graph_data = make_graph(tons_per_mile(emissions_g), ev_per_mile, mileage, state)

    return render_template('result.html', plot_data=graph_data)


if __name__ == '__main__':
    app.run(debug=True)
