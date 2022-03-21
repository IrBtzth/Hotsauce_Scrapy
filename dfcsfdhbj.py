import pandas as pd
df = pd.DataFrame()
nombres = ['Juan', 'Laura', 'Pepe']
edades = [42, 40, 37]

df['Nombre'] = nombres
df['Edad'] = edades
df.to_csv('city.csv')