import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#importing all csv files
domarar = pd.read_csv('csv/blak-domarar.csv', sep=';', header=0)
einstaklingar = pd.read_csv('csv/blak-einstaklingar.csv', sep=';', header=0)
forsvarsmenn = pd.read_csv('csv/blak-forsvarsmenn.csv', sep=';', header=0)
lid = pd.read_csv('csv/blak-lid.csv', sep=';', header=0)
lidimoti = pd.read_csv('csv/blak-lidimoti.csv', sep=';', header=0)
lidsmenn = pd.read_csv('csv/blak-lidsmenn.csv', sep=';', header=0)
lidsstjorar = pd.read_csv('csv/blak-lidsstjorar.csv', sep=';', header=0)
thjalfarar = pd.read_csv('csv/blak-thjalfarar.csv', sep=';', header=0)
mot = pd.read_csv('csv/blak-mot.csv', sep=';', header=0)

# Print data from each csv
#print(domarar)
#print(einstaklingar)
#print(forsvarsmenn)
#print(lid)
#print(lidimoti)
#print(lidsmenn)
#print(lidsstjorar)
print(mot)
#print(thjalfarar)
