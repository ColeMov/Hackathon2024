# outputs CO2 emissions in g/mi then converts to tons for some mileage
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


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

    plt.plot(x, y1, x, y2)

    font1 = {'family': 'serif', 'color': 'blue', 'size': 20}
    font2 = {'family': 'serif', 'color': 'darkred', 'size': 15}

    plt.title(make + " " + model + " versus EV", fontdict=font1)
    plt.xlabel("Miles Traveled in " + state, fontdict=font2)
    plt.ylabel("CO2 Emissions (tons)", fontdict=font2)

    plt.grid()
    plt.show()


file = pd.read_excel('vehicle_data.xlsx')

make = input("Vehicle Manufacturer: ")
model = input("Vehicle Type: ")
year = int(input("Model Year: "))
mileage = int(input("Mileage: "))
state = input("State: ")

vehicle_emissions = file[['co2', 'make', 'model', 'year']]
vehicle_emissions_valid = vehicle_emissions[vehicle_emissions['co2'] != -1]
cars_year = vehicle_emissions_valid[vehicle_emissions_valid['year'] == year]
cars_make = cars_year[cars_year['make'] == make]
cars_model = cars_make[cars_make['model'] == model]

emissions_g = cars_model.iloc[0, 0]
print(total_tons(emissions_g, mileage))

renewable = pd.read_csv("percent_renewable_state.csv")
ev_emissions = ev_emissions_per_mile(renewable, state, mileage)
print(ev_emissions + 8.8)

ev_per_mile = ev_emissions_per_mile(renewable, state, 1)
make_graph(tons_per_mile(emissions_g), ev_per_mile, mileage, state)
