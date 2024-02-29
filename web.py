import pandas as pd
from flask import Flask, request, jsonify, Response, render_template
from markupsafe import escape
import numpy as np
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__, static_url_path='/static/images/renewable_states_map.jpg')

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
    print(gas_emissions)
    for i in range(0, mileage, 10):
        x = np.append(x, i)
        y1 = np.append(y1, gas_emissions * i)
        y2 = np.append(y2, (ev_emissions * i) + 8.8)

    plt.plot(x, y1, label="Gas Vehicle CO2 Emissions")
    plt.plot(x, y2, label="EV CO2 Emissions")

    plt.title("CO2 Emissions Comparison ")
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
def home():
    return render_template('index.html')


@app.route('/process', methods=['POST'])
def process():
    global car_brand, state
    selected_values = {key: value for key, value in request.form.items()}
    car_brand = selected_values.get('Car Make')
    print(car_brand)
    state = selected_values.get('State')
    available_years = car_dict.get(car_brand, {}).keys()
    # Generating options for the years dropdown
    year_options = ""
    for year in available_years:
        year_options += f'<option value="{escape(year)}">{escape(year)}</option>'
    return render_template('home2.html', state=state, car_brand=car_brand, year_options=year_options)


@app.route('/next', methods=['POST'])
def next():
    global year
    selected_values = {key: value for key, value in request.form.items()}
    year = selected_values.get('Year')  # Assuming 'Year' is the name of the year dropdown
    models = car_dict.get(car_brand, {}).get(year, [])
    options = ""
    for model in models:
        options += f'<option value="{escape(model)}">{escape(model)}</option>'
    return render_template('home3.html', options=options, year=year, car_brand=car_brand, state=state)


@app.route('/final', methods=['POST'])
def final():
    global model
    selected_values = {key: value for key, value in request.form.items()}
    model = selected_values.get('Model')
    # return render_template('home4.html', year=year, car_brand=car_brand, state=state, model=model)
    mileage = 160000
    file = pd.read_excel('vehicle_data.xlsx')
    vehicle_emissions = file[['co2', 'make', 'model', 'year']]
    vehicle_emissions_valid = vehicle_emissions[vehicle_emissions['co2'] != -1]
    cars_make = vehicle_emissions_valid[vehicle_emissions_valid['make'] == car_brand]
    cars_model = cars_make[cars_make['model'] == model]
    cars_final = cars_model[cars_model['year'] == int(year)]

    emissions_g = cars_final.iloc[0, 0]

    renewable = pd.read_csv("percent_renewable_state.csv")
    ev_per_mile = ev_emissions_per_mile(renewable, state, 1)

    total_tons_gas = total_tons(emissions_g, 80000)
    total_tons_ev = (ev_per_mile * 80000) + 8.8
    print(total_tons_ev)
    graph_data = make_graph(tons_per_mile(emissions_g), ev_per_mile, mileage, state)

    return render_template('result.html', plot_data=graph_data, total_tons_gas = total_tons_gas, total_tons_ev = total_tons_ev)


# ill have a list of models which can go into the html and will become the drop down models


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, threaded=False)
