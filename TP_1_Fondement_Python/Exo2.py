import random

D = list(())
print("Donner le nombre liste : ")
N = int(input())
print("Donner une taille chaque liste : ")
n = int(input())

#Fonction génératrice de la liste aléatoire
def G():
    K = list()
    x = 0
    while x < n:
        i = random.random()
        y = i*100 
        K.append(round(y,2))
        x+=1
    return K
i = 0
while i < N:
    D.append(G())
    i += 1
print("La liste est D : ", D)

#Fonction pour le calcul du min d'une liste
def MIN(z):
    lmini = z[0]
    for i in range(len(z)):
        if z[i] < lmini:
            lmini = z[i]
    return lmini

#Fonction pour le calcul du max d'une liste
def MAX(z):
    lmaxi = z[0]
    for i in range(len(z)):
        if z[i] > lmaxi:
            lmaxi = z[i]
    return lmaxi

#Affichage de minimun et maximun de chacune des listes composants D
L = list()
p = 0
while p<N:
    print("\nLe Min de la", p ,"ième liste est", MIN(D[p]))
    L.append(MIN(D[p]))
    print("\nLe Max de la", p ,"ième liste est", MAX(D[p]))
    L.append(MAX(D[p]))
    p+=1

#Calcul et Affichage de minimun et maximun global de la liste D 
print("\nLe Min global de la liste D est", MIN(L))
print("\nLe Max global de la liste D est", MAX(L))

#Definition de la fonction f(x)
def funct(x):
    t = pow(x,3) + 3*(pow(x,2)) - 5
    return t

#Definition d'une fonction image(x) pour le calcul de l'image d'une liste 
def image(X):
    T = list()
    for i in range(len(X)): 
        T.append(round(funct(X[i]), 2))
    return T

#Calcul et Affichage de D'
D1 = list()
u = 0
while u<N:
    D1.append(image(D[u]))
    u+=1
    
print("\nla liste D1 est : ",D1)
