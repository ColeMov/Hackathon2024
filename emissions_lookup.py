import pandas as pd

file = pd.read_excel('CarData2014-2022.xlsx')

make = input("Vehicle Manufacturer: ")
model = input("Vehicle Type: ")

cars_2021 = file[file['Model Year'] == 2021]
make_cars = cars_2021[cars_2021['Manufacturer'] == make]
model_cars = make_cars[make_cars['Vehicle Type'] == model]

emissions = model_cars.iloc[0, 5]
print(emissions)