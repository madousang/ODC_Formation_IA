from numpy import arctan

#Fonction f(x)
def funct1(x):
    return (x/(x**2+1))

#Fonction g(x)
def funct2(y):
    return arctan(y)

L = list()
result = list()
sumR = float()

#Calcul de R
try:
    N = int(input("Donnez une valeur à N\n"))
    if N <= 0 :
        raise Exception
except ValueError:
    print("Veuillez entrer un nombre entier")
except Exception:
    print("Veillez entrer un nombre entier strictement positif")
else:
    for i in range(-N, N+1, 1):
        L.append(i)

    for i in L:
        sumR += (funct1(i) - funct2(i))**2

    print("R = ", round(sum, 2))
