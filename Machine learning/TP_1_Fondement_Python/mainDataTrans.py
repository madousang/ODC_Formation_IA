from DataTrans import *
from ExceptClass import *


#Gestion de quelques exceptions
try: 
    print("Donner le nombre de liste : ")
    n = int(input())
    print("Donner une taille chaque liste : ")
    s = int(input())
    if (n<0 or n==0):
        raise ExceptClass(n)
    if (s<0 or n==0):
        raise ExceptClass(s)
        
except IndexError as err:
    print(err)
except ValueError:
    print("Pour les nombres entrés, ils doivent être entiers")
except ExceptClass: 
    pass
except NameError:
    print("Une variable non declare")
else: 
    A1 = DataTrans(n, s)
    D = list()
    i = 0
    while i < n:
        D.append(A1.G()) #Appel de la fonction G() pour generer la lite D
        i += 1
    print("La liste est D : ", D)
    L = list()
    p = 0
    while p<n: #Appel de la fonction MIN() pour calculer le minimun des listes composants D
        print("\nLe Min de la", p ,"ième liste est", A1.MIN(D[p]))
        L.append(A1.MIN(D[p]))
        p+=1
    u = 0
    while u<n: #Appel de la fonction MAX() pour calculer le maximun des listes composants D
        print("\nLe Max de la", u ,"ième liste est", A1.MAX(D[u]))
        L.append(A1.MAX(D[u]))
        u+=1

    #Appel de MIN() et MAX() pour le calcul du min et du max des listes composants D
    print("\nle minimun global de la liste D est : ",A1.MIN(L))
    print("\nle maximun global de la liste D est : ",A1.MAX(L))
    
    #Calcul et Affichage de D'
    D1 = list(())
    i = 0
    while i < n:
        D1.append(A1.image(D[i]))
        i += 1
    print("\nla liste D1 est : ",D1)