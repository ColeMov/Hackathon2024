import pandas as pd

file = pd.read_excel('CarData1975-2022.xlsx')

make = input("Vehicle Manufacturer: ")
model = input("Vehicle Type: ")
year = int(input("Model Year: "))

cars_year = file[file['Model Year'] == year]
cars_make = cars_year[cars_year['Manufacturer'] == make]
cars_model = cars_make[cars_make['Vehicle Type'] == model]

emissions = cars_model.iloc[0, 5]
print(emissions)
