import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def make_pie_chart(x, y):
    font1 = {'family': 'serif', 'color': 'blue', 'size': 20}

    plt.title("CO2 Emissions - Car Manufacturer", fontdict=font1)

    myexplode = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0.2, 0, 0, 0]
    plt.pie(y, labels=x, explode=myexplode)
    plt.show()


def make_bar_graph(x, y):
    font1 = {'family': 'serif', 'color': 'blue', 'size': 20}
    font2 = {'family': 'serif', 'color': 'darkred', 'size': 15}

    plt.title("CO2 Emissions - Car Manufacturer", fontdict=font1)
    plt.xlabel("Manufacturer", fontdict=font2)
    plt.ylabel("CO2 Emissions (g/mi)", fontdict=font2)

    plt.bar(x, y, color="#4CAF50")
    plt.show()


file = pd.read_excel('CarData2014-2022.xlsx')

manufacturers = np.array(["BMW", "Ford", "GM", "Honda", "Hyundai", "Kia", "Mazda", "Mercedes", "Nissan", "Stellantis", "Subaru", "Toyota", "VW"])
all_vehicle_type_emissions = np.array([])
for i in range(0, len(manufacturers)):
    make_cars = file[file['Manufacturer'] == manufacturers[i]]
    make_all_models = make_cars[make_cars['Vehicle Type'] == 'All']
    make_all_2021 = make_all_models[make_all_models['Model Year'] == 2021]
    emissions = make_all_2021.iloc[0, 4]
    all_vehicle_type_emissions = np.append(all_vehicle_type_emissions, emissions)

chart = int(input("Select graph type:\n1)Pie Chart\n2)Bar Graph\n"))

if chart == 1:
    make_pie_chart(manufacturers, all_vehicle_type_emissions)
else:
    make_bar_graph(manufacturers, all_vehicle_type_emissions)



