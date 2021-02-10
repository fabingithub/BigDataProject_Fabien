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




#FINAL STEP (run after everything is done):
#save as new csv inside csv/new
pd.DataFrame(domarar).to_csv("csv/new/blak-domarar.csv")
pd.DataFrame(einstaklingar).to_csv("csv/new/blak-einstaklingar.csv")
pd.DataFrame(forsvarsmenn).to_csv("csv/new/blak-forsvarsmenn.csv.csv")
pd.DataFrame(lid).to_csv("csv/new/blak-lid.csv")
pd.DataFrame(lidimoti).to_csv("csv/new/blak-lidimoti.csv")
pd.DataFrame(lidsmenn).to_csv("csv/new/blak-lidsmenn.csv")
pd.DataFrame(lidsstjorar).to_csv("csv/new/blak-lidsstjorar.csv")
pd.DataFrame(mot).to_csv("csv/new/blak-mot.csv")
pd.DataFrame(thjalfarar).to_csv("csv/new/blak-thjalfarar.csv")
