# outputs CO2 emissions in g/mi then converts to tons for some mileage
import pandas as pd


def to_total_tons(emissions_g, mileage):
    emissions_tons = (emissions_g * mileage) / 907185
    return emissions_tons


file = pd.read_excel('vehicle_data.xlsx')

make = input("Vehicle Manufacturer: ")
model = input("Vehicle Type: ")
year = int(input("Model Year: "))

vehicle_emissions = file[['co2', 'make', 'model', 'year']]
vehicle_emissions_valid = vehicle_emissions[vehicle_emissions['co2'] != -1]
cars_year = vehicle_emissions_valid[vehicle_emissions_valid['year'] == year]
cars_make = cars_year[cars_year['make'] == make]
cars_model = cars_make[cars_make['model'] == model]

mileage = int(input("Mileage: "))

emissions_per_mile = cars_model.iloc[0, 0]
print(to_total_tons(emissions_per_mile, mileage))
