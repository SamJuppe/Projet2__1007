from donnees import charger_donnees
import matplotlib.pyplot as plt
import numpy as np
donne = charger_donnees("donnees/donnees_selectionnees.csv")
print(donne["quality"].value_counts().sort_index()) # on observe que il n'y a aucun vin qui a une note de 1-2-9-10 dans la base de donnee


print(donne["volatile acidity"])
plt.scatter(donne["volatile acidity"],donne["quality"], s = 5)
plt.xlabel('ACIDITE')
plt.ylabel('QUALITE')
plt.show()

plt.hist((donne["volatile acidity"],donne["quality"]), bins = 20)
plt.xlabel('ACIDITE')
plt.ylabel('QUALITE')
plt.show()