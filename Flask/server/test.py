import pandas as pd

cardata = pd.read_csv("data/carData.csv", sep=';')
datarow = cardata[cardata.carModel == "Acura CL"]
car_price = datarow.iloc[0]["carPreis"]
