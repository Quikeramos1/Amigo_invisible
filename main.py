from models import *

print("Bienvenid@ a sorteo de amig@ invisible")
empezar = input("¿Quieres introducir los dastos? (S/N) ")


empezar = empezar.lower()
if empezar == "n":
    print("Ok, vuelve cuando quieras introducir lo datos")
elif empezar == "s":

    personas = sorteo()
    
    




